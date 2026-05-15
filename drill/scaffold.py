"""
Scaffold solution.py from a problem's _spec.py.

Single-function problems (`SIGNATURE` string, `solution` as the function name):
    _spec.py exposes TITLE, SIGNATURE, CASES, MUTATES_INPUT.
    Emits a solution.py with the standard bootstrap, the signature stub,
    and a __main__ that calls run(solution, CASES, ...).

Multi-function drills (`STUBS` list):
    _spec.py exposes STUBS = [(section_or_None, signature, prompt), ...]
    and CASES as a dict keyed by function name.
    Emits one stub per entry, a DRILLS list, and __main__ that calls
    run_many(DRILLS).

Usage:
    python drill/scaffold.py problems/05-comprehensions/01-basics/
    python drill/scaffold.py problems/05-comprehensions/01-basics/ --force
"""
import argparse
import importlib.util
import os
import re
import sys


BOOTSTRAP = '''import sys, os
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


def _fn_name(sig: str) -> str:
    m = re.match(r"\s*def\s+(\w+)\s*\(", sig)
    if not m:
        raise ValueError(f"can't parse function name from: {sig!r}")
    return m.group(1)


def _load_spec(spec_path: str):
    spec = importlib.util.spec_from_file_location("_spec_for_scaffold", spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _render_multi(stubs) -> str:
    out = [BOOTSTRAP, "from drill.harness import run_many", "from _spec import CASES", "", ""]
    names = []
    for section, sig, prompt in stubs:
        if section:
            out.append(f"# ---------- {section} ----------")
            out.append("")
        out.append(sig)
        out.append(f'    """{prompt}"""')
        out.append('    """YOUR CODE HERE"""')
        out.append("    pass")
        out.append("")
        names.append(_fn_name(sig))

    out.append("")
    out.append("DRILLS = [")
    for n in names:
        out.append(f'    ({n}, CASES["{n}"]),')
    out.append("]")
    out.append("")
    out.append("")
    out.append('if __name__ == "__main__":')
    out.append("    run_many(DRILLS)")
    out.append("")
    return "\n".join(out)


def _render_single(signature: str) -> str:
    out = [
        BOOTSTRAP,
        "from drill.harness import run",
        "from _spec import CASES, MUTATES_INPUT",
        "",
        "",
        signature,
        '    """YOUR CODE HERE"""',
        "    pass",
        "",
        "",
        'if __name__ == "__main__":',
        "    run(solution, CASES, mutates_input=MUTATES_INPUT)",
        "",
    ]
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("problem_dir")
    p.add_argument("--force", action="store_true", help="overwrite existing solution.py")
    args = p.parse_args()

    pdir = os.path.abspath(args.problem_dir)
    spec_path = os.path.join(pdir, "_spec.py")
    sol_path = os.path.join(pdir, "solution.py")
    if not os.path.exists(spec_path):
        sys.exit(f"no _spec.py at {spec_path}")
    if os.path.exists(sol_path) and not args.force:
        sys.exit(f"refusing to overwrite existing {sol_path} (use --force)")

    spec = _load_spec(spec_path)
    if hasattr(spec, "STUBS"):
        content = _render_multi(spec.STUBS)
    elif hasattr(spec, "SIGNATURE"):
        content = _render_single(spec.SIGNATURE)
    else:
        sys.exit("_spec.py must define either STUBS (multi) or SIGNATURE (single)")

    with open(sol_path, "w") as f:
        f.write(content)
    print(f"wrote {sol_path}")


if __name__ == "__main__":
    main()
