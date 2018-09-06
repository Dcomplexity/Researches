from PlayGameImitate import *
from Agent import *
from BuildNetwork import *

import multiprocessing
import numpy as np

def writefile(filename, dataname):
    f = open(filename, 'w')
    for i in range(len(dataname)):
        f.write(str(dataname[i]))
        f.write('\n')

if __name__ == "__main__":
    rewardSumList00 = np.zeros(40000)
    rewardSumList11 = np.zeros(40000)

    for roundI in range(10):
        print ("Round: " + str(roundI))
        rewardSumList0 = np.zeros(40000)
        rewardSumList1 = np.zeros(40000)
        popNum = 25
        network = buildNetwork(popNum).completegraph()
        agentList = {0: [agent(agentId=0, agentIndex=x, startLocIndex=0) for x in range(popNum)],
                     1: [agent(agentId=1, agentIndex=x, startLocIndex=2) for x in range(popNum)]}

        for i in range(popNum):
            agentList[0][i].neighbors = network[i]
            agentList[1][i].neighbors = network[i]
        multiprocessNum = 10
        pool = multiprocessing.Pool(processes=multiprocessNum)
        rewardResult = []
        for i in range(multiprocessNum):
            rewardResult.append(pool.apply_async(runGameCalcReward, (agentList, popNum)))
        pool.close()
        pool.join()

        for res in rewardResult: # 0 for action and state, 1 for agent0 strategy, 2 for agent1 strategy.
            rewardSumList0 += np.array(res.get()[0])
            rewardSumList1 += np.array(res.get()[1])

        rewardSumList0 = rewardSumList0 / multiprocessNum
        rewardSumList1 = rewardSumList1 / multiprocessNum

        rewardSumList00 = roundI/(roundI+1)*rewardSumList00 + 1/(roundI+1)*rewardSumList0
        rewardSumList11 = roundI/(roundI+1)*rewardSumList11 + 1/(roundI+1)*rewardSumList1

    rewardSumList00 = list(rewardSumList00)
    rewardSumList11 = list(rewardSumList11)

    writefile('rewardSumList0.txt', rewardSumList00)
    writefile('rewardSumList1.txt', rewardSumList11)