import numpy as np
import datetime
def generateRandomFromDistribution(distribution):
    """
    This function is used to generate a key value from the distribution based on
    the probabilities stored in each values.
    :param distribution: A dictionary structure ... {key: probability}
    :return: the key value based on the probability
    """
    # keyItem = []
    # valueItem = []
    # for keyId in distribution.keys():
    #     keyItem.append(keyId)
    #     valueItem.append(distribution[keyId])
    # return np.random.choice(keyItem, 1, p = valueItem)[0]
    return np.random.choice(list(distribution.keys()), 1, p=list(distribution.values()))[0]

def generateRandomFromDistributionTest (distribution):
    randomIndex = 0
    randomSum = distribution[randomIndex]
    randomFlag = np.random.random_sample()
    while randomFlag > randomSum:
        randomIndex += 1
        randomSum += distribution[randomIndex]
    return randomIndex

if __name__ == "__main__":
    a = []
    starttime = datetime.datetime.now()
    for i in range(1000000):
        a.append(generateRandomFromDistribution({0: 0.3, 1: 0.3, 2:0.4}))
    print (np.sum(a)/1000000)
    endtime = datetime.datetime.now()
    print ((endtime-starttime).seconds)

