import sys
sys.path.append('..')

import pandas as pd
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
    agentY = agentFixedStrategy(alpha=alpha, gamma=gammaValue, delta=deltaValue, epsilon=epsilon, fixedStrategy=[11.0/13.0, 0.5, 7.0/26.0, 0.0])

    pool = multiprocessing.Pool(processes=4)
    agentStrategyList = []
    for _ in range(4):
        agentStrategyList.append(pool.apply_async(rungame, (agentX, agentY)))
    pool.close()
    pool.join()

    myfile = open('../files/results/phc_vs_artificial.txt', 'w')
    myFileStrHistory = open('../files/results/strHistory_phc_vs_artificial.txt', 'w')
    loopTime = 0
    strHistory = []
    for res in agentStrategyList:
        # print (loopTime)
        # if loopTime == 0:
        #     strHistory = res.get()[:]
        # else:
        #     for iTime in range(len(res.get()[:])):
        #         print (iTime)
        #         for itemKey in strHistory[iTime].keys():
        #             for i in range(len(strHistory[iTime][itemKey])):
        #                 strHistory[iTime][itemKey][i] += res.get()[:][iTime][itemKey][i]
        # loopTime += 1
        #strHistory.append(pd.DataFrame(data=res.get()[:]))
        # print (res.get()[-1])
        strHistory = res.get()[:]
        myfile.write(str(res.get()[-1]) + '\n')
    myfile.close()

    # for iTime in range(len(strHistory)):
    #     for itemKey in strHistory[iTime].keys():
    #         for i in range(len(strHistory[iTime][itemKey])):
    #             strHistory[iTime][itemKey][i] /= 4.0
    # print ("finish")
    #
    for iTime in range(len(strHistory)):
        for itemKey in strHistory[iTime].keys():
            myFileStrHistory.write(str(strHistory[iTime][itemKey][1]) + "\t")
        myFileStrHistory.write("\n")
    myFileStrHistory.close()

