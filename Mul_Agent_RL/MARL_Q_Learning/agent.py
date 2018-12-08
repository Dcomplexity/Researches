import numpy as np
import pandas as pd
from game_env import *


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

    def get_q_table(self):
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
        s_a = self.strategy.loc[ob, :]
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

    def update_strategy(self, s, a):
        pass

    def update_time_step(self):
        self.time_step += 1


class AgentFixedStrategy(Agent):
    def __init__(self, alpha, gamma, epsilon, fixed_strategy):
        Agent.__init__(self, alpha, gamma, epsilon)
        self.strategy_vector = np.array(fixed_strategy)
        print(self.strategy_vector)

    def initial_strategy(self):
        self.strategy[1] = pd.Series(self.strategy_vector)
        self.strategy[0] = pd.Series(1.0 - self.strategy_vector)

    def choose_action(self, ob):
        s_a = self.strategy.loc[ob, :]
        a = np.random.choice(s_a.index, size=1, p=s_a.values)[0]
        return a


class AgentPHC(Agent):
    def __init__(self, alpha, gamma, epsilon, delta):
        Agent.__init__(self, alpha, gamma, epsilon)
        self.delta = delta
        self.delta_table = pd.DataFrame(np.zeros((self.states.shape[0], self.actions.shape[0])), columns=self.actions)
        self.delta_top_table = pd.DataFrame(np.zeros((self.states.shape[0], self.actions.shape[0])), columns=self.actions)

    def initial_delta(self):
        """
        Initialize the delta_table to all zeros.
        :return:
        """
        initial_delta_value = pd.Series([0.0] * self.states.shape[0])
        for i in self.delta_table.columns:
            self.delta_table[i] = initial_delta_value
        # print(self.delta_table)

    def initial_delta_top(self):
        """
        Initialize the delta_top_table to all zeros.
        :return:
        """
        initial_delta_top_value = pd.Series([0.0] * self.states.shape[0])
        for i in self.delta_top_table.columns:
            self.delta_top_table[i] = initial_delta_top_value
        # print(self.delta_top_table)

    def update_strategy(self, s, a):
        s_a = self.q_table.loc[s, :]
        print(s_a)
        max_a = np.random.choice(s_a[s_a == np.max(s_a)].index)
        print(max_a)
        len_a = s_a.shape[0]
        print(len_a)
        for j in range(len_a):
            self.delta_table.loc[s, j] = np.amin(np.array([self.strategy.loc[s, j], self.delta / (len_a - 1)]))
        print(self.delta_table)
        sum_delta = 0.0
        for act_i in [act_j for act_j in s_a.index if act_j != max_a]:
            self.delta_top_table.loc[s, act_i] = -self.delta_table.loc[s, act_i]
            sum_delta += self.delta_table.loc[s, act_i]
        self.delta_top_table.loc[s, max_a] = sum_delta
        for j in range(len_a):
            self.strategy.loc[s, j] += self.delta_top_table.loc[s, j]
        print(self.strategy)

if __name__ == "__main__":
    # A = Agent(0.1, 0.2, 0.3, 0.4)
    # A.initial_strategy()
    # A.initial_qtable()
    # q_table = A.get_q_table()
    # strategy = A.get_strategy()
    # state_action = strategy.loc[0, :]
    # print(state_action)
    # print(state_action.values)
    # action = np.random.choice(state_action.index, size=1, p=state_action.values)[0]
    # A.check_state_exist(4)
    # q_table = A.get_q_table()
    # print(action)
    # print(action)
    # print(q_table)
    # print(q_table.loc[1, 0])
    # B = AgentFixedStrategy(0.1, 0.2, 0.4, [0.6, 0.6, 0.6, 0.6])
    # B.initial_strategy()
    # strategy = B.get_strategy()
    # print(strategy)
    C = AgentPHC(0.1, 0.2, 0.3, 0.05)
    C.initial_strategy()
    C.initial_delta()
    C.initial_delta_top()
    C.update_strategy(1, 1)


        