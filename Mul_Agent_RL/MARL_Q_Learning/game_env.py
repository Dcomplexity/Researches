import numpy as np
from itertools import permutations

# Generate the list of actions available in this game
def genAction():
    DEFECT = 0
    COOPERATE = 1
    actions = np.array([DEFECT, COOPERATE])
    return actions

# Generate the list of states available in this game
def genState(actions):
    states = []
    for _ in permutations(actions):
        states.append(_)
    for _ in actions:
        states.append((_,_))
    states.sort()
    return np.array(states)

# Create the prisoners' dilemma game
def PDGame(actionX, actionY):
    T = 5.0; R = 3.0; P = 1.0; S = 0.0
    if (actionX, actionY) == (1,1):
        return np.array([R,R])
    elif (actionX, actionY) == (1, 0):
        return np.array([S, T])
    elif (actionX, actionY) == (0, 1):
        return np.array([T, S])
    elif (actionX, actionY) == (0, 0):
        return np.array([P, P])

if __name__ == "__main__":
    actionX = int(input("Please enter the action of agent X: "))
    actionY = int(input("Please enter the action of agent Y: "))
    payoff = PDGame(actionX, actionY)
    print (payoff)