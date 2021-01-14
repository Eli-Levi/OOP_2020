import json
import unittest
from json.decoder import JSONDecodeError
import networkx as nx
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):

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

    def test_shortest_path(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        algo.load_from_json("C:/Users/eliap/IdeaProjects/OOP_2020/Ex3/data/T0.json")
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 0, 1.1)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(1, 3, 1.8)
        graph.add_edge(2, 3, 1.1)
        expected_array = [0, 1, 3]
        result = algo.shortest_path(0, 3)
        self.assertEqual(2.8, result[0])
        self.assertEqual(expected_array, result[1])

    def test_shortest_path_non_connected_path(self):
        graph = DiGraph()
        algo = GraphAlgo(graph)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(1, 3, 1.8)
        graph.add_edge(2, 3, 1.1)
        expected_size = float("inf")
        expected_array = []
        result = algo.shortest_path(0, 3)
        self.assertEqual(expected_size, result[0])
        self.assertEqual(expected_array, result[1])

    def test_shortest_path_non_existing_src_node(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(1, 3, 1.8)
        graph.add_edge(2, 3, 1.1)
        expected_size = float("inf")
        expected_array = []
        result = algo.shortest_path(0, 3)
        print(result)
        self.assertEqual(expected_size, result[0])
        self.assertEqual(expected_array, result[1])

    def test_shortest_path_non_existing_dest_node(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 0, 1.1)
        graph.add_edge(1, 2, 1.3)
        expected_size = float("inf")
        expected_array = []
        result = algo.shortest_path(0, 3)
        self.assertEqual(expected_size, result[0])
        self.assertEqual(expected_array, result[1])

    def test_load_from_json(self):
        expected_graph = DiGraph()
        expected_graph.add_node(0)
        expected_graph.add_node(1)
        expected_graph.add_node(2)
        expected_graph.add_node(3)
        expected_graph.add_edge(0, 1, 1)
        expected_graph.add_edge(1, 0, 1.1)
        expected_graph.add_edge(1, 2, 1.3)
        expected_graph.add_edge(1, 3, 1.8)
        expected_graph.add_edge(2, 3, 1.1)
        algo = GraphAlgo()
        did_it_work = algo.load_from_json("C:/Users/eliap/IdeaProjects/OOP_2020/Ex3/data/G_10_80_1.json")
        actual_graph = algo.get_graph()
        self.assertTrue(did_it_work)
        self.assertTrue(expected_graph.__eq__(actual_graph))

    def test_load_from_json_file_not_exist(self):
        algo = GraphAlgo()
        self.assertRaises(FileNotFoundError, algo.load_from_json, "")

    def test_load_from_json_emtpy_file(self):
        algo = GraphAlgo()
        self.assertRaises(JSONDecodeError or ResourceWarning, algo.load_from_json,
                          "C:/Users/eliap/IdeaProjects/OOP_2020/Ex3/data/New.json")

    def test_save_to_json(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 0, 1.1)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(1, 3, 1.8)
        graph.add_edge(2, 3, 1.1)
        did_it_work = algo.save_to_json("graph test")
        self.assertTrue(did_it_work)

    def test_save_to_json_None_graph(self):
        algo = GraphAlgo()
        did_it_work = algo.save_to_json("None graph")
        self.assertFalse(did_it_work)

    def test_connected_component(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)
        graph.add_node(5)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(2, 1, 2.4)
        graph.add_edge(3, 1, 1.8)
        graph.add_edge(4, 1, 3)
        graph.add_edge(1, 4, 0.8)
        graph.add_edge(1, 5, 3.5)
        graph.add_edge(5, 1, 0.9)
        expected_scc = [1, 2, 4, 5]
        actual_scc = algo.connected_component(1)
        self.assertEqual(expected_scc, actual_scc)

    def test_connected_component_non_existing_node(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)
        graph.add_node(5)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(2, 1, 2.4)
        graph.add_edge(3, 1, 1.8)
        graph.add_edge(4, 1, 3)
        graph.add_edge(1, 4, 0.8)
        graph.add_edge(1, 5, 3.5)
        graph.add_edge(5, 1, 0.9)
        expected_scc = []
        actual_scc = algo.connected_component(10)
        self.assertEqual(expected_scc, actual_scc)

    def test_connected_component_non_existing_graph(self):
        algo = GraphAlgo()
        expected_scc = []
        actual_scc = algo.connected_component(0)
        self.assertEqual(expected_scc, actual_scc)

    def test_connected_component_single_node_scc(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4)
        graph.add_node(5)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(2, 1, 2.4)
        graph.add_edge(3, 1, 1.8)
        graph.add_edge(4, 1, 3)
        graph.add_edge(1, 4, 0.8)
        graph.add_edge(1, 5, 3.5)
        graph.add_edge(5, 1, 0.9)
        expected_scc = [0]
        actual_scc = algo.connected_component(0)
        self.assertEqual(expected_scc, actual_scc)

    def test_connected_components(self):
        graph = DiGraph()
        algo = GraphAlgo()
        algo.__init__(graph)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 0, 1.1)
        graph.add_edge(1, 2, 1.3)
        graph.add_edge(1, 3, 1.8)
        graph.add_edge(2, 3, 1.1)
        expected_scc = [[0, 1], [2], [3]]
        actual_scc = algo.connected_components()
        self.assertEqual(expected_scc, actual_scc)

    def test_connected_components_non_existing_graph(self):
        algo = GraphAlgo()
        expected_scc = []
        actual_scc = algo.connected_components()
        self.assertEqual(expected_scc, actual_scc)



if __name__ == '__main__':
    unittest.main()
