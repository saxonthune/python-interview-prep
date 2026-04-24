"""
Spec for: lru_cache
"""

TITLE = "LRU Cache"

DESCRIPTION = """
Implement a Least Recently Used (LRU) cache with fixed capacity.

Methods:
    __init__(capacity)         set capacity (>= 1)
    get(key) -> int            return value if present, else -1.
                               accessing a key marks it most-recently-used.
    put(key, value) -> None    insert/update. If at capacity, evict the
                               least-recently-used key. put also marks the
                               key most-recently-used.

Both get and put must run in O(1) average time.

The classic structure: dict[key] -> doubly-linked-list-node, plus a
DLL ordered by recency. Or use collections.OrderedDict and call
move_to_end / popitem(last=False).
"""

CONSTRAINTS = """
- 1 <= capacity <= 3000
- 0 <= key, value <= 10^4
- get and put both O(1) average time
- 'Use' = either get or put on a key
"""

CLASS_NAME = "LRUCache"

SIGNATURE = '''class LRUCache:
    def __init__(self, capacity: int):
        """YOUR CODE HERE"""
        pass

    def get(self, key: int) -> int:
        pass

    def put(self, key: int, value: int) -> None:
        pass'''

CASES = [
    # canonical LeetCode example
    ((2,), [
        ("put", (1, 1), None),
        ("put", (2, 2), None),
        ("get",  1,     1),
        ("put", (3, 3), None),    # evicts key 2
        ("get",  2,    -1),
        ("put", (4, 4), None),    # evicts key 1
        ("get",  1,    -1),
        ("get",  3,     3),
        ("get",  4,     4),
    ]),
    # capacity 1 - every put evicts the previous
    ((1,), [
        ("put", (1, 100), None),
        ("get",  1,       100),
        ("put", (2, 200), None),
        ("get",  1,      -1),
        ("get",  2,       200),
    ]),
    # update existing key should NOT evict, AND should refresh recency
    ((2,), [
        ("put", (1, 1), None),
        ("put", (2, 2), None),
        ("put", (1, 11), None),    # update; now 2 is LRU
        ("put", (3, 3), None),     # evicts 2, not 1
        ("get",  1,     11),
        ("get",  2,    -1),
        ("get",  3,     3),
    ]),
    # get refreshes recency (the whole point)
    ((2,), [
        ("put", (1, 1), None),
        ("put", (2, 2), None),
        ("get",  1,     1),        # 1 becomes MRU; 2 is now LRU
        ("put", (3, 3), None),     # evicts 2
        ("get",  2,    -1),
        ("get",  1,     1),
    ]),
    # miss before any insert
    ((2,), [
        ("get",  99, -1),
        ("put", (5, 50), None),
        ("get",  5,   50),
    ]),
]
