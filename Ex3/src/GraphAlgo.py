import json
from typing import List

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph, Node


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
        pass

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
                edgeslist.append({"src": int(j.get_src()), "dest": int(j.get_dest()), "w": float(j.get_weight())})

        graph_data = {"Edges": edgeslist, "Nodes": nodeslist}

        with open(file_name, 'w') as json_file:
            json.dump(graph_data, json_file)
        return True
