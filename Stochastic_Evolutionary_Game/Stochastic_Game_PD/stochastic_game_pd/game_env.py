import networkx as nx
import numpy as np


def pd_game_0(a_x, a_y):
    if (a_x, a_y) == (1, 1):
        return 3, 3
    elif (a_x, a_y) == (1, 0):
        return 0, 10
    elif (a_x, a_y) == (0, 1):
        return 10, 0
    elif (a_x, a_y) == (0, 0):
        return 2, 2
    else:
        return "ERROR"


def pd_game_1(a_x, a_y):
    if (a_x, a_y) == (1, 1):
        return 4, 4
    elif (a_x, a_y) == (1, 0):
        return 0, 10
    elif (a_x, a_y) == (0, 1):
        return 10, 0
    elif (a_x, a_y) == (0, 0):
        return 1, 1
    else:
        return "ERROR"


def pd_game_2(a_x, a_y):
    if (a_x, a_y) == (1, 1):
        return 4, 4
    elif (a_x, a_y) == (1, 0):
        return 4, 4
    elif (a_x, a_y) == (0, 1):
        return 4, 4
    elif (a_x, a_y) == (0, 0):
        return 4, 4
    else:
        return "ERROR"


# Transition Matrix:
# s0->s1 |0.1 0.9| s1->s0 |0.1 0.9|
#        |0.9 0.1|        |0.9 0.1|
def transition_matrix(s, a_x, a_y):
    t_m = [0.1, 0.9, 0.9, 0.1, 0.1, 0.9, 0.9, 0.1]
    return t_m[s*(2**2) + a_x + a_y]


def next_state(s, a_x, a_y):
    prob = transition_matrix(s, a_x, a_y)
    if np.random.random() < prob:
        s_ = 1 - s
    else:
        s_ = s
    return s_


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
