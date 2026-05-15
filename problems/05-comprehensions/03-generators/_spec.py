"""
Spec for: generator expressions drill.

The third of three comprehension units. Covers generator expressions
piped into reducers (sum / any / all / max) and the
`next(gen, default)` find-first pattern.
"""

TITLE = "Comprehensions: Generators"

DESCRIPTION = """
Practice generator expressions — comprehensions without the brackets,
passed directly into a reducer that consumes them lazily.

Two patterns to internalize:

1. `func(expr for x in xs if cond)` — pass the gen-exp as a sole
   argument and the parentheses can be elided. Use with sum / any /
   all / max / min.
2. `next((expr for x in xs if cond), default)` — find-first with a
   safe default. The default is critical; without it, an empty match
   raises StopIteration.

Traps worth knowing:
- `all([])` is True (vacuous truth). `any([])` is False.
- `max([])` raises; use `max(..., default=0)`.
- `next(gen)` with no default raises on empty.

Coverage map:
    generator + sum/any/all/max       total_squared, any_negative,
                                      all_positive, max_word_length
    next(gen, default) find-first     first_negative, first_key_with_value
"""

CONSTRAINTS = """
- Solve each prompt in a single expression where possible.
- Inputs may be empty; handle the empty case via the reducer's
  default argument or next()'s default — NOT a conditional.
- Don't import anything; everything here is plain builtins.
"""

STUBS = [
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
]

CASES = {
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
}

MUTATES_INPUT = False
