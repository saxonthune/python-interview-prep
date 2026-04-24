"""
Spec for: count_components

Classic "number of provinces" / connected-components problem on an
adjacency matrix. Practice fill-style traversal (DFS or BFS) where the
neighbor lookup is matrix[i] rather than a pre-built adjacency list.
"""

TITLE = "Count Connected Components (Adjacency Matrix)"

DESCRIPTION = """
Given an N x N adjacency matrix `m` for an undirected graph, return the
number of connected components (distinct subgraphs).

m[i][j] == 1 means there is an edge between nodes i and j.
m[i][i] is always 1 (a node is connected to itself).
The matrix is symmetric: m[i][j] == m[j][i].

Example:
    m = [[1, 1, 0],
         [1, 1, 0],
         [0, 0, 1]]
    -> 2 components: {0, 1} and {2}

The drill: for each unvisited node, run a fill (DFS or BFS) that walks
row m[node] to find neighbors, marks them visited, and recurses. Each
fill-launch increments the component count.
"""

CONSTRAINTS = """
- 1 <= N <= 200
- m[i][j] is 0 or 1
- m[i][i] == 1
- m is symmetric (undirected edges)
"""

SIGNATURE = "def solution(m: list[list[int]]) -> int:"

CASES = [
    # canonical: two components
    ([[1, 1, 0],
      [1, 1, 0],
      [0, 0, 1]], 2),
    # fully connected: one component
    ([[1, 1, 1],
      [1, 1, 1],
      [1, 1, 1]], 1),
    # fully disconnected: N components
    ([[1, 0, 0],
      [0, 1, 0],
      [0, 0, 1]], 3),
    # single node
    ([[1]], 1),
    # chain 0-1-2-3 across 4 nodes: one component
    ([[1, 1, 0, 0],
      [1, 1, 1, 0],
      [0, 1, 1, 1],
      [0, 0, 1, 1]], 1),
    # two pairs: {0,1} and {2,3}
    ([[1, 1, 0, 0],
      [1, 1, 0, 0],
      [0, 0, 1, 1],
      [0, 0, 1, 1]], 2),
    # transitive closure required: 0-2 and 1-2 means {0,1,2} is one component
    ([[1, 0, 1],
      [0, 1, 1],
      [1, 1, 1]], 1),
    # mixed: triangle {0,1,2} + isolated 3 + pair {4,5}
    ([[1, 1, 1, 0, 0, 0],
      [1, 1, 1, 0, 0, 0],
      [1, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 1, 1],
      [0, 0, 0, 0, 1, 1]], 3),
]

MUTATES_INPUT = False
