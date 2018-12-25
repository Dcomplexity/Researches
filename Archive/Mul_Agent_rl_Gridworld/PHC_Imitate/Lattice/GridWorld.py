import numpy as np
import datetime
from itertools import permutations
import random

# world height
worldHeight = 3
# world width
worldWidth = 3

# possible actions
actionUp = 0
actionDown = 1
actionLeft = 2
actionRight = 3

gridIndexList = []
for i in range(0, worldHeight):
    for j in range(0, worldWidth):
        gridIndexList.append(worldWidth * i + j)

actions = [actionUp, actionDown, actionLeft, actionRight]
statesAllOne = []
locValidActs = {}

for i in permutations(gridIndexList, 2):
    statesAllOne.append(i)

statesAllOne.append((8, 8))
statesAllOne.append((6, 6))

for i in gridIndexList:
    locValidActs[i] = []

for i in range(0, worldHeight):
    for j in range(0, worldWidth):
        gridIndexNum = worldWidth * i + j
        if i != worldHeight - 1:
            locValidActs[gridIndexNum].append(actionUp)
        if i != 0:
            locValidActs[gridIndexNum].append(actionDown)
        if j != 0:
            locValidActs[gridIndexNum].append(actionLeft)
        if j != worldWidth - 1:
            locValidActs[gridIndexNum].append(actionRight)

def nextGridIndex(action, gridIndex):
    action = action
    indexI = int(gridIndex / 3)
    indexJ = gridIndex - indexI * 3
    if (action == 0):
        indexI += 1
    elif (action == 1):
        indexI -= 1
    elif (action == 2):
        indexJ -= 1
    elif (action == 3):
        indexJ += 1
    nextIndex = indexI * 3 + indexJ
    return nextIndex

def resetStartState():
    agent0LocIndex = np.random.choice([x for x in gridIndexList if x not in [8]])
    while True:
        agent1LocIndex = np.random.choice([x for x in gridIndexList if x not in [6]])
        if agent1LocIndex != agent0LocIndex:
            break
    return (agent0LocIndex, agent1LocIndex)

