from PlayGame import *
from Agent import *
import multiprocessing
import numpy as np


def writefile(filename, dataname):
    f = open(filename, 'w')
    for i in range(len(dataname)):
        f.write(str(dataname[i]))
        f.write('\n')


if __name__ == "__main__":
    rewardSumList00 = np.zeros(1000000)
    rewardSumList11 = np.zeros(1000000)

    for roundI in range(100):
        print ("Round: " + str(roundI))
        pool = multiprocessing.Pool(processes=10)
        rewardSumList0 = np.zeros(1000000)
        rewardSumList1 = np.zeros(1000000)
        rewardsResult = []
        agent0List = [agent(agentId=0, startLocIndex=0) for x in range(10)]
        agent1List = [agent(agentId=1, startLocIndex=2) for x in range(10)]

        for i in range(10):
            rewardsResult.append(pool.apply_async(runGameCalcReward, (agent0List[i], agent1List[i])))
        pool.close()
        pool.join()

        for res in rewardsResult:
            rewardSumList0 += np.array(res.get()[0])
            rewardSumList1 += np.array(res.get()[1])

        rewardSumList0 = rewardSumList0 / 10
        rewardSumList1 = rewardSumList1 / 10

        rewardSumList00 = roundI/(roundI+1)*rewardSumList00 + 1/(roundI+1)*rewardSumList0
        rewardSumList11 = roundI/(roundI+1)*rewardSumList11 + 1/(roundI+1)*rewardSumList1

    rewardSumList00 = list(rewardSumList00)
    rewardSumList11 = list(rewardSumList11)

    writefile("rewardSumList0.txt", rewardSumList00)
    writefile("rewardSumList1.txt", rewardSumList11)
