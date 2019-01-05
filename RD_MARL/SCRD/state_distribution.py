import numpy as np
from scipy.linalg import solve
from game_env import *


def param_state_end(s_start, s_end, a_l, pi):
    r_sum = 0
    for a_x in a_l:
        for a_y in a_l:
            r_sum += transition_prob(s_start, s_end, a_x, a_y) * pi[0][s_start][a_x] * pi[1][s_start][a_y]
    return r_sum


def param_matrix(s_l, a_l, pi):
    p_m = []
    for s_start in s_l:
        p_m.append([])
        for s_end in s_l:
            p_m[s_start].append(param_state_end(s_start, s_end, a_l, pi))
    return p_m


def gen_s_dist(s_l, a_l, pi):
    param_m = param_matrix(s_l, a_l, pi)
    # a = np.array([[param_m[0][0]-1, param_m[1][0]], [1, 1]])
    a = np.array([[param_m[0][1], param_m[1][1]-1], [1, 1]])
    b = np.array([0, 1])
    x = solve(a, b)
    return x


if __name__ == "__main__":
    strategy_pi = [{0: [0.2, 0.8], 1: [0.1, 0.9]}, {0: [0.7, 0.3], 1: [0.6, 0.4]}]
    states = [0, 1]
    actions = [0, 1]
    state_dist = gen_s_dist(states, actions, strategy_pi)
    print(state_dist)
