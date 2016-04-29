from numpy import genfromtxt
import numpy as np
import random
import parmap
import multiprocessing

import time

clusters = {}

def cluster_points(args):
    x = args[0]
    mu = args[1]

    # print  "len of x:" + str(len(x))

    # print "len of  mu: " + str(len(mu))
    # bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
    #             for i in enumerate(mu)], key=lambda t:t[1])[0]
    # print bestmukey

    dist = []

    for cen in mu:
        dist.append(np.linalg.norm(cen - x))

    bestmukey = dist.index(min(dist))

    return bestmukey

    # try:

    # clusters[bestmukey].append(x)

    # from pprint import  pprint
    # pprint(clusters)


    # except:
    #     clusters[bestmukey] = [x]

    # print len(clusters.keys())


def reevaluate_centers():
    newmu = []

    from pprint import  pprint
    pprint(len(clusters[0]) + len(clusters[1]) + len(clusters[2]) + len(clusters[3]) + len(clusters[4]))

    keys = sorted(clusters.keys())

    print len(keys)

    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))

    print "len newmu: " + str(len(newmu))
    print newmu

    return newmu


def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))


def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    it = 0
    while it < 10 and not has_converged(mu, oldmu):
        it += 1

        print "did  one cycle"

        oldmu = mu
        # Assign all points in X to clusters
        arg = [[x, mu] for x in X]

        keys_put = multiprocessing.Pool(processes=8).map(cluster_points, arg)

        print "length of keys_put: " + str(len(keys_put))
        for key in keys_put:
            clusters[key] = []

        for i, key in enumerate(keys_put):
            clusters[key].append(X[i])

        # Reevaluate centers
        mu = reevaluate_centers()

    return(mu, clusters)
# def remove_first(*args):

filename = "data/StarLightCurves_TEST"
odata = genfromtxt(filename, delimiter=',')
print len(odata)

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
