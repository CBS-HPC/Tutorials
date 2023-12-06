# UCloud Tutorial: Run Stata in Batch Mode on UCloud

This is an approach to adress the UCloud capacity issues. 

UCloud batch processing apps are scheduled to run as resources permit without end user interaction. It allows 

Prerequisite reading:

- [Install Stata on UCloud](/Tutorials/STATA/install/)

## Run Stata scrip in batch mode n a new terminal job

Add the "stata17" and other relevant folder to the job:

![img5](/Tutorials/STATA/images/img5.PNG)

Add a bash script(.sh) under "Batch processing" as one of the "Optional Parameters":

![img6](/Tutorials/STATA/images/img6.PNG)
![img7](/Tutorials/STATA/images/img7.PNG)


Below shown bash script can be downloaded from [here](https://github.com/CBS-HPC/Tutorials/blob/main/STATA/batchscript.sh). Use this as a template or [create your own bash script](https://www.howtogeek.com/261591/how-to-create-and-run-bash-shell-scripts-on-windows-10/).

More information on how to run Stata in batch mode can be found here: https://www.stata.com/support/faqs/unix/batch-mode/

```R
#!/bin/bash


# Installing dependencies
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libncurses5 libncurses5:i386 -y

# Set stata17 on UNIX path
export PATH="/work/stata17:$PATH"

# Run stata in Batch mode
stata -b do filename & # USER SHOULD CHANGE THIS LINE (SEE LINK Above)

```
