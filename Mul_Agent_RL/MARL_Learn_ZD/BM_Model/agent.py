from BM_Model.game_env import gen_actions
import random


class AgentBM:
    def __init__(self, lr=None, expc_a=None, init_st=None):
        self.lr = lr
        self.expc_a = expc_a
        self.a = gen_actions()
        self.st = init_st
        self.stimulus = 0

    # def initial_strategy(self):
    #     self.st = 1.0 / len(self.a)

    def get_actions(self):
        return self.a

    def get_strategy(self):
        return self.st

    def choose_actions(self):
        if random.random() < self.st:
            return self.a[1]  # cooperate
        else:
            return self.a[0]  # defect

    def set_stimulus(self, pf=None):
        self.stimulus = (pf - self.expc_a) / (4.0 - self.expc_a)

    def update_strategy(self):
        if self.stimulus >= 0:
            self.st = self.st + self.lr * self.stimulus * (1 - self.st)
        else:
            self.st = self.st + self.lr * self.stimulus * self.st


if __name__ == "__main__":
    A = AgentBM(0.1, 2)
    strategy = A.get_strategy()
    print(strategy)
    print(A.get_actions())
