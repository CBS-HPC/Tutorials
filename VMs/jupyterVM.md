# UCloud Tutorial: Setting up an interactive jupyter notebook session on AAU VMs

### Connect to VM using SSH

Open a terminal app on local machine and SSH onto the VM:


```R
ssh ucloud@IP_address_from_the_red_mark
```

### Install jupyter if needed: 


```R
# Using pip
pip install jupyterlab

# Using conda if conda environment are utilised 
conda install jupyter
```

### Make sure jupyter is installed

In this case jupyter is installed and activated through a conda environment. Please see 


```R
which jupyter

# Example Output:
/home/ucloud/miniconda3/envs/my_env/bin/jupyter
```

### Start Jupyter Notebook from remote server


```R
jupyter notebook --no-browser --port=8080

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
ssh -L 8080:localhost:8080 ucloud@IP_address_from_the_red_mark
```

### Now press the links in the output above and it should open a jupyter notebook
