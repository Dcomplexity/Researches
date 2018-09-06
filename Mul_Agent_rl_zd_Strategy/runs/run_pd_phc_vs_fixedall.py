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
    # here I change the policy in dc states from 7.0/26.0 to 6.0/26.0.
    myfile = open('../files/results/phc_vs_fixedall.txt', 'w')
    for i_0 in np.arange(0, 1.1, 0.2):
        for i_1 in np.arange(0, 1.1, 0.2):
            for i_2 in np.arange(0, 1.1, 0.2):
                for i_3 in np.arange(0, 1.1, 0.2):
                    print (i_0, i_1, i_2, i_3)
                    myfile.write(str(i_0) + ", " + str(i_1) + ', ' + str(i_2) + ', ' + str(i_3) + '\n')
                    agentY = agentFixedStrategy(alpha=alpha, gamma=gammaValue, delta=deltaValue, epsilon=epsilon, fixedStrategy=[i_0, i_1, i_2, i_3])

                    pool = multiprocessing.Pool(processes=4)
                    agentStrategyList = []
                    for _ in range(4):
                        agentStrategyList.append(pool.apply_async(rungame, (agentX, agentY)))
                    pool.close()
                    pool.join()


                    for res in agentStrategyList:
                        print (res.get()[-1])
                        myfile.write(str(res.get()[-1]) + '\n')

    myfile.close()
