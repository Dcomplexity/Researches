import numpy as np
import random
from sympy import Matrix
from scipy.linalg import null_space

def EvolProc(qvec, piRound, beta, nGen):
    """
    Parameters:
    qvec=[q2, q1, q0] ... transition probability to state 1, depending on
    previous number of cooperators,
    piRound = [u1CC, u1CD, u1DC, u1DD, u2CC, u2CD, u2DC, u2DD] ... One-shot
    payoffs depending on current state and on players' actions,
    beta ... selection strength,
    nGen ... number of mutants considered,
    Returns:
    coop ... average cooperation rate,
    freq ... average abundance for each memory-1 strategy
    """

    # Setting up all objects
    N = 100
    pv1 = np.copy(piRound) # payoff vector from the perspective of player 1
    pv2 = np.copy(piRound); pv2[1:3] = piRound[2:0:-1]; pv2[5:7] = piRound[6:4:-1] # from the perspective of player2
    Str = np.array([[0,0,0,0], [0,0,0,1], [0,0,1,0], [0,0,1,1], [0,1,0,0], [0,1,0,1], [0,1,1,0], [0,1,1,1], [1,0,0,0], [1,0,0,1], [1,0,1,0], [1,0,1,1], [1,1,0,0], [1,1,0,1], [1,1,1,0],[1,1,1,1]])
    PayM = np.zeros((16, 16)); C = np.zeros((16, 16)) # Initializing the pairwise payoff matrix and the cooperation matrix
    for i in range(16):
        for j in range(16)[i:16]:
            # Calculating and storing all pairwise payoffs and cooperation rates
            (pi1, pi2, cop1, cop2, s1) = payoff(Str[i], Str[j], qvec, pv1, pv2)
            PayM[i, j] = pi1; PayM[j, i] = pi2; C[i, j] = cop1; C[j, i] = cop2

    # Running the evolutionary process
    Res = 0; pop = np.append(np.array([1]), np.zeros((15))) # Initially all players use the first memory-1 strategy, ALLD
    coop = np.zeros((1, nGen)).flatten(); freq = np.zeros((1, 16)).flatten() # Initializing the output vectors
    for i in range(nGen):
        Mut = random.choice(range(16)) # Introduce a mutant strategy
        rho = CalcRho(Mut, Res, PayM, N, beta) # Calculate fixation probability of mutant
        if random.random() < rho: # If fixation occurs
            Res = Mut # Resident strategy is replaced by mutant strategy
            pop = np.zeros((1, 16)).flatten(); pop[Res] = 1 # Population state is updated
        coop[i] = C[Res, Res] # Storing the cooperation rate at time i
        # It is equivalent to sum all pop and divide by nGen
        freq = i/(i+1)*freq + 1/(i+1)*pop # Updating the average frequency
    return (coop, freq)


def CalcRho(S1, S2, PayM, N, beta):
    """
    Calculates the fixation probability of one S1 mutant in an S2 population

    Parameters:
    S1 ... S1 mutant strategy
    S2 ... S2 population strategy
    PayM ... Payoffs matrix
    N ... The number of players
    beta ... Selection strength

    Returns:
    Rho ... The probability of mutant strategy success
    """
    alpha = np.zeros((1, N-1)).flatten()
    for j in range(N)[1:]: # j ... Number of mutants in the population
        pi1 = (j-1)/(N-1)*PayM[S1, S1] + (N-j)/(N-1)*PayM[S1, S2] # Payoff mutant
        pi2 = j/(N-1)*PayM[S2, S1] + (N-j-1)/(N-1)*PayM[S2, S2]
        alpha[j-1] = np.exp(-beta*(pi1-pi2))
    Rho = 1/(1 + np.sum(np.cumprod(alpha))) # Calculating the fixation probability according to formula given is SI
    return Rho

#def rank(A, atol=1e-13, rtol=0):
#    A = np.atleast_2d(A)
#    s = np.linalg.svd(A, compute_uv=False)
#    tol = max(atol, rtol * s[0])
#    rank = int((s >= tol).sum())
#    return rank
#
#def nullspace(A, atol=1e-13, rtol=0):
#    A = np.atleast_2d(A)
#    u, s, vh = np.linalg.svd(A)
#    tol = max(atol, rtol * s[0])
#    nnz = (s >= tol).sum()
#    ns = vh[nnz:].conj().T
#    return ns

def payoff(p, q, qvec, piv1, piv2):
    """
    Calculate the payoff based on the strategy
    """
    eps = 10**(-3) # Error rate for implementation errors
    p = p*(1-eps) + (1-p)*eps; q = q*(1-eps) + (1-q)*eps # Adding errors to the palyer's strategies
    M = np.array([[qvec[0]*p[0]*q[0], qvec[0]*p[0]*(1-q[0]), qvec[0]*(1-p[0])*q[0], qvec[0]*(1-p[0])*(1-q[0]), (1-qvec[0])*p[0]*q[0], (1-qvec[0])*p[0]*(1-q[0]), (1-qvec[0])*(1-p[0])*q[0], (1-qvec[0])*(1-p[0])*(1-q[0])],
                  [qvec[1]*p[1]*q[2], qvec[1]*p[1]*(1-q[2]), qvec[1]*(1-p[1])*q[2], qvec[1]*(1-p[1])*(1-q[2]), (1-qvec[1])*p[1]*q[2], (1-qvec[1])*p[1]*(1-q[2]), (1-qvec[1])*(1-p[1])*q[2], (1-qvec[1])*(1-p[1])*(1-q[2])],
                  [qvec[1]*p[2]*q[1], qvec[1]*p[2]*(1-q[1]), qvec[1]*(1-p[2])*q[1], qvec[1]*(1-p[2])*(1-q[1]), (1-qvec[1])*p[2]*q[1], (1-qvec[1])*p[2]*(1-q[1]), (1-qvec[1])*(1-p[2])*q[1], (1-qvec[1])*(1-p[2])*(1-q[1])],
                  [qvec[2]*p[3]*q[3], qvec[2]*p[3]*(1-q[3]), qvec[2]*(1-p[3])*q[3], qvec[2]*(1-p[3])*(1-q[3]), (1-qvec[2])*p[3]*q[3], (1-qvec[2])*p[3]*(1-q[3]), (1-qvec[2])*(1-p[3])*q[3], (1-qvec[2])*(1-p[3])*(1-q[3])],
                  [qvec[0]*p[0]*q[0], qvec[0]*p[0]*(1-q[0]), qvec[0]*(1-p[0])*q[0], qvec[0]*(1-p[0])*(1-q[0]), (1-qvec[0])*p[0]*q[0], (1-qvec[0])*p[0]*(1-q[0]), (1-qvec[0])*(1-p[0])*q[0], (1-qvec[0])*(1-p[0])*(1-q[0])],
                  [qvec[1]*p[1]*q[2], qvec[1]*p[1]*(1-q[2]), qvec[1]*(1-p[1])*q[2], qvec[1]*(1-p[1])*(1-q[2]), (1-qvec[1])*p[1]*q[2], (1-qvec[1])*p[1]*(1-q[2]), (1-qvec[1])*(1-p[1])*q[2], (1-qvec[1])*(1-p[1])*(1-q[2])],
                  [qvec[1]*p[2]*q[1], qvec[1]*p[2]*(1-q[1]), qvec[1]*(1-p[2])*q[1], qvec[1]*(1-p[2])*(1-q[1]), (1-qvec[1])*p[2]*q[1], (1-qvec[1])*p[2]*(1-q[1]), (1-qvec[1])*(1-p[2])*q[1], (1-qvec[1])*(1-p[2])*(1-q[1])],
                  [qvec[2]*p[3]*q[3], qvec[2]*p[3]*(1-q[3]), qvec[2]*(1-p[3])*q[3], qvec[2]*(1-p[3])*(1-q[3]), (1-qvec[2])*p[3]*q[3], (1-qvec[2])*p[3]*(1-q[3]), (1-qvec[2])*(1-p[3])*q[3], (1-qvec[2])*(1-p[3])*(1-q[3])]])
    nullMatrix = np.transpose(M) - np.eye(8)
    # v = np.array(nullMatrix.nullspace())
    v = null_space(nullMatrix)
    v = v / np.sum(v) # shape is (8, 1)
    piv1 = piv1.reshape(piv1.size, 1).transpose() # shape is (1, 8)
    piv2 = piv2.reshape(piv2.size, 1).transpose()
    pi1 = np.dot(piv1, v)[0] # This is a dot multiply
    pi2 = np.dot(piv2, v)[0]
    v = v.flatten()
    cop1 = v[0] + v[1] + v[4] + v[5]
    cop2 = v[0] + v[2] + v[4] + v[6]
    s1 = np.sum(v[0:4])
    return (pi1, pi2, cop1, cop2, s1)
