# python-interview-prep

A drill repo of interview problems. Each problem is a self-contained directory
with a spec and a solution skeleton, run via a shared harness.

## Layout

```
problems/
  <NN>-<topic>/
    <NN>-<problem_slug>/
      _spec.py
      solution.py
drill/
  harness.py        # run(...) for functions, run_class(...) for class designs
utils/
```

Topic directories and problem directories are both numbered (`01-`, `02-`, …)
to give a stable order. When adding a new problem, pick the next number in the
chosen topic.

## Two problem styles

**Function-style** (most graph/tree/array problems):
- `_spec.py` exposes `TITLE`, `DESCRIPTION`, `CONSTRAINTS`, `SIGNATURE`,
  `CASES`, `MUTATES_INPUT`.
- `CASES` is a list of `(args, expected)`. If `args` is a tuple it's
  splatted as positional args; otherwise it's passed as a single arg.
- `solution.py` defines `def solution(...)` and calls
  `run(solution, CASES, mutates_input=MUTATES_INPUT)`.

**Class-style** (stateful designs like LRU, Logger, MinStack):
- `_spec.py` additionally exposes `CLASS_NAME`. `CASES` is a list of
  `(init_args, ops)` where `ops` is a list of `(method, args, expected)`.
  Use `Ellipsis` as `expected` to skip a check.
- `solution.py` defines the class and calls `run_class(Cls, CASES)`.

Pick the style that matches the problem. Class-style is only for problems that
are inherently about designing a stateful object; everything else is
function-style, even when it lives under a "design"-flavored topic.

## Conventions for new specs

- `DESCRIPTION` should include a worked example and call out edge cases /
  traps the implementer is likely to miss.
- `CONSTRAINTS` lists input bounds and invariants.
- Test cases should cover: the canonical example, boundary conditions, the
  trap cases mentioned in the description, and at least one adversarial /
  out-of-order input where applicable. Mirror the density of cases in
  neighboring problems rather than the bare minimum.
- The `solution.py` skeleton leaves the function/class body as
  `"""YOUR CODE HERE"""` + `pass`. Don't pre-fill the solution unless asked.
- The bootstrap block at the top of `solution.py` (the `_root` walk-up plus
  `sys.path` inserts, then `from utils import *` and
  `from drill.harness import run`) is identical across problems — copy it
  verbatim from a neighbor.

## Workflow when the user asks to add a problem

1. Confirm the topic placement before writing — if the problem doesn't fit
   the topic the user named, flag it.
2. Read a neighboring problem in the chosen topic to mirror its spec shape
   and bootstrap block exactly.
3. Run the proposed shape (signature, case list outline) by the user before
   writing files, unless they've said to skip that.
4. Hand-verify every expected value in `CASES`. Off-by-one and
   "leaf-delay-doesn't-count"-style mistakes are easy to make and the
   harness can't catch them.
