import numpy as np
import pandas as pd
from game_env import *


class Agent(object):
    def __init__(self, alpha, gamma, epsilon):
        self.time_step = 0
        self.alpha = alpha_time(self.time_step)
        self.gamma = gamma
        self.epsilon = epsilon_time(self.time_step)
        self.cur_s = ()
        self.next_s = ()
        self.cur_a = 0
        self.reward = 0
        # self.s = []  # current state
        # self.s_ = []  # next state
        # self.r = 0  # reward
        # self.a = 0  # current Action
        self.actions = gen_actions()
        self.states = gen_states(self.actions)
        # print(self.states)
        self.q_table = {}
        self.strategy = {}

    def get_action(self):
        return self.cur_a

    def get_state(self):
        return self.cur_s

    def get_q_table(self):
        return self.q_table

    def get_strategy(self):
        return self.strategy

    def set_cur_state(self, s):
        self.cur_s = s

    def set_next_state(self, s_):
        self.next_s = s_

    def set_reward(self, r):
        self.reward = r

    def update_time_step(self):
        self.time_step += 1

    def update_alpha(self):
        self.alpha = alpha_time(self.time_step)

    def update_epsilon(self):
        self.epsilon = epsilon_time(self.time_step)

    def initial_strategy(self):
        """
        Initialize strategy, in each states, play each action by the same probability.
        :return:
        """
        for i in self.states:
            self.strategy[i] = np.zeros(self.actions.shape[0])
            len_a = self.actions.shape[0]
            for j in range(self.actions.shape[0]):
                self.strategy[i][j] = 1.0 / len_a

    def initial_q_table(self):
        """
        Initialize the qTable to all zeros.
        :return:
        """
        for i in self.states:
            self.q_table[i] = np.zeros(self.actions.shape[0])

    # def check_state_exist(self, s):
    #     if s not in self.q_table.index:
    #         # append new state to q table
    #         self.q_table = self.q_table.append(
    #             pd.Series(
    #                 [0]*len(self.actions),
    #                 index=self.q_table.columns,
    #                 name=s,
    #             ))

    def choose_action(self, ob):
        pass

    def update_q_table(self):
        # Q-learning methods
        # self.check_state_exist(s_)
        self.q_table[self.cur_s][self.cur_a] = (1-self.alpha)*self.q_table[self.cur_s][self.cur_a] \
                + self.alpha * (self.reward + self.gamma * np.amax(self.q_table[self.next_s]))  # update

    def update_strategy(self):
        pass

    def update_time_step(self):
        self.time_step += 1


class AgentFixedStrategy(Agent):
    def __init__(self, gamma, fixed_strategy):
        Agent.__init__(self, gamma)
        self.strategy_vector = np.array(fixed_strategy)
        print(self.strategy_vector)

    def initial_strategy(self):
        for i in self.states:
            self.strategy[i] = np.zeros(self.actions.shape[0])
        self.strategy[(1, 1)][0] = 1 - self.strategy_vector[0]
        self.strategy[(1, 1)][1] = self.strategy_vector[0]
        self.strategy[(1, 0)][0] = 1 - self.strategy_vector[1]
        self.strategy[(1, 0)][1] = self.strategy_vector[1]
        self.strategy[(0, 1)][0] = 1 - self.strategy_vector[2]
        self.strategy[(0, 1)][1] = self.strategy_vector[2]
        self.strategy[(0, 0)][0] = 1 - self.strategy_vector[3]
        self.strategy[(0, 0)][1] = self.strategy_vector[3]

    def choose_action(self):
        a = np.random.choice(self.actions, size=1, p=self.strategy[self.cur_s])[0]
        return a


class AgentQ(Agent):
    def __init__(self, gamma):
        Agent.__init__(self, gamma)

    def choose_action(self):
        a_v = np.array(self.q_table[self.cur_s])
        alt_actions = np.where(a_v == np.amax(a_v))[0]
        a = np.random.choice(alt_actions)
        return a


class AgentPHC(Agent):
    def __init__(self, alpha, gamma, epsilon, delta):
        Agent.__init__(self, alpha, gamma, epsilon)
        self.delta = delta
        self.delta_table = {}
        self.delta_top_table = {}

    def initial_delta(self):
        """
        Initialize the delta_table to all zeros.
        :return:
        """
        for i in self.states:
            self.delta_table[i] = np.zeros(self.actions.shape[0])
        # print(self.delta_table)

    def initial_delta_top(self):
        """
        Initialize the delta_top_table to all zeros.
        :return:
        """
        for i in self.states:
            self.delta_top_table[i] = np.zeros(self.actions.shape[0])

    def choose_action(self):
        """
        Choose action epsilon-greedy
        :param ob: The states agent's observation
        :return:
        action: the chosen action
        """
        if np.random.binomial(1, self.epsilon) == 1:
            self.cur_a = np.random.choice(self.actions, size=1)[0]
        else:
            self.cur_a = np.random.choice(self.actions, size=1, p=self.strategy[self.cur_s])[0]

    def update_strategy(self):
        max_a = np.random.choice(np.argwhere(self.q_table[self.cur_s] == np.amax(self.q_table[self.cur_s]))[0])
        len_a = self.actions.shape[0]
        for j in range(self.actions.shape[0]):
            self.delta_table[self.cur_s][j] = np.amin(np.array([self.strategy[self.cur_s][j], self.delta / (len_a - 1)]))
        # print(self.delta_table)
        sum_delta = 0.0
        for act_i in [act_j for act_j in self.actions if act_j != max_a]:
            self.delta_top_table[self.cur_s][act_i] = -self.delta_table[self.cur_s][act_i]
            sum_delta += self.delta_table[self.cur_s][act_i]
        self.delta_top_table[self.cur_s][max_a] = sum_delta
        for j in range(self.actions.shape[0]):
            self.strategy[self.cur_s][j] += self.delta_top_table[self.cur_s][j]


if __name__ == "__main__":
    A = Agent(0.1, 0.2, 0.3)
    A.initial_strategy()
    A.initial_q_table()
    q_table = A.get_q_table()
    strategy = A.get_strategy()
    print(q_table)
    print(q_table[(0, 0)][1])
    # print(strategy)
    # print(state_action.values)
    # action = np.random.choice(state_action.index, size=1, p=state_action.values)[0]
    # A.check_state_exist((1, 2))
    # q_table = A.get_q_table()
    # print(action)
    # print(action)
    # print(q_table)
    # print(q_table.loc[1, 0])
    # B = AgentFixedStrategy(0.1, 0.2, 0.4, [0.6, 0.6, 0.6, 0.6])
    # B.initial_strategy()
    # strategy = B.get_strategy()
    # print(strategy)
    # # C = AgentPHC(0.1, 0.2, 0.3, 0.05)
    # # C.initial_strategy()
    # # C.initial_delta()
    # # C.initial_delta_top()
    # # print(C.delta_table)
    # # C.update_strategy((0, 1), 1)


        