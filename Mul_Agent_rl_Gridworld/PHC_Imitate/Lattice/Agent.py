import numpy as np
import random
import copy
from GridWorld import *
from specFunction import *

class agent:
    def __init__(self, agentId = 0, agentIndex = 0, startLocIndex = 0, gamma = 0.9, delta = 0.0001):
        self.timeStep = 0
        self.alpha = 1 / (10 + 0.002 * self.timeStep)
        self.gamma = gamma
        self.curState = ()
        self.nextState = ()
        self.strategy = {}
        self.ostrategy = {}
        self.agentId = agentId
        self.agentIndex = agentIndex
        self.startLocIndex = startLocIndex
        self.locIndex = startLocIndex
        self.curAct = 0
        self.stateActValues = {}
        self.maxStateAct = 0
        self.deltaStateAct = {}
        self.deltaStateActTop = {}
        self.delta = delta
        self.EPSILON = 0.5 / (1 + 0.0001 * self.timeStep)
        # neighbors of an agent
        self.neighbors = []
        # An agent needs to store his own rewards
        self.evalRewards = 0

    def initialSelfStrategy(self):
        for i in statesAllOne:
            self.strategy[i] = {}
            lenghtOfAct = len(locValidActs[i[self.agentId]])
            for j in locValidActs[i[self.agentId]]:
                self.strategy[i][j] = 1 / lenghtOfAct

    def initialActionValues(self):
        for i in statesAllOne:
            self.stateActValues[i] = {}
            for j in locValidActs[i[self.agentId]]:
                self.stateActValues[i][j] = 0

    def initialDeltaStateAction(self):
        for i in statesAllOne:
            self.deltaStateAct[i] = {}
            for j in locValidActs[i[self.agentId]]:
                self.deltaStateAct[i][j] = 0

    def initialDeltaStateActionTop(self):
        for i in statesAllOne:
            self.deltaStateActTop[i] = {}
            for j in locValidActs[i[self.agentId]]:
                self.deltaStateActTop[i][j] = 0

    def meetNeighbors(self, neighborList):
        for i in neighborList:
            self.neighbors.append(i)

    def imitateStrategy(self, otherStrategy):
        self.strategy = copy.deepcopy(otherStrategy)

    def chooseAction(self, curState):
        if np.random.binomial(1, self.EPSILON) == 1:
            self.curAct = random.choice(locValidActs[curState[self.agentId]])
        else:
            # todo Notice the difference with previous implementation
            self.curAct = generateRandomFromDistribution(self.strategy[curState])
            # actionProbabilityList = list(self.strategy[curState].values())
            # actionIndex = generateRandomFromDistributionTest(actionProbabilityList)
            # actionProbability = actionProbabilityList[actionIndex]
            # potentialactions = []
            # for actionkeys in self.strategy[curState].keys():
                # if self.strategy[curState][actionkeys] == actionProbability:
                    # potentialactions.append(actionkeys)
            # self.curAct = random.choice(potentialactions)
        return self.curAct

    def chooseActionWithFixedStrategy(self, curState):
        self.curAct = generateRandomFromDistribution(self.strategy[curState])
        return self.curAct

    def updateActionValues(self, curState, nextState, agentReward):
        self.stateActValues[curState][self.curAct] = (1-self.alpha) * self.stateActValues[curState][self.curAct] + self.alpha * (agentReward + self.gamma * max(self.stateActValues[nextState].values()))

    def updateStrategy(self, curState):
        maxAct = max(self.stateActValues[curState], key=lambda x:self.stateActValues[curState][x])
        lengthOfAct = len(locValidActs[curState[self.agentId]])
        for j in locValidActs[curState[self.agentId]]:
            self.deltaStateAct[curState][j] = min([self.strategy[curState][j], self.delta/(lengthOfAct - 1)])
        sumDeltaStateAct = 0
        for actI in [actJ for actJ in locValidActs[curState[self.agentId]] if actJ != maxAct]:
            self.deltaStateActTop[curState][actI] = -self.deltaStateAct[curState][actI]
            sumDeltaStateAct += self.deltaStateAct[curState][actI]
        self.deltaStateActTop[curState][maxAct] = sumDeltaStateAct
        for j in locValidActs[curState[self.agentId]]:
            self.strategy[curState][j] += self.deltaStateActTop[curState][j]

    def backupStrategy(self):
        self.ostrategy = copy.deepcopy(self.strategy)

    def chooseAgentRandomly(self, agentList):
        imitateAgent = agentList[self.agentId][random.choice(self.neighbors)]

    def updateTimeStep(self):
        self.timeStep += 1

    def updateEpsilon(self):
        self.EPSILON = 0.5 / (1 + 0.0001 * self.timeStep)

    def updateAlpha(self):
        self.alpha = 1 / (10 + 0.002 * self.timeStep)