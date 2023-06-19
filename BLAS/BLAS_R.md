# RStudio on UCloud

When looking at the different R/RStudio version available on UCloud (see below) it can be observed that some have the suffix "_MKL". These have "Intel MKL" as their default BLAS/LAPACK library, while versions with out the suffix have the "LibBLAST" library whihc is the base R library on linux systems.

![](Rstudio_Ucloud1.png)

### Use the "sessionInfo()" function to check which BLAS/LAPACK library is deployed:

**MKL**

![](sessionInfo_1.png)

**LibBLAS**

![](sessionInfo_2.png)

# Benchmarking the two versions

**Benchmarking a simple matrix multiplication shows that the "MKL" is close 78 times faster than the "LibBLAS"!!**

**MKL** mean = 7.63 milliseconds

![](benchmark_1.png)

**LiBLAS** mean = 592.666 milliseconds

![](benchmark_2.png)



```python
library(microbenchmark)

n <- 1000
mat1 <- matrix(rnorm(n*n), ncol=n)
mat2 <- matrix(rnorm(n*n), ncol=n)

tic()
f <- function() mat1 %*% mat2
res <- microbenchmark(f(), times=100L)
res
```

# Installing and Chaning BLAS & LAPACK Library

Select between the available BLAS/LAPACK libraies by posting the command below i the job terminal. 


```python

# BLAS Selection
sudo update-alternatives --config libblas.so.3-x86_64-linux-gnu

# LAPACK Selection
sudo update-alternatives --config liblapack.so.3-x86_64-linux-gnu



# BLAS Selection Output: 
There are 2 choices for the alternative libblas.so.3-x86_64-linux-gnu (providing /usr/lib/x86_64-linux-gnu/libblas.so.3).

  Selection    Path                                                      Priority   Status
------------------------------------------------------------
* 0            /opt/intel/oneapi/mkl/2022.1.0/lib/intel64//libmkl_rt.so   50        auto mode
  1            /opt/intel/oneapi/mkl/2022.1.0/lib/intel64//libmkl_rt.so   50        manual mode
  2            /usr/lib/x86_64-linux-gnu/blas/libblas.so.3                10        manual mode

Press <enter> to keep the current choice[*], or type selection number:
```

## Install other libraries.

Changing the BLAS/LAPACK libraries is **not** possible for the "MKL" versions of the RStudio applications on UCloud. 


```python
# install OpenBLAS
sudo apt-get install libopenblas-base
# install ATLAS
sudo apt-get install libatlas3-base liblapack3

# BLAS Selection
sudo update-alternatives --config libblas.so.3-x86_64-linux-gnu


# BLAS Selection Output: 
There are 4 choices for the alternative libblas.so.3-x86_64-linux-gnu (providing /usr/lib/x86_64-linux-gnu/libblas.so.3).

  Selection    Path                                                      Priority   Status
------------------------------------------------------------
* 0            /usr/lib/x86_64-linux-gnu/openblas-pthread/libblas.so.3    100       auto mode
  1            /opt/intel/oneapi/mkl/2022.1.0/lib/intel64//libmkl_rt.so   50        manual mode
  2            /usr/lib/x86_64-linux-gnu/atlas/libblas.so.3               35        manual mode
  3            /usr/lib/x86_64-linux-gnu/blas/libblas.so.3                10        manual mode
  4            /usr/lib/x86_64-linux-gnu/openblas-pthread/libblas.so.3    100       manual mode

Press <enter> to keep the current choice[*], or type selection number: ^C
```

## Select an alternative library (Atlas libraries in this case)


Open R and confirm the change of BLAS/LAPACK library using "sessionInfo()" function.

![](sessionInfo_3.png)

