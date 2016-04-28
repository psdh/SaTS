from numpy import genfromtxt
from multiprocessing import Pool
import numpy as np
import random
import parmap

def cluster_points(args):
    clusters  = {}
    x = args[0]
    mu = args[1]
    bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
                for i in enumerate(mu)], key=lambda t:t[1])[0]
    #print bestmukey
    try:
        clusters[bestmukey].append(x)
    except KeyError:
        clusters[bestmukey] = [x]
    return clusters

def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu

def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))

def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        arg = [[x, mu] for x in X]
        pool = Pool(processes=1)
        clusters = pool.map(cluster_points, arg, chunksize=1)[0]
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)


filename = "data/StarLightCurves_TEST"
odata = genfromtxt(filename, delimiter=',')
find_centers(odata, 5)[1]