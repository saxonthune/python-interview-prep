"""JSON encoding for Python objects that appear in problem CASES.

Special markers (decoded by build/web_harness.py in Pyodide):

- set       -> {"__set__": [items...]}
- TreeNode  -> {"__tree__": [level-order values, None for missing]}
- ListNode  -> {"__list__": [values...]}
- tuple     -> {"__tuple__": [items...]}      (preserved as tuple in-runtime)

The web harness reconstructs these before invoking the user's solution and
before comparing results, so `expected` values that contain (e.g.) a set
still compare equal to a real set returned by the solution.

If a new Python-only type starts appearing in CASES, add it here and in
web_harness.py together.
"""
import json

from utils import TreeNode, ListNode, tree_to_list


def _encode(obj):
    if isinstance(obj, TreeNode):
        return {"__tree__": tree_to_list(obj)}
    if isinstance(obj, ListNode):
        vals = []
        node = obj
        seen = set()
        while node is not None and id(node) not in seen:
            seen.add(id(node))
            vals.append(_encode(node.val))
            node = node.next
        return {"__list__": vals}
    if isinstance(obj, set):
        return {"__set__": [_encode(x) for x in obj]}
    if isinstance(obj, tuple):
        return {"__tuple__": [_encode(x) for x in obj]}
    if isinstance(obj, list):
        return [_encode(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k) if not isinstance(k, str) else k: _encode(v) for k, v in obj.items()}
    if obj is Ellipsis:
        return {"__ellipsis__": True}
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    raise TypeError(f"don't know how to encode {type(obj).__name__}: {obj!r}")


def encode(obj) -> object:
    return _encode(obj)


def dumps(obj) -> str:
    return json.dumps(encode(obj), ensure_ascii=False)
