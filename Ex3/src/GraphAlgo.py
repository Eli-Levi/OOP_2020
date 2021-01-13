import json
from typing import List
import matplotlib.pyplot as plt


from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph, Node
from queue import PriorityQueue


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: DiGraph = None):
        self.__graph = graph

    def get_graph(self) -> DiGraph:
        return self.__graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            self.__graph = DiGraph()

            file = open(file_name)
            graph_of_file = json.load(file)

            edgeslist = graph_of_file.get('Edges')
            nodeslist = graph_of_file.get('Nodes')
            for i in nodeslist:
                key = i.get('id')

                if i.get('pos') is not None:
                    pos = str(i.get('pos'))
                    n = Node(key, pos)
                    self.__graph.add_node(n)
                else:
                    self.__graph.add_node(key)

            for i in edgeslist:
                src = i.get('src')
                dest = i.get('dest')
                w = i.get('w')

                self.__graph.add_edge(src, dest, w)

            file.close()

        except FileExistsError:
            return False

        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.get_graph().v_size() < 2:
            return -1, []
        if self.get_graph().v_size() == 2:
            if id2 in self.get_graph().all_out_edges_of_node(id1):
                return self.get_graph().all_out_edges_of_node(id1)[id2], [id1, id2]

        else:
            if id1 in self.get_graph().dictionary and id2 in self.get_graph().dictionary:
                pq = PriorityQueue()
                cost = dict()
                path = dict()
                cost[id1] = 0
                w = -1.0
                pq.put((cost[id1], id1))
                while not pq.empty():
                    n = pq.get()

                    if self.get_graph().all_out_edges_of_node(n[1]) is not None:
                        for i in self.get_graph().all_out_edges_of_node(n[1]):
                            ni = i
                            if not ni in cost:
                                cost[ni] = cost.get(n[1]) + self.get_graph().all_out_edges_of_node(n[1]).get(ni)
                                pq.put((cost[ni], ni))
                                path[ni] = n[1]
                            elif cost[ni] > cost.get(n[1]) + self.get_graph().all_out_edges_of_node(n[1]).get(ni):
                                cost[ni] = cost.get(n[1]) + self.get_graph().all_out_edges_of_node(n[1]).get(ni)
                                pq.put((cost[ni], ni))
                                path[ni] = n[1]
                            if ni == id2:
                                if w == -1.0:
                                    w = cost[ni]
                                else:
                                    w = min(w, cost[ni])
                if w == -1.0:
                    return -1, []
                else:
                    revpathlist = []
                    x = id2
                    revpathlist.append(x)
                    while not x == id1:
                        revpathlist.append(path.get(x))
                        x = path.get(x)
                    revpathlist.reverse()

                    return w, revpathlist

    def connected_component(self, id1: int) -> list:
        cheacklist = set()
        rcheacklist = set()
        self.dfs(cheacklist, id1)
        self.rdfs(rcheacklist, id1)

        scc = []
        for i in cheacklist:
            if i in rcheacklist:
                scc.append(i)
        return scc

    def connected_components(self) -> List[list]:
        scclist = []
        cheack = set()
        for key, v in self.get_graph().get_all_v():
            if key not in cheack:
                cuclist = self.connected_component(key)
                for i in cuclist:
                    cheack.add(i)
                scclist.append(cuclist)

        return scclist

    def plot_graph(self) -> None:
        pass

    def save_to_json(self, file_name: str) -> bool:
        if self.__graph is None:
            return False

        nodeslist = []
        for key, node in self.get_graph().get_all_v():
            pos = node.get_position()

            if pos is not None:
                pos_str = str(pos[0]) + ',' + str(pos[1]) + "," + str(pos[2])
                nodeslist.append({"pos": pos_str, "id": key})

            nodeslist.append({"id": key})

        edgeslist = []
        for key, node in self.get_graph().get_all_v():
            for dest, w in self.get_graph().all_out_edges_of_node(key).items():
                edgeslist.append({"src": key, "dest": dest, "w": w})

        graph_data = {"Edges": edgeslist, "Nodes": nodeslist}

        with open(file_name, 'w') as json_file:
            json.dump(graph_data, json_file)
        return True

    def dfs(self, cheacklist, node):
        if node not in cheacklist:
            cheacklist.add(node)
            if self.get_graph().all_out_edges_of_node(node) is not None:
                for neighbour in self.get_graph().all_out_edges_of_node(node):
                    self.dfs(cheacklist, neighbour)

    def rdfs(self, cheacklist, node):
        if node not in cheacklist:
            cheacklist.add(node)
            if self.get_graph().all_in_edges_of_node(node) is not None:
                for neighbour in self.get_graph().all_in_edges_of_node(node):
                    self.rdfs(cheacklist, neighbour)
