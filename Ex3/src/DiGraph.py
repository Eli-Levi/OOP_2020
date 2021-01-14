from GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.mc = 0
        self.num_of_edges = 0
        self.dictionary = {}

    def v_size(self):
        return len(self.dictionary)

    def e_size(self):
        return self.num_of_edges

    def get_all_v(self):
        return self.dictionary.items()

    def all_in_edges_of_node(self, id1: int):
        n = self.dictionary[id1]
        return n.get_incoming_edges()

    def all_out_edges_of_node(self, id1: int):
        if id1 in self.dictionary:
            n = self.dictionary[id1]
            return n.get_outgoing_edges()

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.dictionary or id2 not in self.dictionary:
            return False
        is_id2_in_id1 = id2 in self.dictionary.get(id1).get_outgoing_edges()
        if weight < 0:
            return False
        if not is_id2_in_id1:
            src_node = self.dictionary.get(id1)
            dest_node = self.dictionary.get(id2)
            src_node.outgoing_edges[id2] = weight
            dest_node.incoming_edges[id1] = weight
            self.num_of_edges += 1
            return True
        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id < 0:
            print("Node id can't be a negative value")
            return False
        graph = self.dictionary
        if node_id not in graph:
            node = Node(node_id, pos)
            graph[node_id] = node
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        graph = self.dictionary
        if node_id in graph:
            for i in list(graph[node_id].get_incoming_edges().keys()):
                self.remove_edge(i, node_id)
            for i in list(graph[node_id].get_outgoing_edges().keys()):
                self.remove_edge(node_id, i)
            del graph[node_id]
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.dictionary.keys() or node_id2 not in self.dictionary.keys():
            return False

        is_id1_in_id2 = node_id1 in self.dictionary[node_id2].get_incoming_edges()
        if is_id1_in_id2:
            src_node = self.dictionary.get(node_id1)
            dest_node = self.dictionary.get(node_id2)
            del src_node.outgoing_edges[node_id2]
            del dest_node.incoming_edges[node_id1]
            self.num_of_edges -= 1
            return True
        return False

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.e_size() != other.e_size():
            return False
        if self.v_size() != other.v_size():
            return False
        for key in self.dictionary:
            if self.dictionary.get(key) != other.dictionary.get(key):
                return False
        return True

    def __str__(self):
        return "Graph has: " + str(self.get_all_v().values()) + " nodes and " + str(self.e_size()) + " edges\n"


class Node:
    def __init__(self, key: int, position: tuple):
        self.key = key
        self.incoming_edges = {}
        self.outgoing_edges = {}
        self.position = position

    def get_incoming_edges(self):
        return self.incoming_edges

    def get_outgoing_edges(self):
        return self.outgoing_edges

    def set_incoming_edges(self, node_id: int, weight: float):
        if node_id not in self.incoming_edges.keys():
            self.incoming_edges[node_id] = weight
            return True
        return False

    def get_position(self):
        return self.position

    def set_position(self, pos):
        self.position = pos

    def get_key(self):
        return self.key

    def __eq__(self, other):
        if self.position != other.position:
            return False
        for key in self.incoming_edges:
            if self.incoming_edges.get(key) != other.incoming_edges.get(key):
                return False
        for key in self.outgoing_edges:
            if self.outgoing_edges.get(key) != other.outgoing_edges.get(key):
                return False
        return True

    '''def __str__(self):
        return "node incoming edges are: " \
               + str(self.incoming_edges()) \
               + " , node outgoing edges are: " \
               + str(self.outgoing_edges) \
               + " and node position is: " \
               + str(self.get_position())'''
