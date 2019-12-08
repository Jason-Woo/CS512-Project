import csv
import random
import numpy as np

file_name = "./datasets/facebook/facebook_combined.txt"
d = 4038
output_label_cnt = 50
k = 3
cluster_num = 50


class Community(object):
    def __init__(self, id, v_list):
        self.id = id
        self.children = []
        self.vertex = []
        for i in range(len(v_list)):
            self.vertex.append(v_list[i])

    def get_degree(self):
        return len(self.vertex)


if __name__ == '__main__':
    edges = []
    adj_matrix = [[0 for col in range(d + 1)] for row in range(d + 1)]
    f = open(file_name)
    for line2 in open(file_name):
        (ele1, ele2) = line2.split()
        adj_matrix[int(ele1)][int(ele2)] = 1
        adj_matrix[int(ele2)][int(ele1)] = 1

        edges.append([int(ele1), int(ele2)])

    degree_list = []
    for i in range(d + 1):
        degree_list.append(sum(adj_matrix[i]))

    p = np.zeros((d + 1, d + 1))
    r = np.zeros((d + 1, d + 1))
    delta_sigma = np.zeros((d + 1, d + 1))
    print("0")
    community_list = []
    vertex_list = []
    for i in range(d + 1):
        community_list.append(Community(i, [i]))
        vertex_list.append(i)
        for j in range(d + 1):
            p[i][j] = adj_matrix[i][j] / degree_list[i]
    print("1")
    p_to_k = np.ones((d + 1, d + 1))
    for i in range(k):
        p_to_k = np.dot(p_to_k, p)
    print("2")
    for i in range(d + 1):
        for j in range(d + 1):
            r_ij = 0
            for m in range(d + 1):
                r_ij += pow(p_to_k[i][m] - p_to_k[j][m], 2) / degree_list[m]
            r[i][j] = np.sqrt(r_ij)
        print(i)
    r_2 = np.dot(r, r)
    print("3")
    for i in range(d + 1):
        for j in range(d + 1):
            delta_sigma = r_2[i][j] / 2
    print("4")
    while len(vertex_list) > cluster_num:
        print(len(vertex_list))
        min_num = 999999
        min_index = [-1, -1]
        for i in range(len(delta_sigma)):
            for j in range(len(delta_sigma)):
                if i in vertex_list and j in vertex_list and delta_sigma[i][j] < min_num:
                    min_num = delta_sigma[i][j]
                    min_index = [i, j]
        print(min_index)
        new_community = Community(len(community_list), community_list[min_index[0]].vertex + community_list[min_index[1]].vertex)
        vertex_list.append(len(community_list))
        vertex_list.remove(min_index[0])
        vertex_list.remove(min_index[1])
        print("merge", min_index[0], min_index[1])
        community_list.append(new_community)

        new_delta_q1 = np.zeros((len(delta_sigma), 1))
        new_delta_q2 = np.zeros((1, len(delta_sigma) + 1))
        c1 = community_list[min_index[0]].get_degree()
        c2 = community_list[min_index[1]].get_degree()
        for i in range(len(delta_sigma)):
            c = community_list[i].get_degree()
            new_delta_q = (c1 + c) * delta_sigma[min_index[0]][i] + (c2 + c) * delta_sigma[min_index[1]][i] - c * delta_sigma[min_index[0]][min_index[1]]
            new_delta_q1[i][1] = new_delta_q
            new_delta_q2[1][i] = new_delta_q
        delta_sigma = np.append(delta_sigma, new_delta_q1, axis=1)
        delta_sigma = np.append(delta_sigma, new_delta_q2, axis=0)

    label = np.zeros((d + 1, 2))
    for i in range(len(vertex_list)):
        for j in range(community_list[vertex_list[i]].get_degree()):
            label[community_list[vertex_list[i]].vertex[j]] = i

    if output_label_cnt > len(community_list):
        print("ERROR")
    else:
        output_label_list = random.sample(range(0, len(community_list) + 1), output_label_cnt)

        with open("walktrap_edges1.csv", "w", newline="") as datacsv:
            csvwriter = csv.writer(datacsv, dialect=("excel"))
            for i in range(len(edges)):
                if label[edges[i][0]][1] in output_label_list and label[edges[i][1]][1] in output_label_list:
                    csvwriter.writerow(edges[i])
        with open("walk_trapvertex1.csv", "w", newline="") as datacsv:
            csvwriter = csv.writer(datacsv, dialect=("excel"))
            for i in range(len(label)):
                if label[i][1] in output_label_list:
                    csvwriter.writerow(label[i])








