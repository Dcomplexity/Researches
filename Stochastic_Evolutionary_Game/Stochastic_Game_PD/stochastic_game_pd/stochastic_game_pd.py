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

    def play_game(self, other_agent):
        self.payoffs += pd_game_2(self.strategy, other_agent.get_strategy())[0]

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
    pd_game_list = [pd_game_0, pd_game_1]
    for i in range(total_num):
        # notice the difference between random.randint and np.random.randint
        popu.append(Agent(i, network[i], random.randint(0, 1)))
    state = {}
    for edge in edges:
        state[tuple(edge)] = 0
    return popu, network, total_num, edges, state, pd_game_list


def evolution_one_step(popu, total_num, edges, state, pd_game_list):
    # Play the game
    # for i in range(total_num):
    #     popu[i].set_payoffs(0)
    #     for j in popu[i].get_link():
    #         popu[i].play_game(popu[j], b)
    for i in range(total_num):
        popu[i].set_payoffs(0)
    state_ = {}
    for edge in edges:
        state_[tuple(edge)] = 0
    for edge in edges:
        i = edge[0]
        j = edge[1]
        a_i = popu[i].get_strategy()
        a_j = popu[j].get_strategy()
        r_i, r_j = pd_game_list[state[tuple(edge)]](a_i, a_j)
        popu[i].add_payoffs(r_i)
        popu[j].add_payoffs(r_j)
        state_[tuple(edge)] = next_state(state[tuple(edge)], a_i, a_j)
    # Backup the strategy in this round
    for i in range(total_num):
        popu[i].set_ostrategy()
    # Update strategy by imitating others' strategy
    for i in range(total_num):
        j = random.choice(popu[i].get_link())
        popu[i].imitate(popu[j])
    return popu, state_


def run():
    run_time = 100
    popu, network, total_num, edges, state, pd_game_list = initialize_population()
    for _ in range(run_time):
        popu, state = evolution_one_step(popu, total_num, edges, state, pd_game_list)
    return popu, network, total_num, edges, state, pd_game_list


def evaluation(popu, edges, state, pd_game_list):
    sample_time = 20
    sample_strategy = []
    total_num = len(popu)
    for _ in range(sample_time):
        popu, state = evolution_one_step(popu, total_num, edges, state, pd_game_list)
        strategy = []
        for i in range(total_num):
            strategy.append(popu[i].get_strategy())
        sample_strategy.append(np.mean(strategy))
    return np.mean(sample_strategy)


if __name__ == "__main__":
    initializations = 10
    result = []
    startTime = datetime.datetime.now()
    print(startTime)
    for _ in range(initializations):
        population, network_v, total_number_v, edges_v, state_v, pd_game_list_v = run()
        result.append(evaluation(population, edges_v, state_v, pd_game_list_v))
    endTime = datetime.datetime.now()
    print(endTime)
    print(endTime - startTime)
    print("The fraction of cooperators is ", np.mean(result))
