import numpy as np
import networkx as nx
import random
import math
import datetime
import argparse
import os
import datetime


def pd_game(strategy_x, strategy_y, b):
    if strategy_x == 1 and strategy_y == 1:
        return b-1, b-1
    elif strategy_x == 1 and strategy_y == 0:
        return -1, b
    elif strategy_x == 0 and strategy_y == 1:
        return b, -1
    elif strategy_x == 0 and strategy_y == 0:
        return 0, 0
    else:
        return "Error: The strategy do not fit the conditions."


def generate_network(structure, xdim=100, ydim=100):
    if structure == "2d_grid":
        g_network = nx.grid_2d_graph(xdim, ydim, periodic=True)
        adj_array = nx.to_numpy_array(g_network)
        adj_link = []
        for i in range(adj_array.shape[0]):
            adj_link.append(np.where(adj_array[i] == 1)[0])
        population_num = xdim * ydim
        g_edge = nx.Graph()
        for i in range(len(adj_link)):
            for j in range(len(adj_link[i])):
                g_edge.add_edge(i, adj_link[i][j])
    return np.array(adj_link), population_num, np.array(g_edge.edges())


class Agent:
    def __init__(self, agent_id, link, strategy):
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

    def add_payoffs(self, p):
        self.payoffs = self.payoffs + p

    def imitate(self, other_agent):
        j_payoffs = other_agent.get_payoffs()
        j_ostrategy = other_agent.get_ostrategy()
        t1 = 1 / (1 + math.e ** (10 * (self.payoffs - j_payoffs)))
        t2 = random.random()
        if t2 < t1:
            self.strategy = j_ostrategy


def initialize_population():
    network, total_num, edges = generate_network(structure='2d_grid')
    # print('network', network)
    # print('total_num', total_num)
    # print('edges', edges)
    popu = []
    for i in range(total_num):
        popu.append(Agent(i, network[i], random.randint(0, 1)))
    return popu, network, total_num, edges


def evolution_one_step(popu, total_num, edges, b):
    for i in range(total_num):
        popu[i].set_payoffs(0)
    for edge in edges:
        i = edge[0]
        j = edge[1]
        r_i, r_j = pd_game(popu[i].get_strategy(), popu[j].get_strategy(), b)
        popu[i].add_payoffs(r_i)
        popu[j].add_payoffs(r_j)
    for i in range(total_num):
        popu[i].set_ostrategy()
    for i in range(total_num):
        j = random.choice(popu[i].get_link())
        popu[i].imitate(popu[j])
    return popu


def run(b):
    run_time = 50
    popu, network, total_num, edges = initialize_population()
    for _ in range(run_time):
        popu = evolution_one_step(popu, total_num, edges, b)
    return popu, network, total_num, edges


def evaluation(popu, edges, b):
    sample_time = 10
    sample_strategy = []
    total_num = len(popu)
    for _ in range(sample_time):
        popu = evolution_one_step(popu, total_num, edges, b)
        strategy = []
        for i in range(total_num):
            strategy.append(popu[i].get_strategy())
        sample_strategy.append(np.mean(strategy))
    return np.mean(sample_strategy)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set the defect parameter b')
    parser.add_argument('-d', '--defect_param', type=float, required=True, help='Set the defector parameter b')
    args = parser.parse_args()
    defect_param_r = args.defect_param
    rounds_r = 5
    result_r = []
    abs_path = os.path.abspath(os.path.join(os.getcwd(), '../'))
    dir_name = abs_path + '/results/re_comparison/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    file_name = dir_name + 'frac_co_comparison_lattice_original_d_%s.txt' % defect_param_r
    f = open(file_name, 'w')
    start_time = datetime.datetime.now()
    print(start_time)
    for _ in range(rounds_r):
        print(_)
        population_r, network_r, total_number_r, edges_r = run(defect_param_r)
        result_r.append(evaluation(population_r, edges_r, defect_param_r))
    end_time = datetime.datetime.now()
    print(end_time)
    print(end_time - start_time)
    frac_co = np.mean(result_r)
    print("The fraction of cooperators is ", frac_co)
    f.write(str(defect_param_r) + ', ' + str(frac_co))


