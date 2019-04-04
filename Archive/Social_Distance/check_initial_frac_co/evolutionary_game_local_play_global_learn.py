import numpy as np
import random
import math
import argparse
import os
import datetime

class SocialStructure:
    def __init__(self, group_size, group_base, group_length, total_num):
        self.group_size = group_size
        self.group_base = group_base
        self.group_length = group_length
        self.total_num = total_num
        if self.total_num != self.group_size * (self.group_base ** (self.group_length-1)):
            print("Error: The total number does not correspond to the social structure")

    def build_social_structure(self):
        self.group_num = self.group_base ** (self.group_length - 1)
        self.ind_pos = [0 for x in range(self.total_num)]
        self.pos_ind = [[] for x in range(self.group_num)]

        for i in range(self.group_num):
            for j in range(i*self.group_size, (i+1)*self.group_size):
                self.ind_pos[j] = i
                self.pos_ind[i].append(j)
        return np.array(self.ind_pos), np.array(self.pos_ind)


def pd_game(strategy_0, strategy_1, b):
    if strategy_0 == 1 and strategy_1 == 1:
        return 1, 1
    elif strategy_0 == 1 and strategy_1 == 0:
        return 0, b
    elif strategy_0 == 0 and strategy_1 == 1:
        return b, 0
    elif strategy_0 == 0 and strategy_1 == 0:
        return 0, 0
    else:
        return "Error"


def build_structure(struc_group_size, struc_group_base, struc_group_length):
    struc_total_num = struc_group_size * (struc_group_base ** (struc_group_length -1))
    struc_social_structure = SocialStructure(struc_group_size, struc_group_base, struc_group_length, struc_total_num)
    (struc_ind_pos, struc_pos_ind) = struc_social_structure.build_social_structure()
    return (struc_ind_pos, struc_pos_ind)


# def initialize_strategy(total_num):
#     ind_strategy = np.random.random(total_num)
#     return ind_strategy

def initialize_strategy(total_num, c_frac):
    ind_strategy = [c_frac for i in range(total_num)]
    return ind_strategy


def run_game(ind_strategy, defec_param, group_size, group_base, group_length, total_num, ind_pos, pos_ind):
    if total_num != len(ind_pos):
        print('Error')
    old_ind_strategy = np.zeros(total_num)
    for i in range(total_num):
        old_ind_strategy[i] = ind_strategy[i]
    opponent_play = np.zeros(total_num, dtype=int)
    opponent_learn = np.zeros(total_num, dtype=int)
    ind_action = np.zeros(total_num, dtype=int)
    payoffs = np.zeros(total_num)
    for i in range(total_num):
        now_position = ind_pos[i]
        individual_pool = list(pos_ind[now_position][:])
        individual_pool.remove(i)
        potential_individual = [x for x in individual_pool]
        opponent_play[i] = np.random.choice(potential_individual)
    for i in range(total_num):
        opponent_learn[i] = np.random.choice(range(0, total_num))
    for i in range(total_num):
        action = np.random.choice([0, 1], p=[1-ind_strategy[i], ind_strategy[i]])
        ind_action[i] = action
    for i in range(total_num):
        player_index = i
        opponent_index = opponent_play[i]
        (payoffs_i, payoffs_j) = pd_game(ind_action[player_index], ind_action[opponent_index], defec_param)
        payoffs[player_index] += payoffs_i
        payoffs[opponent_index] += payoffs_j
    # update strategy based on average payoffs of cooperators and defectors
    average_c_payoff = 0
    average_d_payoff = 0
    c_num = np.sum(ind_action)
    c_frac = c_num / total_num
    d_num = total_num - c_num
    for i in range(total_num):
        if ind_strategy[i] == 1:
            average_c_payoff += payoffs[i]
        else:
            average_d_payoff += payoffs[i]
    if c_num == 0:
        average_c_payoff = 0
    else:
        average_c_payoff = average_c_payoff / c_num
    if d_num == 0:
        average_d_payoff = 0
    else:
        average_d_payoff = average_d_payoff / d_num
    x_gradient = c_frac * (1 - c_frac) * (average_c_payoff - average_d_payoff)
    for i in range(total_num):
        ind_strategy[i] = ind_strategy[i] + 0.001 * x_gradient
        if ind_strategy[i] > 1:
            ind_strategy[i] = 1
        elif ind_strategy[i] < 0:
            ind_strategy[i] = 0
    return ind_strategy


if __name__ == "__main__":
    group_size_r = 4
    group_base_r = 2
    group_length_r = 11
    total_num_r = group_size_r * (group_base_r ** (group_length_r - 1))
    (ind_pos_r, pos_ind_r) = build_structure(group_size_r, group_base_r, group_length_r)

    parser = argparse.ArgumentParser(description="Set the defect_param")
    parser.add_argument('-d', '--defect_param', type=float, required=True, help='Set the defect parameter b')
    args = parser.parse_args()
    defect_param_r = args.defect_param

    abs_path = os.path.abspath(os.path.join(os.getcwd(), "../"))
    dir_name = abs_path + "/Results/Re_check_initial_fraction_of_cooperators/"
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    file_name = dir_name + "Re_Co_Rate_Gs_4_n_%s_Dp_%s.txt" %(total_num_r, defect_param_r)
    f = open(file_name, 'w')

    start_time = datetime.datetime.now()
    run_time = 200
    sample_time = 20
    rounds = 20
    results_r = []
    for co_frac in np.arange(0, 1.1, 0.1):
        print(co_frac)
        round_results_r = np.zeros(rounds)
        for round_index in range(rounds):
            print(round_index)
            ind_strategy_r = initialize_strategy(total_num_r, co_frac)
            for i in range(run_time):
                ind_strategy_r = run_game(ind_strategy_r, defect_param_r, group_size_r, group_base_r, group_length_r, total_num_r, ind_pos_r, pos_ind_r)
            sample_strategy = []
            for i in range(sample_time):
                ind_strategy_r = run_game(ind_strategy_r, defect_param_r, group_size_r, group_base_r, group_length_r, total_num_r, ind_pos_r, pos_ind_r)
                sample_strategy.append(np.mean(ind_strategy_r))
            round_results_r[round_index] = np.mean(sample_strategy)
        final_results = np.mean(round_results_r)
        results_r.append(final_results)
        f.write(str(co_frac) + '\t' + str(final_results) + '\n')
    f.close()
    end_time = datetime.datetime.now()
    print(results_r)
    print(end_time - start_time)


