# This Python file uses the following encoding: utf-8
import numpy as np
import time
import os
import argparse
import json

from joblib import Parallel, parallel_backend
from joblib import register_parallel_backend
from dask.distributed import Client


from sklearn.datasets import load_digits
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC

param_space = {
    'C': np.logspace(-6, 6, 30),
    'gamma': np.logspace(-8, 8, 30),
    'tol': np.logspace(-4, -1, 30),
    'class_weight': [None, 'balanced'],
}

model = SVC(kernel='rbf')
search = RandomizedSearchCV(model, param_space, cv=10, n_iter=500,verbose=1)
digits = load_digits()

start_time = time.perf_counter()

#Using the distributed shared file system, we can access to the Dask cluster
# configuration.
# We read the scheduler address and port from the scheduler file
with open(os.environ["SCHEDULER_FILE"]) as f:
        data = json.load(f)
        scheduler_address=data['address']

# Connect to the the cluster
client = Client(scheduler_address)
#client.wait_for_workers(n_workers = os.environ["NBWORKERS"])
client.wait_for_workers(n_workers = 3)
client

with parallel_backend('dask',wait_for_workers_timeout=20):
 search.fit(digits.data,digits.target)
finish_time = time.perf_counter()
print(finish_time-start_time)
client.shutdown()
