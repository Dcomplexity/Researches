import random
import math
import datetime

from game_env import *

class Agent:
    """
    Build an agent
    """
    def __init__(self, agent_id, link, strategy, alpha, gamma, epsilon):
        self.time_step = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = gen_actions()
        self.states = gen_states(self.actions)
        self.q_table = {}
        self.agent_id = agent_id
        self.link = link
        self.strategy = strategy
        self.ostrategy = strategy
        self.payoffs = 0

    def get_actions(self):
        return self.actions

    def get_states(self):
        return self.states

    def get_q_table(self):
        return self.q_table

    def get_id(self):
        return self.agent_id

    def get_link(self):
        return self.link

    def get_strategy(self):
        return self.strategy

    def get_ostrategy(self):
        return self.ostrategy

    def get_payoffs(self):
        return self.payoffs

    def set_strategy(self, other_strategy):
        self.strategy = other_strategy

    def set_ostrategy(self):
        self.ostrategy = self.strategy

    def set_payoffs(self, p):
        self.payoffs = p

    def set_time_step(self, t):
        self.time_step = t

    def set_alpha(self, t, new_alpha=None):
        if new_alpha:
            self.alpha = new_alpha
        else:
            self.alpha = alpha_time(t)

    def set_epsilon(self, t, new_epsilon=None):
        if new_epsilon:
            self.epsilon = new_epsilon
        else:
            self.epsilon = epsilon_time(t)

    def initial_strategy(self):
        """
        Initialize strategy, in each states, play each action by the same probability.
        :return:
        """
        len_actions = self.actions.shape[0]
        initial_value = 1.0 / len_actions
        for i in self.states:
            self.strategy[i] = np.zeros(len_actions)
            for j in range(len_actions):
                self.strategy[i][j] = initial_value

    def initial_q_table(self):
        """
        Initialize the qTable to all zeros
        :return:
        """
        for i in self.states:
            self.q_table[i] = np.zeros(self.actions.shape[0])

    def choose_action(self, ob):
        """
        Choose action epsilon-greedy
        :param ob: The states agent's observation
        :return:
        action: the chose action
        """
        if np.random.binomial(1, self.epsilon) == 1:
            a = np.random.choice(self.actions, size=1)[0]
        else:
            a = np.random.choice(self.actions, size=1, p=self.strategy[ob])[0]
        return a

    def update_q_table(self, s, a, r, s_):
        q_predict = self.q_table[s][a]
        q_target = r + self.gamma * np.amax(self.qtable[s_])
        self.q_table[s][a] += self.alpha * (q_target - q_predict)  # update

    def update_strategy(self, s, a):
        pass

    def update_time_step(self):
        self.time_step += 1


def initialize_population():
    network, total_num, edges = generate_network(structure='2d_grid')
    popu = []
    for i in range(total_num):
        #
