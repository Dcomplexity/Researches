import sys
sys.path.append('..')
import multiprocessing
import pandas as pd

from agent import *


actions = generateDCActions()
states = generateDCStates(actions)

def oneGame(actionX, actionY):
    actionX = actionX
    actionY = actionY
    [rewardX, rewardY] = PDGame(actionX, actionY)
    nextState = (actionX, actionY)
    return rewardX, rewardY, nextState

def playOneGame(agentX=agentPHC, agentY=agentPHC):
    agentX = agentX
    agentY = agentY
    actionX = np.random.choice(actions)
    actionY = np.random.choice(actions)
    currentState = (actionX, actionY)
    episodes = 0

    agentX.initialSelfStrategy()
    agentX.initialActionValues()
    agentX.initialDeltaStateAction()
    agentX.initialDeltaStateActionTop()
    agentY.initialSelfStrategy()
    agentY.initialActionValues()
    agentY.initialDeltaStateAction()
    agentY.initialDeltaStateActionTop()

    strategy_history = []

    wholeEpisode = 10e5
    randomEpisode = 20

    while episodes < wholeEpisode:
        if episodes % randomEpisode == 0:
            actionX = np.random.choice(actions)
            actionY = np.random.choice(actions)
            currentState = (actionX, actionY)

        strategy_history.append([np.copy(agentX.getStrategy()), np.copy(agentY.getStrategy())])

        agentX.setCurrentState(currentState)
        agentY.setCurrentState(currentState)
        agentX.chooseAction()
        agentY.chooseAction()
        agentXAction = agentX.getAction()
        agentYAction = agentY.getAction()
        rewardX, rewardY, nextState = oneGame(agentXAction, agentYAction)

        agentX.setRewards(rewardX)
        agentY.setRewards(rewardY) # notice the reward here, if the reward is set a rewardX, then the results will be that agent Y will choose cooperation all the time.
        agentX.setNextState(nextState)
        agentY.setNextState(nextState)
        agentX.updateActionValues()
        agentY.updateActionValues()
        agentX.updateStrategy()
        agentY.updateStrategy()
        agentX.updateTimeStep()
        agentY.updateTimeStep()
        agentX.updateEpsilon()
        agentY.updateEpsilon()
        agentX.updateAlpha()
        agentY.updateAlpha()

        episodes += 1
        currentState = nextState

    return strategy_history

def calAgentPayoffs(agentX=agentPHC, agentY=agentPHC):
    agentX = agentX
    agentY = agentY
    actionX = np.random.choice(actions)
    actionY = np.random.choice(actions)
    currentState = (actionX, actionY)
    episodes = 0
    rewardXSum = 0
    rewardYSum = 0

    payoffWholeEpisodes = 10e5
    while episodes < payoffWholeEpisodes:
        agentX.setCurrentState(currentState)
        agentY.setCurrentState(currentState)
        agentX.chooseAction()
        agentXAction = agentX.getAction()
        agentY.chooseAction()
        agentYAction = agentY.getAction()
        rewardX, rewardY, nextState = oneGame(agentXAction,agentYAction)
        initialEpisodes = 0
        rewardXSum += rewardX
        rewardYSum += rewardY
        currentState = nextState
        episodes += 1

    return rewardXSum/(episodes-initialEpisodes), rewardYSum/(episodes-initialEpisodes)

def rungame(agentX=agentPHC, agentY=agentPHC):
    agentX = agentX
    agentY = agentY
    runGameResult = playOneGame(agentX, agentY)
    return runGameResult


def pandas_result(result):
    return pd.DataFrame(result, index=['x', 'y']).T


if __name__ == "__main__":
    gammaValue = 0.99
    deltaValue = 0.0001
    agentX = agentPHC(alpha=alpha, gamma=gammaValue, delta=deltaValue, epsilon=epsilon)
    agentY = agentPHC(alpha=alpha, gamma=gammaValue, delta=deltaValue, epsilon=epsilon)

    pool = multiprocessing.Pool(processes=4)
    agentStrategyList = []
    for _ in range(4):
        agentStrategyList.append(pool.apply_async(rungame, (agentX, agentY)))
    pool.close()
    pool.join()

    #myfile = open('../files/results/pd_phc_vs_phc.txt', 'w')
    for res in agentStrategyList:
        print(pandas_result(res.get()[-1]))
        #myfile.write(str(res.get()[-1]) + '\n')
    #myfile.close()