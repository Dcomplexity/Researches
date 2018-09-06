function [coop, freq] = EvolProc(qvec, r1, r2, c, beta, nGen) % Here I delete the Str as a return parameter
% [coop, freq] = EvolProc(qvec, r1, r2, c, s, nGen)
% qvec = [qn, ..., q0] ... transition probability to state 1, depending on
% previous number of cooperators
% r1, r2 ... multiplication factors in the two states
% c ... cost of cooperation, beta ... strength of selection
% nGen ... number of mutants considered
% coop ... average cooperation rate, freq ... average abundance for each
% memory-1 strategy

global Str binom

%% Setting up the random number generator
C = clock;
rng(C(5)*60 + C(6));

%% Setting up all objects
N = 100; % Population size
n = length(qvec) -1; % Number of players
binom = CalcBinom(N, n); % Pre-calculating all possible binomial coefficients that will be needed
Str = zeros(2^(2*n), 2*n); ns = 2^(2*n); % Constructing a list of all possible strategies
for i = 1:ns
    Str(i, :) = sscanf(dec2bin(i-1, 2*n), '%1d')';
end
PayH = zeros(1, ns); CoopH = zeros(1, ns); % Initializing a vector that contians all payoffs and cooperation rates in homogeneous populations
for i = 1:ns % Calculating the values of PayH and CoopH
    StrH = zeros(n, 2*n);
    for j = 1:n
        StrH(j, :) = Str(i, :);
    end
    [pivec, cvec] = calcPay(StrH, qvec, r1, r2, c);
    PayH(i) = pivec(1); CoopH(i) = cvec(1);
end

%% Running the evolutionary process
Res = 1; pop = zeros(1, 2^(2*n)); pop(Res) = 1; % Initial population: AllD
coop = zeros(1, nGen); freq=zeros(1, 2^(2*n)); % Initializing the output
for i = 1:nGen
    Mut = ceil(2^(2*n) * rand(1)); % Introduce a mutant strategy
    rho = CalcRho(Mut, Res, PayH, N, n, qvec, r1, r2, c, beta); % Calculate fixation probability of mutant
    if rand(1) < rho % If fixation occurs
        Res = Mut; % Resident strategy is replaced by mutant strategy
        pop = zeros(1, 2^(2*n)); pop(Res) = 1; % Population state is updated
    end
    coop(i) = CoopH(Res); % Storing the cooperation rate at time i
    freq = (i-1)/i*freq +1/i*pop; % Updating the average frequency of each strategy
end
end


function Rho = CalcRho(S1, S2, PayH, N, n, rv, r1, r2, c, beta)
% calculates the fixation probability of one S1 mutant in an S2 population
global Str binom
alpha = zeros(1, N-1);

%% First step: Calculating the payoff of an S1 player and an S2 player, depending on number of S1 players in the group
Pay = zeros(n+1, 2); % matrix that contains the payoffs of the two players
Pay(n+1, 1) = PayH(S1); % entry (n+1, 1) .. everyone plays S1
Pay(1, 2) = PayH(S2); % entry (1, 2) .. everyone plays S2
st1 = Str(S1, :);
st2 = Str(S2, :);
for nMut = 1:n-1
    St=[repmat(st1, nMut, 1); repmat(st2, n-nMut, 1)]; % Creating a list of all group members' strategies
    pivec = calcPay(St, rv, r1, r2, c); % Calculating and storing payoffs for that group
    Pay(nMut+1, 1) = pivec(1); Pay(nMut+1, 2) = pivec(end);
end

for j = 1: N-1 % j corresponds to the number of S1 players in the whole population
    pi1 = binom(j, :) * Pay(2:end, 1); % considering all possible groups the S1 player could find herself in
    pi2 = binom(j+1, :) * Pay(1:end-1, 2); % considering all possilbe groups the S2 palyer could find in herself in
    alpha(j) = exp(-beta*(pi1-pi2));
end
Rho = 1/(1 + sum(cumprod(alpha))); % Calculating the fixation probability according to formula given in SI
end

function bm = CalcBinom(N, n)
bm=zeros(N, n);
for row=1:N
    for col=1:n
        if col > row || n-col > N-row
            bm(row, col) = 0;
        else
            % b=nchoosek(n,k) returns the binomial coefficient, defined as
            % n!/((n-k)!k!). This is the number of combinations of n items
            % taken k at a time
            bm(row, col) = nchoosek(row-1, col-1)*nchoosek(N-row,n-col)/nchoosek(N-1,n-1);
        end
    end
end
end