import numpy as np
from scipy.linalg import solve
from game_env import *


def param_start_end(s_start, s_end, a_l, pi):
    r_sum = 0
    for a_x in a_l:
        for a_y in a_l:
            # notice the transition_prob, it is q_s(z,a)
            r_sum += transition_prob(s_end, s_start, a_x, a_y) * pi[0][s_end][a_x] * pi[1][s_end][a_y]
    return r_sum


# def param_matrix(s_l, a_l, pi):
#     p_m = []
#     for s_start in s_l:
#         p_m.append([])
#         for s_end in s_l:
#             p_m[s_start].append(param_start_end(s_start, s_end, a_l, pi))
#     print(p_m)
#     return p_m

def param_matrix(s_l, a_l, pi):
    p_m = {}
    for s_start in s_l:
        for s_end in s_l:
            p_m[(s_start, s_end)] = param_start_end(s_start, s_end, a_l, pi)
    return p_m


def gen_s_pi_dist(s_l, a_l, pi):
    param_m = param_matrix(s_l, a_l, pi)
    # a = np.array([[param_m[0][0]-1, param_m[1][0]], [1, 1]])
    a = np.array([[param_m[(1, 0)], param_m[(1, 1)]-1], [1, 1]])
    b = np.array([0,  1])
    x = solve(a, b)
    return x


if __name__ == "__main__":
    policy_pi = [{0: [0.2, 0.8], 1: [0.3, 0.7]}, {0: [0.7, 0.3], 1: [0.6, 0.4]}]
    states = [0, 1]
    actions = [0, 1]
    # param_m = param_matrix(states, actions, policy_pi)
    # print(param_m)
    state_dist = gen_s_pi_dist(states, actions, policy_pi)
    print(state_dist)
