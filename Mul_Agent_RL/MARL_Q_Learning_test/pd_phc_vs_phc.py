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
    agent_x = agent_x
    agent_y = agent_y
    # s = np.random.randint(0, 2, (2, 1))
    actions = gen_actions()
    states = gen_states(actions)
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
            action_x = np.random.choice(actions)
            action_y = np.random.choice(actions)
            cur_state = (action_x, action_y)
        s_history.append([agent_x.get_strategy().copy(), agent_y.get_strategy().copy()])
        # a_x = agent_x.choose_action(s)
        # a_y = agent_y.choose_action(s)
        agent_x.set_cur_state(cur_state)
        agent_y.set_cur_state(cur_state)
        agent_x.choose_action()
        agent_y.choose_action()
        action_x = agent_x.get_action()
        action_y = agent_y.get_action()
        reward_x, reward_y, next_state = game_env_feedback(action_x, action_y)
        agent_x.set_reward(reward_x)
        agent_y.set_reward(reward_y)
        agent_x.set_next_state(next_state)
        agent_y.set_next_state(next_state)
        agent_x.update_q_table()
        agent_y.update_q_table()
        agent_x.update_strategy()
        agent_y.update_strategy()
        agent_x.update_time_step()
        agent_y.update_time_step()
        agent_x.update_epsilon()  # epsilon (choose action randomly) change with time
        agent_y.update_epsilon()
        agent_x.update_alpha()  # alpha (learning rate) change with time
        agent_y.update_alpha()

        ep += 1
        cur_state = next_state

    return s_history


def run_game(agent_x=AgentPHC, agent_y=AgentPHC):
    agent_x = agent_x
    agent_y = agent_y
    run_game_result = play_one_game(agent_x, agent_y)
    return run_game_result


def run():
    gamma = 0.99
    delta = 0.0001
    agent_x_r = AgentPHC(gamma=gamma, delta=delta)
    agent_y_r = AgentPHC(gamma=gamma, delta=delta)

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

