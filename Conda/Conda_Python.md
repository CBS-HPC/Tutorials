# UCloud Tutorial: Using Conda for easy management of Python environments

https://docs.cloud.sdu.dk/hands-on/conda-setup.html?highlight=conda

The Conda package and environment management system is already included in few applications available on UCloud (see, e.g., JupyerLab and PyTorch). For more general uses of Conda and its powerful package manager it is convenient to create a local installation and save it in a UCloud project.
Conda is included in all versions of Anaconda and Miniconda. For example, to install the latest version of Miniconda, just start any interactive app on UCloud, such as Terminal, and run the following shell commands:

# Installing Conda on UCloud

### Launch a "Terminal App" UCloud Job

Run following commands in the terminal: 


```R

# Download miniconda 
curl -s -L -o /tmp/miniconda_installer.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install miniconda
bash /tmp/miniconda_installer.sh -b -f -p /work/miniconda3
```

### When the job is finished copy the “miniconda3” folder from UCloud “Job” folder to a folder you want within your UCloud project.

![](/Tutorials/Conda/folder1.PNG "folder1")

## Activating Conda in a new UCloud Job


```R
#Running a new UCloud run the following lines in the terminal to activate Conda:
sudo ln -s /work/miniconda3/bin/conda /usr/bin/conda

# Initiate Conda and reboot 
conda init && bash -i
```


```R
#Shows already installed environments:
conda env list
```

### Installing and activate Python environments
https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html 


```R
# Showing available python versions
conda search python

# Installing a Python environment (Python 3.9 in this example) 
conda create -n myenv python=3.9

# Or install packages during installation.
conda create -n myenv python=3.9 numpy=1.16

# Shows already installed environments (R-4.2.3 show be displayed)
conda env list

# Activate environment
conda activate myenv

#Check which Python is in path
which python

#Output should be: 
/work/miniconda3/envs/myenv/bin/python
```

### Install libraries and run python:


```R
# Install conda libraries:
conda install scikit-learn

# Install pip libraries:
pip install --upgrade pip
pip install pandas

# Start Python:
python
```

# VScode on UCloud

### Add the “miniconda3” folder when starting the new Coder python UCloud job. 

https://docs.cloud.sdu.dk/hands-on/conda-coder.html?highlight=coder

In terminal add conda environment:


```R
# Running a new UCloud run the following lines in the terminal to activate Conda:
sudo ln -s /work/miniconda3/bin/conda /usr/bin/conda

# Init Conda:
conda init && bash -i

# Shows already installed environments:
conda env list

# Activate environment:
conda activate myenv

# Check which Python is in path:
which python

# Output should be: 
/work/miniconda3/envs/myenv/bin/python
```

### Now you can launch VSCode interface and open file and activate “myenv” as python interpreter:

Select the menu View -> Command Palette:

![](/Tutorials/Conda/vscode1.png "vscod1")

Execute the command > Python: Select Intepreter:

![](/Tutorials/Conda/vscode2.png "vscode2")


# JupyterLab on UCloud

### Add the “miniconda3” folder when starting the new JupyterLab UCloud job. 

In terminal add conda environment:


```R
# Init conda:
conda init && bash -i

# JupyterLab app on UCloud is Conda based with a installation found on the following path: 
conda info --envs

# Output should be: 
/opt/conda

# Create symbolic link for R environment between the two conda installations: 
sudo ln -s /work/miniconda3/envs/myenv /opt/conda/envs

# Shows already installed environments (Now “myenv” is available):
conda env list

# Activate environment:
conda activate myenv
```


```R
# Install ipykernel:

conda install ipykernel

# 
python -m ipykernel install --user --name myenv --display-name "myenv"

# De-activate environment:
conda deactivate
```

### Now you can launch JupyterLab interface and the “myenv” environment should be available on the frontpage.

![](/Tutorials/Conda/jupyterP.PNG "jupyterP")

# Terminal app on UCloud

### Add the “miniconda3” folder when starting the new Terminal App UCloud job. 

In terminal add conda environment:


```R
# Running a new UCloud run the following lines in the terminal to activate Conda:
sudo ln -s /work/miniconda3/bin/conda /usr/bin/conda

# Init Conda:
conda init && bash -i

# Shows already installed environments:
conda env list

# Activate environment:
conda activate myenv

# Check which Python is in path:
which python

# Output should be: 
/work/miniconda3/envs/myenv/bin/python
```

### Install libraries and run python:


```R
# Install conda libraries:
conda install scikit-learn

# Install pip libraries:
pip install --upgrade pip
pip install pandas

# Start Python:
python
```
