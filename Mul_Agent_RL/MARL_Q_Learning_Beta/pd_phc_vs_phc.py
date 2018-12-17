import sys
import multiprocessing
import pandas as pd


from agent import *
from game_env import *

actions = gen_actions()
states = gen_states(actions)


def one_game(action_x, action_y):
    action_x = action_x
    action_y = action_y
    [reward_x, reward_y] = pd_game(action_x, action_y)
    next_state = (action_x, action_y)
    return reward_x, reward_y, next_state


def play_one_game(agent_x=AgentPHC, agent_y=AgentPHC):
    agent_x = agent_x
    agent_y = agent_y
    action_x = np.random.choice(actions)
    action_y = np.random.choice(actions)
    current_state = (action_x, action_y)
    episodes = 0

    agent_x.initial_strategy()
    agent_x.initial_q_table()
    agent_x.initial_delta()
    agent_x.initial_delta_top()
    agent_y.initial_strategy()
    agent_y.initial_q_table()
    agent_y.initial_delta()
    agent_y.initial_delta_top()

    strategy_history = []

    whole_episode = 10e3
    random_episode = 20

    while episodes < whole_episode:
        if episodes % random_episode == 0:
            action_x = np.random.choice(actions)
            action_y = np.random.choice(actions)
            current_state = (action_x, action_y)

        strategy_history.append([np.copy(agent_x.get_strategy()), np.copy(agent_y.get_strategy())])

        agent_x.set_current_state(current_state)
        agent_y.set_current_state(current_state)
        agent_x.choose_action()
        agent_y.choose_action()
        agent_x_action = agent_x.get_action()
        agent_y_action = agent_y.get_action()
        reward_x, reward_y, next_state = one_game(agent_x_action, agent_y_action)

        agent_x.set_reward(reward_x)
        agent_y.set_reward(reward_y) # notice the reward here, if the reward is set a reward_x, then the results will be that agent Y will choose cooperation all the time.
        agent_x.set_next_state(next_state)
        agent_y.set_next_state(next_state)
        agent_x.update_q_table()
        agent_y.update_q_table()
        agent_x.update_strategy()
        agent_y.update_strategy()
        agent_x.update_time_step()
        agent_y.update_time_step()
        agent_x.update_epsilon()
        agent_y.update_epsilon()
        agent_x.update_alpha()
        agent_y.update_alpha()

        episodes += 1
        current_state = next_state

    return strategy_history


def rungame(agent_x=AgentPHC, agent_y=AgentPHC):
    agent_x = agent_x
    agent_y = agent_y
    run_game_result = play_one_game(agent_x, agent_y)
    return run_game_result

def pandas_result(result):
    return pd.DataFrame(result, index=['x', 'y']).T

if __name__ == "__main__":
    gamma_v = 0.99
    delta_v = 0.0001
    agent_x = AgentPHC(gamma=gamma_v, delta=delta_v)
    agent_y = AgentPHC(gamma=gamma_v, delta=delta_v)

    pool = multiprocessing.Pool(processes=4)
    agentStrategyList = []
    for _ in range(4):
        agentStrategyList.append(pool.apply_async(rungame, (agent_x, agent_y)))
    pool.close()
    pool.join()

    #myfile = open('../files/results/pd_phc_vs_phc.txt', 'w')
    for res in agentStrategyList:
        print (pandas_result(res.get()[-1]))
        #myfile.write(str(res.get()[-1]) + '\n')
    #myfile.close()
