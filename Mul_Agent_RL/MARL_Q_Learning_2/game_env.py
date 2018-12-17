def alpha(timeStep):
    return 1 / (10 + 0.002 * timeStep)

def epsilon(timeStep): # 0.5 / (1000 + 0.000001 * self.timeStep)  #when episodes reach about 1000000, the final EPSILON is about 0.25, which means there is a big probability that it will explore
    return 0.5 / (1 + 0.0001 * timeStep)

def epsilonFixed(timeStep):
    return 0.3


import numpy as np
from itertools import permutations

def generateDCActions():
    DEFECT = 0
    COOPERATE = 1
    actions = np.array([DEFECT, COOPERATE])
    return actions

def generateDCStates(actions):
    states = []
    for _ in permutations(actions, 2):
        states.append(_)
    for _ in actions:
        states.append((_, _))
    states.sort()
    return states

# Create the prisoner dilemma game
def PDGame(actionX, actionY):
    T = 5.0
    R = 3.0
    P = 1.0
    S = 0.0
    if (actionX, actionY) == (1,1):
        return [R,R]
    elif (actionX, actionY) == (1, 0):
        return [S, T]
    elif (actionX, actionY) == (0, 1):
        return [T, S]
    elif (actionX, actionY) == (0, 0):
        return [P, P]

def MPGame(actionX, actionY):
    if (actionX, actionY) == (1, 1):
        return [1, -1]
    elif (actionX, actionY) == (1, 0):
        return [-1, 1]
    elif (actionX, actionY) == (0, 1):
        return [-1, 1]
    elif (actionX, actionY) == (0, 0):
        return [1, -1]