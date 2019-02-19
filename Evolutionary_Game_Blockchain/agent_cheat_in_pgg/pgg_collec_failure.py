import random
import math
import datetime

from game_env import *

class Agent:
    """
    Build an agent
    """
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
    popu = []
    for i in range(total_num):
        popu.append(Agent(i, network[i], random.randint(0, 1)))
    return popu, network, total_num, edges


def evolution_one_step(popu, total_num, edges, r, m):
    for i in range(total_num):
        popu[i].set_payoffs(0)
    for i in range(total_num):
        neigh = list()
        neigh.append(i)
        for j in popu[i].get_link():
            neigh.append(j)
        s_l = list()
        for j in neigh:
            s_l.append(popu[j].get_strategy())
        if np.sum(s_l) > m:
            p_l = public_goods_game(s_l, r)
            for k in range(len(neigh)):
                j = neigh[k]
                popu[j].add_payoffs(p_l[k])
    # Backup the strategy in this round
    for i in range(total_num):
        popu[i].set_ostrategy()
    # Update  strategy by imitating others' strategy
    for i in range(total_num):
        j = random.choice(popu[i].get_link())
        popu[i].imitate(popu[j])
    return popu


def run(r, m):
    run_time = 100
    popu, network, total_num, edges = initialize_population()
    for _ in range(run_time):
        popu = evolution_one_step(popu, total_num, edges, r, m)
    return popu, network, total_num, edges


def evaluation(popu, edges, r, m):
    sample_time = 10
    sample_strategy = []
    total_num = len(popu)
    for _ in range(sample_time):
        popu = evolution_one_step(popu, total_num, edges, r, m)
        strategy = []
        for i in range(total_num):
            strategy.append(popu[i].get_strategy())
        sample_strategy.append(np.mean(strategy))
    return np.mean(sample_strategy)


if __name__ == "__main__":
    r_r = 2.0
    m_r = 3
    initializations = 1
    result = []
    start_time = datetime.datetime.now()
    print(start_time)
    for _ in range(initializations):
        population_r, network_r, total_number_r, edges_r = run(r_r, m_r)
        result.append(evaluation(population_r, edges_r, r_r, m_r))
    end_time = datetime.datetime.now()
    print(end_time)
    print(end_time - start_time)
    print("The fraction of cooperators is ", np.mean(result))
