import numpy as np
import matplotlib.pyplot as plt


# In this work, we define 0 as cooperation and 1 as defection
def play_game(a_x, a_y, r, s, t, p):
    if a_x == 0 and a_y == 0:
        return r, r
    elif a_x == 0 and a_y == 1:
        return s, t
    elif a_x == 1 and a_y == 0:
        return t, s
    elif a_x == 1 and a_y == 1:
        return p, p
    else:
        return "Error"


def choose_action(s):
    if np.random.random() < s:
        return 0
    else:
        return 1

if __name__ == '__main__':
    s_p = [0.50, 0.99, 0.40, 0.01, 0.01]
    s_q = [0.25, 0.25, 0.25, 0.25, 0.25]
    r = 3
    s = 0
    t = 5
    p = 1
    a_p = 0
    a_q = 0
    delta_p = 0.0
    p_list = []
    for i in range(5000):
        if i == 0:
            a_p = choose_action(s_p[0])
            a_q = choose_action(s_q[0])
            payoff_p, payoff_q = play_game(a_p, a_q, r, s, t, p)
            delta_p = s_p[0]
            p_list.append([payoff_p, payoff_q])
        else:
            a_p_last = a_p
            a_q_last = a_q
            if a_q == 0:
                delta_p = delta_p * s_p[1] + (1 - delta_p) * s_p[3]
            else:
                delta_p = delta_p * s_p[2] + (1 - delta_p) * s_p[4]
            a_p = choose_action(delta_p)
            a_q = choose_action(s_q[a_q_last * 2 + a_p_last + 1])
            payoff_p, payoff_q = play_game(a_p, a_q, r, s, t, p)
            p_list.append([payoff_p, payoff_q])

p_list = np.array(p_list)
print(p_list.mean(axis=0))




