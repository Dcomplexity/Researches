import numpy as np
from states_actions_envs.states_actions_envs import *
from agents.agent import *
from agents.agentParameters import *

class agentFixedStrategy(agent):
    def __init__(self, alpha, gamma, delta, epsilon, fixedStrategy):
        agent.__init__(self, alpha, gamma, delta, epsilon)
        self.strategyVector = fixedStrategy

    def initialSelfStrategy(self):
        for i in self.DCStas:
            self.strategy[i] = np.zeros(self.DCActs.shape[0])
        self.strategy[(1,1)][0] = 1 - self.strategyVector[0]
        self.strategy[(1,1)][1] = self.strategyVector[0]
        self.strategy[(1,0)][0] = 1 - self.strategyVector[1]
        self.strategy[(1,0)][1] = self.strategyVector[1]
        self.strategy[(0,1)][0] = 1 - self.strategyVector[2]
        self.strategy[(0,1)][1] = self.strategyVector[2]
        self.strategy[(0,0)][0] = 1 - self.strategyVector[3]
        self.strategy[(0,0)][1] = self.strategyVector[3]

    def chooseAction(self):
        if self.curSta == (1, 1):
            if np.random.random_sample() < self.strategy[(1, 1)][1]:
                self.curAct = 1
            else:
                self.curAct = 0
        elif self.curSta == (1, 0):
            if np.random.random_sample() < self.strategy[(1, 0)][1]:
                self.curAct = 1
            else:
                self.curAct = 0
        elif self.curSta == (0, 1):
            if np.random.random_sample() < self.strategy[(0, 1)][1]:
                self.curAct = 1
            else:
                self.curAct = 0
        elif self.curSta == (0, 0):
            if np.random.random_sample() < self.strategy[(0, 0)][1]:
                self.curAct = 1
            else:
                self.curAct = 0