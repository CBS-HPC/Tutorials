# This Python file uses the following encoding: utf-8
import numpy as np
import time
import os
import argparse

from joblib import Parallel, parallel_backend
from joblib import register_parallel_backend
from ipyparallel import Client
from ipyparallel.joblib import IPythonParallelBackend

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

c = Client(profile=os.environ["profile"])
print(c.ids)
#c.wait_for_engines( int(os.environ.get("NB_WORKERS",1)))
bview = c.load_balanced_view()
# this is taken from the ipyparallel source code
register_parallel_backend('ipyparallel', lambda : IPythonParallelBackend(view=bview))

with parallel_backend('ipyparallel'):
 search.fit(digits.data,digits.target)
finish_time = time.perf_counter()
print(finish_time-start_time)
c.shutdown()
