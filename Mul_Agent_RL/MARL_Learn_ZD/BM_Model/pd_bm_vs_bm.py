import multiprocessing
import random
import pandas as pd
import os
import datetime


from BM_Model.agent import *
from BM_Model.game_env import *


def play_one_game(agent_x: AgentBM, agent_y: AgentBM):
    ep = 0
    st_history = []
    whole_ep = 10e4
    while ep < whole_ep:
        a_x = agent_x.choose_actions()
        a_y = agent_y.choose_actions()
        pf_x, pf_y = pd_game(a_x, a_y)
        agent_x.set_stimulus(pf_x)
        agent_y.set_stimulus(pf_y)
        agent_x.update_strategy()
        agent_y.update_strategy()
        print(ep, agent_x.get_strategy(), agent_y.get_strategy())
        st_history.append((agent_x.get_strategy(), agent_y.get_strategy()))
        ep += 1
    return st_history


def run_game(agent_x: AgentBM, agent_y: AgentBM):
    run_game_result = play_one_game(agent_x, agent_y)
    return run_game_result


def run():
    agent_x_r = AgentBM(lr=0.001, expc_a=1.3, init_st=0.5)
    agent_y_r = AgentBM(lr=0.001, expc_a=3.0, init_st=0.5)
    strategy_history = run_game(agent_x_r, agent_y_r)
    return strategy_history
    # pool = multiprocessing.Pool(processes=4)
    # agent_strategy_list = []
    # for _ in range(4):
    #     agent_strategy_list.append(pool.apply_async(run_game, (agent_x_r, agent_y_r)))
    # pool.close()
    # pool.join()


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(start_time)
    res_agent_strategy_list = run()
    end_time = datetime.datetime.now()
    print(end_time - start_time)
