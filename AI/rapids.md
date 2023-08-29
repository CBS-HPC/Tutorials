# RAPIDS-cuML: Train your Scikit-learn models on AAU GPUs

This tutorial show how to deploy [RAPIDS-cuML-GPU Machine Learning Algorithms](https://github.com/rapidsai/cuml) to efficiently train your scikit-learn models on the AAU GPUs avalaible through UCloud. 

"cuML is a suite of libraries that implement machine learning algorithms and mathematical primitives functions. cuML enables data scientists, researchers, and software engineers to run traditional tabular ML tasks on GPUs without going into the details of CUDA programming. For large datasets, these GPU-based implementations can complete 10-50x faster than their CPU equivalents. For details on performance, see the [cuML Benchmarks Notebook](https://github.com/rapidsai/cuml/tree/branch-23.04/notebooks/tools)."

 **In most cases, cuML's Python API matches the API from scikit-learn. which will make it easy to navigate to scikit-learn to RAPIDS-cuML**

A table of the supported algoritmns can be found [here](https://github.com/rapidsai/cuml#supported-algorithms). 

This tutorial will use a random forrest which can be found on the [cuML notebook examples](https://github.com/rapidsai/cuml/tree/branch-23.04/notebooks)

The following python script is needed to replicate this tutorial: 

- [multigpu_rapids.py](https://github.com/CBS-HPC/Tutorials/tree/main/AI/multigpu_rapids.py) (Can be used as template)


Prerequisite reading:

- [How to Generate SSH key](/Tutorials/VMs/shh/)

- [Access VM using SSH](/Tutorials/VMs/connectVM/)

- [Using Conda for easy workflow deployment on AAU GPU VMs](/Tutorials/VMs/condaVM/)

### Update VM


```R
sudo apt update
sudo apt upgrade -y 
sudo apt install nvidia-driver-525 nvidia-utils-525 -y  # Or newer version
```

### Activate Conda

This can be done by either installing a conda from scratch or by deploying er prior installation. Please see  ["Using Conda for easy workflow deployment on AAU GPU VMs"](/Tutorials/VMs/condaVM/) for information.


```R
# Download and install miniconda (If needed)
curl -s -L -o miniconda_installer.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
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

### Create or re-load a RAPIDS Conda environment

look for latest RAPIDS installation at https://docs.rapids.ai/install


```R
# Create pytorch conda environment if non-exist on the Conda installation
conda deactivate
conda create --solver=libmamba -n rapids -c rapidsai -c conda-forge -c nvidia  \
    rapids=23.08 python=3.10 cuda-version=11.8


# Set pre-installed conda libraries to path (including cudatoolkit=11.2 cudnn=8.1.0 )
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
```


### Transfer Files and Folders (SSH-Copy) to VM
Open a second terminal (1st terminal is connected to the VM):


```R
scp -r "C:\path\pytorch_folder" ucloud@IP_address_from_the_red_mark:
```

### Run a Random Forrest training on multiple GPUs: 


```R
python multigpu_rapids.py
```


```R
import numpy as np
import sklearn
import time

import pandas as pd
import cudf
import cuml

from sklearn import model_selection

from cuml import datasets
from cuml.metrics import accuracy_score
from cuml.dask.common import utils as dask_utils
from dask.distributed import Client, wait
from dask_cuda import LocalCUDACluster
import dask_cudf

from cuml.dask.ensemble import RandomForestClassifier as cumlDaskRF
from sklearn.ensemble import RandomForestClassifier as sklRF


if __name__ == "__main__":
    ### Start Dask cluster
    # This will use all GPUs on the local host by default
    cluster = LocalCUDACluster(n_workers=2)
    #cluster = LocalCUDACluster(threads_per_worker=1)
    c = Client(cluster)

    # Query the client for all connected workers
    workers = c.has_what().keys()
    n_workers = len(workers)
    n_streams = 8 # Performance optimization

    ### Define Parameters
    # Data parameters
    train_size = 500000
    test_size = 1000
    n_samples = train_size + test_size
    n_features = 20

    # Random Forest building parameters
    max_depth = 12
    n_bins = 16
    n_trees = 5000

    ### Generate Data on host
    X, y = datasets.make_classification(n_samples=n_samples, n_features=n_features,
                                    n_clusters_per_class=1, n_informative=int(n_features / 3),
                                    random_state=123, n_classes=5)
    X = X.astype(np.float32)
    y = y.astype(np.int32)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_size)

    ### Distribute data to worker GPUs
    n_partitions = n_workers

    def distribute(X, y):
        # First convert to cudf (with real data, you would likely load in cuDF format to start)
        X_cudf = cudf.DataFrame(X)
        y_cudf = cudf.Series(y)

        # Partition with Dask
        # In this case, each worker will train on 1/n_partitions fraction of the data
        X_dask = dask_cudf.from_cudf(X_cudf, npartitions=n_partitions)
        y_dask = dask_cudf.from_cudf(y_cudf, npartitions=n_partitions)

        # Persist to cache the data in active memory
        X_dask, y_dask = \
        dask_utils.persist_across_workers(c, [X_dask, y_dask], workers=workers)
        
        return X_dask, y_dask

    X_train_dask, y_train_dask = distribute(X_train, y_train)
    X_test_dask, y_test_dask = distribute(X_test, y_test)

    ### Build a scikit-learn model (single node)
    # Use all available CPU cores
    #skl_model = sklRF(max_depth=max_depth, n_estimators=n_trees, n_jobs=-1)
    #skl_model.fit(X_train.get(), y_train.get())
    #finish_time = time.perf_counter()

    ### Predict
    #skl_y_pred = skl_model.predict(X_test.get())
    #print("SKLearn accuracy:  ", accuracy_score(y_test, skl_y_pred))

    ### Train the distributed cuML model
    cuml_model = cumlDaskRF(max_depth=max_depth, n_estimators=n_trees, n_bins=n_bins, n_streams=n_streams)
    cuml_model.fit(X_train_dask, y_train_dask)
    wait(cuml_model.rfs) # Allow asynchronous training tasks to finishfinish_time = time.perf_counter()
    finish_time = time.perf_counter()

    ### Predict
    cuml_y_pred = cuml_model.predict(X_test_dask).compute().to_numpy()
    print("CuML accuracy:     ", accuracy_score(y_test, cuml_y_pred))
```

### Track the GPU usage 


```R
nvidia-smi -l 5 # Will update every 5 seconds

# Expected Output
Mon Aug  7 09:38:25 2023
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      1011      G   /usr/lib/xorg/Xorg                  4MiB |
|    0   N/A  N/A      2312      C   python                           1324MiB |
|    0   N/A  N/A      2381      C   ...a3/envs/rapids/bin/python     1042MiB |
|    1   N/A  N/A      1011      G   /usr/lib/xorg/Xorg                  4MiB |
|    1   N/A  N/A      2383      C   ...a3/envs/rapids/bin/python     1042MiB |
+-----------------------------------------------------------------------------+
Tue Aug 29 11:04:31 2023
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.125.06   Driver Version: 525.125.06   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            Off  | 00000000:00:05.0 Off |                    0 |
| N/A   38C    P0    49W /  70W |   2389MiB / 15360MiB |     93%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   1  Tesla T4            Off  | 00000000:00:06.0 Off |                    0 |
| N/A   36C    P0    53W /  70W |   1067MiB / 15360MiB |     93%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
```

### Transfer Results and Conda enviroment local machine (SSH-Copy)
Open a second terminal (1st terminal is connected to the VM):


```R
scp -r ucloud@IP_address_from_the_red_mark:/home/ucloud/folder "C:\path-to-folder"
```
