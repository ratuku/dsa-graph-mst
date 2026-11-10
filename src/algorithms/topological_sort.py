from sys import path

from src.model.Graph import Graph, Node

WHITE, GRAY, BLACK = 0, 1, 2


def topological_sort(graph: Graph) :
    """Run DFS on a directed graph. If acyclic, return a topological order;
    otherwise return all cycles with their lengths."""

    if not graph.directed:
        raise ValueError("Graph must be directed")

    node_names = sorted(graph.get_node_names())  # sorted for deterministic output
    time = 0
    color = {n: WHITE for n in node_names}
    parent = {n: None for n in node_names}
    discovery, finish = {}, {}
    finished_order = []  # nodes in the order they turn BLACK
    has_cycle = False


    def visit(node_name_):
        nonlocal time, has_cycle
        time += 1
        discovery[node_name_] = time
        color[node_name_] = GRAY
        for neighbor_node_name in sorted(graph.neighbors(node_name_).keys()):  # iterating the dict gives node names
            if color[neighbor_node_name] == WHITE:
                parent[neighbor_node_name] = node_name_
                visit(neighbor_node_name)
            elif color[neighbor_node_name] == GRAY:  # back edge node_name_ -> neighbor_node_name: a cycle exists
                has_cycle = True
        color[node_name_] = BLACK
        time += 1
        finish[node_name_] = time
        finished_order.append(node_name_)

    for node_name in node_names:
        if color[node_name] == WHITE:
            visit(node_name)

    if not has_cycle:
        print("No cycles found\n")
        print("Order: " + " -> ".join(reversed(finished_order)))
        return has_cycle, list(reversed(finished_order)), discovery, finish

    cycles = find_all_cycles(graph, node_names)
    path_cycles = []
    for cycle in cycles:
        path_cycles.append(" -> ".join(cycle + [cycle[0]]) + f", length {len(cycle)}")
    print("Cycles: \n" + "\n".join(path_cycles))
    return has_cycle, cycles, discovery, finish


def find_all_cycles(graph: Graph, node_names: list[str]) -> list[list[str]]:
    index = {node_name: i for i, node_name in enumerate(node_names)}
    cycles = []

    for start_node_name in node_names:
        path = [start_node_name]
        on_path = {start_node_name}

        def extend(node_name_):
            for neighbor_node_name in sorted(graph.neighbors(node_name_)):
                if neighbor_node_name == start_node_name:
                    cycles.append(list(path))            # closed the loop
                elif index[neighbor_node_name] > index[start_node_name] and neighbor_node_name not in on_path:
                    path.append(neighbor_node_name)
                    on_path.add(neighbor_node_name)
                    extend(neighbor_node_name)
                    path.pop()
                    on_path.remove(neighbor_node_name)

        extend(start_node_name)

    return cycles
