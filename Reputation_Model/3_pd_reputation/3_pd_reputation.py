import random
import math
import datetime

from game_env import *


class Agent:
    """  Build an agent
    """
    def __init__(self, agent_id, link, strategy):
        self.agent_id = agent_id
        self.link = link
        self.strategy = strategy
        self.ostrategy = strategy
        self.payoffs = 0
        # print (self.link)

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

    def play_game(self, other_agent, b):
        self.payoffs += pd_game(self.strategy, other_agent.get_strategy(), b)[0]

    def imitate(self, other_agent):
        j_payoffs = other_agent.get_payoffs()
        j_ostrategy = other_agent.get_ostrategy()
        t1 = 1 / (1 + math.e ** (10 * (self.payoffs - j_payoffs)))
        t2 = random.random()
        if t2 < t1:
            self.strategy = j_ostrategy


class AgentReputation(Agent):
    def __init__(self, agent_id, link, strategy):
        Agent.__init__(self, agent_id, link, strategy)
        self.reputation = 1

    def get_reputation(self):
        return self.reputation

    def update_reputation(self, co_frac, method="decrease_by_step"):
        if method == "decrease_by_step":
            if self.strategy == 0:
                self.reputation = self.reputation - self.reputation * co_frac
        if method == "set_frac":
            self.reputation = co_frac


def initialize_population():
    network, total_num, edges = generate_network(structure='2d_grid')
    popu = []
    for i in range(total_num):
        # notice the difference between random.randint and np.random.randint
        popu.append(AgentReputation(i, network[i], random.randint(0, 1)))
    return popu, network, total_num, edges


def evolution_one_step(popu, total_num, edges, b):
    # Play the game
    # for i in range(total_num):
    #     popu[i].set_payoffs(0)
    #     for j in popu[i].get_link():
    #         popu[i].play_game(popu[j], b)
    for i in range(total_num):
        popu[i].set_payoffs(0)
    for edge in edges:
        i = edge[0]
        j = edge[1]
        rep_i = popu[i].get_reputation()
        rep_j = popu[j].get_reputation()
        rep_fre = 1 / (1 + 100 * math.e ** -(rep_i * rep_j * 8))
        if random.random() < rep_fre:
            r_i, r_j = pd_game(popu[i].get_strategy(), popu[j].get_strategy(), b)
            popu[i].add_payoffs(r_i)
            popu[j].add_payoffs(r_j)
    # Backup the strategy in this round
    for i in range(total_num):
        popu[i].set_ostrategy()
    # Update strategy by imitating others' strategy
    for i in range(total_num):
        j = random.choice(popu[i].get_link())
        popu[i].imitate(popu[j])
    for i in range(total_num):
        co_frac_i = 0
        for _ in popu[i].get_link():
            if popu[_].get_strategy() == 1:
                co_frac_i += 1
        co_frac_i = co_frac_i / len(popu[i].get_link())
        popu[i].update_reputation(co_frac_i, method="set_frac")
    return popu


def run(b):
    run_time = 100
    popu, network, total_num, edges = initialize_population()
    for _ in range(run_time):
        popu = evolution_one_step(popu, total_num, edges, b)
    return popu, network, total_num, edges,


def evaluation(popu, edges, b):
    sample_time = 20
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
    b_v = 1.2
    initializations = 10
    result = []
    startTime = datetime.datetime.now()
    print(startTime)
    for _ in range(initializations):
        population, network_v, total_number_v, edges_v = run(b_v)
        result.append(evaluation(population, edges_v, b_v))
    endTime = datetime.datetime.now()
    print(endTime)
    print(endTime - startTime)
    print("The fraction of cooperators is ", np.mean(result))
