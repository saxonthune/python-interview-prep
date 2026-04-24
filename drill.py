#!/usr/bin/env python3
"""
Drill a problem. Usage:

    python drill.py reset   same_tree                     # wipe & regenerate solution.py
    python drill.py reset   01-trees/02-same_tree         # full path also works
    python drill.py test    same_tree                     # run tests without resetting
    python drill.py promote same_tree                     # archive solution.py as example_NN.py
    python drill.py list                                  # list all problems
    python drill.py new     01-trees/03-invert_tree       # scaffold a new problem

`reset` regenerates solution.py from _spec.py — your old attempt is gone.
If you want to preserve it, use `test` instead.
"""
import re
import sys
import argparse
import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
PROBLEMS = ROOT / "problems"


def iter_problem_dirs():
    """Yield every directory under problems/ that contains a _spec.py."""
    if not PROBLEMS.exists():
        return
    for spec in PROBLEMS.rglob("_spec.py"):
        yield spec.parent


def list_problems():
    dirs = sorted(iter_problem_dirs())
    if not dirs:
        print("No problems yet. Create one with --new <path>")
        return
    for d in dirs:
        print(f"  {d.relative_to(PROBLEMS)}")


def resolve(name):
    """Resolve a user-supplied name to a problem dir.

    Accepts either an exact relative path (`01-trees/02-same_tree`) or a
    leaf name (`same_tree`, matched against the trailing `-name` of any dir).
    """
    name = name.strip("/")
    exact = PROBLEMS / name
    if (exact / "_spec.py").exists():
        return exact

    matches = []
    for d in iter_problem_dirs():
        leaf = d.name
        # strip leading "NN-" if present
        bare = leaf.split("-", 1)[1] if leaf[:2].isdigit() and "-" in leaf else leaf
        if leaf == name or bare == name:
            matches.append(d)
    if not matches:
        print(f"No problem matching '{name}'. Try --list.")
        return None
    if len(matches) > 1:
        print(f"Ambiguous '{name}'. Matches:")
        for m in matches:
            print(f"  {m.relative_to(PROBLEMS)}")
        return None
    return matches[0]


def load_spec(spec_file):
    spec = importlib.util.spec_from_file_location("_spec", spec_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_solution_content(problem_dir):
    """Return the fresh solution.py text for a problem, or None if no spec."""
    spec_file = problem_dir / "_spec.py"
    if not spec_file.exists():
        return None

    s = load_spec(spec_file)
    title = getattr(s, "TITLE", problem_dir.name)
    description = getattr(s, "DESCRIPTION", "").strip()
    constraints = getattr(s, "CONSTRAINTS", "").strip()
    signature = getattr(s, "SIGNATURE", "def solution():").strip()
    class_name = getattr(s, "CLASS_NAME", None)

    header = f'''"""
{title}

{description}

Constraints:
{constraints}
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
'''

    if class_name:
        # class-style: SIGNATURE is the full class skeleton
        body = f'''from drill.harness import run_class
from _spec import CASES


{signature}


if __name__ == "__main__":
    run_class({class_name}, CASES)
'''
    else:
        # function-style
        body = f'''from drill.harness import run
from _spec import CASES, MUTATES_INPUT


{signature}
    """YOUR CODE HERE"""
    pass


if __name__ == "__main__":
    run(solution, CASES, mutates_input=MUTATES_INPUT)
'''
    return header + body


def reset_solution(problem_dir):
    """Regenerate solution.py from _spec.py. The 'clean slate' operation."""
    content = build_solution_content(problem_dir)
    if content is None:
        print(f"No spec at {problem_dir / '_spec.py'}")
        return False
    (problem_dir / "solution.py").write_text(content)
    lastrun = problem_dir / "lastrun.log"
    if lastrun.exists():
        lastrun.unlink()
    return True


def new_problem(path):
    problem_dir = PROBLEMS / path.strip("/")
    if problem_dir.exists() and (problem_dir / "_spec.py").exists():
        print(f"Problem '{path}' already exists.")
        return
    problem_dir.mkdir(parents=True, exist_ok=True)

    name = problem_dir.name
    bare = name.split("-", 1)[1] if name[:2].isdigit() and "-" in name else name
    spec_content = f'''"""
Spec for: {bare}
"""

TITLE = "{bare.replace('_', ' ').title()}"

DESCRIPTION = """
Describe the problem here. Include input/output format.
"""

CONSTRAINTS = """
- List constraints
"""

SIGNATURE = "def solution(arg) -> None:"  # add type hints, e.g. (root: 'TreeNode | None') -> list[int]

CASES = [
    # (input, expected),
]

MUTATES_INPUT = False
'''
    (problem_dir / "_spec.py").write_text(spec_content)
    reset_solution(problem_dir)
    rel = problem_dir.relative_to(PROBLEMS)
    print(f"Created problem '{rel}'.")
    print(f"  Spec:     problems/{rel}/_spec.py  (edit this)")
    print(f"  Solution: problems/{rel}/solution.py  (drill here)")


EXAMPLE_RE = re.compile(r"^example_(\d+)\.py$")


def promote_solution(problem_dir):
    """Archive solution.py as example_NN.py, then regenerate a fresh solution.py."""
    solution_file = problem_dir / "solution.py"
    if not solution_file.exists():
        print(f"No solution.py at {solution_file}. Nothing to promote.")
        return False

    highest = 0
    for f in problem_dir.iterdir():
        m = EXAMPLE_RE.match(f.name)
        if m:
            highest = max(highest, int(m.group(1)))
    next_n = highest + 1
    target = problem_dir / f"example_{next_n:02d}.py"

    solution_file.rename(target)
    reset_solution(problem_dir)
    rel = problem_dir.relative_to(PROBLEMS)
    print(f"Promoted: problems/{rel}/{target.name}")
    print(f"Fresh slate ready: problems/{rel}/solution.py")
    return True


def run_solution(problem_dir):
    solution_file = problem_dir / "solution.py"
    if not solution_file.exists():
        print(f"No solution.py at {solution_file}. Drill first.")
        return
    proc = subprocess.run(
        [sys.executable, str(solution_file)],
        capture_output=True, text=True,
    )
    output = proc.stdout + (proc.stderr if proc.stderr else "")
    sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    (problem_dir / "lastrun.log").write_text(output)


def main():
    parser = argparse.ArgumentParser(description="Drill coding problems.")
    sub = parser.add_subparsers(dest="cmd", metavar="<command>")

    p_reset = sub.add_parser("reset", help="Wipe & regenerate solution.py from spec")
    p_reset.add_argument("name", nargs="?", help="Problem name or path under problems/")
    p_reset.add_argument("--all", action="store_true", help="Reset every problem")

    p_test = sub.add_parser("test", help="Run the current solution against test cases")
    p_test.add_argument("name", help="Problem name or path under problems/")

    p_promote = sub.add_parser("promote", help="Archive solution.py as example_NN.py and regen a fresh solution.py")
    p_promote.add_argument("name", help="Problem name or path under problems/")

    p_new = sub.add_parser("new", help="Scaffold a new problem at the given path under problems/")
    p_new.add_argument("path", help="Path under problems/, e.g. 01-trees/03-invert_tree")

    sub.add_parser("list", help="List all problems")

    args = parser.parse_args()

    if args.cmd == "list":
        list_problems()
    elif args.cmd == "new":
        new_problem(args.path)
    elif args.cmd == "reset":
        if args.all:
            count = 0
            for problem_dir in iter_problem_dirs():
                if reset_solution(problem_dir):
                    print(f"  reset problems/{problem_dir.relative_to(PROBLEMS)}")
                    count += 1
            print(f"Reset {count} problem(s).")
            return
        if not args.name:
            p_reset.error("name is required unless --all is given")
        problem_dir = resolve(args.name)
        if not problem_dir:
            return
        if reset_solution(problem_dir):
            rel = problem_dir.relative_to(PROBLEMS)
            print(f"Fresh slate ready: problems/{rel}/solution.py")
            print(f"Run tests: python drill.py test {args.name}")
    elif args.cmd == "test":
        problem_dir = resolve(args.name)
        if not problem_dir:
            return
        run_solution(problem_dir)
    elif args.cmd == "promote":
        problem_dir = resolve(args.name)
        if not problem_dir:
            return
        promote_solution(problem_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
