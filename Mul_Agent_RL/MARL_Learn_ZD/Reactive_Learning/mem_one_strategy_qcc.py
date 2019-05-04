import numpy as np
import matplotlib.pyplot as plt

def mem_one_strategpy(p, q, step_size):
    tm = [[p[0] * q[0], p[0] * (1 - q[0]), (1 - p[0]) * q[0], (1 - p[0]) * (1 - q[0])],
          [p[1] * q[2], p[1] * (1 - q[2]), (1 - p[1]) * q[2], (1 - p[1]) * (1 - q[2])],
          [p[2] * q[1], p[2] * (1 - q[1]), (1 - p[2]) * q[1], (1 - p[2]) * (1 - q[1])],
          [p[3] * q[3], p[3] * (1 - q[3]), (1 - p[3]) * q[3], (1 - p[3]) * (1 - q[3])]]
    v = [0.25, 0.25, 0.25, 0.25]  # The steady state does not realize on the init state
    steady_state = np.dot(v, np.linalg.matrix_power(tm, step_size))
    return steady_state


def cal_payoff(p_state, p_set):
    return np.sum(p_state * p_set)


if __name__ == '__main__':
    # # p_strategy = [0.7881, 0.8888, 0.4686, 0.0792]
    # p_strategy = [11.0 / 13.0, 1.0 / 2.0, 7.0 / 26.0, 0.0]
    # # q_strategy = [0.5, 0.5, 0.5, 0.5]
    # q_strategy = [1.0, 1.0, 1.0, 1.0]
    # steady_state = mem_one_strategpy(p_strategy, q_strategy, 50)
    # p_payoff_set = np.array([3, 0, 5, 1])
    # q_payoff_set = np.array([3, 5, 0, 1])
    # p_payoff = cal_payoff(steady_state, p_payoff_set)
    # q_payoff = cal_payoff(steady_state, q_payoff_set)
    payoff_pair = []
    time = 0
    p_payoff_set = np.array([3, 0, 5, 1])
    q_payoff_set = np.array([3, 5, 0, 1])
    # p_strategy = [11.0 / 13.0, 1.0 / 2.0, 7.0 / 26.0, 0.0]
    p_strategy = [0.7881, 0.8888, 0.4686, 0.0792]
    for i_0 in np.arange(0.0, 1.01, 0.01):
        print(time)
        time += 1
        q_strategy = [i_0, 0.9963, 0.0166, 0.9879]
        steady_state = mem_one_strategpy(p_strategy, q_strategy, 50)
        p_payoff = cal_payoff(steady_state, p_payoff_set)
        q_payoff = cal_payoff(steady_state, q_payoff_set)
        payoff_pair.append([p_payoff, q_payoff])
    payoff_pair = np.array(payoff_pair)
    plt.xlim(left=0, right=5)
    plt.ylim(bottom=0, top=5)
    # s = [2*n for n in range(len(payoff_pair))]
    plt.scatter(payoff_pair[:, 1], payoff_pair[:, 0], s=2.0, c='black')
    plt.savefig("./images/mem_one_strategy_qcc.png")
    plt.show()
