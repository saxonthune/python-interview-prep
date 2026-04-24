# Python Interview Prep

## Quick Start

Roll your own interview coding challenges (in Python). Supports leetcode-style problems or 'implement this class' problems. To get started, use 
```bash
python drill.py reset --all
```
> The below readme content is AI-generated. Apologies.

---

A repo for drilling coding problems. Each problem is defined once in a
spec file. Drilling regenerates a blank `solution.py` from the spec.

## Daily flow

```bash
python drill.py list                      # list all problems
python drill.py reset lru_cache           # wipes solution.py, fresh slate
# ... edit problems/03-design/02-lru_cache/solution.py ...
python drill.py test lru_cache            # run tests
```

You can also open any `solution.py` in VS Code and hit the ▶ Run button —
equivalent to `test` (but won't reset).

## Commands

| Command | What it does |
|---|---|
| `python drill.py reset <name>` | Wipe & regenerate `solution.py` from spec. |
| `python drill.py reset --all` | Regenerate `solution.py` for every problem (use after cloning). |
| `python drill.py test <name>` | Run the current solution against test cases. |
| `python drill.py promote <name>` | Archive `solution.py` as the next `example_NN.py` and regen a fresh `solution.py`. |
| `python drill.py new <path>` | Scaffold a new problem at the given path under `problems/`. |
| `python drill.py list` | List all problems with their full paths. |

`<name>` is either the leaf dir name (`lru_cache`) or the full path
(`03-design/02-lru_cache`). Leaf lookup errors out if ambiguous.

## UI

```bash
pip install pywebview
python ui.py
```

A desktop window with a tree of problems on the left and a detail pane
on the right (title, collapsible description/constraints, Reset and
Promote buttons).

On Linux, `pywebview` needs a system webview backend — either GTK
(`python3-gi` + `gir1.2-webkit2-4.1`) or Qt (`pip install pywebview[qt]`).

## Project layout

```
interview-prep/
├── drill.py                          # CLI: scaffold / reset / run / list
├── utils/__init__.py                 # TreeNode, build_tree, build_graph, ...
├── drill/
│   ├── harness.py                    # run() and run_class() test runners
│   └── _starter_template.py
└── problems/
    ├── 01-trees/
    │   ├── 01-basics/
    │   │   ├── 01-dfs/
    │   │   └── 02-bfs/
    │   └── 02-same_tree/
    ├── 02-graphs/
    │   ├── 01-basics/
    │   │   ├── 01-dfs/
    │   │   └── 02-bfs/
    │   ├── 02-num_islands/
    │   └── 03-count_components/
    └── 03-design/
        ├── 01-min_stack/
        ├── 02-lru_cache/
        └── 03-logger_rate_limiter/
```

Sections and problems are prefixed `NN-` for ordering. Sections can nest
arbitrarily deep — `drill.py` walks the tree looking for any dir with a
`_spec.py`.

Each problem dir has:
- `_spec.py` — description, constraints, signature, test cases
- `solution.py` — your attempt, regenerated every drill

## Adding a new problem

Two flavors: **function-style** (pass args, compare return value) and
**class-style** (stateful object, sequence of ops).

### Function-style

```bash
python drill.py new 01-trees/03-invert_tree
```

Then edit `problems/01-trees/03-invert_tree/_spec.py`:

```python
from utils import build_tree

TITLE = "Invert Binary Tree"

DESCRIPTION = """
Given the root of a binary tree, invert it and return the root.
"""

CONSTRAINTS = """
- 0 <= number of nodes <= 100
"""

SIGNATURE = "def solution(root: 'TreeNode | None') -> 'TreeNode | None':"

# Each case: (args, expected).
# args: single value, OR a tuple for multi-arg.
CASES = [
    (build_tree([4, 2, 7, 1, 3, 6, 9]),
     build_tree([4, 7, 2, 9, 6, 3, 1])),
    (build_tree([]), build_tree([])),
]

MUTATES_INPUT = False   # True if your solution modifies the input
```

Drill and run:
```bash
python drill.py reset invert_tree
# edit problems/01-trees/03-invert_tree/solution.py
python drill.py test invert_tree
```

### Class-style (stateful design problems)

Add `CLASS_NAME` to the spec and make `SIGNATURE` a full class skeleton
with method stubs. Cases become traces of method calls.

```python
TITLE = "My Cache"
DESCRIPTION = """..."""
CONSTRAINTS = """..."""

CLASS_NAME = "MyCache"

SIGNATURE = '''class MyCache:
    def __init__(self, capacity: int):
        """YOUR CODE HERE"""
        pass

    def get(self, key: int) -> int:
        pass

    def put(self, key: int, value: int) -> None:
        pass'''

# Each trace: (init_args_tuple, [(method, args, expected), ...])
#   init_args is always a tuple: (2,) for one arg, () for none
#   per-op args follows the function-harness rule: tuple => splat, single => wrap
#   use Ellipsis (...) as expected to skip the return check
CASES = [
    ((2,), [
        ("put", (1, 1), None),
        ("put", (2, 2), None),
        ("get",  1,     1),
        ("put", (3, 3), None),
        ("get",  2,    -1),
    ]),
]
```

The harness instantiates a fresh object per trace. Per-op failures print
individually; a fully-passing trace collapses to one summary line.
