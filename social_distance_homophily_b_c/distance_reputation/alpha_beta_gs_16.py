import numpy as np
import random
import math
import argparse
import os
import datetime


class SocialStructure():
    def __init__(self, group_size, group_base, group_length, total_num):
        self.group_size = group_size
        self.group_base = group_base
        self.group_length = group_length
        self.total_num = total_num
        self.group_num = self.group_base ** (self.group_length - 1)

        if self.total_num != self.group_size * (self.group_base ** (self.group_length - 1)):
            print("Error: The total num of individuals does not correspond to the social structure")

    def build_social_structure(self):
        ind_pos = [0 for x in range(self.total_num)]
        pos_ind = [[] for x in range(self.group_num)]
        for i in range(self.group_num):
            for j in range(i*self.group_size, (i+1)*self.group_size):
                ind_pos[j] = i
                pos_ind[i].append(j)
        return np.array(ind_pos), np.array(pos_ind)


# T = b, R = b-c, P = 0, S = -c. Here, we define c = 1
def pd_game(strategy_x, strategy_y, b):
    if strategy_x == 1 and strategy_y == 1:
        return b-1, b-1
    elif strategy_x == 1 and strategy_y == 0:
        return -1, b
    elif strategy_x == 0 and strategy_y == 1:
        return b, -1
    elif strategy_x == 0 and strategy_y == 0:
        return 0, 0
    else:
        return "Error: The strategy do not fit the conditions."


def build_structure(struc_group_size, struc_group_base, struc_group_length):
    struc_total_num = struc_group_size * (struc_group_base ** (struc_group_length - 1))
    struc_social_structure = SocialStructure(struc_group_size, struc_group_base, struc_group_length, struc_total_num)
    struc_ind_pos, struc_pos_ind = struc_social_structure.build_social_structure()
    return struc_ind_pos, struc_pos_ind


def distance_prob(group_length, group_size, reg_param):
    distance_dist = np.zeros(group_length)
    if group_size == 1:
        for k in range(1, group_length):
            distance_dist[k] = math.e ** (reg_param * (k + 1))
    else:
        for k in range(group_length):
            distance_dist[k] = math.e ** (reg_param * (k + 1))
    distance_dist = distance_dist / np.sum(distance_dist)
    return np.array(distance_dist)


def get_position(group_length, now_position, distance_prob):
    potential_pos = []
    distance = np.random.choice(group_length, 1, p=distance_prob)[0] + 1
    if distance == 1:
        potential_pos.append(now_position)
    else:
        pos_temp = 2 ** (distance - 1)
        for k in range(0, pos_temp):
            potential_pos.append((now_position // pos_temp) * pos_temp + k)
    return distance, np.array(potential_pos)


def pick_individual(ind_self, positions, pos_ind):
    potential_ind = []
    for i in positions:
        for j in pos_ind[i]:
            potential_ind.append(j)
    # remove the individual itself from the potential opponents list
    potential_ind.remove(ind_self)
    ind_index = np.random.choice(potential_ind, 1)[0]
    return int(ind_index)


def initialize_strategy(total_num):
    ind_strategy = np.random.choice([0, 1], total_num, p=[0.5, 0.5])
    return ind_strategy


def build_rep(ind_strategy, pos_ind, group_base, group_length):
    position_num = group_base ** (group_length - 1)
    position_rep = [0 for x in range(position_num)]
    for i in range(position_num):
        co_num = 0 # co_num -> the number of cooperators in position i
        for j in pos_ind[i]:
            if ind_strategy[j] == 1:
                co_num += 1
        position_rep[i] = co_num / len(pos_ind[i])
    return position_rep


def run_game(step, ind_rep, ind_strategy, alpha, beta, play_num, defect_param, group_size, group_base, group_length, total_num,
             ind_pos, pos_ind, rt, rq):
    if total_num != len(ind_pos):
        print('Error, the sum of individuals does not correspond to total number of individuals')
    old_ind_strategy = np.zeros(total_num)
    for i in range(total_num):
        old_ind_strategy[i] = ind_strategy[i]
    opponent_play = np.zeros(total_num, dtype=int)
    opponent_learn = np.zeros(total_num, dtype=int)
    payoffs = np.zeros(total_num)
    prob_play = distance_prob(group_length, group_size, alpha)
    prob_learn = distance_prob(group_length, group_size, beta)
    opponent_distance = np.zeros(total_num)
    # generate the opponent to play the game
    for i in range(total_num):
        now_position = ind_pos[i]
        potential_distance, potential_pos = get_position(group_length, now_position, prob_play)
        opponent_distance[i] = potential_distance
        opponent_play[i] = pick_individual(i, potential_pos, pos_ind)
    # generate the opponent from whom learn
    for i in range(total_num):
        now_position = ind_pos[i]
        potential_distance, potential_pos = get_position(group_length, now_position, prob_learn)
        opponent_learn[i] = pick_individual(i, potential_pos, pos_ind)
    # every player plays the game with an opponent
    for i in range(total_num):
        player_index = i
        player_strategy = ind_strategy[player_index]
        opponent_index = opponent_play[i]
        opponent_strategy = ind_strategy[opponent_index]
        rep_fre = 1 / (1 + (opponent_distance[i] - 1) * rt * math.e ** -(ind_rep[player_index] * ind_rep[opponent_index] * rq))
        if np.random.random() < rep_fre or step == 0:
            payoffs_i, payoffs_j = pd_game(player_strategy, opponent_strategy, defect_param)
            payoffs[player_index] += payoffs_i
            payoffs[opponent_index] += payoffs_j
    # player updates his strategy
    for i in range(total_num):
        player_index = i
        w1 = 0.01
        w2 = random.random()
        if w1 > w2:
            if ind_strategy[player_index] == 1:
                ind_strategy[player_index] = 0
            else:
                ind_strategy[player_index] = 1
        else:
            opponent_index = opponent_learn[i]
            t1 = 1 / (1 + math.e ** (10 * (payoffs[player_index] - payoffs[opponent_index])))
            t2 = random.random()
            if t2 < t1:
                ind_strategy[player_index] = old_ind_strategy[opponent_index]
    group_rep = build_rep(old_ind_strategy, pos_ind, group_base, group_length)
    for i in range(total_num):
        ind_rep[i] = group_rep[ind_pos[i]]
    return ind_rep, ind_strategy


if __name__ == "__main__":
    group_size_r = 16
    group_base_r = 2
    group_length_r = 7
    total_num_r = group_size_r * (group_base_r ** (group_length_r - 1))
    ind_pos_r, pos_ind_r = build_structure(group_size_r, group_base_r, group_length_r)
    print(ind_pos_r)
    print(pos_ind_r)
    parser = argparse.ArgumentParser(description='Set the defect parameter b')
    parser.add_argument('-d', '--defect_param', type=float, required=True, help='Set the defector parameter b')
    parser.add_argument('-t', '--rt', type=float, required=True, help='Set the rt parameter for the use of reputation')
    parser.add_argument('-q', '--rq', type=float, required=True, help='Set the rq parameter for the use of reputation')
    args = parser.parse_args()
    defect_param_r = args.defect_param
    rt_r = args.rt
    rq_r = args.rq
    play_num_r = 1
    abs_path = os.path.abspath(os.path.join(os.getcwd(), '../'))
    dir_name = abs_path + '/results/re_distance_reputation/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    file_name = dir_name + 'frac_co_distance_reputation_gs_%s_d_%s.txt' % (group_size_r, defect_param_r)
    f = open(file_name, 'w')

    start_time = datetime.datetime.now()
    run_time = 50
    sample_time = 10
    rounds = 5
    results_r = []
    for alpha_r in range(-2, 3):
        for beta_r in range(-2, 3):
            print(alpha_r, beta_r)
            round_results_r = np.zeros(rounds)
            for round_index in range(rounds):
                ind_strategy_r = initialize_strategy(total_num_r)
                ind_rep_r = np.zeros(total_num_r)
                for step_i in range(run_time):
                    ind_rep_r, ind_strategy_r = run_game(step_i, ind_rep_r, ind_strategy_r, alpha_r, beta_r, play_num_r, defect_param_r, group_size_r,
                                              group_base_r, group_length_r, total_num_r, ind_pos_r, pos_ind_r, rt_r, rq_r)
                sample_strategy = []
                for step_i in range(sample_time):
                    ind_rep_r, ind_strategy_r = run_game(run_time+step_i, ind_rep_r, ind_strategy_r, alpha_r, beta_r, play_num_r, defect_param_r, group_size_r,
                                              group_base_r, group_length_r, total_num_r, ind_pos_r, pos_ind_r, rt_r, rq_r)
                    sample_strategy.append(np.mean(ind_strategy_r))
                round_results_r[round_index] = np.mean(sample_strategy)
            final_results = np.mean(round_results_r)
            results_r.append(final_results)
            f.write(str(alpha_r) + '\t' + str(beta_r) + '\t' + str(final_results) + '\n')
    f.close()
    end_time = datetime.datetime.now()
    print(results_r)
    print(end_time - start_time)

