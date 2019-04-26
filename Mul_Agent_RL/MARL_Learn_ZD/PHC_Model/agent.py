import numpy as np
from game_env import gen_actions, gen_states, alpha_time


class Agent:
    def __init__(self, alpha=None, gamma=None, epsilon=None):
        self.time_step = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = gen_actions()
        self.states = gen_states(self.actions)
        self.q_table = {}
        self.strategy = {}

    def get_actions(self):
        return self.actions

    def get_states(self):
        return self.states

    def get_q_table(self):
        return self.q_table

    def get_strategy(self):
        return self.strategy

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
            self.epsilon = 0.3

    def initial_strategy(self):
        """
        Initialize strategy, in each states, play each action by the same probability.
        :return:
        """
        len_actions = len(self.actions)
        initial_value = 1.0 / len_actions
        for i in self.states:
            self.strategy[i] = [0 for _ in range(len_actions)]
            for j in range(len_actions):
                self.strategy[i][j] = initial_value

    def initial_q_table(self):
        """
        Initialize the qTable to all zeros.
        :return:
        """
        len_actions = len(self.actions)
        for i in self.states:
            self.q_table[i] = [0.0 for _ in range(len_actions)]

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

    def update_q_table(self, s, a, r, s_):
        # Q-learning methods
        # self.check_state_exist(s_)
        q_predict = self.q_table[s][a]
        q_target = r + self.gamma * max(self.q_table[s_])
        self.q_table[s][a] += self.alpha * (q_target - q_predict)  # update

    def update_strategy(self, s, a):
        pass

    def update_time_step(self):
        self.time_step += 1


class AgentFixedStrategy(Agent):
    def __init__(self, alpha=None, gamma=None, epsilon=None, fixed_strategy=None):
        Agent.__init__(self, alpha, gamma, epsilon)
        self.strategy_vector = fixed_strategy
        print(self.strategy_vector)

    def initial_strategy(self):
        len_actions = len(self.actions)
        for i in self.states:
            self.strategy[i] = [0 for _ in range(len_actions)]
        self.strategy[(1, 1)][0] = 1 - self.strategy_vector[0]
        self.strategy[(1, 1)][1] = self.strategy_vector[0]
        self.strategy[(1, 0)][0] = 1 - self.strategy_vector[1]
        self.strategy[(1, 0)][1] = self.strategy_vector[1]
        self.strategy[(0, 1)][0] = 1 - self.strategy_vector[2]
        self.strategy[(0, 1)][1] = self.strategy_vector[2]
        self.strategy[(0, 0)][0] = 1 - self.strategy_vector[3]
        self.strategy[(0, 0)][1] = self.strategy_vector[3]

    def choose_action(self, ob):
        a = np.random.choice(self.actions, size=1, p=self.strategy[ob])[0]
        return a


class AgentQ(Agent):
    def __init__(self, alpha=None, gamma=None, epsilon=None):
        Agent.__init__(self, alpha, gamma, epsilon)

    def choose_action(self, ob):
        a_v = np.array(self.q_table[ob])
        alt_actions = np.where(a_v == np.amax(a_v))[0]
        a = np.random.choice(alt_actions)
        return a


class AgentPHC(Agent):
    def __init__(self, alpha=None, gamma=None, epsilon=None, delta=None):
        Agent.__init__(self, alpha, gamma, epsilon)
        self.delta = delta
        self.delta_table = {}
        self.delta_top_table = {}

    def initial_delta(self):
        """
        Initialize the delta_table to all zeros.
        :return:
        """
        len_actions = len(self.actions)
        for i in self.states:
            self.delta_table[i] = np.zeros(len_actions)
        # print(self.delta_table)

    def initial_delta_top(self):
        """
        Initialize the delta_top_table to all zeros.
        :return:
        """
        len_actions = len(self.actions)
        for i in self.states:
            self.delta_top_table[i] = np.zeros(len_actions)

    def choose_action(self, ob):
        """
        Choose action epsilon-greedy
        :param ob: The states agent's observation
        :return:
        action: the chosen action
        """
        if np.random.binomial(1, self.epsilon) == 1:
            a = np.random.choice(self.actions)
        else:
            a = np.random.choice(self.actions, size=1, p=self.strategy[ob])[0]
        return a

    def update_strategy(self, s, a):
        max_a = np.random.choice(np.argwhere(self.q_table[s] == np.amax(self.q_table[s]))[0])
        len_a = len(self.actions)
        for j in range(len_a):
            self.delta_table[s][j] = min(np.array([self.strategy[s][j], self.delta / (len_a - 1)]))
        # print(self.delta_table)
        sum_delta = 0.0
        for act_i in [act_j for act_j in self.actions if act_j != max_a]:
            self.delta_top_table[s][act_i] = -self.delta_table[s][act_i]
            sum_delta += self.delta_table[s][act_i]
        self.delta_top_table[s][max_a] = sum_delta
        for j in range(len_a):
            self.strategy[s][j] += self.delta_top_table[s][j]
        # print(self.strategy)


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
