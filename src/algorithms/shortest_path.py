from src.model.Graph import Graph


def dijkstra(graph: Graph, source_name: str):
    dist = {node_names: float("inf") for node_names in graph.get_node_names()}
    previous = {name: [] for name in dist.keys()}

    if source_name not in dist:
        raise Exception(f"Source node {source_name} not found")

    unvisited_node_names = set(dist.keys())

    # start node distance = 0
    dist[source_name] = 0

    while len(unvisited_node_names) > 0:
        current_node_name = min(unvisited_node_names, key = dist.get)

        if dist[current_node_name] == float('inf'):
            break

        neighbors = graph.neighbors(current_node_name)
        for neighbor_name, weight in neighbors.items():
            if neighbor_name not in unvisited_node_names:
                continue

            new_dist = dist[current_node_name] + weight
            if dist[neighbor_name] > new_dist:
                dist[neighbor_name] = new_dist
                previous[neighbor_name] = [current_node_name]
            elif new_dist == dist[neighbor_name]:
                previous[neighbor_name].append(current_node_name)

        unvisited_node_names.remove(current_node_name)

    #print("\n")
    #print(previous)
    print(_get_shortest_path_summary(dist, previous, source_name))

def _get_shortest_path_summary(dist: dict, previous: dict, source_node_name: str) -> str:
    output = ["", f"Shortest Path from {source_node_name}: Summary", ""]

    for name in dist:
        paths = _get_all_paths(previous, source_node_name, name)
        if not paths:
            output.append(f"{source_node_name} -> {name}: Unreachable")
            continue
        for p in paths:
            output.append(f"{source_node_name} -> {name}: {' -> '.join(p)}, {dist[name]}")

    return "\n".join(output)

def _get_all_paths(previous: dict, source: str, node: str) -> list[list[str]]:
    if node == source:
        return [[node]]
    paths = []
    for parent in previous[node]:
        for p in _get_all_paths(previous, source, parent):
            paths.append(p + [node])

    return paths
