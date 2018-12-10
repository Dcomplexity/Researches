import numpy as np
import random
import math
import argparse
import os
import datetime
import networkx as nx

class Agent():
    """  Build an agent
    """
    def __init__(self, id, link, strategy):
        self.id = id
        self.link = link
        self.strategy = strategy
        self.ostrategy = strategy
        self.payoffs = 0
        # print (self.link)

    def getId(self):
        return self.id

    def getLink(self):
        return self.link

    def getStrategy(self):
        return self.strategy

    def getOstrategy(self):
        return self.ostrategy

    def getPayoffs(self):
        return self.payoffs

    def setStrategy(self, otherStrategy):
        self.strategy = otherStrategy

    def setOstrategy(self):
        self.ostrategy = self.strategy

    def playGame(self, b):
        self.payoffs = 0
        for i in self.link:
            self.payoffs += PDGame(self.strategy, population[i].getStrategy(), b)[0]

    def imitate(self):
        j = random.choice(self.link)
        jPayoffs = population[j].getPayoffs()
        jOstrategy = population[j].getOstrategy()
        t1 = 1 / (1 + math.e ** (10 * (self.getPayoffs()-jPayoffs)))
        t2 = random.random()
        if t2 < t1:
            self.setStrategy(jOstrategy)

def PDGame(strategy0, strategy1, b):
    if strategy0 == 1 and strategy1 == 1:
        return (1, 1)
    elif strategy0 == 1 and strategy1 == 0:
        return (0, b)
    elif strategy0 == 0 and strategy1 == 1:
        return (b, 0)
    elif strategy0 == 0 and strategy1 == 0:
        return (0, 0)
    else:
        return "Error"

def generateNetwork(structure, xdim=100, ydim=100):
    if structure == "2d_grid":
        G = nx.grid_2d_graph(xdim, ydim, periodic=True)
        adjArray = nx.to_numpy_array(G)
        adjLink = []
        for i in range(adjArray.shape[0]):
            adjLink.append(np.where(adjArray[i] == 1)[0])
        populationNum = xdim * ydim
    return np.array(adjLink), populationNum

def initializePopulation():
    network, totalNum = generateNetwork(structure='2d_grid')
    population = []
    for i in range(totalNum):
        population.append(Agent(i, network[i], random.randint(0, 1)))  # notice the difference between random.randint and np.random.randint
    return population, totalNum

def evolutionOneStep(population):
    # Play the game
    for i in range(totalNum):
        population[i].playGame(b)
    # Backup the strategy in this round
    for i in range(totalNum):
        population[i].setOstrategy()
    # Update strategy by imitating others' strategy
    for i in range(totalNum):
        population[i].imitate()
    return population

def evolution(population):
    for i in range(runTime):
        population = evolutionOneStep(population)
    return population

def evaluation(population):
    sampleStrategy = []
    for i in range(sampleTime):
        population = evolutionOneStep(population)
        strategy = []
        for i in range(totalNum):
            strategy.append(population[i].getStrategy())
        sampleStrategy.append(np.mean(strategy))
    return (np.mean(sampleStrategy))

if __name__ == "__main__":
    b = 1.0
    runTime = 100
    sampleTime = 10
    initializations = 10
    result = []
    startTime = datetime.datetime.now()
    print (startTime)
    for _ in range(initializations):
        population, totalNum = initializePopulation()
        population = evolution(population)
        result.append(evaluation(population))
    endTime = datetime.datetime.now()
    print (endTime)
    print (endTime - startTime)
    print ("The fraction of cooperators is ", np.mean(result))

