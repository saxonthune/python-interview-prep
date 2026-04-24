"""
Spec for: trees / basics / dfs (post-order)
"""
from utils import build_tree

TITLE = "Tree DFS - Post-order Traversal"

DESCRIPTION = """
Given the root of a binary tree, return a list of node values in
post-order: left subtree, then right subtree, then the node itself.

Example:
        1
       / \\
      2   3
     / \\
    4   5

Post-order: [4, 5, 2, 3, 1]
"""

CONSTRAINTS = """
- 0 <= number of nodes <= 1000
- Node values are integers
- Return [] for an empty tree
"""

SIGNATURE = "def solution(root: 'TreeNode | None') -> list[int]:"

# build_tree takes LeetCode-style level-order input (None for missing children)
CASES = [
    (build_tree([1, 2, 3, 4, 5]),         [4, 5, 2, 3, 1]),
    (build_tree([1]),                     [1]),
    (build_tree([]),                      []),
    (build_tree([1, 2]),                  [2, 1]),
    (build_tree([1, None, 2]),            [2, 1]),
    (build_tree([1, 2, 3, 4, None, None, 5]), [4, 2, 5, 3, 1]),
    # left-skewed
    (build_tree([1, 2, None, 3, None, 4]), [4, 3, 2, 1]),
    # right-skewed
    (build_tree([1, None, 2, None, 3, None, 4]), [4, 3, 2, 1]),
]

MUTATES_INPUT = False
