import numpy as np

# pd_game_1 = [[2, 2], [10, 0], [0, 10], [3, 3]]
# pd_game_2 = [[1, 1], [10, 0], [0, 10], [4, 4]]
pd_game_1 = [[0.2, 0.2], [1, 0], [0, 1], [0.3, 0.3]]
pd_game_2 = [[0.1, 0.1], [1, 0], [0, 1], [0.4, 0.4]]
transition_matrix = [[0.1, 0.9, 0.9, 0.1], [0.1, 0.9, 0.9, 0.1]]


def play_pd_game_1(a_x, a_y):
    return pd_game_1[a_x * 2 + a_y]


def play_pd_game_2(a_x, a_y):
    return pd_game_2[a_x * 2 + a_y]


def transition_prob(s, s_, a_x, a_y):
    if s != s_:
        return transition_matrix[s][a_x * 2 + a_y]
    else:
        return 1-transition_matrix[s][a_x * 2 + a_y]


def next_state(s, a_x, a_y):
    prob = transition_matrix[s][a_x * 2 + a_y]
    # print(prob)
    if np.random.random() < prob:
        s_ = 1 - s
    else:
        s_ = s
    return s_


if __name__ == "__main__":
    for action_x in range(0, 2):
        for action_y in range(0, 2):
            reward_x, reward_y = play_pd_game_1(action_x, action_y)
            print(action_x, action_y, reward_x, reward_y)
    s_sum = 0
    for i in range(1000):
        s_sum += next_state(0, 1, 1)
    print(s_sum)
