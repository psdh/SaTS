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
def calculateED(s):
    """
        Calculates euclidean distance between two series
    """
    return np.sqrt(np.sum((s[1] - s[0])**2))


def calc(series):
    len1 = len(series)
    ser = []
    for i in range(len1):
        for j in range(i + 1, len1):
            ser.append([series[i], series[j]])
    res = parmap.map(calculateED, ser, processes=50)
    return np.array(res)


def CF(Q, C):
    CEQ = calculateC(Q)
    CEC = calculateC(C)

    return float(max(CEQ, CEC)) / min(CEQ, CEC)


def CID(Q, C):
    return calculateED(Q, C) * CF(Q, C)
