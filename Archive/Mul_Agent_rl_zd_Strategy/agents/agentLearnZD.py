import numpy as np
from states_actions_envs.states_actions_envs import *
from agents.agent import *
from agents.agentParameters import *

class agentLearnZD(agent):
    def __init__(self, alpha, gamma, delta, epsilon):
        agent.__init__(self, alpha, gamma, delta, epsilon)
        self.extroFac = 1.0

    def generateStrategyDist(self):
        self.strategyDist = {}
        for i in self.DCStas:
            self.strategyDist[i] = 0.0
        self.strategyDist[(1,1)] = 1.0-(self.extroFac-1.0)/(4.0*self.extroFac+1.0)
        self.strategyDist[(1,0)] = 0.5
        self.strategyDist[(0,1)] = (4.0+self.extroFac)/(2.0*(4.0*self.extroFac+1.0))
        self.strategyDist[(0,0)] = 0.0

    def initialSelfStrategy(self):
        self.extroFac = 1.0 # fariness factor
        self.generateStrategyDist()
        for i in self.DCStas:
            self.strategy[i] = np.zeros(self.DCActs.shape[0])
        self.changeSelfStrategy()

    def changeSelfStrategy(self):
        self.strategy[(1,1)][0] = 1.0 - self.strategyDist[(1,1)]
        self.strategy[(1,1)][1] = self.strategyDist[(1,1)]
        self.strategy[(1,0)][0] = 1.0 - self.strategyDist[(1,0)]
        self.strategy[(1,0)][1] = self.strategyDist[(1,0)]
        self.strategy[(0,1)][0] = 1.0 - self.strategyDist[(0,1)]
        self.strategy[(0,1)][1] = self.strategyDist[(0,1)]
        self.strategy[(0,0)][0] = 1.0 - self.strategyDist[(0,0)]
        self.strategy[(0,0)][1] = self.strategyDist[(0,0)]
