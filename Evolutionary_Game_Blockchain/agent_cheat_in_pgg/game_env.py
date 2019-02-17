import networkx as nx
import numpy as np


def public_goods_game(s_l, r):
    s_num = len(s_l)
    p_l = []
    p = r * np.sum(s_l) / s_num
    for i in range(s_num):
        p_l.append(p - s_l[i])
    return p_l
    # agent_num = len(strategy)
    # payoffs = np.array([np.sum(strategy)*r/agent_num for _ in range(agent_num)]) - np.array(strategy)
    # return payoffs

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
    adj_link_r, p_num_r, p_edge_r = generate_network(structure='2d_grid')
    # print(adj_link_r)
    # print(p_num_r)
    # print(p_edge_r)
    payoffs_list = public_goods_game([1, 0, 0, 0], 2.0)
    print(payoffs_list)
