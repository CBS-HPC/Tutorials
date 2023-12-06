# Run Stata in jupyter-notebooks

This is a guide shows how to setup "pystata" in order to run Stata in Python using jupyter notebooks.

For more in depth decumnetation see [here](https://www.stata.com/python/pystata18/notebook/Quick%20Start0.html)


Prerequisite reading:

- [Install Stata on UCloud](/Tutorials/STATA/install/)

## Start a Jupyter Job in UCloud

Add the stata17 folder to the job

![](/Tutorials/STATA/images/jupyter1.PNG)

# Activate Stata and install stata-setup

Open the Terminal and run the code snippets below.

![](/Tutorials/STATA/images/jupyter2.PNG)


```R
# Install dependencies
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libncurses5 libncurses5:i386 -y

# Set stata to Unix path
export PATH="/work/stata17:$PATH"

# Check stata installation
which stata

# Example Output
/work/stata17/stata # use later

# Install stata-setup using pip
pip install stata-setup

# Install pystata using pip
pip install pystata
```


# Run Stata in a Jupyter notebook

## Start Jupyter interface
![](/Tutorials/STATA/images/jupyter3.PNG)
## Open a new python notebook
![](/Tutorials/STATA/images/jupyter4.PNG)


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

. 
```

![](/Tutorials/STATA/images/jupyter5.PNG)
