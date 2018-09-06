import numpy as np
import random
from scipy.special import comb
import re
from numpy.matlib import repmat

from calcPay import calcPay


def EvolProc(qvec, r1, r2, c, beta, nGen):
    """
    The process of evolution
    :param qvec: qvec=[qn ... q0] .... transition probability to state 1,
    depending on previous number of cooperation
    :param r1: multiplication factors in the 1 state
    :param r2: multiplication factors in the 2 state
    :param c: cost of cooperation
    :param beta: strength of selection
    :param nGen: number of mutants considered
    :return:
    coop: average cooperation rate
    freq: average abundance for each memory-1 strategy
    """

    # Setting up all objects
    N = 100 # Population size
    n = qvec.shape[0] - 1 # Number of players
    global binom, Str
    binom = calcBinom(N, n) # Pre-calculating all possible binomial coefficients that will be needed
    Str = np.zeros((2**(2*n), 2*n)); ns = 2**(2*n) # Constructing a list of all possible strategies
    for i in range(ns):
        s = np.binary_repr(i, 2*n)
        sSplit = re.findall('\d', s)
        for j in range(2*n):
            Str[i, j] = int(sSplit[j])

    PayH = np.zeros((1, ns)).flatten(); CoopH = np.zeros((1, ns)).flatten() # Initializing a vector that contains all payoffs and cooperation rates in homogeneous populations
    for i in range(ns): # Calculating the values of PayH and CoopH
        StrH = np.zeros((n, 2*n))
        for j in range(n):
            StrH[j] = np.copy(Str[i])
        (pivec, cvec) = calcPay(StrH, qvec, r1, r2, c)
        PayH[i] = pivec[0]; CoopH[i] = cvec

    # Running the evolutionary process
    Res = 0; pop = np.zeros((1, 2**(2*n))).flatten(); pop[Res] = 1 # Initial population: AllD
    coop = np.zeros((1, nGen)).flatten(); freq = np.zeros((1, 2**(2*n))).flatten() # Initializing the output
    for i in range(nGen):
        Mut = random.choice(range(2**(2*n))) # Introduce a mutant strategy
        rho = calcRho(Mut, Res, PayH, N, n, qvec, r1, r2, c, beta) # Calculate fixation probability of mutant
        if random.random() < rho: # If fixation occurs
            Res = Mut # Resident strategy is replaced by mutant strategy
            pop = np.zeros((1, 2**(2*n))).flatten(); pop[Res] = 1 # Population state is updated
        coop[i] = CoopH[Res] # Storing the cooperation rate at time i
        freq = i/(i+1)*freq + 1/(i+1)*pop

    return (coop, freq)



def calcRho(S1, S2, PayH, N, n, rv, r1, r2, c, beta):
    """
    Calaculates the fixation probability of one S1 mutant in an S2 population
    :param S1: Strategy S1
    :param S2: Strategy S2
    :param PayH: Matrix of payoff
    :param N: Population size
    :param n: Group size
    :param rv: Transition probability between states
    :param r1: Multiplication of state 1
    :param r2: Multiplication of state 2
    :param c: Cost of public goods game
    :param beta: Strength of mutation
    :return:
    """

    alpha = np.zeros((1, N-1)).flatten()

    # First step: Calculating the payoff of an S1 player and an S2 player, depending on number of S1 players in the group
    Pay = np.zeros((n+1, 2)) # matrix that contains the payoffs of the two players
    Pay[n, 0] = PayH[S1] # entry (n, 0) ... everyone plays S1
    Pay[0, 1] = PayH[S2] # entry (1, 2) ... everyone plays S2
    st1 = Str[S1]; st2 = Str[S2] # Two strategies
    for nMut in range(n-1): # number of mutants
        St = np.append(repmat(st1, nMut+1, 1), repmat(st2, n-nMut-1, 1), axis=0)
        (pivec, cvec) = calcPay(St, rv, r1, r2, c) # Calculating and storing payoffs for that group
        Pay[nMut+1, 0] = pivec[0]; Pay[nMut+1, 1] = pivec[-1]

    for j in range(N-1): # j + 1 corresponds to the number of S1 players in the whole population
        # if j = 0, means there are 1 S1 players, the s1 player will face the group that containing all S2 players
        # Pay[1:, 0] means that the payoff if there are at least one S1 player
        # From the perspective of S2, if there are one S1 player, then the probabilities of possible groups are stored in binom[j+1]
        pi1 = np.dot(binom[j], Pay[1:, 0].reshape(Pay.shape[0]-1, 1)) # considering all possible groups the S1 player could find herself in
        pi2 = np.dot(binom[j+1], Pay[0:-1, 1].reshape(Pay.shape[0]-1, 1)) # considering all possible groups the S2 player could find herself in
        alpha[j] = np.exp(-beta*(pi1[0]-pi2[0]))
    Rho = 1/(1 + np.sum(np.cumprod(alpha)))
    return Rho # Calculating the fixation probability according to formula given is SI

def calcBinom(N, n):
    """
    Calculates the probability of a certain group composition given there are only two
    strategies present
    row - 1 ... number of players with strategy 1 among all other players in population
    col - 1 ... number of co-players with strategy 1 in Group
    :param N: The totla number
    :param n: The number of pickup things
    :return: bm: a Nxn matrix
    """
    bm = np.zeros((N, n))
    for row in range(N):
        for col in range(n):
            bm[row, col] = comb(row, col) * comb(N-row-1, n-col-1) / comb(N-1, n-1)

    return bm
