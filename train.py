import math


# TODO<shivin> parallelize this to use multiple cores
def calculateC(series):
    """
        This is the primary function responsible for calculating the complexity measure for a given time series
    """

    complexityF = 0

    # can make this step multi-core to speed up things
    for i, ele in enumerate(series[:-1]):
        complexityF += (series[i] - series[i+1]) ** 2

    complexityF = math.sqrt(complexityF)

    return complexityF


# TODO<shivin> parallelize this to use multiple cores
def calculateED(series1, series2):
    """
        Calculates euclidean distance between two series
    """

    edistance = 0

    for i in range(series1):
        edistance = (series1[i] - series2[i]) ** 2


    edistance = math.sqrt(edistance)

    return edistance


def CF(Q, C):
    CEQ = calculateC(Q)
    CEC = calculateC(C)

    return float(max(CEQ, CEC)) / min(CEQ, CEC)


def CID(Q, C):
    return calculateED(Q, C) * CF(Q, C)
