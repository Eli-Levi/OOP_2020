import json
from typing import List

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
                n = self.get_graph().dictionary.get(id1)
                cost[id1] = 0
                w = -1.0
                pq.put(cost[id1], id1)
                while not pq.empty():
                    n = pq.get()
                    for i in self.get_graph().all_out_edges_of_node(n):
                        ni = i
                        if not ni in cost:
                            cost[ni] = cost.get(n.getKey) + self.get_graph().all_out_edges_of_node(n).get(ni)
                            pq.put(cost[ni], ni)
                            path[ni] = n
                        elif cost[ni] > cost.get(n.getKey) + self.get_graph().all_out_edges_of_node(n).get(ni):
                            cost[ni] = cost.get(n.getKey) + self.get_graph().all_out_edges_of_node(n).get(ni)
                            pq.put(cost[ni], ni)
                            path[ni] = n
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
                    while x == id1:
                        revpathlist.__add__(path[x])
                        x = path[x]
                    revpathlist.__add__(id1)

                    return w, revpathlist.reverse()

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

    def save_to_json(self, file_name: str) -> bool:
        if self.__graph is None:
            return False

        nodeslist = []
        for i in self.get_graph().get_all_v():
            # TODO
            key = i
            pos = self.get_graph().get_node(key).get_location()

            if pos.get_x() is not None:
                pos_str = str(pos.get_x()) + ',' + str(pos.get_y()) + "," + str(pos.get_z())
                nodeslist.append({"pos": pos_str, "id": key})

            nodeslist.append({"id": key})

        edgeslist = []
        for i in self.get_graph().get_all_v():
            for j in self.get_graph().get_neighbors(i):
                edgeslist.append({"src": j.get_src(), "dest": j.get_dest(), "w": j.get_weight()})

        graph_data = {"Edges": edgeslist, "Nodes": nodeslist}

        with open(file_name, 'w') as json_file:
            json.dump(graph_data, json_file)
        return True
