import numpy as np
import random
from scipy.linalg import null_space
import re

def calcPay(Str, qvec, r1, r2, c):
    """
    Calculates the payoff and cooperation rates in a stochastic game with
    deterministic transitions, playing a PGG in each state
    :param Str: Matrix with n rows, each row contains the strategy of a player
    Strategies have the form (pC,n-1, ..., pC,0, pD,n-1, ..., pD, 0) where the letter
    refers to the player's previous own action and number refers to cooperators among co-players.
    :param qvec: [qn, ..., q0] vector that contains the transition
    probabilities qi to go to state 1 in the next round, depending on the number of cooperators
    :param r1: multiplication factors of PGG in state 1
    :param r2: multiplication factors of PGG in state 2
    :param c: cost of cooperation
    :return:
    pivec:
    cvec:
    """

    # PART I --- Preparing a list of all possible states of the markov chain,
    # preparing a list of all possible payoffs in a given round

    # A state has the form (s, a1, ..., an) where s is the state of the
    # stochastic game and a1, ..., an are the player's actions.
    # Hence there are 2^(n+1) states.

    n = Str.shape[0]
    possState = np.zeros((2**(n+1), n+1)) # Matrix where each row corresponds to a possible state
    for i in range(2**(n+1)):
        s = np.binary_repr(i, n+1)
        sSplit = re.findall('\d', s)
        for j in range(n+1):
            possState[i, j] = int(sSplit[j])
    piRound = np.zeros((2**(n+1), n)) # Matrix where each row gives the payoff of all players in a given state
    for i in range(2**(n+1)):
        state = np.copy(possState[i]); nrCoop = np.sum(state[1:]); Mult = state[0]*r2 + (1-state[0])*r1
        for j in range(n):
            piRound[i, j] = nrCoop * Mult / n - state[j+1]*c

    # PART II -- Creating the transition matrix between states
    M = np.zeros((2**(n+1), 2**(n+1)))
    ep = 0.001; Str = (1-ep)*Str + ep*(1-Str)
    for row in range(2**(n+1)):
        stOld = np.copy(possState[row]) # PreviousState
        nrCoop = np.sum(stOld[1:]); envNext = qvec[int(n-nrCoop)]
        for col in range(2**(n+1)):
            stNew = np.copy(possState[col]) # NextState
            if stNew[0] == 1 - envNext:
                trpr = 1 # TransitionProbability
                for i in range(n):
                    iCoopOld = stOld[1+i]
                    pval = Str[i, int(2*n-1-nrCoop-(n-1)*iCoopOld)]
                    iCoopNext = stNew[1+i]
                    trpr = trpr*(pval*iCoopNext+(1-pval)*(1-iCoopNext))
            else:
                trpr = 0
            M[row, col] = trpr

    # np.nan_to_num(M)
    nullMatrix = np.transpose(M) - np.eye(2**(n+1))
    # nullMatrix.dropna(inplace=True)
    np.nan_to_num(nullMatrix) # translate the nan and inf to a number (0 and 1.79769313e+308)
    v = null_space(nullMatrix) # the shape of v is (2**(n+1), 1)
    freq = np.transpose(v) / np.sum(v) # the shape of freq is (1, 2**(n+1))
    pivec = np.dot(freq, piRound).flatten() # the shape of freq: (1, 2**(n+1)), the shape of piRound: (2**(n+1), n)
    cvec = np.sum(np.dot(freq, possState[:, 1:])) / n

    return (pivec, cvec)


