import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

def build_network():
    G = nx.karate_club_graph()
    adj_array = nx.to_numpy_array(G)
    adj_link = []
    for i in range(adj_array.shape[0]):
        adj_link.append(list(np.where(adj_array[i] == 1)[0]))
    node_num = len(adj_link)
    return adj_array, adj_link, node_num

class agent:
    def __init__(self, id, init_op):
        self.id = id
        self.op = init_op
        self.old_op = init_op

    def set_op(self, new_op):
        self.op = new_op

    def get_op(self):
        return self.op

    def get_old_op(self):
        return self.old_op

    def get_id(self):
        return self.id

    def backup(self):
        self.old_op = self.op

    def learn(self, other_op):
        self.op = (other_op + self.op) / 2


def init_population():
    population = []
    population.append(agent(0, 0.0))
    adj_array, adj_link, node_num = build_network()
    for i in range(1, node_num-1):
        population.append(agent(i, random.random()))
    population.append(agent(node_num-1, 1.0))
    return adj_array, adj_link, node_num, population


def run():
    adj_array, adj_link, node_num, popu = init_population()
    round_num = 10000
    for _ in range(round_num):


if __name__ == '__main__':

    print(adj_array)

