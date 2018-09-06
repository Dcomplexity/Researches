import numpy as np
import random
import copy

from agents.agentPHC import *
from agents.agentParameters import *
from states_actions_envs.states_actions_envs import *

actions = generateDCActions()
states = generateDCStates(actions)

def oneGame(actionX, actionY):
    actionX = actionX
    actionY = actionY
    rewardX = 0
    rewardY = 0
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

        strategy_history.append((np.copy(agentX.getStrategy()), np.copy(agentY.getStrategy())))

        agentX.setCurrentState(currentState)
        agentY.setCurrentState(currentState)
        agentX.chooseSmartAction()
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
