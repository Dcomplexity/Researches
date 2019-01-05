import numpy as np
from scipy.linalg import solve
from game_env import *


def param_start_end(s_start, s_end, a_l, pi):
    r_sum = 0
    for a_x in a_l:
        for a_y in a_l:
            r_sum += transition_prob(s_start, s_end, a_x, a_y) * pi[0][s_start][a_x] * pi[1][s_start][a_y]
    return r_sum


def param_matrix(s_l, a_l, pi):
    q_m = []
    for s_start in s_l:
        q_m.append([])
        for s_end in s_l:
            q_m[s_start].append(param_start_end(s_start, s_end, a_l, pi))
    p_m = []
    for s_start


def param_matrix