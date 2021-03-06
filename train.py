from scipy.fftpack import dct as dct
import numpy as np
import parmap
import math


def calculateC(series):
    """
        This is the primary function responsible for calculating the complexity
        measure for a given time series
    """

    complexityF = 0

    s1 = series[1:len(series) - 1]
    s2 = series[0:len(series) - 2]
    return np.linalg.norm(np.array(s1) - np.array(s2))

    # for i, ele in enumerate(series[:-1]):
    #     complexityF += (series[i] - series[i + 1]) ** 2

    # complexityF = math.sqrt(complexityF)
    # # print complexityF
    return complexityF


def calculateED(s0, s1):
    """
        Calculates euclidean distance between two series
    """
    return np.linalg.norm(s0 - s1)

def calculateCorr(s0, s1):
    """
        Calculates the correlation between the fourier transformation of the time series
    """
    return np.correlate(dct(s0, norm='ortho'), dct(s1, norm='ortho'))

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
