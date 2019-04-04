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
    return np.array(adj_link), population_num
