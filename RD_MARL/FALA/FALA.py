import numpy as np


class Agent:
    def __init__(self, alpha):
        self.strategy = {}
        self.actions = [0, 1]
        self.states = [0, 1]
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
                self.strategy[state][0] = 1 - new_s[state]
                self.strategy[state][1] = new_s[state]

    def choose_action(self, s):
        a = np.random.choice(np.array(self.actions), size=1, p=self.strategy[s])[0]
        return a

    def update_strategy(self, s, a, r):
        for action in self.actions:
            if action == a:
                self.strategy[s][action] = self.strategy[s][action] + self.alpha * r * (1 - self.strategy[s][action])
            else:
                self.strategy[s][action] = self.strategy[s][action] - self.alpha * r * self.strategy[s][action]


if __name__ == "__main__":
    Alice = Agent()
    Alice.initial_strategy()
    Alice.set_strategy(new_s=[0.1, 0.3])
    Alice_sum = 0
    for i in range(1000):
        Alice_sum += Alice.choose_action(0)
    print(Alice_sum)
