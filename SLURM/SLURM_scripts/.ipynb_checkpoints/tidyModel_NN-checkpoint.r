library(tidymodels)
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
holidays <- c("AllSouls", "AshWednesday", "ChristmasEve", "Easter", 
              "ChristmasDay", "GoodFriday", "NewYearsDay", "PalmSunday")

nnet_recipe <- 
  recipe(children ~ ., data = hotel_train) %>% 
  step_date(arrival_date) %>%                           # creates predictors for the year, month, and day of the week.
  step_holiday(arrival_date, holidays = holidays) %>%   # generates a set of indicator variables for specific holidays.
  step_rm(arrival_date) %>%                             # removes orginal variables;
  step_dummy(all_nominal_predictors()) %>%              # Converts characters or factors dummy variables.
  step_zv(all_predictors()) %>%                         #removes orginal variables;
  step_normalize(all_predictors())

# Create Workflow and Tune Models 
set.seed(345)

# Define Model
nnet_model <- 
  mlp(hidden_units = tune(), penalty = tune(), epochs = tune()) %>% 
  set_engine("nnet", trace = 0,MaxNWts = 10000) %>% 
  set_mode("classification") 

# Define Workflow
nnet_workflow <- 
  workflow() %>% 
  add_model(nnet_model) %>% 
  add_recipe(nnet_recipe)


tic()
# Starting Up Cluster
cl <- makePSOCKcluster(names=hosts)
#cl <- makePSOCKcluster(parallel::detectCores())

registerDoParallel(cl)

# Grid-Tune
nnet_tune <- 
  nnet_workflow  %>% 
  tune_grid(hotel_validation,
            grid = nGrid,
            control = control_grid(save_pred = TRUE,parallel_over = "everything"),
            #control = control_grid(save_pred = TRUE,parallel_over = "resamples"),
            metrics = metric_set(roc_auc))
toc()
stopCluster(cl)