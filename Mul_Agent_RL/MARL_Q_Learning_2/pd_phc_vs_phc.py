import sys
sys.path.append('..')
import multiprocessing
import pandas as pd

from agent import *


actions = gen_actions()
states = gen_states(actions)

def oneGame(actionX, actionY):
    actionX = actionX
    actionY = actionY
    [rewardX, rewardY] = pd_game(actionX, actionY)
    nextState = (actionX, actionY)
    return rewardX, rewardY, nextState

def playOneGame(agentX=AgentPHC, agentY=AgentPHC):
    agentX = agentX
    agentY = agentY
    actionX = np.random.choice(actions)
    actionY = np.random.choice(actions)
    currentState = (actionX, actionY)
    episodes = 0

    agentX.initial_strategy()
    agentX.initial_q_table()
    agentX.initial_delta()
    agentX.initial_delta_top()
    agentY.initial_strategy()
    agentY.initial_q_table()
    agentY.initial_delta()
    agentY.initial_delta_top()

    strategy_history = []

    wholeEpisode = 10e5
    randomEpisode = 20

    while episodes < wholeEpisode:
        if episodes % randomEpisode == 0:
            actionX = np.random.choice(actions)
            actionY = np.random.choice(actions)
            currentState = (actionX, actionY)

        strategy_history.append([np.copy(agentX.get_strategy()), np.copy(agentY.get_strategy())])

        agentX.set_cur_state(currentState)
        agentY.set_cur_state(currentState)
        agentX.choose_action()
        agentY.choose_action()
        agentXAction = agentX.get_action()
        agentYAction = agentY.get_action()
        rewardX, rewardY, nextState = oneGame(agentXAction, agentYAction)

        agentX.set_reward(rewardX)
        agentY.set_reward(rewardY) # notice the reward here, if the reward is set a rewardX, then the results will be that agent Y will choose cooperation all the time.
        agentX.set_next_state(nextState)
        agentY.set_next_state(nextState)
        agentX.update_q_table()
        agentY.update_q_table()
        agentX.update_strategy()
        agentY.update_strategy()
        agentX.update_time_step()
        agentY.update_time_step()
        agentX.update_epsilon()
        agentY.update_epsilon()
        agentX.update_alpha()
        agentY.update_alpha()

        episodes += 1
        currentState = nextState

    return strategy_history

# def calAgentPayoffs(agentX=agentPHC, agentY=agentPHC):
#     agentX = agentX
#     agentY = agentY
#     actionX = np.random.choice(actions)
#     actionY = np.random.choice(actions)
#     currentState = (actionX, actionY)
#     episodes = 0
#     rewardXSum = 0
#     rewardYSum = 0
#
#     payoffWholeEpisodes = 10e5
#     while episodes < payoffWholeEpisodes:
#         agentX.set_current_state(currentState)
#         agentY.set_current_state(currentState)
#         agentX.chooseAction()
#         agentXAction = agentX.getAction()
#         agentY.chooseAction()
#         agentYAction = agentY.getAction()
#         rewardX, rewardY, nextState = oneGame(agentXAction,agentYAction)
#         initialEpisodes = 0
#         rewardXSum += rewardX
#         rewardYSum += rewardY
#         currentState = nextState
#         episodes += 1
#
#     return rewardXSum/(episodes-initialEpisodes), rewardYSum/(episodes-initialEpisodes)

def rungame(agentX=AgentPHC, agentY=AgentPHC):
    agentX = agentX
    agentY = agentY
    runGameResult = playOneGame(agentX, agentY)
    return runGameResult


def pandas_result(result):
    return pd.DataFrame(result, index=['x', 'y']).T


if __name__ == "__main__":
    gammaValue = 0.99
    deltaValue = 0.0001
    agentX = AgentPHC(gamma=gammaValue, delta=deltaValue)
    agentY = AgentPHC(gamma=gammaValue, delta=deltaValue)

    pool = multiprocessing.Pool(processes=4)
    agentStrategyList = []
    for _ in range(4):
        agentStrategyList.append(pool.apply_async(rungame, (agentX, agentY)))
    pool.close()
    pool.join()

    #myfile = open('../files/results/pd_phc_vs_phc.txt', 'w')
    for res in agentStrategyList:
        print(res.get()[-1])
        #myfile.write(str(res.get()[-1]) + '\n')
    #myfile.close()