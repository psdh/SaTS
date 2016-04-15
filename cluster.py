# file to write the agglomerative clustering algorithm
import numpy as np

mat = np.array([0, 10, 15, 5, 10, 0, 25, 7, 15, 25, 0, 10, 5, 7, 10 ,0]).reshape(4, 4)

# def reshape(clusters):
#     counter = 0
#     for x in range(len(clusters.keys())):
#         if not clusters.has_key(x):

def generateMat(mat, i, j):
    answer = np.zeros(shape=(mat.shape[0] - 1, mat.shape[0] - 1))

    x = 0
    while x < i:
        answer[x] = mat[x]



def agglomerativeClustering(n_clus, mat):
    ini_clus = mat.shape[0]

    clusters = {}

    for x in  range(ini_clus):
        cluster[x] = [x]

    i, j = getClosestClusters(mat)

    clusters[min(i, j)] = clusters[min(i, j)] + clusters[max(i, j)]

    clusters.pop(max(i, j), None)

    # reshape(clusters)

    mat = generateMat(mat, min(i, j), max(i, j))

    for x in xrange(1, ini_clus + 1):
        distance[x] = []
