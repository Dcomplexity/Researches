import sys
sys.path.append('..')

import multiprocessing
from experiments.pd_phc_vs_phc import *
from agents.agentPHC import *
from agents.agentParameters import *
from states_actions_envs.states_actions_envs import *

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

    myfile = open('../files/results/pd_phc_vs_phc.txt', 'w')
    for res in agentStrategyList:
        print (res.get()[-1])
        myfile.write(str(res.get()[-1]) + '\n')
    myfile.close()