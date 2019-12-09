from Louvain import *
from Walktrap import *
from Visualization import *

aim_id = 20

if __name__ == '__main__':
    label, edges, center = louvain(aim_id)
    aim_cluster = label[aim_id][1]
    aim_community = []
    aim_edges = []
    for i in range(len(label)):
        if label[i][1] == aim_cluster:
            aim_community.append(label[i][0])
    for i in range(len(edges)):
        if edges[i][0] in aim_community and edges[i][0] in aim_community:
            aim_edges.append(edges[i])
    print(center)
    show_img(aim_edges, len(label), center)
