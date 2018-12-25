from GridWorld import *
from Agent import *

def gridGameOne(action0, action1, currentState):
    action0 = action0
    action1 = action1
    curState = currentState
    reward0 = 0
    reward1 = 0
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
    return (reward0, reward1, nextState, endGameFlag)

def playGameInitial(agentList, agentIndex):
    agent0 = agentList[0][agentIndex]
    agent1 = agentList[1][agentIndex]
    agent0.initialSelfStrategy()
    agent1.initialSelfStrategy()
    agent0.initialActionValues()
    agent1.initialActionValues()
    agent0.initialDeltaStateAction()
    agent1.initialDeltaStateAction()
    agent0.initialDeltaStateActionTop()
    agent1.initialDeltaStateActionTop()

def playGameRL(agentList, agentIndex):
    agent0 = agentList[0][agentIndex]
    agent1 = agentList[1][agentIndex]
    curState = (agent0.startLocIndex, agent1.startLocIndex)
    endGameFlag = 0

    while True:
        agent0Act = agent0.chooseAction(curState)
        agent1Act = agent1.chooseAction(curState)
        reward0, reward1, nextState, endGameFlag = gridGameOne(agent0Act, agent1Act, curState)
        agent0.updateActionValues(curState, nextState, reward0)
        agent1.updateActionValues(curState, nextState, reward1)
        agent0.updateStrategy(curState)
        agent1.updateStrategy(curState)

        if (endGameFlag == 1):
            curState = resetStartState()
            agent0.updateTimeStep()
            agent1.updateTimeStep()
            agent0.updateEpsilon()
            agent1.updateEpsilon()
            agent0.updateAlpha()
            agent1.updateAlpha()
            break
        curState = nextState

    (rewardSum0, rewardSum1) = evaluateStrategy(agent0, agent1)
    agent0.evalRewards = rewardSum0
    agent1.evalRewards = rewardSum1
    agent0.backupStrategy()
    agent1.backupStrategy()

def imitateProcess(agentLearn = agent, otherAgent = agent, beta = 0):
    pi1 = agentLearn.evalRewards
    pi2 = otherAgent.evalRewards
    alpha = 1 / (1 + np.exp(-beta * (pi1 - pi2)))
    if random.random() < alpha:
        agentLearn.imitateStrategy(otherAgent.ostrategy)

def imitateOtherStrategy(agentList, agentIndex):
    agent0 = agentList[0][agentIndex]
    agent1 = agentList[1][agentIndex]
    otherAgent0Index = random.choice(agent0.neighbors)
    otherAgent0 = agentList[0][otherAgent0Index]
    otherAgent1Index = random.choice(agent1.neighbors)
    otherAgent1 = agentList[1][otherAgent1Index]
    imitateProcess(agent0, otherAgent0)
    imitateProcess(agent1, otherAgent1)

def playGameOne(agentList, popNum, returnRewardsList = False):
    for i in range(popNum):
        playGameInitial(agentList, i)

    if returnRewardsList:
        rewardSumList0 = []
        rewardSumList1 = []

    steps = 0
    while steps < 40000:
        if steps % 100 == 0:
            print (steps)
        if returnRewardsList:
            rewardSumList00 = []
            rewardSumList11 = []
            for i in range(popNum):
                (rewardSum0, rewardSum1) = evaluateStrategy(agentList[0][i], agentList[1][i])
                rewardSumList00.append(rewardSum0)
                rewardSumList11.append(rewardSum1)
            # rewardSumList is a list of agents in population in one step
            rewardSumList0.append(np.sum(rewardSumList00)/len(rewardSumList00))
            rewardSumList1.append(np.sum(rewardSumList11)/len(rewardSumList11))

        for i in range(popNum):
            playGameRL(agentList, i)

        if steps % 100 == 0:
            for i in range(popNum):
                imitateOtherStrategy(agentList, i)

        steps = steps + 1

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


# Return the rewardSum of two agent based on their strategies in one round
def evaluateStrategy(agent0 = agent, agent1 = agent):
    agent0 = agent0
    agent1 = agent1
    startState = (0, 2)
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


def runGame(agentList, popNum):
    playGameOne(agentList, popNum)
    # choose a member from the population randomly to test
    randomIndex = random.choice(range(popNum)) # choose one agent randomly to test the performance
    agent0 = agentList[0][randomIndex]
    agent1 = agentList[1][randomIndex]
    runGameResult = test(agent0, agent1)
    return runGameResult

def runGameCalcReward(agentList, popNum):
    (rewardSumList0, rewardSumList1) = playGameOne(agentList, popNum, returnRewardsList=True)
    return (rewardSumList0, rewardSumList1)