from GridWorld import *
from Agent import *

def gridGameOne(action0, action1, currentState):
    action0 = action0
    action1 = action1
    curState = currentState
    reward0 = 0
    reward1 = 1
    endGameFlag = 0
    curIndex0 = curState[0]
    curIndex1 = curState[1]
    nextIndex0 = nextGridIndex(action0, curIndex0)
    nextIndex1 = nextGridIndex(action1, curIndex1)

    if (nextIndex0 == 8 and nextIndex1 == 6):
        reward0 = 100
        reward1 = 100
        nextState = (nextIndex0, nextIndex1)
        endGameFlag = 1
    elif (nextIndex0 == 8 and nextIndex1 != 6):
        reward0 = 100
        reward1 = -1
        nextState = (nextIndex0, nextIndex1)
        endGameFlag = 1
    elif (nextIndex0 != 8 and nextIndex1 == 6):
        reward0 = -1
        reward1 = 100
        nextState = (nextIndex0, nextIndex1)
        endGameFlag = 1
    elif (nextIndex0 != 8 and nextIndex1 != 6 and nextIndex0 == nextIndex1):
        reward0 = -10
        reward1 = -10
        nextState = (curIndex0, curIndex1)
        endGameFlag = 0
    else:
        reward0 = -1
        reward1 = -1
        nextState = (nextIndex0, nextIndex1)
        endGameFlag = 0
    return (reward0, reward1 ,nextState, endGameFlag)

def playGameOne(agent0 = agent, agent1 = agent, returnRewardsList = False):
    agent0 = agent0
    agent1 = agent1
    curState = (agent0.startLocIndex, agent1.startLocIndex)
    episodes = 0
    endGameFlag = 0
    agent0.initialSelfStrategy()
    agent1.initialSelfStrategy()
    agent0.initialActionValues()
    agent1.initialActionValues()
    agent0.initialDeltaStateAction()
    agent1.initialDeltaStateAction()
    agent0.initialDeltaStateActionTop()
    agent1.initialDeltaStateActionTop()

    if returnRewardsList:
        rewardSumList0 = []
        rewardSumList1 = []
    while episodes < 1000000:
        if returnRewardsList:
            (rewardSum0, rewardSum1) = evaluateStrategy(agent0, agent1)
            rewardSumList0.append(rewardSum0)
            rewardSumList1.append(rewardSum1)
        if episodes % 10000 ==0:
            print (episodes)
        while True:
            agent0Act = agent0.chooseAction(curState)
            agent1Act = agent1.chooseAction(curState)
            reward0, reward1, nextState, endGameFlag = gridGameOne(agent0Act, agent1Act, curState)
            agent0.updateActionValues(curState, nextState, reward0)
            agent1.updateActionValues(curState, nextState, reward1)
            agent0.updateStrategy(curState)
            agent1.updateStrategy(curState)

            if (endGameFlag == 1): # one episode of the game ends
                episodes += 1
                curState = resetStartState()
                agent0.updateTimeStep()
                agent1.updateTimeStep()
                agent0.updateEpsilon()
                agent1.updateEpsilon()
                agent0.updateAlpha()
                agent1.updateAlpha()
                break
            curState = nextState

    if returnRewardsList:
        return (rewardSumList0, rewardSumList1)

def test(agent0 = agent, agent1 = agent):
    agent0 = agent0
    agent1 = agent1
    startState = (0, 2)
    endGameFlag = 0
    runs = 0
    agentActList = []
    curState = startState
    while endGameFlag != 1:
        agent0Act = agent0.chooseActionWithFixedStrategy(curState)
        agent1Act = agent1.chooseActionWithFixedStrategy(curState)
        agentActList.append([agent0Act, agent1Act])
        reward0, reward1, nextState, endGameFlag = gridGameOne(agent0Act, agent1Act, curState)
        curState = nextState
    agentActList.append(curState)
    return agentActList, agent0.strategy, agent1.strategy

def runGame(agent0 = agent, agent1 = agent):
    agent0 = agent0
    agent1 = agent1
    playGameOne(agent0, agent1)
    runGameResult = test(agent0, agent1)
    return runGameResult

def runGameCalcReward(agent0 = agent, agent1 = agent):
    agent0 = agent0
    agent1 = agent1
    (rewardSumList0, rewardSumList1) = playGameOne(agent0, agent1, returnRewardsList=True)
    return (rewardSumList0, rewardSumList1)

def evaluateStrategy(agent0 = agent, agent1 = agent):
    agent0 = agent0
    agent1 = agent1
    startState = (0, 2) # The start state is fixed in (0,2) when evaluating the strategy.
    endGameFlag = 0
    runs = 0
    curState = startState
    rewardSum0 = 0
    rewardSum1 = 0
    while endGameFlag != 1 and runs < 100:
        runs += 1
        agent0Act = agent0.chooseActionWithFixedStrategy(curState)
        agent1Act = agent1.chooseActionWithFixedStrategy(curState)
        reward0, reward1, nextState, endGameFlag = gridGameOne(agent0Act, agent1Act, curState)
        rewardSum0 += reward0
        rewardSum1 += reward1
        curState = nextState
    return (rewardSum0, rewardSum1)



