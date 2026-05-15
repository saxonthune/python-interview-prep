"""
Spec for: first_non_repeating_char
"""

TITLE = "First Non-Repeating Character"

DESCRIPTION = """
Given a string, return the index of the first character that does NOT
repeat anywhere else in the string. "Repeating" means occurring more
than once anywhere in the string -- nothing to do with adjacency.
If no such character exists, return -1.

Example:
    s = "loveleetcode"
    -> 2 ('v' is the first character whose total count in s is 1.
          'l', 'o', 'e' all appear more than once.)

Traps:
- "First character that's unique SO FAR" is wrong. You need overall
  counts across the whole string, not a running first-seen check.
  e.g. "abcabd" -> 2 ('c'), not 0 ('a' repeats later).
- Comparison is case-sensitive: 'a' and 'A' are distinct.
- Empty string returns -1.
"""

CONSTRAINTS = """
- 0 <= len(s) <= 10^5
- s may contain any unicode characters (don't assume ASCII-only)
- Case-sensitive
"""

SIGNATURE = "def solution(s: str) -> int:"

CASES = [
    # canonical: first char is unique
    ("leetcode", 0),
    # unique is buried in the middle
    ("loveleetcode", 2),
    # no unique character at all
    ("aabb", -1),
    # single character
    ("z", 0),
    # empty string
    ("", -1),
    # unique is the last character
    ("aabbc", 4),
    # trap: 'a' and 'b' both repeat LATER -- naive first-seen returns 0
    ("abcabd", 2),
    # case sensitivity: 'a' != 'A', so index 0 is unique
    ("aAbBcC", 0),
]

MUTATES_INPUT = False
