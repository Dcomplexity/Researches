import numpy as np
import pandas as pd
from Game_Env import *


class Agent:
    def __init__(self, alpha, gamma, epsilon):
        self.time_step = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        # self.s = []  # current state
        # self.s_ = []  # next state
        # self.r = 0  # reward
        # self.a = 0  # current Action
        self.actions = genAction()
        self.states = genState(self.actions)
        # index =
        self.q_table = pd.DataFrame(np.zeros((self.states.shape[0], self.actions.shape[0])), columns=self.actions)
        self.strategy = pd.DataFrame(np.zeros((self.states.shape[0], self.actions.shape[0])), columns=self.actions)
        
    def get_actions(self):
        return self.actions

    def get_states(self):
        return self.states

    def get_qtable(self):
        return self.q_table

    def get_strategy(self):
        return self.strategy

    def initial_strategy(self):
        """
        Initialize strategy, in each states, play each action by the same probability.
        :return:
        """
        initial_value = 1.0 / self.actions.shape[0]
        initial_strategy = pd.Series([initial_value]*self.states.shape[0])
        # for i in range(self.q_table.shape[0]):
        #     for j in range(self.q_table.shape[1]):
        #         self.q_table.iloc[i, j] = initialValue
        for i in self.strategy.columns:
            self.strategy[i] = initial_strategy

    def initial_qtable(self):
        """
        Initialize the qTable to all zeros.
        :return:
        """
        initial_qvalue = pd.Series([0.0]*self.states.shape[0])
        for i in self.q_table.columns:
            self.q_table[i] = initial_qvalue

    def check_state_exist(self, s):
        if s not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=s,
                ))

    def choose_action(self, ob):
        """
        Choose action epsilon-greedy
        :param ob: The states agent's observation
        :return:
        action: the chosen action
        """
        s_a = self.q_table.loc[ob, :]
        if np.random.binomial(1, self.epsilon) == 1:
            a = np.random.choice(s_a.index, size=1)[0]
        else:
            a = np.random.choice(s_a.index, size=1, p=s_a.values)[0]
        return a

    def update_qtable(self, s, a, r, s_):
        # Q-learning methods
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        q_target = r + self.gamma * self.q_table[s_, :].max()
        self.q_table[s, a] += self.alpha * (q_target - q_predict)  # update

    def update_strategy(self):
        pass

    def update_time_step(self):
        self.time_step += 1


if __name__ == "__main__":
    A = Agent(0.1, 0.2, 0.3, 0.4)
    A.initial_strategy()
    A.initial_qtable()
    q_table = A.get_qtable()
    strategy = A.get_strategy()
    state_action = strategy.loc[0, :]
    print(state_action)
    print(state_action.values)
    action = np.random.choice(state_action.index, size=1, p=state_action.values)[0]
    A.check_state_exist(4)
    q_table = A.get_qtable()
    print(action)
    print(action)
    print(q_table)
    print(q_table.loc[1, 0])

        