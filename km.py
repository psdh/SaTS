from profilehooks import profile
from numpy import genfromtxt
import numpy as np
import random
import parmap

# cntr is one centroid point
def l2(odata, cntr):
    return np.sum((odata - cntr)**2, axis=1)

def calcdist(args):
    x = args[0]
    mu = args[1]
    idx = args[2]
    print distance(x, mu[idx])
    return [idx, distance(x, mu[idx])]

def findMin(res):
    out = []
    # check for all data points
    for i in range(len(res[0][1])):
        min1 = np.inf
        minpos = -1
        # len(res) = number of centroid points
        for j in range(len(res)):
            if res[j][1][i] < min1:
                min1 = res[j][1][i]
                # the index
                minpos = res[j][0]
        out.append(minpos)
    return out


def caldist(args):
    X = args[0]
    idx = args[1]
    mu = args[2]
    return [idx, l2(X, mu)]

def cluster_points(X, mu):
    clusters  = {}

    # calculate distance of x from every centroid, i[0] is first centroid
    for x in X:
        arg = [[x, mu, i[0]] for i in enumerate(mu)]
        # print len(arg)
        # bestmukey = parmap.map(calcdist, arg, processes=4)
        # print "executed parmap"
        # bestmukey = min(bestmukey, key=lambda t:t[1])[0]
        bestmukey = np.argmin([np.linalg.norm(x-mu[i[0]]) \
                    for i in enumerate(mu)])
        try:
            clusters[bestmukey[i]].append(X[i])
        except KeyError:
            clusters[bestmukey[i]] = [X[i]]
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
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)


filename = "data/StarLightCurves_TEST"
odata = genfromtxt(filename, delimiter=',')
find_centers(odata, 5)[1]
