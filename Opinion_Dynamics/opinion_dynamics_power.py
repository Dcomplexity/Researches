import numpy as np
import random

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

def init_population(num):
    population = []
    for i in range(num):
        population.append(agent(i, i / 100))
    return population

def run(num):
    population = init_population(num)
    rounds_num = 10000
    for _ in range(rounds_num):
        popu_id = list(range(0, 100))
        i = np.random.choice(popu_id)
        popu_id.remove(i)
        j = np.random.choice(popu_id)
        avg_op = 0
        for k in range(num):
            avg_op += population[k].get_op()
        avg_op = avg_op / num
        print(avg_op)
        if abs(population[i].get_op() - population[j].get_op()) < 1.0:
            population[i].backup()
            population[j].backup()
            # population[i].learn(population[j].get_old_op())
            # population[j].learn(population[i].get_old_op())
            r_i = 1 - abs(0.0 - population[i].get_old_op())
            r_j = 1 - abs(0.0 - population[j].get_old_op())
            power_i = r_i / (r_i + r_j)
            power_j = r_j / (r_i + r_j)
            print(power_i, power_j)
            new_i_op = population[i].get_old_op() * power_i + population[j].get_old_op() * power_j
            new_j_op = population[i].get_old_op() * power_i + population[j].get_old_op() * power_j
            population[i].set_op(new_i_op)
            population[j].set_op(new_j_op)
    for i in population:
        print(i.get_op())

if __name__ == '__main__':
    run(100)

