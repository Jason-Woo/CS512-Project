import networkx as nx
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


def show_img(edges, size, center, user):
    g = nx.Graph(edges)
    node_size = [20 for i in range(size)]
    node_size[center] = 60
    node_size[user] = 60
    node_color = ['black' for i in range(size)]
    node_color[center] = 'r'
    node_color[user] = 'blue'
    nx.draw(g, node_color=[node_color[v] for v in g], node_size=[node_size[v] for v in g], linecolor='gray', linewidths=0, width=0.1)
    plt.savefig('tmp.png')
    distance = nx.dijkstra_predecessor_and_distance(g, center)[1]
    return max(distance.values()), (g.degree[center]/len(distance))*100



