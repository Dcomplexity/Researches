from game_env import *
import state_joint_action_distribution as sjad
import state_policy_distribution as spd
import os
import pandas as pd
import datetime


def payoff_cal(agent_id, s, a_l, mixed_s, p_matrix, pi):
    p = 0
    if agent_id == 0:
        for act_i in a_l:
            p_j = 0
            for act_j in a_l:
                p_j += p_matrix[s*(2**2)+act_i*2+act_j][0] * pi[1-agent_id][s][act_j]
            p += mixed_s[act_i] * p_j
    else:
        for act_i in a_l:
            p_j = 0
            for act_j in a_l:
                p_j += p_matrix[s*(2**2)+act_j*2+act_i][1] * pi[1-agent_id][s][act_j]
            p += mixed_s[act_i] * p_j
    return p


def evolve(strategy, steps):
    s_l = [0, 1]
    a_l = [0, 1]
    s00, s01, s10, s11 = strategy
    pi = [{0: [s00, 1-s00], 1: [s01, 1-s01]}, {0: [s10, 1-s10], 1: [s11, 1-s11]}]
    s_dist, p_matrix = sjad.run(pi)
    s_pi_dist = spd.gen_s_pi_dist(s_l, a_l, pi)
    ds00 = (payoff_cal(0, 0, a_l, [0, 1], p_matrix, pi) - payoff_cal(0, 0, a_l, pi[0][0], p_matrix, pi)) * s00 * s_pi_dist[0]
    ds01 = (payoff_cal(0, 1, a_l, [0, 1], p_matrix, pi) - payoff_cal(0, 1, a_l, pi[0][1], p_matrix, pi)) * s01 * s_pi_dist[1]
    ds10 = (payoff_cal(1, 0, a_l, [0, 1], p_matrix, pi) - payoff_cal(1, 0, a_l, pi[1][0], p_matrix, pi)) * s10 * s_pi_dist[0]
    ds11 = (payoff_cal(1, 1, a_l, [0, 1], p_matrix, pi) - payoff_cal(1, 1, a_l, pi[1][1], p_matrix, pi)) * s11 * s_pi_dist[1]
    return [s00+ds00*steps, s01+ds01*steps, s10+ds10*steps, s11+ds11*steps]


if __name__ == "__main__":
    states = [0, 1]
    actions = [0, 1]
    t = np.arange(0, 1000)
    d = []
    p = [0.2, 0.1, 0.7, 0.5]
    d.append(p)
    abspath = os.path.abspath(os.path.join(os.getcwd(), "./"))
    filename = abspath + "/strategy_trace_by_simulation.csv"
    f = open(filename, 'w')
    for v in t:
        p = evolve(p, steps=0.0001)
        d.append(p)
    ddf = pd.DataFrame(d)
    ddf.to_csv(filename, index=None)
    print(d)

