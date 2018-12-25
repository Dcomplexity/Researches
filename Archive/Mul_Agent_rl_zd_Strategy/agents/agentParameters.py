def alpha(timeStep):
    return 1 / (10 + 0.002 * timeStep)

def epsilon(timeStep): # 0.5 / (1000 + 0.000001 * self.timeStep)  #when episodes reach about 1000000, the final EPSILON is about 0.25, which means there is a big probability that it will explore
    return 0.5 / (1 + 0.0001 * timeStep)

def epsilonFixed(timeStep):
    return 0.3