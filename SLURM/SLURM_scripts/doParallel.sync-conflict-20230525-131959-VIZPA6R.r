# load the parallel 
library(parallel)
library(doParallel)

args = commandArgs(trailingOnly=TRUE)
nproces = as.numeric(args[1])

hostlist <- paste(unlist(read.delim(file="hostnames.txt", header=F, sep =" ")))

for (i in 0:length(hostlist)){
if (i == 0){
hosts <- rep(hostlist[i],nproces)
} else {
hosts <-c(hosts, rep(hostlist[i],nproces))
}
}

cl <- makePSOCKcluster(names=hosts)
registerDoParallel(cl)

#run the parallel calculation
x <- iris[which(iris[,5] != "setosa"), c(1,5)]
trials <- 200000
system.time({
r <- foreach(icount(trials), .combine=rbind) %dopar% {
ind <- sample(100, 100, replace=TRUE)
result1 <- glm(x[ind,2]~x[ind,1], family=binomial(logit))
coefficients(result1)
}
})

stopCluster(cl)