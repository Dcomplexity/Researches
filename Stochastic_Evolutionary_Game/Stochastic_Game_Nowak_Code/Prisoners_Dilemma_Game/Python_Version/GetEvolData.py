import numpy as np
from  EvolProc import EvolProc
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-b1", "--b1", type=float, default=2.0, help="The parameter of state 1")
parser.add_argument("-b2", "--b2", type=float, default=1.2, help = "The parameter of state 2")
args = parser.parse_args()

def GetEvolData():
    """
    Creates the data for the dynamics of cooperation rate with time
    Simulates the dynamics of the stochastic game, and of the two corresponding
    repeated games
    Returns:
    coop ... matrix that contains the average cooperation rate in population
    for each timestep and each of the three scenarios
    freq ... matrix that contains the average abundance of each strategy
    Data ... stores the parameters used for the simulation
    """

    # Setting up the objects and defining the parameters
    beta = 1; b2 = args.b2; c = 1; b1 = args.b1; nGen = 10**4; nIt = 100
    coopS = np.zeros((1, nGen)).flatten(); coop1 = np.zeros((1, nGen)).flatten(); coop2 = np.zeros((1, nGen)).flatten() # Vectors that store the cooperation rates for each scenario in each round
    freqS = np.zeros((1, 2**4)).flatten(); freq1 = np.zeros((1, 2**4)).flatten(); freq2 = np.zeros((1, 2**4)).flatten() # Vectors that store the average frequency of each memory-1 strategy
    qS = np.array([1, 0, 0]); q1 = np.array([1, 1, 1]); q2 = np.array([0, 0, 0]) # Defining the transitions of the three scenarios
    piRound = np.array([b1-c, -c, b1, 0, b2-c, -c, b2, 0]) # Vector with all possible one-shot payoffs

    for i in range(nIt):
        print (i)
        (coop, freq) = EvolProc(qS, piRound, beta, nGen); coopS = i/(i+1)*coopS+1/(i+1)*coop; freqS = i/(i+1)*freqS+1/(i+1)*freq
        (coop, freq) = EvolProc(q1, piRound, beta, nGen); coop1 = i/(i+1)*coop1+1/(i+1)*coop; freq1 = i/(i+1)*freq1+1/(i+1)*freq
        (coop, freq) = EvolProc(q2, piRound, beta, nGen); coop2 = i/(i+1)*coop2+1/(i+1)*coop; freq2 = i/(i+1)*freq2+1/(i+1)*freq

    coop = np.array([coopS, coop1, coop2])
    freq = np.array([freqS, freq1, freq2])
    return (coop, freq)

def writefile(filename, dataname):
    f = open(filename, 'w')
    shape = dataname.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if j < (shape[1] - 1):
                f.write(str(dataname[i][j]) + ",")
            else:
                f.write(str(dataname[i][j]))
        f.write('\n')
    f.close()

(coopRe, freqRe) = GetEvolData()
writefile("Pri_Coop_Time.txt", coopRe)