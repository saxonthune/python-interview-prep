"""Walk problems/, build problems.json and copy web_harness for the web layer.

Usage:
    python build/transform.py

Output:
    web/public/problems.json
    web/public/web_harness.py
    web/public/utils.py            # copy of utils/__init__.py for Pyodide FS
"""
import importlib.util
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from build.encoders import encode  # noqa: E402


PROBLEMS_DIR = os.path.join(ROOT, "problems")
WEB_PUBLIC = os.path.join(ROOT, "web", "public")


def _load_spec(spec_path: str):
    name = "_spec_" + re.sub(r"\W+", "_", spec_path)
    spec = importlib.util.spec_from_file_location(name, spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fn_name(sig: str) -> str:
    m = re.match(r"\s*def\s+(\w+)\s*\(", sig)
    if not m:
        raise ValueError(f"can't parse function name from: {sig!r}")
    return m.group(1)


def _skeleton_function(sig: str) -> str:
    return "\n".join([
        sig,
        '    """YOUR CODE HERE"""',
        "    pass",
        "",
    ])


def _skeleton_class(sig: str) -> str:
    return sig + "\n"


def _skeleton_multi(stubs) -> str:
    out = []
    for section, sig, prompt in stubs:
        if section:
            out.append(f"# ---------- {section} ----------")
            out.append("")
        out.append(sig)
        out.append(f'    """{prompt}"""')
        out.append('    """YOUR CODE HERE"""')
        out.append("    pass")
        out.append("")
    return "\n".join(out)


def _problem_id(spec_path: str) -> str:
    rel = os.path.relpath(os.path.dirname(spec_path), PROBLEMS_DIR)
    return rel.replace(os.sep, "/")


def _topic(problem_id: str) -> str:
    head = problem_id.split("/", 1)[0]
    return re.sub(r"^\d+-", "", head)


def _build_one(spec_path: str) -> dict:
    spec = _load_spec(spec_path)
    pid = _problem_id(spec_path)
    base = {
        "id": pid,
        "topic": _topic(pid),
        "title": getattr(spec, "TITLE", pid),
        "description": getattr(spec, "DESCRIPTION", "").strip(),
        "constraints": getattr(spec, "CONSTRAINTS", "").strip(),
    }

    if hasattr(spec, "STUBS"):
        names = [_fn_name(sig) for _, sig, _ in spec.STUBS]
        base.update({
            "kind": "multi",
            "skeleton": _skeleton_multi(spec.STUBS),
            "function_names": names,
            "cases": encode(spec.CASES),
        })
    elif hasattr(spec, "CLASS_NAME"):
        base.update({
            "kind": "class",
            "class_name": spec.CLASS_NAME,
            "signature": spec.SIGNATURE,
            "skeleton": _skeleton_class(spec.SIGNATURE),
            "cases": encode(spec.CASES),
        })
    elif hasattr(spec, "SIGNATURE"):
        base.update({
            "kind": "function",
            "signature": spec.SIGNATURE,
            "skeleton": _skeleton_function(spec.SIGNATURE),
            "mutates_input": bool(getattr(spec, "MUTATES_INPUT", False)),
            "cases": encode(spec.CASES),
        })
    else:
        raise ValueError(f"{spec_path}: missing STUBS / CLASS_NAME / SIGNATURE")

    return base


def _natural_key(s: str):
    parts = re.split(r"(\d+)", s)
    return [int(p) if p.isdigit() else p for p in parts]


def collect() -> list[dict]:
    specs = []
    for dirpath, _, filenames in os.walk(PROBLEMS_DIR):
        if "_spec.py" in filenames:
            specs.append(os.path.join(dirpath, "_spec.py"))
    specs.sort(key=lambda p: _natural_key(os.path.relpath(p, PROBLEMS_DIR)))
    return [_build_one(p) for p in specs]


def main():
    problems = collect()
    os.makedirs(WEB_PUBLIC, exist_ok=True)

    out_path = os.path.join(WEB_PUBLIC, "problems.json")
    with open(out_path, "w") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"wrote {out_path} ({len(problems)} problems)")

    for src_name, dst_name in [
        (os.path.join(HERE, "web_harness.py"), "web_harness.py"),
        (os.path.join(ROOT, "utils", "__init__.py"), "utils.py"),
    ]:
        dst = os.path.join(WEB_PUBLIC, dst_name)
        shutil.copyfile(src_name, dst)
        print(f"copied {dst}")


if __name__ == "__main__":
    main()
