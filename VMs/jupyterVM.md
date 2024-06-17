# Run Python and R jupyter notebooks on AAU VMs

Prerequisite reading:

- [How to Generate SSH key](/Tutorials/SHH/shh_create/)

- [Access VM using SSH](/Tutorials/SSH/ssh_connect/)

- [Conda: for easy workflow deployment on AAU GPU VMs](/Tutorials/VMs/condaVM/)

### Connect to VM using SSH

Open a terminal app on local machine and SSH onto the VM:


```R
ssh ucloud@IP_address_from_the_red_mark
```

## Install or activate Conda installation

See ["Conda: for easy workflow deployment on AAU GPU VMs"](/Tutorials/VMs/condaVM/) for more information.

## Install and/or activate existing Python or R Environment using Conda


```R
# Python 
conda deactivate
conda create --name myenv_python python
conda activate myenv_python
conda install ipykernel
conda install nb_conda_kernels

# R 
conda deactivate
conda create --solver=libmamba -n myenv_R -y -c conda-forge r-base
conda activate myenv_R
conda install -c conda-forge r-irkernel
conda install nb_conda_kernels

# Install cudatoolkit and cudnn
conda install -c conda-forge cudatoolkit cudnn

# Set pre-installed conda libraries to path
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
```

### Check jupyter installtion and get config-directory


```R
which jupyter

# Example Output:
/home/ucloud/miniconda3/envs/my_env/bin/jupyter

# Get config-directory
jupyter --config-dir

# Example Output:
/home/ucloud/.jupyter/

# Create folder if does not exist
 mkdir -p /home/ucloud/.jupyter/

# Create jupyter_config.json  in config-dir
echo '{"CondaKernelSpecManager": {"kernelspec_path": "--user"}}' > /home/ucloud/.jupyter/jupyter_config.json

# Check content of jupyter_config.json

cat /home/ucloud/.jupyter/jupyter_config.json
```

### Install nb_conda_kernels

https://github.com/Anaconda-Platform/nb_conda_kernels#installation


```R
# Export all existing conda environment with ipykernel or r-irkernel installed
python -m nb_conda_kernels list

# Example Output: 
[ListKernelSpecs] WARNING | Config option `kernel_spec_manager_class` not recognized by `ListKernelSpecs`.
[ListKernelSpecs] Removing existing kernelspec in /home/ucloud/.local/share/jupyter/kernels/conda-env-jupyter-py
[ListKernelSpecs] Installed kernelspec conda-env-jupyter-py in /home/ucloud/.local/share/jupyter/kernels/conda-env-jupyter-py
[ListKernelSpecs] Installed kernelspec conda-env-my_env-py in /home/ucloud/.local/share/jupyter/kernels/conda-env-my_env-py
[ListKernelSpecs] Removing existing kernelspec in /home/ucloud/.local/share/jupyter/kernels/conda-env-myenv-py
[ListKernelSpecs] Installed kernelspec conda-env-myenv-py in /home/ucloud/.local/share/jupyter/kernels/conda-env-myenv-py
[ListKernelSpecs] Removing existing kernelspec in /home/ucloud/.local/share/jupyter/kernels/conda-env-rapids-py
[ListKernelSpecs] Installed kernelspec conda-env-rapids-py in /home/ucloud/.local/share/jupyter/kernels/conda-env-rapids-py
[ListKernelSpecs] [nb_conda_kernels] enabled, 4 kernels found
Available kernels:
  conda-env-jupyter-py    /home/ucloud/miniconda3/envs/jupyter/share/jupyter/kernels/python3
  conda-env-myenv-py      /home/ucloud/miniconda3/envs/myenv/share/jupyter/kernels/python3
  conda-env-rapids-py     /home/ucloud/miniconda3/envs/rapids/share/jupyter/kernels/python3
  conda-env-my_env-py     /home/ucloud/miniconda3/envs/my_env/share/jupyter/kernels/python3
```

### Check that the conda environment kernels are discovered by jupyter:


```R
jupyter kernelspec list

# Example output:
[ListKernelSpecs] WARNING | Config option `kernel_spec_manager_class` not recognized by `ListKernelSpecs`.
0.00s - Debugger warning: It seems that frozen modules are being used, which may
0.00s - make the debugger miss breakpoints. Please pass -Xfrozen_modules=off
0.00s - to python to disable frozen modules.
0.00s - Note: Debugging will proceed. Set PYDEVD_DISABLE_FILE_VALIDATION=1 to disable this validation.
Available kernels:
  python3                 /home/ucloud/miniconda3/envs/my_env/share/jupyter/kernels/python3
  conda-env-jupyter-py    /home/ucloud/.local/share/jupyter/kernels/conda-env-jupyter-py
  conda-env-my_env-py     /home/ucloud/.local/share/jupyter/kernels/conda-env-my_env-py
  conda-env-myenv-py      /home/ucloud/.local/share/jupyter/kernels/conda-env-myenv-py
  conda-env-rapids-py     /home/ucloud/.local/share/jupyter/kernels/conda-env-rapids-py
```

### Start Jupyter Notebook from remote server


```R
jupyter notebook --no-browser --port=8080 # Change the port number if multiple jupyter notebook are started within the same session

# Output

[I 10:26:32.873 NotebookApp] Serving notebooks from local directory: /home/ucloud
[I 10:26:32.873 NotebookApp] The Jupyter Notebook is running at:
[I 10:26:32.873 NotebookApp] http://localhost:8080/?token=b754cbea9f5a6640e647f21c7d2e7112a6954eb26f032d73
[I 10:26:32.873 NotebookApp]  or http://127.0.0.1:8080/?token=b754cbea9f5a6640e647f21c7d2e7112a6954eb26f032d73
[I 10:26:32.873 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 10:26:32.899 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/ucloud/.local/share/jupyter/runtime/nbserver-3074-open.html
    Or copy and paste one of these URLs:
        http://localhost:8080/?token=b754cbea9f5a6640e647f21c7d2e7112a6954eb26f032d73
     or http://127.0.0.1:8080/?token=b754cbea9f5a6640e647f21c7d2e7112a6954eb26f032d73

```

### SSH connect to VM using a new terminal app on local machine

Open a 2nd instance of Terminal on Local machine


```R
ssh -L 8080:localhost:8080 ucloud@IP_address_from_the_red_mark # Change the port number if multiple jupyter notebook are started within the same session
```

### Open Jupyter Notebook

Press the link in the output above and it should open a jupyter notebook

Now the R and Python kernel should be available (see figure below)

![](/Tutorials/VMs/kernel_choice.PNG "kernel")

![](/Tutorials/VMs/kernel_choice2.PNG "kernel")
