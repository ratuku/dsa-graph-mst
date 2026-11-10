from src.model.Graph import Graph
from src.algorithms.union_find import UnionFind


def minimum_spanning_tree(graph: Graph):
    """ Given a connected, undirected, weighted graph,
    find a spanning tree using edges that minimizes the total weight
    . Uses Kruskal's algorithm to find Minimum Spanning Tree (MST).
    It will print-out edges of the tree and total cost of minimum spanning tree."""
    if graph.is_weighted() is False:
        raise ValueError("Graph is not weighted")

    nodes = graph.get_nodes()
    edges = get_undirected_edges(graph)
    edges.sort(key=lambda e: e[0])

    total_cost = 0
    number_of_edges = 0
    uf = UnionFind(graph.get_node_names())
    mst_edges = []

    for weight, node1, node2 in edges:
        if uf.find(node1) == uf.find(node2):
            continue
        uf.union(node1, node2)
        mst_edges.append(f"{node1} -> {node2}, {weight}")
        number_of_edges += 1
        total_cost += weight

        if number_of_edges ==  len(nodes) - 1:
            break

    if number_of_edges != len(nodes) - 1:
        raise ValueError("Graph is not weighted")

    print("Minimum Spanning Tree (MST):")
    print(f"Total  Cost: {total_cost}")
    print("\n".join(mst_edges))
    return total_cost, mst_edges

def get_undirected_edges(graph: Graph) -> list:
    """ Remember we store edge A - C, in C and A. Need to avoid duplicate edges."""

    undirected_edges = []
    for node in graph.get_nodes():
        #print(f"Node: {node}")
        for destination_node_name, weight in node.get_edges().items():
            if node.get_name() < destination_node_name:
                undirected_edges.append((weight, node.get_name(), destination_node_name))

    return undirected_edges