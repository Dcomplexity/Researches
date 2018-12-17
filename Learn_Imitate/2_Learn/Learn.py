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
        self.agent_id = agent_id
        self.link = link
        self.strategy = strategy
        self.ostrategy = strategy
        self.payoffs = 0

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

    def learn(self):

# class Tester:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     def get_a(self):
#         return self.a
#
#     def get_b(self):
#         return self.b
#
#     def set_a(self, o_a):
#         self.a = o_a
#
#     def set_b(self, o_b):
#         self.b = o_b
#
#     def set_a_b(self):
#         self.a = self.b
#
#
# if __name__ == "__main__":
#     test_v = Tester(1, 2)
#     a_v = test_v.get_a()
#     b_v = test_v.get_b()
#     test_v.set_a_b()
#     test_v.set_b(3)
#     b_v = test_v.get_b()
#     a_v = test_v.get_a()
#     print(a_v, b_v)

