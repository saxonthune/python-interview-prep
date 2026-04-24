"""Shared helpers for all problems. Import what you need."""
from collections import deque


# ---------- Trees ----------

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def build_tree(values):
    """LeetCode-style level-order input: [1,2,3,None,4] -> tree.
    Use None (or null if you copy from LeetCode, just swap them) for missing children.
    """
    if not values:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    """Inverse of build_tree. Useful for comparing trees in tests."""
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
        else:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    # trim trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


def print_tree(root):
    """Visualize a tree for debugging. Horizontal layout."""
    if not root:
        print("(empty)")
        return
    lines = []

    def helper(node, prefix="", is_left=True):
        if not node:
            return
        if node.right:
            helper(node.right, prefix + ("│   " if is_left else "    "), False)
        lines.append(prefix + ("└── " if is_left else "┌── ") + str(node.val))
        if node.left:
            helper(node.left, prefix + ("    " if is_left else "│   "), True)

    helper(root)
    print("\n".join(lines))


# ---------- Graphs ----------

def build_graph(edges, directed=False):
    """Adjacency list from edge list. edges: [[u, v], ...]"""
    graph = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u) if not directed else graph.setdefault(v, [])
    return graph


# ---------- Grids ----------

def print_grid(grid):
    """Pretty-print a 2D grid."""
    if not grid:
        print("(empty)")
        return
    for row in grid:
        print(" ".join(str(c) for c in row))
    print()


# ---------- Linked Lists (for later) ----------

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals = []
        node = self
        seen = set()
        while node and id(node) not in seen:
            seen.add(id(node))
            vals.append(str(node.val))
            node = node.next
        return "ListNode(" + " -> ".join(vals) + ")"


def build_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    node = head
    for v in values[1:]:
        node.next = ListNode(v)
        node = node.next
    return head
