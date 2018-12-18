from game_env import *
import numpy as np


class Agent:
    def __init__(self, gamma):
        self.time_step = 0
        self.cur_s = []
        self.next_s = []
        self.reward = 0
        self.cur_a = 0
        self.strategy = {}
        self.q_table = {}
        self.epsilon = epsilon_time(self.time_step)
        self.alpha = alpha_time(self.time_step)
        self.gamma = gamma

        try:
            self.actions = gen_actions()
            self.states = gen_states(self.actions)
        except ValueError:
            print("There are errors of creating actions and states")

    def initial_strategy(self):
        len_a = self.actions.shape[0]
        for i in self.states:
            self.strategy[i] = np.zeros(len_a)
            for j in range(self.actions.shape[0]):
                self.strategy[i][j] = 1.0 / len_a

    def initial_q_table(self):
        len_a = self.actions.shape[0]
        for i in self.states:
            self.q_table[i] = np.zeros(len_a)

    def set_cur_state(self, s):
        self.cur_s = s

    def set_next_state(self, s_):
        self.next_s = s_

    def set_reward(self, r):
        self.reward = r

    def choose_action(self):
        if np.random.binomial(1, self.epsilon) == 1:
            self.cur_a = np.random.choice(self.actions, size=1)[0]
        else:
            self.cur_a = np.random.choice(self.actions, size=1, p=self.strategy[self.cur_s])[0]

    def update_q_table(self):
        self.q_table[self.cur_s][self.cur_a] = (1-self.alpha)*self.q_table[self.cur_s][self.cur_a] \
                                                    + self.alpha*(self.reward+self.gamma*np.amax(self.q_table[self.next_s]))

    def update_strategy(self):
        pass

    def update_time_step(self):
        self.time_step += 1

    def update_epsilon(self):
        self.EPSILON = epsilon_time(self.time_step)

    def update_alpha(self):
        self.alpha = alpha_time(self.time_step)

    def change_epsilon(self, new_epsilon):
        self.epsilon = new_epsilon

    def get_strategy(self):
        return self.strategy

    def get_action(self):
        return self.cur_a


class AgentPHC(Agent):
    def __init__(self, gamma, delta):
        Agent.__init__(self, gamma)
        self.delta = delta
        self.deltaStaAct = {}
        self.deltaStaActTop = {}

    def initial_delta(self):
        for i in self.states:
            self.deltaStaAct[i] = np.zeros(self.actions.shape[0])

    def initial_delta_top(self):
        for i in self.states:
            self.deltaStaActTop[i] = np.zeros(self.actions.shape[0])

    # def chooseSmartAction(self):
    #     #if np.random.binomial(1, self.epsilon) == 1:
    #         #self.cur_a = np.random.choice(self.actions, size=1)[0]
    #     #else:
    #         if self.cur_s == (1, 1):
    #             if np.random.binomial(1, 11/13) == 1:
    #                 self.cur_a = 1
    #             else:
    #                 #self.cur_a = 0
    #                 self.cur_a = np.random.choice(self.actions, size=1, p=self.strategy[self.cur_s])[0]
    #         elif self.cur_s == (1, 0):
    #             if np.random.binomial(1, 1/2) == 1:
    #                 self.cur_a = 1
    #             else:
    #                 #self.cur_a = 0
    #                 self.cur_a = np.random.choice(self.actions, size=1, p=self.strategy[self.cur_s])[0]
    #         elif self.cur_s == (0, 1):
    #             if np.random.binomial(1, 7/26) == 1:
    #                 self.cur_a = 1
    #             else:
    #                 #self.cur_a = 0
    #                 self.cur_a = np.random.choice(self.actions, size=1, p=self.strategy[self.cur_s])[0]
    #         else:
    #             #self.cur_a = 0
    #             self.cur_a = np.random.choice(self.actions, size=1, p=self.strategy[self.cur_s])[0]

    def update_strategy(self):
        maxAction = np.random.choice(np.argwhere(self.q_table[self.cur_s]==np.amax(self.q_table[self.cur_s]))[0])
        lengthOfAction = self.actions.shape[0]
        for j in range(self.actions.shape[0]):
            self.deltaStaAct[self.cur_s][j] = np.amin(np.array([self.strategy[self.cur_s][j], self.delta/(lengthOfAction-1)]))
        sumDeltaStaAct = 0.0
        for act_i in [act_j for act_j in self.actions if act_j != maxAction]:
            self.deltaStaActTop[self.cur_s][act_i] = -self.deltaStaAct[self.cur_s][act_i]
            sumDeltaStaAct += self.deltaStaAct[self.cur_s][act_i]
        self.deltaStaActTop[self.cur_s][maxAction] = sumDeltaStaAct
        for j in range(self.actions.shape[0]):
            self.strategy[self.cur_s][j] += self.deltaStaActTop[self.cur_s][j]