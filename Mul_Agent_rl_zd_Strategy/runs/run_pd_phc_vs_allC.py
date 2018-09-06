import sys
sys.path.append('..')

import multiprocessing
from experiments.pd_phc_vs_fixed import *
from agents.agentFixedStrategy import *
from agents.agentPHC import *
from agents.agentParameters import *
from states_actions_envs.states_actions_envs import *

if __name__ == "__main__":
    gammaValue = 0.99
    deltaValue = 0.0001
    agentX = agentPHC(alpha=alpha, gamma=gammaValue, delta=deltaValue, epsilon=epsilon)
    agentY = agentFixedStrategy(alpha=alpha, gamma=gammaValue, delta=deltaValue, epsilon=epsilon, fixedStrategy=[1.0, 1.0, 1.0, 1.0])

    pool = multiprocessing.Pool(processes=4)
    agentStrategyList = []
    for _ in range(4):
        agentStrategyList.append(pool.apply_async(rungame, (agentX, agentY)))
    pool.close()
    pool.join()

    myfile = open('../files/results/phc_vs_allC.txt', 'w')
    for res in agentStrategyList:
        print (res.get()[-1])
        myfile.write(str(res.get()[-1]) + '\n')
    myfile.close()