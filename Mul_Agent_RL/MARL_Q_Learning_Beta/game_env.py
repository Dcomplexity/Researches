import numpy as np
from itertools import permutations


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


def pd_game(action_x, action_y):
    t = 5.0
    r = 3.0
    p = 1.0
    s = 0.0
    if (action_x, action_y) == (1, 1):
        return r, r
    elif (action_x, action_y) == (1, 0):
        return s, t
    elif (action_x, action_y) == (0, 1):
        return t, s
    elif (action_x, action_y) == (0, 0):
        return p, p


def alpha_time(time_step):
    return 1 / (10 + 0.002 * time_step)


def epsilon_time(time_step):
    return 0.5 / (1 + 0.0001 * time_step)
