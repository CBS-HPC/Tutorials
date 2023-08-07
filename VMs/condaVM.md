# UCloud Tutorial: Using Conda for easy deployment on AAU VMs

Introduction text

https://docs.cloud.sdu.dk/hands-on/conda-setup.html?highlight=conda

The Conda package and environment management system is already included in few applications available on UCloud (see, e.g., JupyerLab and PyTorch). For more general uses of Conda and its powerful package manager it is convenient to create a local installation and save it in a UCloud project.
Conda is included in all versions of Anaconda and Miniconda. For example, to install the latest version of Miniconda, just start any interactive app on UCloud, such as Terminal, and run the following shell commands:

## Initial installation of Conda on a AAU VM job

### SSH to Server through local Terminal

Add public SSH key while starting a VM job

![](startjob.png "startjob")

Identify VM IP when UCloud job is ready.

![](jobready.png "jobready")

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
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0

# Set pre-installed conda libraries to path (including cudatoolkit=11.2 cudnn=8.1.0 )
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/

# install tensorflow
pip install --upgrade pip; pip install tensorflow

# test if tensorflow is probably configurated:
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
# Expected Output
2023-08-07 09:58:29.129577: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1639] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 13775 MB memory:  -> device: 0, name: Tesla T4, pci bus id: 0000:00:05.0, compute capability: 7.5
tf.Tensor(-875.0791, shape=(), dtype=float32)
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
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0

# Set pre-installed conda libraries to path (including cudatoolkit=11.2 cudnn=8.1.0 )
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/

# install tensorflow
pip install --upgrade pip; pip install tensorflow

# test if tensorflow is probably configurated:
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

# Expected Output
2023-08-07 09:58:29.129577: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1639] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 13775 MB memory:  -> device: 0, name: Tesla T4, pci bus id: 0000:00:05.0, compute capability: 7.5
tf.Tensor(-875.0791, shape=(), dtype=float32)
```

#### GPU conda environment is ready to use
