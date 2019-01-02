import numpy as np


def pd_game_0(a_x, a_y):
    if (a_x, a_y) == (1, 1):
        return 3, 3
    elif (a_x, a_y) == (1, 0):
        return 0, 10
    elif (a_x, a_y) == (0, 1):
        return 10, 0
    elif (a_x, a_y) == (0, 0):
        return 2, 2
    else:
        return "ERROR"


def pd_game_1(a_x, a_y):
    if (a_x, a_y) == (1, 1):
        return 4, 4
    elif (a_x, a_y) == (1, 0):
        return 0, 10
    elif (a_x, a_y) == (0, 1):
        return 10, 0
    elif (a_x, a_y) == (0, 0):
        return 1, 1
    else:
        return "ERROR"


# Transition Matrix:
# s0->s1 |0.1 0.9| s1->s0 |0.1 0.9|
#        |0.9 0.1|        |0.9 0.1|
def transition_matrix(s, a_x, a_y):
    t_m = [0.1, 0.9, 0.9, 0.1, 0.1, 0.9, 0.9, 0.1]
    return t_m[s*(2**2) + a_x*2 + a_y]


def next_state(s, a_x, a_y):
    prob = transition_matrix(s, a_x, a_y)
    # print(prob)
    if np.random.random() < prob:
        s_ = 1 - s
    else:
        s_ = s
    return s_


if __name__ == "__main__":
    s_sum = 0
    for i in range(1000):
        p_s = next_state(1, 1, 1)
        s_sum += p_s
    print(s_sum)
