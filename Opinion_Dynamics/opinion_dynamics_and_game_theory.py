import numpy as np
import random
import math

class agent:
    def __init__(self, id, init_op, strategy):
        self.id = id
        self.op = init_op
        self.old_op = init_op
        self.strategy = strategy
        self.ostrategy = strategy
        self.payoffs = 0

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

    def set_strategy(self, new_s):
        self.strategy = new_s

    def set_ostrategy(self):
        self.ostrategy = self.strategy

    def get_strategy(self):
        return self.strategy

    def get_ostrategy(self):
        return self.ostrategy

    def get_payoffs(self):
        return self.payoffs

    def set_payoffs(self, p):
        self.payoffs = p

    def add_payoffs(self, p):
        self.payoffs = self.payoffs + p


def init_population(num):
    population = []
    for i in range(num):
        population.append(agent(i, random.random(), np.random.choice([0, 1])))
    return population


def play_donation_game(a_x, a_y, b):
    if a_x ==  1 and a_y == 1:
        return b-1, b-1
    elif a_x == 1 and a_y == 0:
        return -1, b
    elif a_x == 0 and a_y == 1:
        return b, -1
    elif a_x == 0 and a_y == 0:
        return 0, 0
    else:
        return "Error"


def run(num):
    population = init_population(num)
    rounds_num = 100
    for _ in range(rounds_num):
        popu_op = [[] for s in range(num)]
        for i in range(num):
            popu_op[i].append(population[i].get_op())
            population[i].set_payoffs(0)
        for i in range(num):
            popu_id = list(range(0, num))
            popu_id.remove(i)
            j_l = np.random.choice(popu_id, 3)
            for j in j_l:
                if abs(population[i].get_op() - population[j].get_op()) < 0.1:
                    r_i, r_j = play_donation_game(population[i].get_strategy(), population[j].get_strategy(), 1.0)
                    population[i].add_payoffs(r_i)
                    population[j].add_payoffs(r_j)
                    if (population[i].get_strategy() == 1 and population[j].get_strategy() == 1):
                        popu_op[i].append(population[j].get_op())
                        popu_op[j].append(population[i].get_op())
        for i in range(num):
            population[i].set_ostrategy()
        for i in range(num):
            ind = population[i]
            w1 = 0.01
            w2 = random.random()
            if w2 < w1:
                potential_strategy = [0, 1]
                potential_strategy.remove(ind.get_ostrategy())
                ind.set_strategy(np.random.choice(potential_strategy))
            else:
                ind_payoffs = ind.get_payoffs()
                while True:
                    j = random.choice(range(num))
                    if j != i:
                        break
                # j = random.choice(popu[i].get_link())
                opponent = population[j]
                opponent_payoffs = opponent.get_payoffs()
                opponent_ostrategy = opponent.get_ostrategy()
                t1 = 1 / (1 + math.e ** (2.0 * (ind_payoffs - opponent_payoffs)))
                t2 = random.random()
                if t2 < t1:
                    ind.set_strategy(opponent_ostrategy)
        for i in range(num):
            population[i].set_op(np.sum(popu_op[i]) / len(popu_op[i]))
    for i in population:
        print(i.get_op())
        print(i.get_strategy())

if __name__ == '__main__':
    run(100)

