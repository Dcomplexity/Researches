from game_env import *

class agent(object):
    def __init__(self, alpha, gamma, delta, epsilon):
        self.timeStep = 0
        self.curSta = []
        self.nextSta = []
        self.rewards = 0
        self.nextSta = []
        self.curAct = 0
        self.maxStaAct = 0
        self.strategy = {}
        self.staActVal = {}
        self.alpha = alpha(self.timeStep) # using a function as a parameter, such as alpha = 1 / (10 + 0.002 * self.timeStep)
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon(self.timeStep)

        try:
            self.DCActs = generateDCActions()
            self.DCStas = generateDCStates(self.DCActs)
        except:
            print ("There are errors of creating actions and states")

    def initialSelfStrategy(self):
        for i in self.DCStas:
            self.strategy[i] = np.zeros(self.DCActs.shape[0])
            lengthOfAction = self.DCActs.shape[0]
            for j in range(self.DCActs.shape[0]):
                self.strategy[i][j] = 1.0 / lengthOfAction

    def initialActionValues(self):
        for i in self.DCStas:
            self.staActVal[i] = np.zeros(self.DCActs.shape[0])

    def setCurrentState(self, currentState):
        self.curSta = currentState

    def setNextState(self, nextState):
        self.nextSta = nextState

    def setRewards(self, agentRewards):
        self.rewards = agentRewards

    def chooseAction(self):
        if np.random.binomial(1, self.epsilon) == 1:
            self.curAct = np.random.choice(self.DCActs, size=1)[0]
        else:
            self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]

    def updateActionValues(self):
        self.staActVal[self.curSta][self.curAct] = (1-self.alpha)*self.staActVal[self.curSta][self.curAct] \
                                                    + self.alpha*(self.rewards+self.gamma*np.amax(self.staActVal[self.nextSta]))

    def updateStrategy(self):
        pass

    def updateTimeStep(self):
        self.timeStep += 1

    def updateEpsilon(self):
        self.EPSILON = epsilon(self.timeStep)

    def updateAlpha(self): # if you want to update alpha, you have to execute this fucntion
                           # just update timeStep will not change the alpha automatically.
        self.alpha = alpha(self.timeStep)

    def changeEpsilon(self, newEpsilon):
        self.epsilon = newEpsilon

    def getStrategy(self):
        return self.strategy

    def getAction(self):
        return self.curAct


import numpy as np


class agentPHC(agent):
    def __init__(self, alpha, gamma, delta, epsilon):
        agent.__init__(self, alpha, gamma, delta, epsilon)
        self.deltaStaAct = {}
        self.deltaStaActTop = {}

    def initialDeltaStateAction(self):
        for i in self.DCStas:
            self.deltaStaAct[i] = np.zeros(self.DCActs.shape[0])

    def initialDeltaStateActionTop(self):
        for i in self.DCStas:
            self.deltaStaActTop[i] = np.zeros(self.DCActs.shape[0])

    # def chooseSmartAction(self):
    #     #if np.random.binomial(1, self.epsilon) == 1:
    #         #self.curAct = np.random.choice(self.DCActs, size=1)[0]
    #     #else:
    #         if self.curSta == (1, 1):
    #             if np.random.binomial(1, 11/13) == 1:
    #                 self.curAct = 1
    #             else:
    #                 #self.curAct = 0
    #                 self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]
    #         elif self.curSta == (1, 0):
    #             if np.random.binomial(1, 1/2) == 1:
    #                 self.curAct = 1
    #             else:
    #                 #self.curAct = 0
    #                 self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]
    #         elif self.curSta == (0, 1):
    #             if np.random.binomial(1, 7/26) == 1:
    #                 self.curAct = 1
    #             else:
    #                 #self.curAct = 0
    #                 self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]
    #         else:
    #             #self.curAct = 0
    #             self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]

    def updateStrategy(self):
        maxAction = np.random.choice(np.argwhere(self.staActVal[self.curSta]==np.amax(self.staActVal[self.curSta]))[0])
        lengthOfAction = self.DCActs.shape[0]
        for j in range(self.DCActs.shape[0]):
            self.deltaStaAct[self.curSta][j] = np.amin(np.array([self.strategy[self.curSta][j], self.delta/(lengthOfAction-1)]))
        sumDeltaStaAct = 0.0
        for act_i in [act_j for act_j in self.DCActs if act_j != maxAction]:
            self.deltaStaActTop[self.curSta][act_i] = -self.deltaStaAct[self.curSta][act_i]
            sumDeltaStaAct += self.deltaStaAct[self.curSta][act_i]
        self.deltaStaActTop[self.curSta][maxAction] = sumDeltaStaAct
        for j in range(self.DCActs.shape[0]):
            self.strategy[self.curSta][j] += self.deltaStaActTop[self.curSta][j]