import numpy as np
from states_actions_envs.states_actions_envs import *
from agents.agent import *
from agents.agentParameters import *
from states_actions_envs.states_actions_envs import *

class agentWolfPHC(agent):
    def __init__(self, alpha, gamma, delta, epsilon):
        agent.__init__(self, alpha, gamma, delta, epsilon)
        self.deltaStaAct = {}
        self.deltaStaActTop = {}
        self.staCount = {}
        self.deltaWin = 0.0
        self.deltaLose = 0.0
        self.aveStrategy = {}
        for i in self.DCStas:
            self.aveStrategy[i] = {}
            lengthOfAction = self.DCActs.shape[0]
            for j in range(self.DCActs.shape[0]):
                self.aveStrategy[i][j] = 1 / lengthOfAction
        self.sumActValue = {}
        self.sumAveActValue = {}

    def initialStateCount(self):
        for i in self.DCStas:
            self.staCount[i] = 0

    def initialDeltaStateAction(self):
        for i in self.DCStas:
            self.deltaStaAct[i] = np.zeros(self.DCActs.shape[0])

    def initialDeltaStateActionTop(self):
        for i in self.DCStas:
            self.deltaStaActTop[i] = np.zeros(self.DCActs.shape[0])

    def updateStrategy(self):
        self.staCount[self.curSta] += 1.0
        self.deltaWin = 1.0 / (1000 + self.timeStep / 1000.0)
        self.deltaLose = 4.0 * self.deltaWin
        lengthOfAction = self.DCActs.shape[0]
        for j in range(self.DCActs.shape[0]):
            self.aveStrategy[self.curSta][j] += (1.0 / self.staCount[self.curSta]) * (self.strategy[self.curSta][j] - self.aveStrategy[self.curSta][j])
        self.sumActValue[self.curSta] = 0.0
        self.sumAveActValue[self.curSta] = 0.0
        for j in range(self.DCActs.shape[0]):
            self.sumActValue[self.curSta] += self.strategy[self.curSta][j] * self.staActVal[self.curSta][j]
            self.sumAveActValue[self.curSta] += self.aveStrategy[self.curSta][j] * self.staActVal[self.curSta][j]
        if self.sumActValue[self.curSta] > self.sumAveActValue[self.curSta]:
            self.delta = self.deltaWin
        else:
            self.delta = self.deltaLose

        self.maxAction = np.random.choice(np.argwhere(self.staActVal[self.curSta]==np.amax(self.staActVal[self.curSta]))[0])
        for j in range(self.DCActs.shape[0]):
            self.deltaStaAct[self.curSta][j] = np.amin(np.array([self.strategy[self.curSta][j], self.delta/(lengthOfAction-1)]))
        self.sumDeltaStaAct = 0.0
        for act_i in [act_j for act_j in self.DCActs if act_j != self.maxAction]:
            self.deltaStaActTop[self.curSta][act_i] = -self.deltaStaAct[self.curSta][act_i]
            self.sumDeltaStaAct += self.deltaStaAct[self.curSta][act_i]
        self.deltaStaActTop[self.curSta][self.maxAction] = self.sumDeltaStaAct
        for j in range(self.DCActs.shape[0]):
            self.strategy[self.curSta][j] += self.deltaStaActTop[self.curSta][j]


