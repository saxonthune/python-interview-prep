"""
Spec for: valid_brackets
"""

TITLE = "Valid Brackets"

DESCRIPTION = """
Given a string s containing only the characters '(', ')', '{', '}',
'[' and ']', determine if the brackets are properly nested.

A string is valid if:
- every opening bracket is closed by the SAME type of bracket, AND
- brackets are closed in the correct (LIFO) order, AND
- every opening bracket has a matching close (stack is empty at end).

Example:
    s = "{[]}"      -> True
    s = "([)]"      -> False  (interleaved, not nested)
    s = "("         -> False  (unclosed)

Traps:
- Interleaving is NOT nesting. "([)]" has matching counts of each
  bracket type but the close order is wrong.
- Counting opens vs. closes is insufficient -- "(){" has equal opens
  and closes overall but is invalid (also "][" has count parity).
- Don't forget to check the stack is empty at the END. A run that
  never hits a mismatch but leaves opens on the stack (e.g. "(") is
  still invalid.
- Empty string is vacuously valid.
"""

CONSTRAINTS = """
- 0 <= len(s) <= 10^4
- s contains only the characters '()[]{}'
"""

SIGNATURE = "def solution(s: str) -> bool:"

CASES = [
    # simplest valid pair
    ("()", True),
    # sequential, all three types
    ("()[]{}", True),
    # properly nested, two levels
    ("{[]}", True),
    # deep nesting, all three types
    ("([{}])", True),
    # mismatched close type
    ("(]", False),
    # trap: interleaved, not nested
    ("([)]", False),
    # empty string is vacuously valid
    ("", True),
    # single unclosed open
    ("(", False),
    # close with empty stack
    (")", False),
    # multiple unclosed
    ("((", False),
    # multiple stray closes
    ("))", False),
    # balanced counts per type, but wrong close order
    ("({[)]}", False),
]

MUTATES_INPUT = False
