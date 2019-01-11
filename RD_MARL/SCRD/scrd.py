from game_env import *
import state_joint_action_distribution as sjad
import state_policy_distribution as spd

unit_vector = [{0: [0, 1], 1: [0, 1]}, {0: [0, 1], 1: [0, 1]}]


def payoff_cal(agent_id, s, a_l, mixed_s, p_matrix, pi):
    p = 0
    for act_i in a_l:
        p_j = 0
        for act_j in a_l:
            if agent_id == 0:
                p_j += p_matrix[s*2**2+act_i*2+act_j][agent_id] * pi[1-agent_id][s][act_j]
            else
        p += mixed_s[act_i] * p_j



policy_pi = [{0: [0.2, 0.8], 1: [0.3, 0.7]}, {0: [0.7, 0.3], 1: [0.8, 0.2]}]
state_dist, payoff_matrix = sjad.run(policy_pi)
print(state_dist)
print(payoff_matrix)