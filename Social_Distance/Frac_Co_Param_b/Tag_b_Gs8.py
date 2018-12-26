import numpy as np
import random
import math
import argparse
import os
import datetime

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


def PDGame(strategy0, strategy1, b):
    if strategy0 == 1 and strategy1 == 1:
        return (1, 1)
    elif strategy0 == 1 and strategy1 == 0:
        return (0, b)
    elif strategy0 == 0 and strategy1 == 1:
        return (b, 0)
    elif strategy0 == 0 and strategy1 == 0:
        return (0, 0)
    else:
        return "Error"

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
            distanceProb[k] = math.e ** (regParam * (k+1))
    else:
        for k in range(groupLength):
            distanceProb[k] = math.e ** (regParam * (k+1))
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

def buildTag(totalNum):
    indTag = np.random.random(totalNum)
    return indTag

def initializeStrategy(totalNum):
    indStrategy = np.random.randint(0, 2, totalNum)
    return indStrategy

def runGame(indStrategy, indTag, alpha, beta, playNum, defectParam, groupSize, groupBase, groupLength, totalNum, indPos, posInd, tolerance):
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
        if abs(indTag[playerIndex] - indTag[opponentIndex]) < tolerance:
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
            if indStrategy[playerIndex] == 1:
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
    buildGroupSize = 8
    buildGroupBase = 2
    buildGroupLength = 8
    buildTotalNum = buildGroupSize * (buildGroupBase ** (buildGroupLength - 1))
    (buildIndPos, buildPosInd) = buildStrucure(buildGroupSize, buildGroupBase, buildGroupLength)
    print (buildIndPos)
    print (buildPosInd)

    # buildAlpha = 0
    # buildBeta = 0
    buildPlayNum = 1
    # buildDefectParam = 0.9

    # parser = argparse.ArgumentParser(description="Set the buildDefectParam")
    # parser.add_argument('-d', '--defectParam', type=float, required=True, help='Set the defect Parameter')
    # parser.add_argument('-t', '--tolerance', type=float, required=True, help="Set the tolerance Parameter")
    # args = parser.parse_args()
    # buildDefectParam = args.defectParam
    # buildTolerance = args.tolerance
    buildTolerance = 0.1
    buildAlpha = -2
    buildBeta = 2

    abspath = os.path.abspath(os.path.join(os.getcwd(), "../"))
    dirname = abspath + "/Results/Re_Frac_Co_Param_b/"
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    filename = dirname + "Re_Tag_b_Gs_8.txt"
    f = open(filename, 'w')

    startTime = datetime.datetime.now()
    runtime = 50    
    sampletime = 10
    rounds = 5
    buildResults = []
    for buildDefectParam in [x/10.0 for x in range(10, 31)]:
        print (buildDefectParam)
        roundResults = np.zeros(rounds)
        for roundIndex in range(rounds):
            buildIndStrategy = initializeStrategy(buildTotalNum)
            buildIndTag = buildTag(buildTotalNum)
            for i in range(runtime):
                buildIndStrategy = runGame(buildIndStrategy, buildIndTag, buildAlpha, buildBeta, buildPlayNum, buildDefectParam, buildGroupSize, buildGroupBase, buildGroupLength, buildTotalNum, buildIndPos, buildPosInd, buildTolerance)
            sampleStrategy = []
            for i in range(sampletime):
                buildIndStrategy = runGame(buildIndStrategy, buildIndTag, buildAlpha, buildBeta, buildPlayNum, buildDefectParam, buildGroupSize, buildGroupBase, buildGroupLength, buildTotalNum, buildIndPos, buildPosInd, buildTolerance)
                sampleStrategy.append(np.mean(buildIndStrategy))
            roundResults[roundIndex] = np.mean(sampleStrategy)
        finalResults = np.mean(roundResults)
        buildResults.append(finalResults)
        f.write(str(buildDefectParam) + '\t' + str(finalResults) + '\n')
    f.close()
    endTime = datetime.datetime.now()
    print (buildResults)

    print (endTime-startTime)


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





