import numpy as np
import pandas as pd
import networkx as nx
import random
import math
import datetime
import argparse
import os
import datetime


def pd_game(strategy_x, strategy_y, b):
    if (strategy_x == 1 or strategy_x == 2) and (strategy_y == 1 or strategy_y == 2):
        return b-1, b-1
    elif (strategy_x == 1 or strategy_x == 2) and strategy_y == 0:
        return -1, b
    elif strategy_x == 0 and (strategy_y == 1 or strategy_y == 2):
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
        self.neigh_defectors = []

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
        popu.append(Agent(i, network[i], np.random.choice([0, 1, 2], p=[0.5, 0.25, 0.25])))
    return popu, network, total_num, edges


def find_neigh_defectors(popu, network, total_num):
    neigh_defectors = [[] for _ in range(total_num)]
    for i in range(total_num):
        for j in network[i]:
            if popu[j].get_strategy() == 0:
                neigh_defectors[i].append(j)
    return neigh_defectors


def evolution_one_step(popu, network, total_num, edges, b, punishment_cost):
    for i in range(total_num):
        popu[i].set_payoffs(0)
    for edge in edges:
        i = edge[0]
        j = edge[1]
        r_i, r_j = pd_game(popu[i].get_strategy(), popu[j].get_strategy(), b)
        popu[i].add_payoffs(r_i)
        popu[j].add_payoffs(r_j)
    neigh_defectors = find_neigh_defectors(popu, network, total_num)
    for i in range(total_num):
        if popu[i].get_strategy() == 2:
            num_defectors = len(neigh_defectors[i])
            if num_defectors > 0:
                popu[i].add_payoffs(-punishment_cost)
                for j in neigh_defectors[i]:
                    popu[j].add_payoffs(-1.0/num_defectors)
    for i in range(total_num):
        popu[i].set_ostrategy()
    for i in range(total_num):
        j = random.choice(popu[i].get_link())
        popu[i].imitate(popu[j])
    return popu


def run(b, punishment_cost):
    run_time = 50
    popu, network, total_num, edges = initialize_population()
    for _ in range(run_time):
        popu = evolution_one_step(popu, network, total_num, edges, b, punishment_cost)
    return popu, network, total_num, edges


def evaluation(popu, network, edges, b, punishment_cost):
    sample_time = 10
    sample_strategy = []
    total_num = len(popu)
    for _ in range(sample_time):
        popu = evolution_one_step(popu, network, total_num, edges, b, punishment_cost)
        cal_strategy = np.zeros(3)
        for i in range(total_num):
            cal_strategy[popu[i].get_strategy()] += 1
        cal_strategy = cal_strategy / total_num
        sample_strategy.append(cal_strategy)
    return np.mean(sample_strategy, axis=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set the defect parameter b')
    parser.add_argument('-d', '--defect_param', type=float, required=True, help='Set the defector parameter b')
    parser.add_argument('-p', '--punishment_cost_param', type=float, required=True, help='Set the punishment cost parameter')
    args = parser.parse_args()
    defect_param_r = args.defect_param
    punishment_cost_r = args.punishment_cost_param
    rounds_r = 5
    abs_path = os.path.abspath(os.path.join(os.getcwd(), '../'))
    dir_name = abs_path + '/results/re_comparison/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    file_name = dir_name + 'frac_co_comparison_lattice_c_punishment_cost_%s_d_%s.txt' % (punishment_cost_r, defect_param_r)
    f = open(file_name, 'w')
    start_time = datetime.datetime.now()
    print(start_time)
    round_results_r = []
    for _ in range(rounds_r):
        print(_)
        population_r, network_r, total_number_r, edges_r = run(defect_param_r, punishment_cost_r)
        round_results_r.append(evaluation(population_r, network_r, edges_r, defect_param_r, punishment_cost_r))
    results_r = np.mean(round_results_r, axis=0)
    results_r_pd = pd.DataFrame(results_r)
    print(results_r)
    results_r_pd.to_csv(f)
    end_time = datetime.datetime.now()
    print(end_time)
    print(end_time - start_time)


