import csv
import random

file_name = "./datasets/facebook/facebook_combined.txt"
d = 4038
output_label_cnt = 10


def louvain(aim_id):

    class Community(object):
        def __init__(self, v, degree):
            self.vertex = []
            self.inner_edges = 0
            self.total_edges = degree
            self.vertex.append(v)

        def merge(self, n):
            self.inner_edges += community_list[n].inner_edges
            for j in range(len(self.vertex)):
                for k in range(len(community_list[n].vertex)):
                    if adj_matrix[self.vertex[j]][community_list[n].vertex[k]] != 0:
                        self.inner_edges += 1
            self.total_edges += community_list[n].total_edges
            self.vertex.extend(community_list[n].vertex)


    def cal_delta_q(c, n):
        k_i_inner = 0
        for j in range(len(community_list[c].vertex)):
            for k in range(len(community_list[n].vertex)):
                k_i_inner += adj_matrix[community_list[c].vertex[j]][community_list[n].vertex[k]]
        k_i_inner *= 2
        k_i = community_list[n].total_edges - community_list[n].inner_edges
        tmp_delta_q = (k_i_inner / (2 * degree_sum)) - ((community_list[c].total_edges * k_i) / (2 * pow(degree_sum, 2)))
        return tmp_delta_q


    def connect(m, n):
        for ii in range(len(community_list[m].vertex)):
            for jj in range(len(community_list[n].vertex)):
                if adj_matrix[community_list[m].vertex[ii]][community_list[n].vertex[jj]] != 0:
                    return True
        return False

    def PageRank(commu, alpha):
        centrality = [0 for i in range(max(commu.vertex) + 1)]
        for i in commu.vertex:
            centrality[i] = 1/len(commu.vertex)
        k = 0
        while k < 1000:
            # if k % 100 == 0:
                # print(k)
            for i in commu.vertex:
                centrality[i] += (1-alpha)/len(commu.vertex)
                for j in commu.vertex:
                    if adj_matrix[i][j] == 1:
                        centrality[i] += alpha * (centrality[j]/degree_list[j])
            k += 1
        return centrality.index(max(centrality))

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
    degree_sum = sum(degree_list) / 2

    community_list = []
    for i in range(d + 1):
        community_list.append(Community(i, degree_list[i]))

    finish = False
    while not finish:
        # for i in range(len(community_list)):
            # print(i, community_list[i].vertex)
        new_community = [k for k in range(len(community_list))]
        for i in range(len(community_list)):
            max_delta_q = -1
            max_delta_q_index = -1
            for j in range(len(community_list)):
                if i != j and connect(i, j):
                    tmp_cal_delta_q = cal_delta_q(i, j)
                    if tmp_cal_delta_q > max_delta_q:
                        max_delta_q = tmp_cal_delta_q
                        max_delta_q_index = j
            if max_delta_q > 0:
                new_community[i] = new_community[max_delta_q_index]
        for i in range(len(new_community)):
            finish = True
            if new_community[i] != i:
                finish = False
                community_list[new_community[i]].merge(i)
                # print("merge", i, new_community[i])
        del_cnt = 0
        for i in range(len(new_community)):
            if new_community[i] != i:
                community_list.pop(i - del_cnt)
                del_cnt += 1
    label = [[i, 0] for i in range(d + 1)]
    for i in range(len(community_list)):
        for j in range(len(community_list[i].vertex)):
            label[community_list[i].vertex[j]] = [community_list[i].vertex[j], i]

    clu_center = PageRank(community_list[label[aim_id][1]], 0.85)

    return label, edges, clu_center
    # if output_label_cnt > len(community_list):
    #     print("ERROR")
    # else:
    #     output_label_list = random.sample(range(0, len(community_list) + 1), output_label_cnt)
    #
    #     with open("edges1.csv", "w", newline="") as datacsv:
    #         csvwriter = csv.writer(datacsv, dialect=("excel"))
    #         for i in range(len(edges)):
    #             if label[edges[i][0]][1] in output_label_list and label[edges[i][1]][1] in output_label_list:
    #                 csvwriter.writerow(edges[i])
    #     with open("vertex1.csv", "w", newline="") as datacsv:
    #         csvwriter = csv.writer(datacsv, dialect=("excel"))
    #         for i in range(len(label)):
    #             if label[i][1] in output_label_list:
    #                 csvwriter.writerow(label[i])




