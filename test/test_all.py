import pytest

from src.model.Graph import Graph
from src.model.Graph import Node
from src.algorithms.shortest_path import dijkstra
from src.algorithms.minimum_spanning_tree import minimum_spanning_tree
from src.algorithms.topological_sort import topological_sort
from src.mapper.GraphMapper import GraphMapper

def get_undirected_weighted_graph() -> Graph:
    g = Graph(directed=False, weighted=True)
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_d = Node('D')
    node_e = Node('E')
    node_f = Node('F')

    g.add_node(node_a)
    g.add_node(node_b)
    g.add_node(node_c)
    g.add_node(node_d)
    g.add_node(node_e)
    g.add_node(node_f)

    g.add_edge(node_a, node_b, 1)
    g.add_edge(node_a, node_c, 2)
    g.add_edge(node_b, node_c, 1)
    g.add_edge(node_b, node_d, 3)
    g.add_edge(node_b, node_e, 2)
    g.add_edge(node_c, node_d, 1)
    g.add_edge(node_c, node_e, 2)
    g.add_edge(node_d, node_e, 4)
    g.add_edge(node_d, node_f, 3)
    g.add_edge(node_e, node_f, 3)

    return g

def test_graph_creation_undirected_weighted():
    g = get_undirected_weighted_graph()
    print(g)

def test_graph_copy():
    g = get_undirected_weighted_graph()
    print(g)

    g_copy = g.get_copy()
    print(g_copy)

def test_shortest_path():
    g = get_undirected_weighted_graph()
    start_node = g.get_node('A')

    dijkstra(g, 'A')

def test_minimum_spanning_tree():
    g = get_undirected_weighted_graph()

    total, edges = minimum_spanning_tree(g)
    assert(total == 8)
    assert(len(edges) == 5)

""" Test Graph Mapper """
def test_parses_sample_graph():
    text = "U, W\nA B 1\nA C 2\nB C 1"
    g = GraphMapper.mapp_to_graph_from_console(text)
    assert len(g.get_nodes()) == 3

def test_bad_header_reports_line():
    with pytest.raises(ValueError, match="Line 1"):
        GraphMapper.mapp_to_graph_from_console("X, W\nA B 1")

def test_weighted_edge_missing_weight():
    with pytest.raises(ValueError, match="Line 2"):
        GraphMapper.mapp_to_graph_from_console("U, W\nA B")

""" Test Topological Sort """
def test_topological_sort():
    graph = GraphMapper.mapp_to_graph_from_console("D, UNW\nA B\nB C\nC A\nC D\nD D")

    has_cycle, cycles, _, _ = topological_sort(graph)

    assert has_cycle
    assert cycles == [["A", "B", "C"], ["D"]]
