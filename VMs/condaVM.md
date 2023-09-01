# Conda: for easy workflow deployment on AAU GPU VMs

Package, dependency and environment management for any language—Python, R and [more](https://docs.conda.io/en/latest/).

The following tutorial provides step-by-step guides on how to install and use Conda for R and Python on the AAU GPU VMs available on UCloud.

Using a Conda environement elimnates the need for re-installing all the needed packages/libraries when starting a new AAU GPU VM.

Prerequisite reading:

- [How to Generate SSH key](/Tutorials/VMs/shh/)

- [Access VM using SSH](/Tutorials/VMs/connectVM/)

## Initial installation of Conda on a AAU VM job

### Connect to VM using SSH

Open a terminal app on local machine and SSH onto the VM:


```R
ssh ucloud@IP_address_from_the_red_mark
```

### Update VM


```R
sudo apt update
sudo apt upgrade -y 
sudo apt install nvidia-driver-525 nvidia-utils-525 -y  # Or newer version
```

### Download and Install Conda 


```R
# Download miniconda 
curl -s -L -o miniconda_installer.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 

# Install miniconda
bash miniconda_installer.sh -b -f -p miniconda3

# Set conda to path
export PATH=/home/ucloud/miniconda3/bin:$PATH # Set conda to path

# initialize conda
conda init && bash -i

# Reboot VM
sudo reboot
```

### Re-connect to VM using SSH 


```R
ssh ucloud@IP_address_from_the_red_mark
```

### Check nvidia driver Configuration


```R

nvidia-smi

# Expected Output
Mon Aug  7 09:38:25 2023
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.199.02   Driver Version: 470.199.02   CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:05.0 Off |                    0 |
| N/A   70C    P0    31W /  70W |      0MiB / 15109MiB |      7%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

### Create conda environment and test GPU configuration

```R
# Create conda environment 
conda deactivate
conda create --name my_env python
conda activate my_env

# Install cudatoolkit and cudnn
conda install -c conda-forge cudatoolkit cudnn

# Set pre-installed conda libraries to path
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
```

#### GPU conda environment is ready to use

### Compress Conda installation to tar.gz file

```R
tar -czvf /home/ucloud/miniconda3.tar.gz /home/ucloud/miniconda3
```

### Transfer "miniconda3.tar.gz" to local PC using SSH-Copy

Open a 2nd instance of a terminal app on local machine


```R
scp -r ucloud@IP_address_from_the_red_mark:/home/ucloud/miniconda3 "C:\path-to-folder"
```

## Transfer Conda install to a new AAU VM job

### Connect to VM using SSH

Open a terminal app on local machine and SSH onto the VM:


```R
ssh ucloud@IP_address_from_the_red_mark
```

### Update VM


```R
sudo apt update
sudo apt upgrade -y 
sudo apt install nvidia-headless-460 nvidia-utils-460 -y
```

### Transfer "miniconda3.tar.gz" from local PC to VM using SSH-Copy

Open a 2nd instance of a terminal app on local machine


```R
scp -r "C:\path-to-folder\miniconda.tar.gz ucloud@IP_address_from_the_red_mark:
```

### Unzip tar.gz

Move back to the terminal app connected to VM and run following command:


```R
tar -xzf miniconda.tar.gz
```

### Set Conda on path and initialise 


```R
# Set conda to path
export PATH=/home/ucloud/miniconda3/bin:$PATH # Set conda to path

# init conda
conda init && bash -i

# Reboot VM
sudo reboot
```

### Re-connect to VM using SSH 


```R
ssh ucloud@IP_address_from_the_red_mark
```

### Check nvidia driver configuration


```R
nvidia-smi

# Expected Output:
Mon Aug  7 09:41:34 2023
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.199.02   Driver Version: 470.199.02   CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:05.0 Off |                    0 |
| N/A   51C    P0    27W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

### Activate conda environment and test GPU configuration


```R
# Create conda environment 
conda deactivate
conda create --name my_env python
conda activate my_env

# Install cudatoolkit and cudnn
conda install -c conda-forge cudatoolkit cudnn

# Set pre-installed conda libraries to path (including cudatoolkit=11.2 cudnn=8.1.0 )
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/

#### GPU conda environment is ready to use
