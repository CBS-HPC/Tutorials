# Tensorflow: Train your deep-learning models on AAU GPUs

This tutorial show how to apply "Distributed Data Parallel (DDP) using Tensorflow/Keras" to efficiently train your deep-learning models on the AAU GPUs avalaible through UCloud.

See [here](https://www.tensorflow.org/guide/keras/distributed_training) for a more detailed tutorial on DDP using Tensorflow.

This tutorial specifically focuses on [Multi-GPU DDP Training with fault tolerance](https://www.tensorflow.org/guide/keras/distributed_training#using_callbacks_to_ensure_fault_tolerance)

The following python script is needed to replicate this tutorial: 

- [multigpu_torchrun.py](https://github.com/CBS-HPC/Tutorials/tree/main/AI/multigpu_tensorflow.py) (Can be used as template)


Prerequisite reading:

- [How to Generate SSH key](/Tutorials/VMs/shh/)

- [Access VM using SSH](/Tutorials/VMs/connectVM/)

- [Using Conda for easy workflow deployment on AAU GPU VMs](/Tutorials/VMs/condaVM/)


### Update VM


```R
sudo apt update
sudo apt upgrade -y 
sudo apt install nvidia-headless-460 nvidia-utils-460 -y
```

### Activate Conda

This can be done by either installing a conda from scratch or by deploying er prior installation. Please see  ["Using Conda for easy workflow deployment on AAU GPU VMs"](/Tutorials/VMs/condaVM/) for information.


```R
# Download and install miniconda 
curl -s -L -o miniconda_installer.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
bash miniconda_installer.sh -b -f -p miniconda3

# OR 

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

### Create or re-load a Tensorflow/Keras Conda environment


```R
# Create pytorch conda environment if non-exist on the Conda installation
conda deactivate
conda create --name tensorflow
conda activate tensorflow
conda install -c anaconda tensorflow-gpu

# Set pre-installed conda libraries to path (including cudatoolkit=11.2 cudnn=8.1.0 )
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
```


### Transfer Files and Folders (SSH-Copy) to VM
Open a second terminal (1st terminal is connected to the VM):


```R
scp -r "C:\path\pytorch_folder" ucloud@IP_address_from_the_red_mark:
```

### Run Tensorflow training in DDP mode: 

In this example a model is trained for 10 epocs using 2 GPUs with a model checkpoint being saved with "ckpt" folder for each epoc and the final model being saved as "final_model.keras". 

functions "get_compiled_model" and "get_dataset" need to be changed to adjust training data and model.


```R
# Run the model with 10 epcos and 2 GPUs
python multigpu_tensorflow.py 10 2

# Run the model with 10 epcos and all avaiable GPUs
python multigpu_tensorflow.py 10
```

### Transfer Results and Conda enviroment local machine (SSH-Copy)
Open a second terminal (1st terminal is connected to the VM):


```R
scp -r ucloud@IP_address_from_the_red_mark:/home/ucloud/folder "C:\path-to-folder"
```
