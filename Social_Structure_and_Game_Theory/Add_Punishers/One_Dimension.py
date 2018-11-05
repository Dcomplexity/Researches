import numpy as np
import random
import math
import argparse
import os

class socialStructure():
    """Classify a social strucutre

    Attributes:
        groupSize (int) : The number of individuals in every group.
        groupBase (int) : The number of groups in one level, for example: 2.
        groupLength (int) : The total length of the social structure.
        totalNum (int) : The number of individuals in whole population.
    """

    def __init__(self, groupSize, groupBase, groupLength, totalNum):
        self.groupSize = groupSize
        self.groupBase = groupBase
        self. groupLength = groupLength
        self.totalNum = totalNum

        if self.totalNum != self.groupSize * (self.groupBase ** (self.groupLength-1)):
            print ("Error: The totalNum dose not correspond to the social structure")


    def buildSocialStructure(self):
        """
        Build the social structure

        Returns:
            indPos (dict) : individual index -> position
            posInd (dict) : position -> individual index
        """
        self.groupNum = self.groupBase ** (self.groupLength-1)
        self.indPos = [0 for x in range(self.totalNum)]
        self.posInd = [[] for x in range(self.groupNum)]

        for i in range(self.groupNum):
            groupCount = 0;
            for j in range(i*self.groupSize, (i+1)*self.groupSize):
                self.indPos[j] = i
                self.posInd[i].append(j)
        return np.array(self.indPos), np.array(self.posInd)

# Here I define the punishment strategy 2
# If b = 1.1, 1.2, 1.3
# if strategy is 2, than defectors suffer a punishment 0.2,
# punishers take a cost 0.2
def PDGame(strategy0, strategy1, b):
    payoffs_punishment = b - 0.2
    payoffs_cost = -0.2
    if strategy0 == 1 and strategy1 == 1:
        return (1, 1)
    elif strategy0 == 1 and strategy1 == 0:
        return (0, b)
    elif strategy0 == 0 and strategy1 == 1:
        return (b, 0)
    elif strategy0 == 0 and strategy1 == 0:
        return (0, 0)
    elif strategy0 == 0 and strategy1 == 2:
        return (payoffs_punishment, payoffs_cost)
    elif strategy0 == 2 and strategy1 == 0:
        return (payoffs_cost, payoffs_punishment)
    else:
        return (1, 1)

def buildStrucure(strucGroupSize, strucGroupBase, strucGroupLength):
    strucTotalNum = strucGroupSize * (strucGroupBase ** (strucGroupLength-1))
    strucSocialStructure = socialStructure(strucGroupSize, strucGroupBase, strucGroupLength, strucTotalNum)
    (strucIndPos, strucPosInd) = strucSocialStructure.buildSocialStructure()
    return (strucIndPos, strucPosInd)

def distanceProb(groupLength, groupSize, regParam):
    """
    Generate the probability of various distance.
    :param groupLength: the height of the tree
    :param regPara: the regulation Parameter, such as alpha for play and beta for learn
    :param groupSize: the number of individuals in one group, which influences the distanceProb
    :return:
    distanceProb (np.array): the probability of various distance.
    """
    distanceProb = np.zeros(groupLength)
    if groupSize == 1:
        for k in range(1, groupLength):
            distanceProb[k] = math.e ** (-regParam * (k+1))
    else:
        for k in range(groupLength):
            distanceProb[k] = math.e ** (-regParam * (k+1))
    distanceProb = distanceProb / np.sum(distanceProb)
    return np.array(distanceProb)

def getPosition(groupLength, nowPosition, distanceProb):
    """
    Get the potential position based on the current position and distance probability
    :param groupLength: the height of tree
    :param nowPosition: the position of individual
    :param distanceProb: the probability of various distance
    :return:
    potentialPos (np.array): the position of potential individuals
    """
    potentialPos = []
    # Here, the distance is a np.array, like [1].
    distance = np.random.choice(groupLength, 1, p=distanceProb)[0] + 1
    # print ("distance: ", distance)
    if distance == 1:
        potentialPos.append(nowPosition)
    else:
        posTemp = 2**(distance - 1)
        if nowPosition % posTemp < posTemp // 2:
            for k in range(posTemp//2, posTemp):
                potentialPos.append((nowPosition//posTemp)*posTemp + k)
        else:
            for k in range(0, posTemp//2):
                potentialPos.append((nowPosition//posTemp)*posTemp + k)
    return np.array(potentialPos)

def pickIndividual(positions, posInd):
    """
    pick an individual from positions.
    :param positions: the positions from which pick up an individual
    :param posInd: position->individual
    :return:
    indIndex (int): the index of individual.
    """
    potentialInd = []
    for i in positions:
        for j in posInd[i]:
            potentialInd.append(j)
    indIndex = np.random.choice(potentialInd, 1)[0]
    return int(indIndex)

def initailizeStrategy(totalNum):
    indStrategy = np.random.randint(0, 2, totalNum)
    for i in range(len(indStrategy)):
        if  indStrategy[i] == 1:
            if np.random.binomial(1, 0.5) == 1:
                indStrategy[i] = 1
            else:
                indStrategy[i] = 2
    return indStrategy


def runGame(indStrategy, alpha, beta, playNum, defectParam, groupSize, groupBase, groupLength, totalNum, indPos, posInd):
    """
    Run one game
    :param indStrategy: strategies of each individuals used in this round
    :param alpha: parameter of play, -1~3
    :param beta: parameter of learn, -1~3
    :param playNum: The number of plays during playing period
    :return:
        newIndStrategy: strategies of each individuals which have been updated
    """
    if totalNum != len(indPos):
        print ("error")
    oldIndStrategy = np.zeros(totalNum)
    for i in range(totalNum):
        oldIndStrategy[i] = indStrategy[i]

    opponentPlay = np.zeros(totalNum, dtype=int)
    opponentLearn = np.zeros(totalNum, dtype=int)

    payoffs = np.zeros(totalNum)

    # Generate the probability.
    probPlay = distanceProb(groupLength, groupSize, alpha)
    probLearn = distanceProb(groupLength, groupSize, beta)

    # generate the opponent to play the game
    for i in range(totalNum):
        nowPosition = indPos[i]
        potentialPos = getPosition(groupLength, nowPosition, probPlay)
        opponentPlay[i] = pickIndividual(potentialPos, posInd)

    # generate the opponent from whom learn
    for i in range(totalNum):
        nowPosition = indPos[i]
        potentialPos = getPosition(groupLength, nowPosition, probLearn)
        opponentLearn[i] = pickIndividual(potentialPos, posInd)

    # every player plays the game with an opponent.
    for i in range(totalNum):
        playerIndex = i
        playerStrategy = indStrategy[playerIndex]
        opponentIndex = opponentPlay[i]
        opponentStrategy = indStrategy[opponentIndex]
        # print ("player: ", i, "opponent: ", opponentIndex)
        (payoffsI, payoffsJ) = PDGame(playerStrategy, opponentStrategy, defectParam)
        # print (payoffsI, payoffsJ)
        payoffs[playerIndex] += payoffsI
        payoffs[opponentIndex] += payoffsJ

    # player tries to update his strategy
    for i in range(totalNum):
        playerIndex = i
        w1 = 0.01
        w2 = random.random()
        if w1 > w2:
            if indStrategy[playerIndex] == 1 or indStrategy[playerIndex] == 2:
                indStrategy[playerIndex] = 0
            else:
                indStrategy[playerIndex] = 1
        else:
            opponentIndex = opponentLearn[i]
            t1 = 1 / (1 + math.e ** (10 * (payoffs[playerIndex] - payoffs[opponentIndex])))
            t2 = random.random()
            if t2 < t1:
                indStrategy[playerIndex] = oldIndStrategy[opponentIndex]

    return indStrategy


if __name__ == "__main__":
    buildGroupSize = 2
    buildGroupBase = 2
    buildGroupLength = 10
    buildTotalNum = buildGroupSize * (buildGroupBase ** (buildGroupLength - 1))
    (buildIndPos, buildPosInd) = buildStrucure(buildGroupSize, buildGroupBase, buildGroupLength)
    print (buildIndPos)
    print (buildPosInd)

    # buildAlpha = 0
    # buildBeta = 0
    buildPlayNum = 1
    # buildDefectParam = 0.9

    parser = argparse.ArgumentParser(description="Set the buildDefectParam")
    parser.add_argument('-d', '--defectParam', type=float, required=True, help='Set the defect Parameter')
    args = parser.parse_args()
    buildDefectParam = args.defectParam

    abspath = os.path.abspath(os.path.join(os.getcwd(), "../"))
    dirname = abspath + "/Results/Add_Punisher/One_Dimension_GroupSize_2/"
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    filename = dirname + "Co_Rate_GroupSize_2_DefectParam_%s.txt" %buildDefectParam
    f = open(filename, 'w')

    rounds = 2
    buildResults = []
    for buildAlpha in range(-3, 4):
        for buildBeta in range(-3, 4):
            print (buildAlpha, buildBeta)
            roundResults = []
            for roundIndex in range(rounds):
                buildIndStrategy = initailizeStrategy(buildTotalNum) 
                for i in range(1):
                    buildIndStrategy = runGame(buildIndStrategy, buildAlpha, buildBeta, buildPlayNum, buildDefectParam, buildGroupSize, buildGroupBase, buildGroupLength, buildTotalNum, buildIndPos, buildPosInd)
                strategyFre = np.zeros(3)
                for strategyIndex in buildIndStrategy:
                    strategyFre[strategyIndex] += 1
                roundResults.append(strategyFre / buildTotalNum)
            roundResults = np.array(roundResults)
            finalResults = np.mean(roundResults, axis=0)
            buildResults.append(finalResults)
            f.write(str(buildAlpha) + '\t' + str(buildBeta) + '\t' + str(finalResults[0]) + '\t' + str(finalResults[1]) + '\t' + str(finalResults[2]) + '\n')
    f.close()
    print (buildResults)


    # indOldStrategy = np.zeros(buildTotalNum)
    # indPayoffs = np.zeros(buildTotalNum)
    #
    # buildDistanceProb = distanceProb(buildGroupLength, buildGroupSize, 0)
    #
    # test = []
    # for i in range(10):
    #     buildPotentialPos = getPosition(buildGroupLength, 6, buildDistanceProb)
    #     print(buildPotentialPos)
    #     test.append(pickIndividual(buildPotentialPos, buildPosInd))
    # print (test)





