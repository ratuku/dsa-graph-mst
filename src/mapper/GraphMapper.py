import math
from pathlib import Path

from src.model.Graph import Graph, Node

DATA_FILE = Path(__file__).resolve().parents[2] / "resources" / "graph-data.txt"


class GraphMapper:
    @staticmethod
    def mapp_to_graph(data_file=DATA_FILE) -> Graph:
        """Read a graph from a text file. Raises FileNotFoundError or ValueError."""
        text = Path(data_file).read_text(encoding="utf-8")
        return GraphMapper._parse(text)

    @staticmethod
    def mapp_to_graph_from_console(text: str) -> Graph:
        """Build a graph from multi-line text in the same format as the file."""
        return GraphMapper._parse(text)

    @staticmethod
    def _parse(text: str) -> Graph:
        # keep original line numbers so error messages point at the right line
        lines = [(n, line.strip()) for n, line in enumerate(text.splitlines(), start=1)]
        lines = [(n, line) for n, line in lines if line and not line.startswith("#")]

        if not lines:
            raise ValueError("No data found: expected a header line like 'U, W'")

        header_no, header = lines[0]
        directed, weighted = GraphMapper._parse_header(header, header_no)
        graph = Graph(directed=directed, weighted=weighted)

        expected_tokens = 3 if weighted else 2
        known_nodes: set[str] = set()
        known_edges: set[tuple[str, str]] = set()

        for line_no, line in lines[1:]:
            tokens = line.split()
            if len(tokens) != expected_tokens:
                shape = "'A B weight'" if weighted else "'A B'"
                raise ValueError(
                    f"Line {line_no}: expected {shape} for a "
                    f"{'weighted' if weighted else 'unweighted'} graph, got '{line}'"
                )

            source, destination = tokens[0], tokens[1]
            weight = GraphMapper._parse_weight(tokens[2], line_no) if weighted else 1.0

            # A-B and B-A are the same edge in an undirected graph
            key = (source, destination) if directed else tuple(sorted((source, destination)))
            if key in known_edges:
                raise ValueError(f"Line {line_no}: duplicate edge {source} - {destination}")
            known_edges.add(key)

            for name in (source, destination):
                if name not in known_nodes:
                    known_nodes.add(name)
                    node = Node(name=name)
                    graph.add_node(node)

            graph.add_edge(graph.get_node(source), graph.get_node(destination), weight)

        return graph

    @staticmethod
    def _parse_header(header: str, line_no: int) -> tuple[bool, bool]:
        """Return (directed, weighted) from a header such as 'U, W' or 'D, UNW'."""
        parts = [p.strip().upper() for p in header.split(",")]
        if len(parts) != 2 or parts[0] not in ("U", "D") or parts[1] not in ("W", "UNW"):
            raise ValueError(
                f"Line {line_no}: header must be like 'U, W' "
                f"(U or D, then W or UNW), got '{header}'"
            )
        return parts[0] == "D", parts[1] == "W"

    @staticmethod
    def _parse_weight(token: str, line_no: int) -> float:
        try:
            weight = float(token)
        except ValueError:
            raise ValueError(f"Line {line_no}: invalid weight '{token}'") from None
        if not math.isfinite(weight):
            raise ValueError(f"Line {line_no}: invalid weight '{token}'")
        return weight