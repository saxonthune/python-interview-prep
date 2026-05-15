"""
Spec for: min_stack
"""

TITLE = "Min Stack"

DESCRIPTION = """
Implement a stack that supports push, pop, top, and retrieving the
minimum element — all in O(1) time.

Methods:
    push(val) -> None
    pop()     -> None
    top()     -> int   (the value on top, without removing)
    getMin()  -> int   (the current minimum in the stack)

The trick: a single auxiliary stack of running minimums (or pairs of
(val, min_so_far)) keeps each operation O(1).
"""

CONSTRAINTS = """
- pop, top, getMin are only called on non-empty stacks
- Values are integers
- All four operations must be O(1)
"""

CLASS_NAME = "MinStack"

SIGNATURE = '''class MinStack:
    def __init__(self):
        """YOUR CODE HERE"""
        pass

    def push(self, val: int) -> None:
        pass

    def pop(self) -> None:
        pass

    def top(self) -> int:
        pass

    def getMin(self) -> int:
        pass'''

# Each trace: (init_args_tuple, [(method, args, expected), ...])
# args follows function-harness convention: tuple => splat, single value => wrap.
CASES = [
    # canonical LeetCode example
    ((), [
        ("push",   -2,  None),
        ("push",    0,  None),
        ("push",   -3,  None),
        ("getMin", (), -3),
        ("pop",    (), None),
        ("top",    (),  0),
        ("getMin", (), -2),
    ]),
    # min repeats - getMin must still work after popping a duplicate min
    ((), [
        ("push",    1, None),
        ("push",    1, None),
        ("getMin", (), 1),
        ("pop",    (), None),
        ("getMin", (), 1),   # not undefined — duplicate min still present
        ("pop",    (), None),
    ]),
    # strictly increasing pushes - min stays at the first
    ((), [
        ("push",    5, None),
        ("push",    7, None),
        ("push",    9, None),
        ("getMin", (), 5),
        ("top",    (), 9),
    ]),
    # strictly decreasing pushes - min updates each time
    ((), [
        ("push",    9, None),
        ("push",    5, None),
        ("push",    1, None),
        ("getMin", (), 1),
        ("pop",    (), None),
        ("getMin", (), 5),
        ("pop",    (), None),
        ("getMin", (), 9),
    ]),
    # single element
    ((), [
        ("push",   42, None),
        ("top",    (), 42),
        ("getMin", (), 42),
    ]),
]
