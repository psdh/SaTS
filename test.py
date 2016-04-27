import numpy as np
import multiprocessing

def diff(args):
    x1 = args[0]
    x2 = args[1]
    return np.sqrt(np.sum((x1-x2)**2))

pool = multiprocessing.Pool()
a = [np.array([1, 2, 3]), np.array([4, 5, 6])]

results = pool.map(diff, a)
print results
