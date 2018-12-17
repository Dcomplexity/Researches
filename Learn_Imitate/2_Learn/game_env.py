import networkx as nx
import numpy as np
from itertools import permutations


# Generate the list of actions available in this game
def get_actions():
    defect = 0
    cooperate = 1
    actions = np.array([defect, cooperate])
    return actions


# Generate the list of states available in this game
def gen_states(actions):
    states = []
    for _ in permutations(actions):
        states.append(_)
    for _ in actions:
        states.append((_, _))
    states.sort()
    return states


def pd_game(a_x, a_y):
    t = 5.0; r = 3.0; p = 1.0; s = 0.0
    if (a_x, a_y) == (1, 1):
        return r, r
    elif (a_x, a_y) == (1, 0):
        return s, t
    elif (a_x, a_y) == (1, 0):
        return t, s
    elif (a_x, a_y) == (0, 0):
        return p, p
    else:
        return 'Error'


def pd_game_b(a_x, a_y, b):
    if (a_x, a_y) == (1, 1):
        return 1, 1
    elif (a_x, a_y) == (1, 0):
        return 0, b
    elif (a_x, a_y) == (0, 1):
        return b, 0
    elif (a_x, a_y) == (0, 0):
        return 0, 0
    else:
        return 'Error'


def generate_network(structure, xdim=100, ydim=100):
    if structure == '2d_grid':
        g_network = nx.grid_2d_graph(xdim, ydim, periodic=True)
        adj_array = nx.to_numpy_array(g_network)
        adj_link = []
        for i in range(adj_array.shape[0]):
            adj_link.append(np.where(adj_array[i] == 1)[0])
        population_num = xdim * ydim
    return np.array(adj_link), population_num


def alpha_time(time_step):
    return 1 / (10 + 0.002 * time_step)


def epsilon_time(time_step):
    return 0.5 / (1 + 0.0001 * time_step)


if __name__ == "__main__":
    adj_link_v, p_num_v = generate_network(structure='2d_grid')
    print(adj_link_v)
