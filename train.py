import numpy as np
import parmap
import math


# series is a matrix of series
# TODO<shivin> parallelize this to use multiple cores

global n
n = 501

def calculateC(series):
    """
        This is the primary function responsible for calculating the complexity
        measure for a given time series
    """

    complexityF = 0

    # can make this step multi-core to speed up things
    for i, ele in enumerate(series[:-1]):
        complexityF += (series[i] - series[i + 1]) ** 2

    complexityF = math.sqrt(complexityF)

    return complexityF


# TODO<shivin> parallelize this to use multiple cores
def calculateED(s):
    """
        Calculates euclidean distance between two series
    """
    return np.sqrt(np.sum((s[1] - s[0])**2))

def calcCF(series):
    distances = parmap.map(calculateC, series)

    print "len of distances: " + str(len(distances))

    return distances

def calc(series):
    len1 = len(series)
    ser = []
    for i in range(len1):
<<<<<<< HEAD
        for j in range(i + 1, len1):
            ser.append([series[i], series[j]])
    res = parmap.map(calculateED, ser, processes=50)
    return np.array(res)
=======
        for j in range(i+1, len1):
            ser.append([series[i], series[j]])

    distances = parmap.map(calculateED, ser)

    print "len of distances: " + str(len(distances))

    return distances

def CF(Q, C, cf):
    CEQ = cf[Q-1]
    CEC = cf[C-1]

    try:
        return float(max(CEQ, CEC)) / min(CEQ, CEC)
    except:
        return 1


def sum_ser(n):
    return (1.0 * n * (n+1))/2.0


def CID(Q, C, ed, cf):
    Q = abs(Q)
    C = abs(C)
    mi = min(Q, C)
    ma = max(Q, C)


    print
    print mi
    print ma
    ed_Q_C = ed[int(sum_ser(n-1) - sum_ser(n-1-mi) - 1 + (ma - mi - 1))]

    print ed_Q_C
    return ed_Q_C * CF(Q, C, cf)


def main():

    filename = "data/SwedishLeaf_TRAIN"

    data = open(filename, 'r').read()

    data = data.split('\n')

    print len(data)
    features = np.zeros(shape=(len(data), 128))

    for i, x in enumerate(data):
        if (len(x) == 0):
            continue
        features[i] = (x.split(','))[1:]

    distancesED = calc(features)

    CFdistances = calcCF(features)
>>>>>>> f95df29e4cb8eaf42bd3a54ec3c1e16d3336a1ab

    CID(500, 501, distancesED, CFdistances)

    print CFdistances

    print "Now clustering"

    from hcluster import hcluster
    hcluster(features, distancesED, CFdistances)

if __name__ == '__main__':
    main()
