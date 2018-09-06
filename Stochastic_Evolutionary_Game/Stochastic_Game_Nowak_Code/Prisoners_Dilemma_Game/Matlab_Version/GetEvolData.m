function [coop, freq, Data] = GetEvolData()

% [coop, freq, Data] = GetEvolData();
% Creates the data for Figure 2a by calling the suuroutine EvolProc.m that
% simulates the dynamics of the stochastic game, and fo the two
% corresponding repeated games.
% coop ... matrix that contains the average cooperation rate in population
% for each timestep and each of the three scenarios
% freq ... matrix that contains the average abundance of each strategy
% Data ... stores the parameters used for the simulations

%% Setting up the objects and defining the parameters
beta = 1; b2 = 1.2; c = 1; b1 = 2; nGen = 10^4; nIt = 100; % Parameters in Fig.2a
coopS = zeros(1, nGen); coop1 = coopS; coop2 = coopS; % Vectors that store the cooperation rates for each scenario in each round
freqS = zeros(1, 2^4); freq1 = freqS; freq2 = freqS; % Vectors that store the average frequency of each memory-1 startegy
qS = [1 0 0]; q1 = [1 1 1]; q2 = [0 0 0]; % Defining the transition of the three scenarios
piRound = [b1-c, -c, b1, 0, b2-c, -c, b2, 0]; % Vector with all possible one-shot payoffs

for i = 1: nIt % Running nIt independent simulations of the dynamics and averaging over the outcomes
    i
    [coop,freq]=EvolProc(qS,piRound,beta,nGen); coopS=(i-1)/i*coopS+1/i*coop; freqS=(i-1)/i*freqS+1/i*freq;
    [coop,freq]=EvolProc(q1,piRound,beta,nGen); coop1=(i-1)/i*coop1+1/i*coop; freq1=(i-1)/i*freq1+1/i*freq;
    [coop,freq]=EvolProc(q2,piRound,beta,nGen); coop2=(i-1)/i*coop2+1/i*coop; freq2=(i-1)/i*freq2+1/i*freq;
end
coop = [coopS; coop1; coop2]; % Creating the output
freq = [freqS; freq1; freq2];
Data = ['b1=', num2str(b1), '; b2=', num2str(b2), '; c=', num2str(c), '; beta=', num2str(beta), '; nGen=', num2str(nGen), '; nIt=', num2str(nIt)];
end