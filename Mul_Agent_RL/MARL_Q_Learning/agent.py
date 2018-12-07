import numpy as np
import pandas as pd
from Game_Env import *

class agent():
    def __init__(self, alpha, gamma, delta, epsilon):
        self.timeStep = 0
        self.alpha = alpha
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
        self.s = [] # current state
        self.s_ = [] # next state
        self.r = 0 # rewar
        self.a = 0 # current Action
        self.actions = genAction()
        self.states = genState(self.actions)
        # index =
        self.qTable = pd.DataFrame(np.zeros((self.states.shape[0], self.actions.shape[0])), columns=self.actions)
        self.strategy = pd.DataFrame(np.zeros((self.states.shape[0], self.actions.shape[0])), columns=self.actions)
        
    def getActions(self):
        return self.actions
    def getStates(self):
        return self.states
    def getQTable(self):
        return self.qTable
    
if __name__ == "__main__":
    A = agent(0.1, 0.2, 0.3, 0.4)
    print (A.getActions())
    print (A.getStates())
    qTable = A.getQTable()
    print (qTable)
    print (qTable.loc[1, 0])

        