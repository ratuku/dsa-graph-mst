""" This module defines the Graph class. Graph can be directed or undirected. It can also be weighted or unweighted.
But can't have negative weights """
from _pytest import nodes


class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}
        #self.visited = False
        #self.distance = float("inf")

    def _add_edge(self, node_name: str, weight: float = 1.0):
        self.edges[node_name] = weight

    def get_name(self) -> str:
        return self.name

    def get_edges(self) -> dict:
        return self.edges

class Graph:
    def __init__(self, directed=False, weighted=False):
        self.nodes = {}
        self.directed = directed
        self.weighted = weighted

    def get_node(self, name) -> Node:
        node = self.nodes.get(name)
        if node is None:
            error = "Node {} not found in graph".format(name)
            raise ValueError(error)
        return node

    def add_node(self, node: Node):
        self.nodes[node.name] = node

    def add_edge(self, node1: Node, node2: Node, weight: float = 1.0):
        if weight < 0:
            error = "Weight must be positive"
            raise ValueError(error)

        if weight != 1.0 and self.weighted == False:
             error = "Unweighted Graph can't have weights" # All edges should have a weight of 1.0 for unweighted graph
             raise ValueError(error)

        self.nodes[node1.name]._add_edge(node2.name, weight)
        if not self.directed:
            self.nodes[node2.name]._add_edge(node1.name, weight)

    def __str__(self) -> str:
        output = []
        header = "\n"
        if self.directed:
            header += "Directed, "
        else:
            header += "Undirected, "

        if self.weighted:
            header += "Weighted"
        else:
            header += "Unweighted"
        output.append(header)

        for node_name in self.nodes:
            node_edges = ", ".join(f"{key}({weight})" for key, weight in self.nodes[node_name].edges.items())
            output.append(f"{node_name} ->> {node_edges}")
        return "\n".join(output)

    def get_copy(self):
        graph_c = Graph(directed=self.directed, weighted=self.weighted)
        for node_name in self.nodes:
            node_copy = Node(name=node_name)
            graph_c.add_node(node_copy)

            # get current node's edge destination name and copy it
            original_node_edge_dict = self.nodes[node_name].edges
            for destination_name, weight in original_node_edge_dict.items():
                node_copy.edges[destination_name] = weight

        return graph_c

    def get_nodes(self):
        return self.nodes.values()

    def get_node_names(self):
        return self.nodes.keys()

    def neighbors(self, node_name: str) -> dict:
        return self.nodes[node_name].edges

    def is_weighted(self) -> bool:
        return self.weighted