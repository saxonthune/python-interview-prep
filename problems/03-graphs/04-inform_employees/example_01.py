"""
Time Needed to Inform All Employees

You are given a list of employees as tuples (id, manager_id, delay).
The CEO is identified by manager_id == -1. `delay` on each employee is
the time that employee takes to inform their direct reports.

Return the number of minutes until every employee has been informed —
i.e. the maximum weighted root-to-leaf path in the management tree,
where edge weight is the parent's delay.
"""
import sys, os
_here = os.path.dirname(os.path.abspath(__file__))
_root = _here
while not os.path.exists(os.path.join(_root, "drill.py")):
    parent = os.path.dirname(_root)
    if parent == _root:
        raise RuntimeError("Could not find repo root (no drill.py found above)")
    _root = parent
sys.path.insert(0, _root)
sys.path.insert(0, _here)

from utils import *
from drill.harness import run
from _spec import CASES, MUTATES_INPUT

#                                  id, mngr, delay
def solution(employees: list[tuple[int, int, int]]) -> int:
    """YOUR CODE HERE"""

    class Employee:
        def __init__(self, id, delay, manager_id, reports_ids: list[int]):
            self.id = id
            self.delay = delay
            self.reports = reports_ids
            self.manager_id = manager_id

    ee_lookup = {ee[0]: Employee(ee[0], ee[2], ee[1], []) for ee in employees}
    ceo_id = next(ee[0] for ee in employees if ee[1] == -1)
    ceo_id = next(ee for ee in ee_lookup.values() if ee.manager_id == -1).id
    ceo_id = next(id for id, ee in ee_lookup.items() if ee.manager_id == -1)

    # build reports
    for ee in employees:
        if ee[1] != -1:
            ee_lookup[ee[1]].reports.append(ee[0]) # add ee to manager's reports list

    def dfs(ee: Employee) -> int:
        if not ee.reports:
            return 0
        return ee.delay + max(dfs(ee_lookup[r]) for r in ee.reports)

    return dfs(ee_lookup[ceo_id])



if __name__ == "__main__":
    run(solution, CASES, mutates_input=MUTATES_INPUT)
