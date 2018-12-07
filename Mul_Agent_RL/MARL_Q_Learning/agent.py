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
        self.s = []  # current state
        self.s_ = []  # next state
        self.r = 0  # reward
        self.a = 0  # current Action
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

    def initialStrategy(self):
        """
        Initialize strategy, in each states, play each action by the same probability.
        :return:
        """
        initialValue = 1.0 / self.actions.shape[0]
        initialStrategy = pd.Series([initialValue for i in range(self.states.shape[0])])
        # for i in range(self.qTable.shape[0]):
        #     for j in range(self.qTable.shape[1]):
        #         self.qTable.iloc[i, j] = initialValue
        for i in self.strategy.columns:
            self.strategy[i] = initialStrategy

    def initialQTable(self):
        """
        Initialize the qTable to all zeros.
        :return:
        """
        initialQValue = pd.Series([0.0 for i in range(self.states.shape[0])])
        for i in self.qTable.columns:
            self.qTable[i] = initialQValue

    def chooseAction(self, observation):
        """
        Choose action epsilon-greedy
        :param observation: The states agent observed
        :return:
        action: the chosen action
        """
        state_action = self.qTable.loc[observation, :]
        if np.random.binomial(1, self.epsilon) == 1:
            action = np.random.choice(state_action.index, size=1)[0]
        else:
            action = np.random.choice(state_action.index, size=1, p=state_action.values)[0]
        return action

if __name__ == "__main__":
    A = agent(0.1, 0.2, 0.3, 0.4)
    A.initialStrategy()
    A.initialQTable()
    qTable = A.getQTable()
    state_action = qTable.loc[0, :]
    print (state_action.values)
    action = np.random.choice(state_action.index, size=1, p = state_action)[0]
    print (action)
    print (action)
    print (qTable)
    print (qTable.loc[1, 0])

        