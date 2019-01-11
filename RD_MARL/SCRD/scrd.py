from game_env import *
import state_joint_action_distribution as sjad
import state_policy_distribution as spd
from scipy.integrate import odeint


def payoff_cal(agent_id, s, a_l, mixed_s, p_matrix, pi):
    p = 0
    if agent_id == 0:
        for act_i in a_l:
            p_j = 0
            for act_j in a_l:
                p_j += p_matrix[s*2**2+act_i*2+act_j][0] * pi[1-agent_id][s][act_j]
            p += mixed_s[act_i] * p_j
    else:
        for act_i in a_l:
            p_j = 0
            for act_j in a_l:
                p_j += p_matrix[s*2**2+act_j*2+act_i][1] * pi[1-agent_id][s][act_j]
            p += mixed_s[act_i] * p_j
    return p


def deriv(x, step):
    s_l = [0, 1]
    a_l = [0, 1]
    pi = [{0: [1-x[0], x[0]], 1: [1-x[1], x[1]]}, {0: [1-x[2], x[2]], 1: [1-x[3], x[3]]}]
    s_dist, p_matrix = sjad.run(pi)
    s_pi_dist = spd.gen_s_pi_dist(s_l, a_l, pi)
    # dx0 = (payoff_cal(0, 0, a_l, [0, 1], p_matrix, pi) - payoff_cal(0, 0, a_l, pi[0][0], p_matrix, pi)) * x[0] * \
    #        s_pi_dist[0]
    # dx1 = (payoff_cal(0, 1, a_l, [0, 1], p_matrix, pi) - payoff_cal(0, 1, a_l, pi[0][1], p_matrix, pi)) * x[1] * \
    #        s_pi_dist[0]
    # dx2 = (payoff_cal(1, 0, a_l, [0, 1], p_matrix, pi) - payoff_cal(1, 0, a_l, pi[1][0], p_matrix, pi)) * x[2] * \
    #        s_pi_dist[1]
    # dx3 = (payoff_cal(1, 1, a_l, [0, 1], p_matrix, pi) - payoff_cal(1, 1, a_l, pi[1][1], p_matrix, pi)) * x[3] * \
    #        s_pi_dist[1]
    x[0] = (payoff_cal(0, 0, a_l, [0, 1], p_matrix, pi) - payoff_cal(0, 0, a_l, pi[0][0], p_matrix, pi)) * x[0] * \
           s_pi_dist[0]
    x[1] = (payoff_cal(0, 1, a_l, [0, 1], p_matrix, pi) - payoff_cal(0, 1, a_l, pi[0][1], p_matrix, pi)) * x[1] * \
           s_pi_dist[0]
    x[2] = (payoff_cal(1, 0, a_l, [0, 1], p_matrix, pi) - payoff_cal(1, 0, a_l, pi[1][0], p_matrix, pi)) * x[2] * \
           s_pi_dist[1]
    x[3] = (payoff_cal(1, 1, a_l, [0, 1], p_matrix, pi) - payoff_cal(1, 1, a_l, pi[1][1], p_matrix, pi)) * x[3] * \
           s_pi_dist[1]
    # return np.array([x[0]+step*dx0, x[1]+step*dx1, x[2]+step*dx2, x[3]*step*dx3])
    return x


if __name__ == "__main__":
    states = [0, 1]
    actions = [0, 1]
    # unit_vector = [{0: [0, 1], 1: [0, 1]}, {0: [0, 1], 1: [0, 1]}]
    # policy_pi = [{0: [0.2, 0.8], 1: [0.3, 0.7]}, {0: [0.7, 0.3], 1: [0.8, 0.2]}]
    # state_dist, payoff_matrix = sjad.run(policy_pi)
    # p = payoff_cal(0, 0, actions, [0, 1], payoff_matrix, policy_pi)
    # print(p)
    t = np.arange(0, 100, 0.01)
    x = np.array([0.2, 0.1, 0.7, 0.5])
    x = odeint(deriv, x, t)
    print(x)
    # d = []
    # for i in range(100000):
    #     print(i)
    #     x = deriv(x, 0.001)
    #     d.append(x)
    # print(d)
