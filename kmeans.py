from numpy import genfromtxt
import numpy as np
import random
import parmap
import multiprocessing

import time

clusters = {}

def cluster_points(args):
    X = args[0]
    mu = args[1]

    # print  "len of x:" + str(len(x))

    # print "len of  mu: " + str(len(mu))
    # bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
    #             for i in enumerate(mu)], key=lambda t:t[1])[0]
    # print bestmukey

    dist = []
    for i in range(len(X)):
        d = []
        for j in range(len(mu)):
            d.append(np.linalg.norm(mu[j] - odata[i]))
        dist.append(d)

    out = []

    for i in range(len(dist)):
        out.append([X[i], np.argmin(dist[i])])
    return out

def reevaluate_centers(dim):
    newmu = []

    from pprint import pprint
    # pprint(len(clusters[0]) + len(clusters[1]) + len(clusters[2]) + len(clusters[3]) + len(clusters[4]))

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
    while it < 50:
        it += 1
        for i in range(len(clusters)):
            clusters[i] = []

        oldmu = mu
        # Assign all points in X to clusters

        proc = 3
        arg =[]
        s = 0
        add = len(X)/proc

        for i in range(proc-1):
            arg.append([X[s:s+add], mu])
            s = s + add

        arg.append([X[s:], mu])

        tn = time.clock()

        pool = multiprocessing.Pool(processes=proc)
        keys_put = pool.map(cluster_points, arg)

        print "intermediate time: "
        print time.clock() - tn
        for clust in keys_put:
            for point in clust:
                clusters[point[1]].append(point[0])
        print it
        # Reevaluate centers
        mu = reevaluate_centers(len(X[0]))
        pool.close()

    return(mu, clusters)
# def remove_first(*args):

filename = "./data/StarLightCurves_TRAIN"
odata = genfromtxt(filename, delimiter=',')

ts = time.clock()

# len_4 = len(odata)/4

# first_loc_del = [odata[:len_4], odata[len_4:2*len_4], odata[2*len_4:3*len_4], odata[3*len_4:]]

# multiprocessing.Pool(processes=4).map(remove_first, first_loc_del)
# import sys
# sys.exit(0)
clusters[0] = []
clusters[1] = []
clusters[2] = []
clusters[3] = []
clusters[4] = []

find_centers(odata, 5)[1]

print "time taken: "
print time.clock() - ts
