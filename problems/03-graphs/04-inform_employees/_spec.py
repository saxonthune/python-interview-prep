"""
Spec for: inform_employees

Weighted-tree longest-path problem. The CEO sends an email; each manager
takes `delay` minutes to inform their direct reports (in parallel), and
those reports then inform their own subordinates. Return the number of
minutes until the last employee receives the email.
"""

TITLE = "Time Needed to Inform All Employees"

DESCRIPTION = """
You are given a list of employees as tuples (id, manager_id, delay).

The CEO is identified by manager_id == -1. `delay` on each employee is
the time that employee takes to inform their direct reports (so the
CEO's delay is the time before the CEO's reports receive the email).

When a manager receives the email, they take `delay` minutes to inform
all of their direct reports (informing happens in parallel — every
direct report receives it at the same moment, `delay` minutes later).
Each report then independently informs their own subordinates after
their own delay. Leaves have no one to inform, so their delay does not
contribute.

Return the total number of minutes until every employee has been
informed — equivalently, the maximum weighted root-to-leaf path in the
management tree, where edge weight is the parent's delay.

Example:
    employees = [
        (0, -1, 5),  # CEO, takes 5 min to inform reports
        (1,  0, 3),  # report of CEO, takes 3 to inform their reports
        (2,  0, 1),  # report of CEO, takes 1
        (3,  1, 0),  # leaf under 1
        (4,  2, 0),  # leaf under 2
    ]
    Path to 3: 5 + 3 = 8
    Path to 4: 5 + 1 = 6
    -> 8

Edges to watch:
- The input order is arbitrary — don't assume index == id or that
  parents appear before children.
- Leaf delay is irrelevant (no one to inform).
- The tree may be a single node (just the CEO) -> 0.
"""

CONSTRAINTS = """
- Exactly one employee has manager_id == -1 (the CEO)
- ids are unique
- The structure is a tree (no cycles, every non-CEO has exactly one manager)
- delay >= 0
- 1 <= len(employees)
"""

SIGNATURE = "def solution(employees: list[tuple[int, int, int]]) -> int:"

CASES = [
    # CEO only, no one to inform
    ([(0, -1, 0)], 0),

    # CEO with one direct report; CEO delay = 1
    ([(0, -1, 1), (1, 0, 0)], 1),

    # Branching: longer branch wins
    ([(0, -1, 5), (1, 0, 3), (2, 0, 1), (3, 1, 0), (4, 2, 0)], 8),

    # Linear chain 0 -> 1 -> 2 -> 3 with delays 1,2,3,4 (last delay irrelevant)
    ([(0, -1, 1), (1, 0, 2), (2, 1, 3), (3, 2, 4)], 6),

    # LeetCode 1376 example: n=6, head=2, all delays 0 except CEO=1
    # manager=[2,2,-1,2,2,2], informTime=[0,0,1,0,0,0] -> 1
    ([(0, 2, 0), (1, 2, 0), (2, -1, 1), (3, 2, 0), (4, 2, 0), (5, 2, 0)], 1),

    # Input given out of order (children before parents, ids not sequential)
    ([(7, 3, 0), (3, 1, 4), (1, -1, 2), (5, 1, 1), (9, 5, 0)], 6),

    # Two branches of equal length — either is fine, max is the same
    ([(0, -1, 2), (1, 0, 3), (2, 0, 3), (3, 1, 0), (4, 2, 0)], 5),

    # Deeper branch with smaller per-step delay still wins on total
    ([(0, -1, 1), (1, 0, 1), (2, 1, 1), (3, 2, 1), (4, 0, 10), (5, 4, 0)], 11),
]

MUTATES_INPUT = False
