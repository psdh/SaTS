from scipy.fftpack import dct as dct
import numpy as np
import parmap
import math

global n
n = 501

def calculateC(series):
    """
        This is the primary function responsible for calculating the complexity
        measure for a given time series
    """
    s1 = np.array(series[1:len(series) - 1])
    s2 = np.array(series[0:len(series) - 2])
    return np.linalg.norm(s1 - s2)

def calculateED(s0, s1):
    """
        Calculates euclidean distance between two series
    """
    return np.linalg.norm(np.array(s0) - np.array(s1))

def fdist(s1, s2):
    """
        Calculates the correlation between the fourier transformation of the time series
    """
    dist = float(1)/(np.correlate(dct(s1, norm='ortho'), dct(s2, norm='ortho'))[0])
    return dist

def calcCF(series):
    distances = parmap.map(calculateC, series)
    print "len of distances: " + str(len(distances))
    return distances

def calc(series):
    len1 = len(series)
    ser = []
    for i in range(len1):
        for j in range(i+1, len1):
            ser.append([series[i], series[j]])

    distances = parmap.map(calculateED, ser)

    print "len of distances: " + str(len(distances))

    return distances

def CF(Q, C):
    CEQ = calculateC(Q)
    CEC = calculateC(C)
    # print CEQ
    # print CEC
    try:
        return float(max(CEQ, CEC)) / min(CEQ, CEC)
    except:
        return 1


def sum_ser(n):
    return (1.0 * n * (n+1))/2.0


def CID(Q, C):
    return calculateED(Q, C) * CF(Q, C)


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

    CID(500, 501, distancesED, CFdistances)

    # print CFdistances

    print "Now clustering"

    from hcluster import hcluster
    hcluster(features, distancesED, CFdistances)

if __name__ == '__main__':
    main()
