"""
Spec for: logger_rate_limiter
"""

TITLE = "Logger Rate Limiter"

DESCRIPTION = """
Design a logger that decides whether a message should be printed.

A message should print if and only if it has NOT been printed in the
last 10 seconds. Timestamps arrive in non-decreasing order.

Methods:
    __init__()
    shouldPrintMessage(timestamp, message) -> bool
        - True  => print the message (and record this timestamp)
        - False => suppress (don't update the recorded timestamp)

Example:
    log = Logger()
    log.shouldPrintMessage(1,  "foo")  -> True   (first time)
    log.shouldPrintMessage(2,  "bar")  -> True   ("bar" never seen)
    log.shouldPrintMessage(3,  "foo")  -> False  (gap = 2 < 10)
    log.shouldPrintMessage(11, "foo")  -> True   (gap = 10, allowed)
    log.shouldPrintMessage(12, "foo")  -> False  (gap = 1 since t=11)

Edge to watch: when shouldPrint returns False you must NOT update the
stored timestamp. Otherwise repeated suppressed calls would slide the
window forward and never let the message through.
"""

CONSTRAINTS = """
- Timestamps arrive in non-decreasing order
- 'Last 10 seconds' means: print only if (timestamp - last_printed) >= 10
- Message strings are arbitrary
"""

CLASS_NAME = "Logger"

SIGNATURE = '''class Logger:
    def __init__(self):
        """YOUR CODE HERE"""
        pass

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        pass'''

CASES = [
    # canonical LeetCode example
    ((), [
        ("shouldPrintMessage", (1,  "foo"), True),
        ("shouldPrintMessage", (2,  "bar"), True),
        ("shouldPrintMessage", (3,  "foo"), False),
        ("shouldPrintMessage", (8,  "bar"), False),
        ("shouldPrintMessage", (10, "foo"), False),
        ("shouldPrintMessage", (11, "foo"), True),
    ]),
    # exactly 10s boundary: gap == 10 should print (>= 10)
    ((), [
        ("shouldPrintMessage", (0,  "x"), True),
        ("shouldPrintMessage", (9,  "x"), False),
        ("shouldPrintMessage", (10, "x"), True),
    ]),
    # suppressed calls must NOT advance the window
    # (the trap: if False updates last-printed, "x" never prints again)
    ((), [
        ("shouldPrintMessage", (0,  "x"), True),
        ("shouldPrintMessage", (5,  "x"), False),    # suppressed
        ("shouldPrintMessage", (8,  "x"), False),    # still suppressed (last printed = 0)
        ("shouldPrintMessage", (10, "x"), True),     # 10 - 0 = 10 >= 10
    ]),
    # different messages are independent
    ((), [
        ("shouldPrintMessage", (1, "a"), True),
        ("shouldPrintMessage", (1, "b"), True),
        ("shouldPrintMessage", (1, "c"), True),
        ("shouldPrintMessage", (2, "a"), False),
        ("shouldPrintMessage", (2, "b"), False),
    ]),
    # same timestamp, same message: second call suppressed
    ((), [
        ("shouldPrintMessage", (5, "hi"), True),
        ("shouldPrintMessage", (5, "hi"), False),
    ]),
]
