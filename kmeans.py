from multiprocessing import Pool
from numpy import genfromtxt
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
from train import CID, fdist
import random
import parmap

import time

clusters = {}

def norm(x, y):
    return np.linalg.norm(x - y)

distance = fdist

def cluster_points(args):
    X = args[0]
    mu = args[1]

    dist = []
    for i in range(len(X)):
        d = []
        for j in range(len(mu)):
            d.append(distance(mu[j][1:], odata[i][1:]))
        dist.append(d)

    out = []

    for i in range(len(dist)):
        out.append([X[i], np.argmin(dist[i])])
    return out

def reevaluate_centers(dim):
    newmu = []

    from pprint import pprint

    keys = sorted(clusters.keys())

    # print len(keys)

    for k in keys:
        if(clusters[k] == []):
            newmu.append(dim*[0.0])
        else:
            newmu.append(np.mean(clusters[k], axis = 0))

    # print "len newmu: " + str(len(newmu))
    # print newmu

    return newmu


def has_converged(mu, oldmu):
    flag = 0
    for i in range(len(mu)):
        for d in range(len(mu[0])):
            if(abs(mu[i][d]-oldmu[i][d]) > 0.001):
                return 0
    return 1

def find_centers(X, K):
    # Initialize to K random centers
    random.seed(100)
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    it = 0
    while not has_converged(mu, oldmu):
        it += 1
        for i in range(len(clusters)):
            clusters[i] = []

        oldmu = mu
        # Assign all points in X to clusters
        proc = 4
        arg =[]
        s = 0
        add = len(X)/proc

        for i in range(proc-1):
            arg.append([X[s:s+add], mu])
            s = s + add

        arg.append([X[s:], mu])

        pool = multiprocessing.Pool(processes=proc)
        keys_put = pool.map(cluster_points, arg)

        for clust in keys_put:
            for point in clust:
                clusters[point[1]].append(point[0])
        print it
        # Reevaluate centers
        mu = reevaluate_centers(len(X[0]))
        pool.close()
    # print clusters
    return(mu, clusters)
# def remove_first(*args):

def predict(centres, clusters, X):
    dist = []
    for i in range(len(X)):
        d = []
        for j in range(len(centres)):
            d.append(distance(centres[j][1:], X[i][1:]))
        dist.append(d)

    out = []

    for i in range(len(dist)):
        out.append(np.argmin(dist[i]))
    # print out
    # index of point
    purity = {}

    for i in range(clust):
        purity[i] = 0
    # print purity
    print "purity of predicted cluster"
    # print clusters
    # for cnum in range(clust):
    #     for i in range(len(clusters[cnum])):
    #         purity[int(clusters[cnum][i][0]) - 1] += 1
    #     print purity
        # purity = {}

    while(1):
        plt.close()
        idx = int(raw_input("line to classify?\n"))
        plt.plot(X[idx], label = "test curve")
        print "species of data point is " + str(X[idx][0])
        print "predicted cluster is " + str(out[idx])
        rlist = random.sample(range(len(clusters[out[idx]])), 5)
        print "species of nearby is "
        for r in rlist:
            print clusters[out[idx]][r][0]
            plt.plot(clusters[out[idx]][r][1:], label = "curve" + str(r))
        # print clusters
        plt.legend()
        # for i in range(10):
        #     print clusters[out[idx]][i][0]
        # print purity
        plt.show()
    return out


filename = "./data/SwedishLeaf_TEST"
odata = genfromtxt(filename, delimiter=',')

ts = time.clock()

# number of clusters
clust = 5
for i in range(clust):
    clusters[i] = []

filename = "./data/SwedishLeaf_TRAIN"
test = genfromtxt(filename, delimiter=',')


(centres, clusters) = find_centers(odata, clust)
predict(centres, clusters, test)

print "time taken: "
print time.clock() - ts
