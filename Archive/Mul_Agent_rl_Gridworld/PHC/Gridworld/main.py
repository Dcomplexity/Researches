from PlayGame import *
from Agent import *
import multiprocessing


def writeStrategy(filename, dataname):
    f = open(filename, 'a')
    for i in dataname.keys():
        f.write("(" + str(i[0]) + "," + str(i[1]) + ")" + ': {')
        for j in dataname[i].keys():
            f.write(str(j) + ": " + str(dataname[i][j]) + ", ")
        f.write("}")
    f.write("\n")

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 4)
    agentActList = []
    agent0List = [agent(agentId=0, startLocIndex=0) for x in range(4)]
    agent1List = [agent(agentId=1, startLocIndex=2) for x in range(4)]
    for i in range(4):
        agentActList.append(pool.apply_async(runGame, (agent0List[i], agent1List[i])))
    pool.close()
    pool.join()

    for res in agentActList:
        print(res.get()[0])
        writeStrategy("Agent0_Strategy.txt", res.get()[1])
        writeStrategy("Agent1_Strategy.txt", res.get()[2])



