from game_env import *


class Agent:
    def __init__(self, alpha, agent_id):
        self.id = agent_id
        self.strategy = {}
        self.actions = [0, 1]  # 0 for defect and 1 for cooperate
        self.states = [0, 1]  # There are two states: state 0 and state 1
        self.alpha = alpha

    def get_strategy(self):
        return self.strategy

    def initial_strategy(self):
        for state in self.states:
            self.strategy[state] = []
        for state in self.states:
            for _ in self.actions:
                self.strategy[state].append(1 / len(self.actions))

    def set_strategy(self, new_s=None):
        """
        Initialize the strategy
        :param new_s: The probability to play cooperation (action[1])
        :return:
        """
        if new_s:
            for state in self.states:
                self.strategy[state][0] = 1 - new_s[state][self.id]
                self.strategy[state][1] = new_s[state][self.id]

    def choose_action(self, s):
        a = np.random.choice(np.array(self.actions), size=1, p=self.strategy[s])[0]
        return a

    def update_strategy(self, s, a, r):
        for action in self.actions:
            if action == a:
                self.strategy[s][action] = self.strategy[s][action] + self.alpha * r * (1 - self.strategy[s][action])
            else:
                self.strategy[s][action] = self.strategy[s][action] - self.alpha * r * self.strategy[s][action]


def run_game(initial_strategy, s_0):
    """

    :param initial_strategy: like {state_0: [pi_01, pi_11], state_1: [pi_01, pi_11]}, pi_01 for agent 0 play action 1
    :param s_0: initial_strategy
    :return:
    """
    agent_0 = Agent(alpha=0.0001, agent_id=0)
    agent_1 = Agent(alpha=0.0001, agent_id=1)
    agent_0.initial_strategy()
    agent_1.initial_strategy()
    agent_0.set_strategy(initial_strategy)
    agent_1.set_strategy(initial_strategy)
    cur_s = s_0
    games = [pd_game_0, pd_game_1]
    r_0 = np.array([0, 0])  # store the sum of reward of agent_0 for each state: state 0 and state 1
    r_1 = np.array([0, 0])
    tau_0 = np.array([0, 0])  # the reward of agent_0 used to update the strategy for each state
    tau_1 = np.array([0, 0])
    time_step = np.array([0, 0])  # store the sum of time of each state: state 0 and state 1
    first_visit = [1, 1]
    for _ in range(10000):
        if first_visit[cur_s]:
            first_visit[cur_s] = 0
            a_0 = agent_0.choose_action(cur_s)
            a_1 = agent_1.choose_action(cur_s)
            r_0, r_1 = games[cur_s](a_0, a_1)
            r_0 += r_0
            r_1 += r_1
            time_step += 1
            cur_s = next_state(cur_s, a_0, a_1)
        else:

            a_0 = agent_0.choose_action(cur_s)
            a_1 = agent_1.choose_action(cur_s)
            tau_0[cur_s] = r_0[cur_s] / time_step[cur_s]
            tau_1[cur_s] = r_1[cur_s] / time_step[cur_s]
            agent_0.update_strategy(cur_s, a_0, tau_0[cur_s])
            agent_1.update_strategy(cur_s, a_1, tau_1[cur_s])
            r_0, r_1 = games[cur_s](a_0, a_1)
            r_0[cur_s] = 0
            r_1[cur_s] = 0
            r_0 += r_0
            r_1 += r_1
            time_step[cur_s] = 0
            time_step += 1
            cur_s = next_state(cur_s, a_0, a_1)


if __name__ == "__main__":
    Alice = Agent(alpha=0.0001, agent_id=0)
    Alice.initial_strategy()
    Alice.set_strategy(new_s=[0.1, 0.3])
    Alice_sum = 0
    for i in range(1000):
        Alice_sum += Alice.choose_action(0)
    print(Alice_sum)
