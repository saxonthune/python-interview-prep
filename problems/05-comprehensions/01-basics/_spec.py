"""
Spec for: comprehensions basics drill.

A single-file drill of small prompts, each exercising one mental model
for Python comprehensions / generator expressions. Implement each stub
in solution.py; __main__ runs all of them.

Each entry in CASES is keyed by the function name in solution.py.
"""

TITLE = "Comprehensions Basics"

DESCRIPTION = """
Practice the syntactic surface and idiomatic uses of comprehensions:
list / dict / set comps, generator expressions, conditional values,
nested iteration, unpacking in the `for` clause, and the `next(gen, default)`
find-first pattern.

Each function below has a one-line docstring prompt. Aim to solve each in
ONE expression (a comprehension or a generator-expression argument). If
you find yourself reaching for a loop body or a helper, you're probably
fighting the comp — step back.

Coverage map:
    map / filter / map+filter         doubles, positives, squared_evens
    conditional value                 clamp_negatives
    enumerate                         indexed_positives
    zip                               pairwise_sums
    flatten / nested comp / product   flatten, transpose, cartesian
    set comp                          unique_lengths
    dict comp / invert / filter       length_by_word, invert_dict,
                                      filter_dict_by_value
    generator + sum/any/all/max       total_squared, any_negative,
                                      all_positive, max_word_length
    next(gen, default) find-first     first_negative, first_key_with_value
    unpacking in `for`                swap_pairs
"""

CONSTRAINTS = """
- Solve each prompt in a single expression where possible.
- Inputs may be empty; handle the empty case naturally (your comp
  should already do the right thing).
- Don't import anything; everything here is plain builtins.
"""

STUBS = [
    # (section_header_or_None, signature, prompt)
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

    ("set comp",
     "def unique_lengths(words: list[str]) -> set[int]:",
     "Return the set of distinct word lengths."),

    ("dict comp",
     "def length_by_word(words: list[str]) -> dict[str, int]:",
     "Return a dict mapping each word to its length."),
    (None,
     "def invert_dict(d: dict) -> dict:",
     "Return d with keys and values swapped (assume values are unique)."),
    (None,
     "def filter_dict_by_value(d: dict[str, int], threshold: int) -> dict[str, int]:",
     "Return the entries of d whose value is >= threshold."),

    ("generator expression + reducer",
     "def total_squared(xs: list[int]) -> int:",
     "Return the sum of squares of xs (use sum() with a generator)."),
    (None,
     "def any_negative(xs: list[int]) -> bool:",
     "Return True if any element is strictly negative."),
    (None,
     "def all_positive(xs: list[int]) -> bool:",
     "Return True if every element is strictly positive. Empty list -> True."),
    (None,
     "def max_word_length(words: list[str]) -> int:",
     "Return the length of the longest word, or 0 if there are none."),

    ("next(gen, default) — find-first",
     "def first_negative(xs: list[int]) -> int | None:",
     "Return the first negative element, or None if there is none."),
    (None,
     "def first_key_with_value(d: dict, target) -> object | None:",
     "Return the first key whose value equals target, or None."),

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
    "unique_lengths": [
        (["a", "bb", "cc", "ddd"], {1, 2, 3}),
        ([], set()),
        (["abc"], {3}),
        (["xx", "yy"], {2}),
    ],
    "length_by_word": [
        (["a", "bb", "ccc"], {"a": 1, "bb": 2, "ccc": 3}),
        ([], {}),
    ],
    "invert_dict": [
        ({"a": 1, "b": 2}, {1: "a", 2: "b"}),
        ({}, {}),
    ],
    "filter_dict_by_value": [
        (({"a": 1, "b": 5, "c": 3}, 3), {"b": 5, "c": 3}),
        (({"a": 1}, 5), {}),
        (({}, 0), {}),
    ],
    "total_squared": [
        ([1, 2, 3], 14),
        ([], 0),
        ([-2, 2], 8),
    ],
    "any_negative": [
        ([1, 2, -1], True),
        ([1, 2, 3], False),
        ([], False),
        ([0], False),
    ],
    "all_positive": [
        ([1, 2, 3], True),
        ([1, 0, 3], False),
        ([], True),  # vacuous truth — trap worth knowing
        ([-1], False),
    ],
    "max_word_length": [
        (["a", "bbb", "cc"], 3),
        ([], 0),  # must use default=0 in max(...)
        (["x"], 1),
    ],
    "first_negative": [
        ([1, 2, -3, 4, -5], -3),
        ([1, 2, 3], None),
        ([], None),
        ([-1], -1),
    ],
    "first_key_with_value": [
        (({"a": 1, "b": 2, "c": 2}, 2), "b"),  # dicts are insertion-ordered
        (({"a": 1}, 99), None),
        (({}, 0), None),
    ],
    "swap_pairs": [
        ([(1, 2), (3, 4)], [(2, 1), (4, 3)]),
        ([], []),
        ([("a", "b")], [("b", "a")]),
    ],
}

MUTATES_INPUT = False
