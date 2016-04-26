import numpy as np
import parmap
import math


# series is a matrix of series
# TODO<shivin> parallelize this to use multiple cores


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
def calculateED(s0, s1):
    """
        Calculates euclidean distance between two series
    """
    return np.sqrt(np.sum((s1 - s0)**2))


def calc(series):
    len1 = len(series)
    ser = []
    for i in range(len1):
        for j in range(i, len1):
            ser.append([series[i], series[j]])

    parmap.map(calculateED, ser)


def CF(Q, C):
    CEQ = calculateC(Q)
    CEC = calculateC(C)

    try:
        return float(max(CEQ, CEC)) / min(CEQ, CEC)
    except:
        return 1

def CID(Q, C):
    return calculateED(Q, C) * CF(Q, C)


def main():

    filename = "data/SwedishLeaf_TRAIN"

    data = open(filename, 'r').read()

    data = data.split('\n')

    features = np.zeros(shape=(len(data), 128))

    for i, x in enumerate(data):
        if (len(x) == 0):
            continue
        features[i] = (x.split(','))[1:]

    print "Now clustering"

    from hcluster import hcluster
    hcluster(features)

if __name__ == '__main__':
    main()
