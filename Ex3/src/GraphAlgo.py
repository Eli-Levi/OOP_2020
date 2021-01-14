import json
from typing import List
#import matplotlib.pyplot as plt
import networkx as nx

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
                    self.__graph.add_node(n.get_key(), n.get_position())
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

        self.__init__(self.__graph)
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.__graph.v_size() < 2:
            return float("inf"), []
        if self.get_graph().v_size() == 2:
            if id2 in self.get_graph().all_out_edges_of_node(id1):
                return self.get_graph().all_out_edges_of_node(id1)[id2], [id1, id2]

        else:
            if id1 in self.get_graph().dictionary and id2 in self.get_graph().dictionary:
                pq = PriorityQueue()
                cost = dict()
                path = dict()
                cost[id1] = 0
                w = float("inf")
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
                                w = min(w, cost[ni])
                if w == float("inf"):
                    return w, []
                else:
                    revpathlist = []
                    x = id2
                    revpathlist.append(x)
                    while not x == id1:
                        revpathlist.append(path.get(x))
                        x = path.get(x)
                    revpathlist.reverse()

                    return w, revpathlist
            else:
                return float("inf"), []

    def connected_component(self, id1: int) -> list:
        if self.get_graph() is None:
            return []
        if id1 not in self.get_graph().dictionary:
            return []
        cheacklist = set()
        rcheacklist = set()
        oder = [id1]
        for node in oder:
            if node not in cheacklist:
                cheacklist.add(node)
                if self.get_graph().all_out_edges_of_node(node) is not None:
                    for neighbour in self.get_graph().all_out_edges_of_node(node):
                        oder.append(neighbour)
        oder.clear()
        oder.append(id1)
        for node in oder:
            if node not in rcheacklist:
                rcheacklist.add(node)
                if self.get_graph().all_in_edges_of_node(node) is not None:
                    for neighbour in self.get_graph().all_in_edges_of_node(node):
                        oder.append(neighbour)

        scc = []
        for i in cheacklist:
            if i in rcheacklist:
                scc.append(i)
        return scc

    def connected_components(self) -> List[list]:
        if self.get_graph() is None:
            return []
        scclist = []
        cheack = set()
        for key, v in self.get_graph().get_all_v():
            if key not in cheack:
                cuclist = self.connected_component(key)
                for i in cuclist:
                    cheack.add(i)
                scclist.append(cuclist)

        return scclist

    #TODO modify the function
    # def plot_graph(self) -> None:
    #     if self.get_graph() is None:
    #         return
    #
    #     x_values = []
    #     y_values = []
    #
    #     for i in self.get_graph().get_all_v():
    #         node = self.get_graph().get_node(i)
    #
    #         if node.get_location().get_x() is None or node.get_location().get_y() is None:
    #             node.set_location(GeoLocation(random.uniform(0, 100), random.uniform(0, 100)))
    #
    #         position = [node.get_location().get_x(), node.get_location().get_y()]
    #
    #         x_values.append(position[0])
    #         y_values.append(position[1])
    #         plt.text(position[0], position[1], node.get_key(), color='green')
    #
    #     plt.plot(x_values, y_values, '.', color='red')
    #
    #     for i in self.get_graph().get_all_v():
    #         node = self.get_graph().get_node(i)
    #         src_position = [node.get_location().get_x(), node.get_location().get_y()]
    #
    #         for j in self.get_graph().get_neighbors(i):
    #             dest = self.get_graph().get_node(j.get_dest())
    #             dest_position = [dest.get_location().get_x(), dest.get_location().get_y()]
    #
    #             delta_x = float(dest_position[0]) - float(src_position[0])
    #             delta_y = float(dest_position[1]) - float(src_position[1])
    #             distance = (delta_x ** 2 + delta_y ** 2) ** 0.5
    #
    #             plt.arrow(src_position[0], src_position[1], delta_x, delta_y, width=0.01 * distance, color='black')
    #
    #     plt.title(self.get_graph())
    #     plt.show()

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

    def load_from_json_nx(self, file_name: str):
        try:
            graph = nx.DiGraph()
            file = open(file_name)
            graph_of_file = json.load(file)

            edgeslist = graph_of_file.get('Edges')
            nodeslist = graph_of_file.get('Nodes')
            for i in nodeslist:
                key = i.get('id')

                if i.get('pos') is not None:
                    pos = list()
                    for i in i.get('pos').split(','):
                        i = float(i)
                        pos.append(i)
                    pos = tuple(pos)
                    graph.add_node(key, pos=pos)
                else:
                    graph.add_node(key)

            for i in edgeslist:
                src = i.get('src')
                dest = i.get('dest')
                w = i.get('w')

                graph.add_edge(src, dest, weight=w)

            file.close()

        except FileExistsError:
            return False

        return graph
