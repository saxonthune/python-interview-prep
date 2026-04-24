"""
Spec for: graphs / basics / dfs
"""

TITLE = "Graph DFS - Visit Order"

DESCRIPTION = """
Given an adjacency-list graph and a start node, return the order in
which nodes are visited by depth-first search starting from `start`.

Visit neighbors in the order they appear in graph[node]. Skip already-
visited nodes. Only nodes reachable from `start` should appear.

Example:
    graph = {0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}
    start = 0
    DFS order: [0, 1, 3, 4, 2]
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
    # branching tree-shape
    (({0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}, 0), [0, 1, 3, 4, 2]),
    # cycle
    (({0: [1], 1: [0, 2], 2: [1, 0]}, 0), [0, 1, 2]),
    # disconnected: only component containing start
    (({0: [1], 1: [0], 2: [3], 3: [2]}, 0), [0, 1]),
    # star
    (({0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}, 0), [0, 1, 2, 3]),
    # start from non-zero
    (({0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}, 2), [2, 0, 1, 3, 4]),
]

MUTATES_INPUT = False
