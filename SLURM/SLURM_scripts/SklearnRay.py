# This Python file uses the following encoding: utf-8
import numpy as np
import time
import ray
from joblib import parallel_backend
from sklearn.datasets import load_digits
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from ray.util.joblib import register_ray
register_ray()

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
ray.init(address="auto")
with parallel_backend('ray'):
 search.fit(digits.data,digits.target)
finish_time = time.perf_counter()
print(finish_time-start_time)
ray.shutdown()
