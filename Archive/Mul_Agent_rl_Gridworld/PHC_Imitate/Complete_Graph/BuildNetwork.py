import numpy as np
import networkx as nx

class buildNetwork:
    def __init__(self, agentAmount):
        self.agentAmount = agentAmount
        self.network = {}
        for i in range(self.agentAmount):
            self.network[i] = []

    def completegraph(self):
        G = nx.complete_graph(self.agentAmount)
        for i in range(self.agentAmount):
            self.network[i] = [n for n in G.neighbors(i)]
        return self.network

    def circle(self):
        for i in range(self.agentAmount):
            self.network[i].append((i + 1) % self.agentAmount)
        return self.network

    def lattice(self, m, n):
        G = nx.grid_2d_graph(m, n, periodic=True)
        if self.agentAmount != m*n:
            return ("error, The agentAmount does not equal to the dimension of network")
        else:
            for i in range(m*n):
                self.network[i] = [nn[0]*n+nn[1] for nn in G.neighbors((i//n, i-(i//n)*n))]
        return self.network

    def regulargraph(self, degree):
        G = nx.random_regular_graph(degree, self.agentAmount)
        for i in range(self.agentAmount):
            self.network[i] = [n for n in G.neighbors(i)]
        return self.network

    def WSnetwork(self, nearneigh, prob):
        G = nx.connected_watts_strogatz_graph(self.agentAmount, nearneigh, prob)
        for i in range(self.agentAmount):
            self.network[i] = [n for n in G.neighbors(i)]
        return self.network

    def BAnetwork(self, edgesNum):
        G = nx.barabasi_albert_graph(self.agentAmount, m=edgesNum)
        for i in range(self.agentAmount):
            self.network[i] = [n for n in G.neighbors(i)]
        return self.network


if __name__ == "__main__":
    network = buildNetwork(25).WSnetwork(nearneigh=4, prob=0.5)
    print(network)
    degree = 0
    for i in network.keys():
        degree += len(network[i])
    print (degree / 25)
