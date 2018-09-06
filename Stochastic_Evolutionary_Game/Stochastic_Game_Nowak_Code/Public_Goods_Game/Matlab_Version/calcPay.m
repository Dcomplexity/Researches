function [pivec, cvec] = calcPay(Str, QVec, r1, r2, c)

% Calculates the payoff and cooperation rates in a stochastic game with
% deterministic transitions, playing a PGG in each state
% Str ... Matrix with n rows, each row contains the strategy of a player
% Strategies have the form (pC, n-1, ... pC, 0, pD, n-1, ... pD, 0) where
% the letter refers to the player's own action and number refers to
% cooperators among co-players.
% QVec = (qn, ..., q0) vector that contains the transition probabilities qi
% to go to state 1 in the next round, depending on the number of
% cooperators.
% r1, r2 ... multiplication factors of PGG in each state
% c ... cost of cooperation

% PART I -- PREPARING A LIST OF ALL POSSIBLE STATES OF THE MARKOV CHAIN,
% PREPARING A LIST OF ALL POSSIBLE PAYOFFS IN A GIVEN ROUND

% A state has the form (s, a1, ..., an) where s is the state of the
% stochastic game and a1, ..., an are the player's action.
% Hence, there are 2^(n+1) states.

n = size(Str, 1);
PossState = zeros(2^(n+1), n+1); % Matrix where each row corresponds to a possible state
for i = 1: 2^(n+1)
    PossState(i, :) = sscanf(dec2bin(i-1, n+1), '%1d')'; % Using dec2bin to generate all the possible states.
end
piRound = zeros(2^(n+1), n); % Matrix where each row gives the payoff of all players in a given state
for i = 1: 2^(n+1)
    State = PossState(i, :);
    nrCoop = sum(State(2: end));
    Mult = State(1) * r2 + (1 - State(1)) * r1; % Calculate the multiplication factor of the game
    for j = 1 : n
        % i refers to the state, j refers to the player
        % State(j+1) is the action of player j
        piRound(i, j) = nrCoop * Mult / n - State(j+1) * c;
    end
end

% PART II -- CREATING THE TRANSITION MATRIX BETWEEN STATES
M = zeros(2^(n+1), 2^(n+1)); % There are 2^(n+1) states totally
ep = 0.001;
Str = (1-ep) * Str + ep * (1-Str);
for row = 1: 2^(n+1)
    StOld = PossState(row, :); % Previous State
    nrCoop = sum(StOld(2: end));
    % QVec = (qn, ... , q0) vector contains the transition probabilities qi
    % to go to state 1 in the next round, depending on the number of
    % cooperators
    EnvNext = QVec(n+1-nrCoop);
    for col = 1: 2^(n+1)
        StNew = PossState(col, :);
        if StNew(1) == 1 - EnvNext
            trpr = 1; % Transition Probability
            for i = 1: n
                iCoopOld = StOld(1+i);
                pval = Str(i, 2*n-nrCoop-(n-1)*iCoopOld);
                iCoopNext = StNew(1+i);
                trpr = trpr * (pval * iCoopNext + (1-pval) * (1-iCoopNext));
            end
        else
            trpr = 0;
        end
        M(row, col) = trpr;
    end
end
v = null(M' - eye(2^(n+1)));
freq = v' / sum(v);
pivec = freq * piRound;
cvec = sum(freq * PossState(:, 2: end)) / n;

end
