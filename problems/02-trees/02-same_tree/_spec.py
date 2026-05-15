"""
Spec for: same_tree
"""
from utils import build_tree

TITLE = "Same Tree"

DESCRIPTION = """
Given the roots of two binary trees p and q, return True if they are
structurally identical AND every corresponding node has the same value.

Two empty trees are considered equal.
"""

CONSTRAINTS = """
- 0 <= number of nodes in each tree <= 100
- Node values are integers
"""

SIGNATURE = "def solution(p: 'TreeNode | None', q: 'TreeNode | None') -> bool:"

CASES = [
    # identical
    ((build_tree([1, 2, 3]),       build_tree([1, 2, 3])),       True),
    # both empty
    ((build_tree([]),              build_tree([])),              True),
    # one empty, one not
    ((build_tree([1]),             build_tree([])),              False),
    ((build_tree([]),              build_tree([1])),             False),
    # different values
    ((build_tree([1, 2, 3]),       build_tree([1, 2, 4])),       False),
    # same values, different shape (left vs right child)
    ((build_tree([1, 2]),          build_tree([1, None, 2])),    False),
    # deeper identical
    ((build_tree([1, 2, 3, 4, 5]), build_tree([1, 2, 3, 4, 5])), True),
    # deeper differing only at a leaf
    ((build_tree([1, 2, 3, 4, 5]), build_tree([1, 2, 3, 4, 6])), False),
    # single nodes equal
    ((build_tree([42]),            build_tree([42])),            True),
    # single nodes differ
    ((build_tree([1]),             build_tree([2])),             False),
]

MUTATES_INPUT = False
