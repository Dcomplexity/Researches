import numpy as np
from EvolProc import EvolProc
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-r1", "--r1", type=float, default=1.6, help="The parameter of state 1")
parser.add_argument("-r2", "--r2", type=float, default=1.2, help="The parameter of state 2")
args = parser.parse_args()

def GetEvolData():
    """
    Creates the data for the dynamics of cooperation rate with time
    Simulates the dynamics of the stochastic game, and of the two corresponding repeated game
    :return:
    coop: matrix that contains the average cooperation rate in population
    for each timestep and each of the three scenarios
    freq: matrix that contains the average abundance of each strategy
    Data: stores the parameters used for the simulations
    """

    # Setting up the objects and definning the parameters
    grSize = 4; beta = 100; r2 = 1.2; c = 1; r1 = 1.6; nGen = 10**4; nIt = 100; # Parameters in Fig. 2b
    coopS = np.zeros((1, nGen)).flatten(); coop1 = np.zeros((1, nGen)).flatten(); coop2 = np.zeros((1, nGen)).flatten()
    freqS = np.zeros((1, 2**(2*grSize))).flatten(); freq1 = np.zeros((1, 2**(2*grSize))).flatten(); freq2 = np.zeros((1, 2**(2*grSize))).flatten()
    qS = np.append(np.array([1]), np.zeros((grSize))); q1 = np.ones((1, grSize+1)).flatten(); q2 = np.zeros((1, grSize+1)).flatten() # Defining the transitions of the three scenarios

    for i in range(nIt):
        print (i)
        starttime = datetime.datetime.now()
        (coop, freq) = EvolProc(qS, r1, r2, c, beta, nGen); coopS = i/(i+1)*coopS+1/(i+1)*coop; freqS = i/(i+1)*freqS+1/(i+1)*freq
        endtimeS = datetime.datetime.now()
        print ("Complete State s", (endtimeS-starttime).seconds)
        (coop, freq) = EvolProc(q1, r1, r2, c, beta, nGen); coop1 = i/(i+1)*coop1+1/(i+1)*coop; freq1 = i/(i+1)*freq1+1/(i+1)*freq
        endtime1 = datetime.datetime.now()
        print ("Complete State 1", (endtime1-starttime).seconds)
        (coop, freq) = EvolProc(q2, r1, r2, c, beta, nGen); coop2 = i/(i+1)*coop2+1/(i+1)*coop; freq2 = i/(i+1)*freq2+1/(i+1)*freq
        endtime2 = datetime.datetime.now()
        print ("Complete State 2", (endtime2-starttime).seconds)

    # Creating the output
    coop = np.array([coopS, coop1, coop2])
    freq = np.array([freqS, freq1, freq2])
    return (coop, freq)

def writefile(filename, dataname):
    f = open(filename, 'w')
    shape = dataname.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if j < (shape[1] - 1):
                f.write(str(dataname[i][j]) + ',')
            else:
                f.write(str(dataname[i][j]))
        f.write('\n')
    f.close()

(coopRe, freRe) = GetEvolData()
writefile("Pub_Coop_Time.txt", coopRe)

