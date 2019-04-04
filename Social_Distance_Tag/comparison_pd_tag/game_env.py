import networkx as nx
import numpy as np


def pd_game(strategy0, strategy1, b):
    if strategy0 == 1 and strategy1 == 1:
        return 1, 1
    elif strategy0 == 1 and strategy1 == 0:
        return 0, b
    elif strategy0 == 0 and strategy1 == 1:
        return b, 0
    elif strategy0 == 0 and strategy1 == 0:
        return 0, 0
    else:
        return "Error"


def generate_network(structure, xdim=100, ydim=100):
    if structure == "2d_grid":
        g_network = nx.grid_2d_graph(xdim, ydim, periodic=True)
        adj_array = nx.to_numpy_array(g_network)
        adj_link = []
        for i in range(adj_array.shape[0]):
            adj_link.append(np.where(adj_array[i] == 1)[0])
        population_num = xdim * ydim
        g_edge = nx.Graph()
        for i in range(len(adj_link)):
            for j in range(len(adj_link[i])):
                g_edge.add_edge(i, adj_link[i][j])
    return np.array(adj_link), population_num, np.array(g_edge.edges())


if __name__ == "__main__":
    adj_link_v, p_num_v, p_edge = generate_network(structure='2d_grid')
    print(adj_link_v)
    print(p_num_v)
    print(p_edge)
