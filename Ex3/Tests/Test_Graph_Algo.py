import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):
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
        did_it_work = algo.load_from_json("C:/Users/eliap/IdeaProjects/OOP_2020/Ex3/data/T0.json")
        actual_graph = algo.get_graph()
        self.assertTrue(did_it_work)
        self.assertEqual(expected_graph, actual_graph.__str__())
        self.assertEqual(expected_graph.get_mc(), actual_graph.get_mc().__str__())

    def test_load_from_json_empty_file(self):
        algo = GraphAlgo()
        self.assertRaises(FileNotFoundError, algo.load_from_json, "")

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
        # TODO write the test
        pass

    def test_connected_components(self):
        # TODO write the test
        pass


if __name__ == '__main__':
    unittest.main()
