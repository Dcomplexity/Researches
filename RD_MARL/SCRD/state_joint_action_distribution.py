import numpy as np
from scipy.linalg import solve
from game_env import *


def param_start_end(s_start, s_end, a_l, pi):  # calculate the Q value
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
    return q_m


def gen_s_joint_action_dist(s_l, a_l, s, a_x, a_y, pi):
    param_m = param_matrix(s_l, a_l, pi)
    if s == 0:
        a = np.array([[transition_prob(s, 1-s, a_x, a_y), param_m[1-s][1-s] - 1], [1, 1]])
    elif s == 1:
        a = np.array([[param_m[1-s][1-s]-1, transition_prob(s, 1-s, a_x, a_y)], [1, 1]])
    # a = np.array([[transition_prob(s, s, a_x, a_y) - 1, param_m[1-s][s]], [1, 1]])
    b = np.array([0, 1])
    x = solve(a, b)
    return x


def gen_payoff_matrix(pds, a_l, s, a_x, a_y, pi, s_d):
    p = np.array(pds[s](a_x, a_y))*s_d[s*2**2 + a_x*2 + a_y][s]
    for a_x_s_ in a_l:
        for a_y_s_ in a_l:
            p += np.array(pds[1-s](a_x_s_, a_y_s_))*pi[0][1-s][a_x_s_]*pi[1][1-s][a_y_s_]*s_d[s*2**2+a_x*2+a_y][1-s]
    return p


def run(pi):
    pd_games = [play_pd_game_1, play_pd_game_2]
    states = [0, 1]
    actions = [0, 1]
    s_dist = []
    for s in states:
        for a_x in actions:
            for a_y in actions:
                s_dist.append(gen_s_joint_action_dist(states, actions, s, a_x, a_y, pi))
    p_matrix = []
    for s in states:
        for a_x in actions:
            for a_y in actions:
                p_matrix.append(gen_payoff_matrix(pd_games, actions, s, a_x, a_y, pi, s_dist))
    return s_dist, p_matrix


if __name__ == "__main__":
    policy_pi = [{0: [0.3, 0.7], 1: [0.3, 0.7]}, {0: [0.8, 0.2], 1: [0.8, 0.2]}]
    state_dist, payoff_matrix = run(policy_pi)
    print(state_dist)
    print(payoff_matrix)
