library(tidymodels)
library(ranger)
library(doParallel)
library(foreach)
library(readr)       # for importing data
library(vip)         # for variable importance plots
library(tictoc)     # For Timing 



# Get Input arguments
args = commandArgs(trailingOnly=TRUE)
nproces = as.numeric(args[1])

# Get Cluster Info
hostlist <- paste(unlist(read.delim(file="hostnames.txt", header=F, sep =" ")))
for (i in 0:length(hostlist)){
  if (i == 0){
    hosts <- rep(hostlist[i],nproces)
  } else {
    hosts <-c(hosts, rep(hostlist[i],nproces))
  }
}


nGrid = 24

## THE HOTEL BOOKINGS DATA
hotels <- 
  read_csv('https://tidymodels.org/start/case-study/hotels.csv') %>%
  mutate(across(where(is.character), as.factor))


## Data Overview
hotels %>% 
  count(children) %>% 
  mutate(prop = n/sum(n))

#DATA SPLITTING
set.seed(123)
splits      <- initial_split(hotels, strata = children)

hotel_train <- training(splits)
hotel_test  <- testing(splits)

# training set proportions by children
hotel_train %>% 
  count(children) %>% 
  mutate(prop = n/sum(n))

# test set proportions by children
hotel_test  %>% 
  count(children) %>% 
  mutate(prop = n/sum(n))


# Data Resampling (Creating a Validation Set)
set.seed(234)
hotel_validation <- validation_split(hotel_train, 
                                     strata = children, 
                                     prop = 0.80)

# CREATE THE RECIPE
rf_recipe <- 
  recipe(children ~ ., data = hotel_train) %>% 
  step_date(arrival_date) %>%  # creates predictors for the year, month, and day of the week.
  step_holiday(arrival_date) %>% # generates a set of indicator variables for specific holidays.
  step_rm(arrival_date) #removes variables;


# Create Workflow and Tune Models (Random Forrest - Ranger) 
set.seed(345)

# Define Model
rf_model <- 
  rand_forest(mtry = tune(), min_n = tune(), trees = 1000) %>% 
  set_engine("ranger") %>% 
  set_mode("classification")

# Define Workflow
rf_workflow <- 
  workflow() %>% 
  add_model(rf_model) %>% 
  add_recipe(rf_recipe)


tic()
# Starting Up Cluster
cl <- makePSOCKcluster(names=hosts)
#cl <- makePSOCKcluster(parallel::detectCores())

registerDoParallel(cl)
# Grid-Tune
rf_tune <- 
  rf_workflow %>% 
  tune_grid(hotel_validation,
            grid = nGrid,
            control = control_grid(save_pred = TRUE,parallel_over = "everything"),
            metrics = metric_set(roc_auc))
toc()