# DSA Project 2

A Python console app for Dijkstra’s shortest paths, Kruskal’s minimum spanning tree, and DFS topological sorting and cycle detection.

## Run

Run these commands from the repository root.

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 src/UIRunner.py
```

Choose option 1 to load `resources/graph-data.txt` or option 2 to enter a graph in the terminal. End terminal input with a blank line.

## Graph input

The first line combines `U` (undirected) or `D` (directed) with `W` (weighted) or `UNW` (unweighted). Enter one edge per line with its two vertices and, for weighted graphs, its weight.

```text
U, W
A B 1
A C 2
B C 3
```
