function [coop, freq] = EvolProc(qvec, piRound, beta, nGen)

% [coop, freq] = EvolProc(qvec, piRound, beta, nGen);
% qvec=[q2, q1, q0] ... transition probability to state 1, depending on
% previous number of cooperators
% piRound = [u1CC, u1CD, u1DC, u1DD, u2CC, u2CD, u2DC, u2DD] ... One-shot
% payoffs depending on current state and on players' actions
% beta ... selection strength, nGen ... number of mutants considered
% coop ... average cooperation rate, freq ... average abundance for each
% memory-1 strategy

%% Setting up the random number generator
C = clock;
rng(C(5)*60 + C(6));

%% Setting up all objects
N = 100;
pv1 = piRound; % payoff vector from the perspective of player 1
pv2 = piRound; pv2(2:3) = piRound(3:-1:2); pv2(6:7) = piRound(7:-1:6); % from the perspective of player 2
Str = [0 0 0 0; 0 0 0 1; 0 0 1 0; 0 0 1 1; 0 1 0 0; 0 1 0 1; 0 1 1 0; 0 1 1 1;...
       1 0 0 0; 1 0 0 1; 1 0 1 0; 1 0 1 1; 1 1 0 0; 1 1 0 1; 1 1 1 0; 1 1 1 1]; % list of all memory-1 strategies
PayM = zeros(16, 16); C = zeros(16, 16); % Initializing the pairwise payoff matrix and the cooperation matrix
for i = 1: 16
    for j = i: 16
        [pi1, pi2, cop1, cop2, s1] = payoff(Str(i, :), Str(j, :), qvec, pv1, pv2);
        PayM(i, j) = pi1; PayM(j, i) = pi2; C(i, j) = cop1; C(j, i) = cop2; %Calculating and storing all pairwise payoffs and cooperation rates
    end
end

%% Running the evolutionary process
Res = 1; pop = [1, zeros(1, 15)]; % Initially all players use the first memory-1 strategy, ALLD
coop = zeros(1, nGen); freq = zeros(1, 16); % Initializing the output vectors
for i = 1: nGen
    Mut = ceil(16 * rand(1)); % Introduce a mutant strategy
    rho = CalcRho(Mut, Res, PayM, N, beta); % Calculate fixation probability of mutant
    if rand(1) < rho % If fixation occurs
        Res = Mut; % Resident strategy is replaced by mutant strategy
        pop = zeros(1, 16); pop(Res) = 1; % Population state is updated
    end
    coop(i) = C(Res, Res); % Storing the cooperation rate at time i
    freq = (i-1)/i * freq + 1/i*pop; % Updating the average frequency
end
end

function Rho = CalcRho(S1, S2, PayM, N, beta)
% Calculates the fixation probability of one S1 mutant in an S2 population
alpha = zeros(1, N-1);
for j = 1: N-1 % j ... Number of mutants in the population
    pi1 = (j-1)/(N-1)*PayM(S1, S1) + (N-j)/(N-1)*PayM(S1, S2); % Payoff mutant
    pi2 = j/(N-1)*PayM(S2, S1) + (N-j-1)/(N-1)*PayM(S2, S2); % Payoff resident
    alpha(j) = exp(-beta*(pi1-pi2));
end
Rho = 1/(1+sum(cumprod(alpha))); % Calculating the fixation probability according to formula given is SI
end

function [pi1, pi2, cop1, cop2, s1] = payoff(p, q, qvec, piv1, piv2)
eps = 10^(-3); % Error rate for implementation errors
p = p*(1-eps) + (1-p)*eps; q = q*(1-eps) + (1-q)*eps; % Adding errors to the players' strategies
M=[qvec(1)*p(1)*q(1), qvec(1)*p(1)*(1-q(1)), qvec(1)*(1-p(1))*q(1), qvec(1)*(1-p(1))*(1-q(1)), (1-qvec(1))*p(1)*q(1), (1-qvec(1))*p(1)*(1-q(1)), (1-qvec(1))*(1-p(1))*q(1), (1-qvec(1))*(1-p(1))*(1-q(1));
   qvec(2)*p(2)*q(3), qvec(2)*p(2)*(1-q(3)), qvec(2)*(1-p(2))*q(3), qvec(2)*(1-p(2))*(1-q(3)), (1-qvec(2))*p(2)*q(3), (1-qvec(2))*p(2)*(1-q(3)), (1-qvec(2))*(1-p(2))*q(3), (1-qvec(2))*(1-p(2))*(1-q(3));
   qvec(2)*p(3)*q(2), qvec(2)*p(3)*(1-q(2)), qvec(2)*(1-p(3))*q(2), qvec(2)*(1-p(3))*(1-q(2)), (1-qvec(2))*p(3)*q(2), (1-qvec(2))*p(3)*(1-q(2)), (1-qvec(2))*(1-p(3))*q(2), (1-qvec(2))*(1-p(3))*(1-q(2));
   qvec(3)*p(4)*q(4), qvec(3)*p(4)*(1-q(4)), qvec(3)*(1-p(4))*q(4), qvec(3)*(1-p(4))*(1-q(4)), (1-qvec(3))*p(4)*q(4), (1-qvec(3))*p(4)*(1-q(4)), (1-qvec(3))*(1-p(4))*q(4), (1-qvec(3))*(1-p(4))*(1-q(4));
   qvec(1)*p(1)*q(1), qvec(1)*p(1)*(1-q(1)), qvec(1)*(1-p(1))*q(1), qvec(1)*(1-p(1))*(1-q(1)), (1-qvec(1))*p(1)*q(1), (1-qvec(1))*p(1)*(1-q(1)), (1-qvec(1))*(1-p(1))*q(1), (1-qvec(1))*(1-p(1))*(1-q(1));
   qvec(2)*p(2)*q(3), qvec(2)*p(2)*(1-q(3)), qvec(2)*(1-p(2))*q(3), qvec(2)*(1-p(2))*(1-q(3)), (1-qvec(2))*p(2)*q(3), (1-qvec(2))*p(2)*(1-q(3)), (1-qvec(2))*(1-p(2))*q(3), (1-qvec(2))*(1-p(2))*(1-q(3));
   qvec(2)*p(3)*q(2), qvec(2)*p(3)*(1-q(2)), qvec(2)*(1-p(3))*q(2), qvec(2)*(1-p(3))*(1-q(2)), (1-qvec(2))*p(3)*q(2), (1-qvec(2))*p(3)*(1-q(2)), (1-qvec(2))*(1-p(3))*q(2), (1-qvec(2))*(1-p(3))*(1-q(2));
   qvec(3)*p(4)*q(4), qvec(3)*p(4)*(1-q(4)), qvec(3)*(1-p(4))*q(4), qvec(3)*(1-p(4))*(1-q(4)), (1-qvec(3))*p(4)*q(4), (1-qvec(3))*p(4)*(1-q(4)), (1-qvec(3))*(1-p(4))*q(4), (1-qvec(3))*(1-p(4))*(1-q(4))];
% Constructing the transition matrix M for the Markov chain of the game
% dynamics
v = null(M'-eye(8)); v = v/sum(v); % Calculating the normalized left eigenvector with respect to EV 1.
pi1 = piv1 * v; pi2 = piv2 * v; % Calculating expected payoffs of the two players
cop1 = v(1) + v(2) + v(5) + v(6); cop2 = v(1) + v(3) + v(5) + v(7); % Calculating the cooperation frequency of the two players
s1 = sum(v(1:4)); % Calculating how often players are in the first state
end
