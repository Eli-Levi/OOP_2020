import unittest
from DiGraph import DiGraph


class MyTestCase(unittest.TestCase):

    def test_add_node(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        self.assertEqual(1, graph.v_size())

    def test_add_node_twice(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        result = graph.add_node(1, (1, 1))
        self.assertFalse(result)

    def test_number_of_nodes_in_graph(self):
        graph = DiGraph()
        for i in range(10):
            graph.add_node(i, (i, i))
        self.assertEqual(10, graph.v_size())

    def test_add_negative_node_id(self):
        graph = DiGraph()
        result = graph.add_node(-1, (15, 10))
        self.assertFalse(result)

    def test_add_edge(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        graph.add_node(2, (2, 2))
        result = graph.add_edge(1, 2, 10)
        self.assertTrue(result)

    def test_add_edge_multiple_nodes_one_dest(self):
        graph = DiGraph()
        for i in range(3):
            graph.add_node(i, (i, i))
        for i in range(1, 3):
            graph.add_edge(i, 0, 10 + i)
        num_of_edges = graph.e_size()
        self.assertTrue(2, num_of_edges)
        self.assertEqual(2, len(graph.all_in_edges_of_node(0)))
        self.assertIn(1, graph.all_in_edges_of_node(0).keys())
        self.assertIn(2, graph.all_in_edges_of_node(0).keys())

    def test_add_edge_multiple_nodes_one_src(self):
        graph = DiGraph()
        for i in range(3):
            graph.add_node(i, (i, i))
        graph.add_edge(0, 1, 10)
        graph.add_edge(0, 2, 20)
        self.assertEqual(2, len(graph.all_out_edges_of_node(0)))
        self.assertEqual(1, len(graph.all_in_edges_of_node(1)))
        self.assertEqual(1, len(graph.all_in_edges_of_node(2)))
        self.assertEqual(2, graph.e_size())

    def test_add_edge_to_same_node(self):
        graph = DiGraph()
        for i in range(2):
            graph.add_node(i, (i, i))

        graph.add_edge(0, 1, 10)
        result = graph.add_edge(0, 1, 20)
        self.assertFalse(result)

    def test_add_edge_to_non_existing_src_node(self):
        graph = DiGraph()
        graph.add_node(1, (0, 0))
        result = graph.add_edge(0, 1, 10)
        self.assertFalse(result)

    def test_add_edge_to_non_existing_dest_node(self):
        graph = DiGraph()
        graph.add_node(1, (0, 0))
        result = graph.add_edge(1, 0, 10)
        self.assertFalse(result)

    def test_add_negative_edge(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        graph.add_node(2, (2, 2))
        result = graph.add_edge(1, 2, -10)
        self.assertFalse(result)

    def test_remove_node(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        graph.remove_node(1)
        self.assertEqual(0, graph.v_size())

    def test_remove_non_existing_node(self):
        graph = DiGraph()
        result = graph.remove_node(0)
        self.assertFalse(result)

    def test_remove_node_and_connected_edge(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        graph.add_node(2, (2, 2))
        graph.add_edge(1, 2, 10)
        graph.remove_node(2)
        print(graph.all_out_edges_of_node(1).keys())
        self.assertNotIn(2, graph.all_out_edges_of_node(1).keys())
        self.assertEqual(0, len(graph.all_out_edges_of_node(1).keys()))

    def test_remove_edge(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        graph.add_node(2, (2, 2))
        graph.add_edge(1, 2, 10)
        graph.remove_edge(1, 2)
        self.assertEqual(0, graph.e_size())

    def test_remove_non_existing_edge(self):
        graph = DiGraph()
        graph.add_node(1, (1, 1))
        graph.add_node(2, (2, 2))
        result = graph.remove_edge(1, 2)
        self.assertFalse(result)
        self.assertEqual(0, graph.e_size())


if __name__ == '__main__':
    unittest.main()
