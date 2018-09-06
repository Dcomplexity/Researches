import numpy as np
from states_actions_envs.states_actions_envs import *
from agents.agent import *
from agents.agentParameters import *

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
    def chooseSmartAction(self):
        if np.random.binomial(1, self.epsilon) == 1:
            self.curAct = np.random.choice(self.DCActs, size=1)[0]
        else:
            if self.curSta == (1, 0) or self.curSta == (1, 1):
                if np.random.binomial(1, 0.8) == 1:
                    self.curAct = 1
                else:
                    self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]
            else:
                self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]

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
