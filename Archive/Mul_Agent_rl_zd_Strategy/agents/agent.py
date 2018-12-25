import numpy as np
from states_actions_envs.states_actions_envs import *
from agents.agentParameters import *

class agent(object):
    def __init__(self, alpha, gamma, delta, epsilon):
        self.timeStep = 0
        self.curSta = []
        self.nextSta = []
        self.rewards = 0
        self.nextSta = []
        self.curAct = 0
        self.maxStaAct = 0
        self.strategy = {}
        self.staActVal = {}
        self.alpha = alpha(self.timeStep) # using a function as a parameter, such as alpha = 1 / (10 + 0.002 * self.timeStep)
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon(self.timeStep)

        try:
            self.DCActs = generateDCActions()
            self.DCStas = generateDCStates(self.DCActs)
        except:
            print ("There are errors of creating actions and states")

    def initialSelfStrategy(self):
        for i in self.DCStas:
            self.strategy[i] = np.zeros(self.DCActs.shape[0])
            lengthOfAction = self.DCActs.shape[0]
            for j in range(self.DCActs.shape[0]):
                self.strategy[i][j] = 1.0 / lengthOfAction

    def initialActionValues(self):
        for i in self.DCStas:
            self.staActVal[i] = np.zeros(self.DCActs.shape[0])

    def setCurrentState(self, currentState):
        self.curSta = currentState

    def setNextState(self, nextState):
        self.nextSta = nextState

    def setRewards(self, agentRewards):
        self.rewards = agentRewards

    def chooseAction(self):
        if np.random.binomial(1, self.epsilon) == 1:
            self.curAct = np.random.choice(self.DCActs, size=1)[0]
        else:
            self.curAct = np.random.choice(self.DCActs, size=1, p=self.strategy[self.curSta])[0]

    def updateActionValues(self):
        self.staActVal[self.curSta][self.curAct] = (1-self.alpha)*self.staActVal[self.curSta][self.curAct] \
                                                    + self.alpha*(self.rewards+self.gamma*np.amax(self.staActVal[self.nextSta]))

    def updateStrategy(self):
        pass

    def updateTimeStep(self):
        self.timeStep += 1

    # def updateEpsilon(self):
        # self.EPSILON = epsilon(self.timeStep)  # Notice the epsilon, in the former settings, I make a mistake, I write
                                               # the epsilon as EPSILON, which means the epsilon does not change.
                                               # It remains as 0.5
    def updateEpsilon(self):
        # In phc vs phc experiment, the result will not converge to defect vs defect
        # Because the eploration rate is small, many states will not be met.
        self.epsilon = epsilon(self.timeStep)
        # self.epsilon = 0.5

    def updateAlpha(self): # if you want to update alpha, you have to execute this fucntion
                           # just update timeStep will not change the alpha automatically.
        self.alpha = alpha(self.timeStep)

    def changeEpsilon(self, newEpsilon):
        self.epsilon = newEpsilon

    def getStrategy(self):
        return self.strategy

    def getAction(self):
        return self.curAct


