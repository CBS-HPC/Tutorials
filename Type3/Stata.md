# Install Stata on DieC large memory HPC/TYPE 3 (Hippo)

This is a guide on how to install Stata on DieC large memory HPC/TYPE 3 (Hippo).

Prerequisite reading:

- [Using Conda for easy management of Python and R environments](/Tutorials/SHH/shh_create/)

## Get Stata license and Installation file (CBS Users)

Follow the instructions to get a Stata license at CBS https://studentcbs.sharepoint.com/sites/ITandCampus/SitePages/en/Free-software.aspx

You will recieve an email with license and installation information (see image below).

![](/Tutorials/Type3/images/stata1.PNG)

 Download the installation file (Stata17Linux64.tar) and upload this to your UCloud directory.

![](/Tutorials/Type3/images/stata2.PNG)

## Installing Stata on Type 3

### Launch a "Terminal App" UCloud Job and include the stata installation file (Stata17Linux64.tar)


Run following commands in the terminal: 


```R

# Unzip installation file to temp folder
mkdir /home/user/statafiles
cd /home/user/statafiles
tar -zxf /home/user/Stata17Linux64.tar.gz

# Install Stata on in "/home/user/stata17". Say yes when asked during installtion
mkdir /home/user/stata17 
cd /home/user/stata17

/home/user/statafiles/install

# Set stata to Unix path
export PATH="/home/user/stata17:$PATH"

# Initialize Stata
/home/user/stata17/stinit

# Follow instructions and add "Serial number", "Code" and "Authorization" from the Stata license mail

# Check stata installation
which stata

# Run stata
stata
# or
stata-se
# or
stata-mp

# Get following dependency error: 
stata: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory

```

## Install dependencies using Easybuild


```R
eb ncurses-5.9.eb -r

module load ncurses/5.9
```

## Run Stata


```R
# Run stata
stata
# or
stata-se
# or
stata-mp

# Output
  ___  ____  ____  ____  ____ ®
 /__    /   ____/   /   ____/      17.0
___/   /   /___/   /   /___/       BE—Basic Edition

 Statistics and Data Science       Copyright 1985-2021 StataCorp LLC
                                   StataCorp
                                   4905 Lakeway Drive
                                   College Station, Texas 77845 USA
                                   800-STATA-PC        https://www.stata.com
                                   979-696-4600        stata@stata.com

Stata license: Unlimited-user network, expiring 27 Dec 2023
Serial number: 401709301397
  Licensed to: Kristoffer Gulmark Poulsen
               Type 3

Notes:
      1. Unicode is supported; see help unicode_advice.

.
```

## “stata17” and "easybuild" will not be placed on the Hippo Home folder

![](/Tutorials/Type3/images/stata3.PNG)

## Activate Stata on a new Type 3 Job

Add the stata17 folder to the job

![](/Tutorials/Type3/images/stata4.PNG)


```R
# Set stata to Unix path
export PATH="/home/user/stata17:$PATH"

# Check stata installation
which stata

# Load dependies
module load ncurses/5.9

# Run stata
stata
# or
stata-se
# or
stata-mp

# Output

  ___  ____  ____  ____  ____ ®
 /__    /   ____/   /   ____/      17.0
___/   /   /___/   /   /___/       BE—Basic Edition

 Statistics and Data Science       Copyright 1985-2021 StataCorp LLC
                                   StataCorp
                                   4905 Lakeway Drive
                                   College Station, Texas 77845 USA
                                   800-STATA-PC        https://www.stata.com
                                   979-696-4600        stata@stata.com

Stata license: Unlimited-user network, expiring 27 Dec 2023
Serial number: 401709301397
  Licensed to: Kristoffer Gulmark Poulsen
               Type 3

Notes:
      1. Unicode is supported; see help unicode_advice.

.
```

## Create a Conda Stata environment

Assumes that miniconda3 has been installed. For more information on how to install conda on Type 3 see [here](/Tutorials/SHH/shh_create/).



```R
# Create conda environment
conda create -n myenv_stata python
conda activate myenv_stata
conda install ipykernel
pip install stata-setup
pip install pystata
ipython kernel install --name myenv_stata --user # Make python available to JupyterLab

```


# Run Stata in a Jupyter notebook

## Start Jupyter interface
![](/Tutorials/Type3/images/stata5.PNG)

## Add token to open jupyter
![](/Tutorials/Type3/images/stata6.PNG)

## Open a new python notebook
![](/Tutorials/Type3/images/stata7.PNG)

## Configure the stata installation


```R
import stata_setup

stata_setup.config("/work/stata17", "se")

# Output

  ___  ____  ____  ____  ____ ®
 /__    /   ____/   /   ____/      17.0
___/   /   /___/   /   /___/       SE—Standard Edition

 Statistics and Data Science       Copyright 1985-2021 StataCorp LLC
                                   StataCorp
                                   4905 Lakeway Drive
                                   College Station, Texas 77845 USA
                                   800-STATA-PC        https://www.stata.com
                                   979-696-4600        stata@stata.com

Stata license: Unlimited-user network, expiring 27 Dec 2023
Serial number: 401709301397
  Licensed to: Kristoffer Gulmark Poulsen
               CBS Account

Notes:
      1. Unicode is supported; see help unicode_advice.
      2. Maximum number of variables is set to 5,000; see help set_maxvar.
```

## Run your code using the stata magic (%%stata) the Configure the stata installation

"%%stata" - cell magic is used to execute Stata code within a cell.

"%stata" - line magic provides users a quick way to execute a single-line Stata command.

Find more information on the stata magic [here](https://www.stata.com/python/pystata18/notebook/Quick%20Start0.html).


```R
%%stata

sysuse auto, clear

summarize mpg

# Output
. 
. sysuse auto, clear
(1978 automobile data)

. 
. summarize mpg

    Variable |        Obs        Mean    Std. dev.       Min        Max
-------------+---------------------------------------------------------
         mpg |         74     21.2973    5.785503         12         41
```

![](/Tutorials/Type3/images/stata8.PNG)
