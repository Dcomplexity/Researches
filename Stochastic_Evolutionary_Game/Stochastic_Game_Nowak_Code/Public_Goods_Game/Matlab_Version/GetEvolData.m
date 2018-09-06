function [coop, freq, Data] = GetEvolData()
    
    % [coop, freq, Data] = GetEvolData();
    % Create the data for Figure 2b by calling the subroutine EvolProc.m
    % that simulates the dynamics of the stochasitc game, and of the two
    % corresponding repeated games.
    % coop ... matrix that contains the average cooperation rate in
    % population
    % for each timestep and each of the three scenarios
    % freq ... matrix that contains the average abundance of each strategy
    % Data ... stores the parameters used for the simulations
    
    %% Setting up the objects and defining the parameters
    grSize = 4; beta = 100; r2 = 1.2; r1 = 1.6; c = 1; nGen = 10^4; nIt = 100; % Parameters in Fig. 2b
    coopS = zeros(1, nGen); coop1 = coopS; coop2 = coopS; % Vectors that store the cooperation rates for each scenario in each round
    freqS = zeros(1, 2^(2*grSize)); freq1 = freqS; freq2 = freqS; % Vectors that store the average frequency of each memory-1 strategy
    qS = [1, zeros(1, grSize)]; q1 = ones(1, grSize+1); q2 = zeros(1, grSize+1); % Defining the transition of the three scenarios
    
    for t = 1:nIt % Running nIt independent simulations of the dynamics and averaging over the outcomes
        t;
        [coS, freS] = EvolProc(qS, r1, r2, c, beta, nGen); coopS = (t-1)/t*coopS + coS/t; freqS = (t-1)/t*freqS + freS/t;
        [co1, fre1] = EvolProc(q1, r1, r1, c, beta, nGen); coop1 = (t-1)/t*coop1 + co1/t; freq1 = (t-1)/t*freq1 + fre1/t;
        [co2, fre2] = EvolProc(q2, r2, r2, c, beta, nGen); coop2 = (t-1)/t*coop2 + co2/t; freq2 = (t-1)/t*freq2 + fre2/t;
    end
    
% Creating the output
coop = [coopS; coop1; coop2];
freq = [freqS; freq1; freq2];
Data = ['r1=', num2str(r1), '; r2=', num2str(r2), '; c=', num2str(c), '; beta=', num2str(beta), '; nIt=', num2str(nIt)]; 
end