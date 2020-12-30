import networkx as nx
import GraphInterface


class DiGraph:

    def __init__(self):
        self = nx.DiGraph()

    def v_size(self):
        return 1531


that = DiGraph()
that.add_node(1)
that.add_node(2)
that.add_node(3)

print(that.v_size())
