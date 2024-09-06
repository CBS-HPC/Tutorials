# UCloud Tutorial: SSH Connection to UCloud using Terminal or VSCode

Direct SSH Connection is available for a range of different UCloud applications: 

- [Terminal](https://cloud.sdu.dk/app/jobs/create?app=terminal-ubuntu)
- [Coder](https://cloud.sdu.dk/app/jobs/create?app=coder)
- [RStudio](https://cloud.sdu.dk/app/jobs/create?app=rstudio)
- [JupyterLab](https://cloud.sdu.dk/app/jobs/create?app=jupyter-all-spark)
- [Ubuntu Xfce - virtual desktop environment](https://cloud.sdu.dk/app/jobs/create?app=ubuntu-xfce)
- [AlmaLinux Xfce - virtual desktop environment](https://cloud.sdu.dk/app/jobs/create?app=almalinux-xfce)


This tutorial provided a step-by-step guide on how to connect the UCloud application directly to a Terminal or VSCode application on your local PC. 

It will also be shown how to setup a conda environment and how to run a jupyter notebook through VSCode.

Prerequisite reading:

- [How to Generate SSH key](/Tutorials/SHH/shh_create/)


## Add public SSH key to UCloud

![](/Tutorials/SSH/image1.PNG)

### Step 1: On UCloud go to "Resources -> SHH-Keys -> Create SSH key" 

![](/Tutorials/SSH/image2.PNG)

### Step 2: Paste pulic key, give a meaningful name and press "Add SSH key". 

![](/Tutorials/SSH/image1.PNG)

![](/Tutorials/SSH/image3.PNG)

![](/Tutorials/SSH/image4.PNG)


More information can be found in the UCloud [documentation](https://docs.cloud.sdu.dk/Apps/general_settings.html#configure-ssh-access).


## Start UCloud Job

### Step 1: Start UCloud Job by filling out the necessary fields. **Remember to check the "Enable SSH server" checkbox"**

![](/Tutorials/SSH/image5.PNG)

### Step 2: When job ready please locate and copy the SSH address 

![](/Tutorials/SSH/image6.PNG)

## Connect the using a Local Terminal App

Paste the SSH address into a terminal, press enter and follow a few intuitive steps.

![](/Tutorials/SSH/image14.PNG)

##  Connect using Visual Studio Code (VScode)

### Open Visual Studio Code (VScode)

### Install "Remote - SSH" extension

![](/Tutorials/SSH/image7.PNG)

### Access remote UCloud Job

- Press "Ctrl + shift + p" to open Command Palette
- Search and press "Remote-SSH:Connect to Host..."
- Press "Add New SSH Host..."

![](/Tutorials/SSH/image8.PNG)

### Paste UCloud Job SSH address and press Enter
![](/Tutorials/SSH/iImage9.PNG)

Follow a few intuitive steps.


### Navigate to /work folder on UCloud

![](/Tutorials/SSH/image10.PNG)


![](/Tutorials/SSH/image11.PNG)



## Run a Jupyter notebook (Through VSCode)

### Install VScode Extension "Python" and "Jupyter" on remote machine

![](/Tutorials/SSH/image12.PNG)


![](/Tutorials/SSH/image13.PNG)


## Activate a Conda Environment (Through VSCode)


```python
#Running a new UCloud run the following lines in the terminal to activate Conda:
sudo ln -s /work/miniconda3/bin/conda /usr/bin/conda

# Initiate Conda and reboot 
conda init && bash -i

# Activate environment:
conda activate myenv

# Install ipykernel if not installed:

conda install ipykernel

# 
python -m ipykernel install --user --name myenv --display-name "myenv"
```
