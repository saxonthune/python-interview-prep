"""
Spec for: trees / basics / bfs (level-order)
"""
from utils import build_tree

TITLE = "Tree BFS - Level-order Traversal"

DESCRIPTION = """
Given the root of a binary tree, return its level-order traversal as a
list of lists, where each inner list contains the node values at that
depth (left to right).

Example:
        3
       / \\
      9   20
         /  \\
        15   7

Level-order: [[3], [9, 20], [15, 7]]

The level grouping is the point of this drill: it forces you to track
level boundaries on the queue, not just enqueue/dequeue blindly.
"""

CONSTRAINTS = """
- 0 <= number of nodes <= 1000
- Node values are integers
- Return [] for an empty tree
"""

SIGNATURE = "def solution(root: 'TreeNode | None') -> list[list[int]]:"

CASES = [
    (build_tree([3, 9, 20, None, None, 15, 7]), [[3], [9, 20], [15, 7]]),
    (build_tree([1]),                            [[1]]),
    (build_tree([]),                             []),
    (build_tree([1, 2, 3]),                      [[1], [2, 3]]),
    (build_tree([1, 2, None, 3]),                [[1], [2], [3]]),       # left-skewed
    (build_tree([1, None, 2, None, 3]),          [[1], [2], [3]]),       # right-skewed
    (build_tree([1, 2, 3, 4, 5, 6, 7]),          [[1], [2, 3], [4, 5, 6, 7]]),
    (build_tree([1, 2, 3, 4, None, None, 5]),    [[1], [2, 3], [4, 5]]),  # asymmetric
]

MUTATES_INPUT = False
