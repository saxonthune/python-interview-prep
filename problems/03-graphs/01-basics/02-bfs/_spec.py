"""
Spec for: graphs / basics / bfs
"""

TITLE = "Graph BFS - Visit Order"

DESCRIPTION = """
Given an adjacency-list graph and a start node, return the order in
which nodes are visited by breadth-first search starting from `start`.

Enqueue neighbors in the order they appear in graph[node]. Mark a node
visited when you enqueue it (not when you dequeue) to avoid duplicates.
Only nodes reachable from `start` should appear.

Example:
    graph = {0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}
    start = 0
    BFS order: [0, 1, 2, 3, 4]
"""

CONSTRAINTS = """
- Nodes are integers
- Graph may contain cycles
- Graph may be disconnected (only return the component reachable from start)
- 0 <= number of nodes <= 1000
"""

SIGNATURE = "def solution(graph: dict[int, list[int]], start: int) -> list[int]:"

CASES = [
    # single node
    (({0: []}, 0), [0]),
    # linear chain
    (({0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}, 0), [0, 1, 2, 3]),
    # branching tree-shape (BFS visits all of depth 1 before depth 2)
    (({0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}, 0), [0, 1, 2, 3, 4]),
    # cycle
    (({0: [1], 1: [0, 2], 2: [1, 0]}, 0), [0, 1, 2]),
    # disconnected: only component containing start
    (({0: [1], 1: [0], 2: [3], 3: [2]}, 0), [0, 1]),
    # star
    (({0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}, 0), [0, 1, 2, 3]),
    # start from non-zero
    (({0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}, 2), [2, 0, 1, 3, 4]),
    # wider graph - BFS vs DFS diverges clearly
    (({0: [1, 2, 3], 1: [0, 4], 2: [0, 5], 3: [0, 6], 4: [1], 5: [2], 6: [3]}, 0),
     [0, 1, 2, 3, 4, 5, 6]),
]

MUTATES_INPUT = False
