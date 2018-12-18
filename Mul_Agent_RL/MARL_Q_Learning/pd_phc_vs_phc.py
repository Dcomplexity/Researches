import multiprocessing
import os
import datetime


from agent import *
from game_env import *


def game_env_feedback(a_x, a_y):
    r_x, r_y = pd_game(a_x, a_y)
    s_ = (a_x, a_y)
    return r_x, r_y, s_


def play_one_game(agent_x=AgentPHC, agent_y=AgentPHC):
    actions = gen_actions()
    states = gen_states(actions)
    # s = np.random.randint(0, 2, (2, 1))
    ep = 0
    agent_x.initial_strategy()
    agent_x.initial_q_table()
    agent_x.initial_delta()
    agent_x.initial_delta_top()
    agent_y.initial_strategy()
    agent_y.initial_q_table()
    agent_y.initial_delta()
    agent_y.initial_delta_top()
    s_history = []
    whole_ep = 10e5
    random_ep = 20
    while ep < whole_ep:
        if ep % random_ep == 0:
            a_x = np.random.choice(actions)
            a_y = np.random.choice(actions)
            s = (a_x, a_y)
        s_history.append([agent_x.get_strategy().copy(), agent_y.get_strategy().copy()])
        a_x = agent_x.choose_action(s)
        a_y = agent_y.choose_action(s)
        r_x, r_y, s_ = game_env_feedback(a_x, a_y)
        agent_x.update_q_table(s, a_x, r_x, s_)
        agent_y.update_q_table(s, a_y, r_y, s_)
        agent_x.update_strategy(s)
        agent_y.update_strategy(s)
        ep += 1
        agent_x.set_alpha(ep)  # alpha (learning rate) change with time
        agent_y.set_alpha(ep)
        agent_x.set_epsilon(ep)  # epsilon (choose action randomly) change with time
        agent_y.set_epsilon(ep)
        s = s_
    return s_history


def run_game(agent_x=AgentPHC, agent_y=AgentPHC):
    run_game_result = play_one_game(agent_x, agent_y)
    return run_game_result


def run():
    gamma = 0.99
    delta = 0.001
    initial_alpha = alpha_time(0)
    initial_epsilon = epsilon_time(0)
    fixed_epsilon = 0.3
    agent_x_r = AgentPHC(alpha=initial_alpha, gamma=gamma, epsilon=initial_epsilon, delta=delta)
    agent_y_r = AgentPHC(alpha=initial_alpha, gamma=gamma, epsilon=initial_epsilon, delta=delta)

    pool = multiprocessing.Pool(processes=4)
    agent_strategy_list = []
    for _ in range(4):
        agent_strategy_list.append(pool.apply_async(run_game, (agent_x_r, agent_y_r)))
    pool.close()
    pool.join()

    return agent_strategy_list


def pandas_result(result):
    return (pd.DataFrame(result, index=['x', 'y'])).T


def write_res(f, result):
    abs_path = os.getcwd()
    dir_name = abs_path + '/files/results/'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    file_name = dir_name + f
    my_file = open(file_name, 'w')
    for res in result:
        my_file.write(str(pandas_result(res.get()[-1])) + '\n')
    my_file.close()


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(start_time)
    res_agent_strategy_list = run()
    run_end_time = datetime.datetime.now()
    print(run_end_time - start_time)
    for res_r in res_agent_strategy_list:
        print(pandas_result(res_r.get()[-1]))
    end_time = datetime.datetime.now()
    print(end_time)
    print(end_time-start_time)
    write_res("pd_phc_vs_phc.txt", res_agent_strategy_list)

