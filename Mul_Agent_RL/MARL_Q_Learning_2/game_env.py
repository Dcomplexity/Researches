import numpy as np
from itertools import permutations


def alpha_time(time_step):
    return 1 / (10 + 0.002 * time_step)


def epsilon_time(time_step):
    return 0.5 / (1 + 0.0001 * time_step)


def epsilon_fixed(time_step):
    return 0.3


def gen_actions():
    defect = 0
    cooperate = 1
    actions = np.array([defect, cooperate])
    return actions


def gen_states(actions):
    states = []
    for _ in permutations(actions, 2):
        states.append(_)
    for _ in actions:
        states.append((_, _))
    states.sort()
    return states


# Create the prisoner dilemma game
def pd_game(a_x, a_y):
    t = 5.0
    r = 3.0
    p = 1.0
    s = 0.0
    if (a_x, a_y) == (1, 1):
        return r, r
    elif (a_x, a_y) == (1, 0):
        return s, t
    elif (a_x, a_y) == (0, 1):
        return t, s
    elif (a_x, a_y) == (0, 0):
        return p, p


def mp_game(a_x, a_y):
    if (a_x, a_y) == (1, 1):
        return 1, -1
    elif (a_x, a_y) == (1, 0):
        return -1, 1
    elif (a_x, a_y) == (0, 1):
        return -1, 1
    elif (a_x, a_y) == (0, 0):
        return 1, -1
