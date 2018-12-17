from game_env import *


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
        self.actions = gen_actions()
        self.states = gen_states(self.actions)

    def initial_strategy(self):
        for i in self.states:
            self.strategy[i] = np.zeros(self.actions.shape[0])
            len_a = self.actions.shape[0]
            for j in range(self.actions.shape[0]):
                self.strategy[i][j] = 1.0 / len_a

    def initial_q_table(self):
        for i in self.states:
            self.q_table[i] = np.zeros(self.actions.shape[0])

    def set_current_state(self, s):
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
        self.q_table[self.cur_s][self.cur_a] = (1 - self.alpha) * self.q_table[self.cur_s][self.cur_a] \
                                        + self.alpha * (self.reward + self.gamma * np.amax(self.q_table[self.next_s]))

    def update_strategy(self):
        pass

    def update_time_step(self):
        self.time_step += 1

    def update_epsilon(self):
        self.epsilon = epsilon_time(self.time_step)

    def update_alpha(self):
        self.alpha = alpha_time(self.time_step)

    def get_strategy(self):
        return self.strategy

    def get_action(self):
        return self.cur_a


class AgentPHC(Agent):
    def __init__(self, gamma, delta):
        Agent.__init__(self, gamma)
        self.delta = delta
        self.delta_sta_act = {}
        self.delta_sta_act_top = {}

    def initial_delta(self):
        for i in self.states:
            self.delta_sta_act[i] = np.zeros(self.actions.shape[0])

    def initial_delta_top(self):
        for i in self.states:
            self.delta_sta_act_top[i] = np.zeros(self.actions.shape[0])

    def update_strategy(self):
        max_a = np.random.choice(np.argwhere(self.q_table[self.cur_s] == np.amax(self.q_table[self.cur_s]))[0])
        len_action = self.actions.shape[0]
        for j in range(self.actions.shape[0]):
            self.delta_sta_act[self.cur_s][j] = np.amin(np.array([self.strategy[self.cur_s][j], self.delta/(len_action-1)]))
        sum_delta = 0.0
        for act_i in [act_j for act_j in self.actions if act_j != max_a]:
            self.delta_sta_act_top[self.cur_s][act_i] = -self.delta_sta_act[self.cur_s][act_i]
            sum_delta += self.delta_sta_act[self.cur_s][act_i]
        self.delta_sta_act_top[self.cur_s][max_a] = sum_delta
        for j in range(self.actions.shape[0]):
            self.strategy[self.cur_s][j] += self.delta_sta_act_top[self.cur_s][j]
