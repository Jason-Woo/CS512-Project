import networkx as nx
import matplotlib.pyplot as plt


def show_img(edges, size, center):
    g = nx.Graph(edges)
    node_size = [30 for i in range(size)]
    node_size[center] = 70
    node_color = ['b' for i in range(size)]
    node_color[center] = 'r'
    nx.draw(g, node_color=[node_color[v] for v in g], node_size=[node_size[v] for v in g], linecolor='gray', linewidths=0, width=0.1)
    plt.show()



