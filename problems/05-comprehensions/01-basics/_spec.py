"""
Spec for: comprehensions basics drill.

The first of three comprehension units. Covers the syntactic surface:
list comps with map / filter / both, conditional value (ternary inside
the comp), enumerate, zip, nested iteration (flatten / transpose /
cartesian product), and tuple-unpacking in the `for` clause.

See sibling problems for set + dict comps, and for generator-based
patterns (sum / any / all / max, next-with-default).
"""

TITLE = "Comprehensions: Basics"

DESCRIPTION = """
Practice the syntactic surface of list comprehensions: map, filter,
map+filter, conditional value, enumerate, zip, nested iteration,
and tuple-unpacking in the `for` clause.

Each function below has a one-line docstring prompt. Aim to solve each in
ONE expression (a list comprehension). If you find yourself reaching for
a loop body or a helper, you're probably fighting the comp — step back.

Coverage map:
    map / filter / map+filter         doubles, positives, squared_evens
    conditional value (ternary)       clamp_negatives
    enumerate                         indexed_positives
    zip                               pairwise_sums
    flatten / nested comp / product   flatten, transpose, cartesian
    unpacking in `for`                swap_pairs
"""

CONSTRAINTS = """
- Solve each prompt in a single expression where possible.
- Inputs may be empty; handle the empty case naturally (your comp
  should already do the right thing).
- Don't import anything; everything here is plain builtins.
"""

STUBS = [
    ("map / filter",
     "def doubles(xs: list[int]) -> list[int]:",
     "Return each element doubled."),
    (None,
     "def positives(xs: list[int]) -> list[int]:",
     "Return only the strictly-positive elements."),
    (None,
     "def squared_evens(xs: list[int]) -> list[int]:",
     "Return the squares of the even elements."),

    ("conditional value",
     "def clamp_negatives(xs: list[int]) -> list[int]:",
     "Return xs with every negative replaced by 0 (keep non-negatives as-is)."),

    ("enumerate",
     "def indexed_positives(xs: list[int]) -> list[tuple[int, int]]:",
     "Return (index, value) pairs for the strictly-positive elements."),

    ("zip",
     "def pairwise_sums(a: list[int], b: list[int]) -> list[int]:",
     "Return elementwise sums of a and b (stop at the shorter list)."),

    ("nested iteration",
     "def flatten(grid: list[list[int]]) -> list[int]:",
     "Flatten a list of lists into a single list."),
    (None,
     "def transpose(grid: list[list[int]]) -> list[list[int]]:",
     "Transpose a rectangular grid (rows become columns)."),
    (None,
     "def cartesian(a: list, b: list) -> list[tuple]:",
     "Return all (x, y) pairs with x from a, y from b, in row-major order."),

    ("unpacking in the for clause",
     "def swap_pairs(pairs: list[tuple]) -> list[tuple]:",
     "Given a list of (a, b) tuples, return [(b, a), ...]."),
]

CASES = {
    "doubles": [
        ([1, 2, 3], [2, 4, 6]),
        ([], []),
        ([-1, 0, 5], [-2, 0, 10]),
    ],
    "positives": [
        ([-2, -1, 0, 1, 2], [1, 2]),
        ([], []),
        ([0], []),
        ([-1, -2], []),
    ],
    "squared_evens": [
        ([1, 2, 3, 4], [4, 16]),
        ([1, 3, 5], []),
        ([2], [4]),
        ([], []),
    ],
    "clamp_negatives": [
        ([-3, -1, 0, 4, -2], [0, 0, 0, 4, 0]),
        ([1, 2, 3], [1, 2, 3]),
        ([], []),
    ],
    "indexed_positives": [
        ([0, -1, 3, -4, 5], [(2, 3), (4, 5)]),
        ([1, 2, 3], [(0, 1), (1, 2), (2, 3)]),
        ([], []),
        ([-1, -2], []),
    ],
    "pairwise_sums": [
        (([1, 2, 3], [10, 20, 30]), [11, 22, 33]),
        (([], []), []),
        (([1, 2], [10, 20, 30]), [11, 22]),  # zip stops at shorter
    ],
    "flatten": [
        ([[1, 2], [3, 4, 5], [6]], [1, 2, 3, 4, 5, 6]),
        ([], []),
        ([[]], []),
        ([[1], [], [2, 3]], [1, 2, 3]),
    ],
    "transpose": [
        ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
        ([[1]], [[1]]),
        ([[1, 2], [3, 4], [5, 6]], [[1, 3, 5], [2, 4, 6]]),
    ],
    "cartesian": [
        (([1, 2], ["a", "b"]), [(1, "a"), (1, "b"), (2, "a"), (2, "b")]),
        (([], [1, 2]), []),
        (([1], ["a"]), [(1, "a")]),
    ],
    "swap_pairs": [
        ([(1, 2), (3, 4)], [(2, 1), (4, 3)]),
        ([], []),
        ([("a", "b")], [("b", "a")]),
    ],
}

MUTATES_INPUT = False
