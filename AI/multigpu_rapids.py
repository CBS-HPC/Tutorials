
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
    #start_time = time.perf_counter()
    #skl_model = sklRF(max_depth=max_depth, n_estimators=n_trees, n_jobs=-1)
    #skl_model.fit(X_train.get(), y_train.get())
    #finish_time = time.perf_counter()
    #print(finish_time-start_time)
    ### Predict
    #skl_y_pred = skl_model.predict(X_test.get())
    #print("SKLearn accuracy:  ", accuracy_score(y_test, skl_y_pred))

    ### Train the distributed cuML model
    start_time = time.perf_counter()
    cuml_model = cumlDaskRF(max_depth=max_depth, n_estimators=n_trees, n_bins=n_bins, n_streams=n_streams)
    cuml_model.fit(X_train_dask, y_train_dask)
    wait(cuml_model.rfs) # Allow asynchronous training tasks to finishfinish_time = time.perf_counter()
    finish_time = time.perf_counter()
    print(finish_time-start_time)
    ### Predict
    cuml_y_pred = cuml_model.predict(X_test_dask).compute().to_numpy()
    print("CuML accuracy:     ", accuracy_score(y_test, cuml_y_pred))