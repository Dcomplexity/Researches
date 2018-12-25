from PlayGameImitate import *
from Agent import *
from BuildNetwork import *

import multiprocessing
import numpy as np

if __name__ == "__main__":
    popNum = 25
    network = buildNetwork(popNum).BAnetwork(edgesNum=2)
    agentList = {0: [agent(agentId=0, agentIndex=x, startLocIndex=0) for x in range(popNum)],
                 1: [agent(agentId=1, agentIndex=x, startLocIndex=2) for x in range(popNum)]}

    for i in range(popNum):
        agentList[0][i].neighbors = network[i]
        agentList[1][i].neighbors = network[i]

    pool = multiprocessing.Pool(processes=4)
    agentActList = []
    for i in range(4):
        agentActList.append(pool.apply_async(runGame, (agentList, popNum)))
    pool.close()
    pool.join()

    for res in agentActList: # 0 for action and state, 1 for agent0 strategy, 2 for agent1 strategy
        print (res.get()[0])