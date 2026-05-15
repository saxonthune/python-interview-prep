"""
Spec for: set and dict comprehensions drill.

The second of three comprehension units. Covers set comprehensions and
the three core dict-comprehension patterns: build, invert, filter.
"""

TITLE = "Comprehensions: Set and Dict"

DESCRIPTION = """
Practice set and dict comprehensions. The syntax mirrors list comps
but with `{}` braces; for dicts you write `key: value` after the brace.

Aim to solve each in ONE expression. The dict-comprehension patterns
here cover the three things you'll do 90% of the time: build from a
sequence, invert an existing dict, and filter an existing dict.

Coverage map:
    set comp                          unique_lengths
    dict comp / build                 length_by_word
    dict comp / invert                invert_dict
    dict comp / filter                filter_dict_by_value
"""

CONSTRAINTS = """
- Solve each prompt in a single expression where possible.
- Inputs may be empty; handle the empty case naturally.
- Don't import anything; everything here is plain builtins.
"""

STUBS = [
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
]

CASES = {
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
}

MUTATES_INPUT = False
