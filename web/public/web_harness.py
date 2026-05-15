"""In-Pyodide test runner. Mirrors drill/harness.py with two differences:

1. Cases arrive as Python objects revived from JSON (markers like
   {"__tree__": [...]} get turned back into TreeNode etc. here).
2. Output goes to stdout for the browser to pipe into a <pre>.

Entrypoint: run_problem(kind, payload, user_globals).

- `kind` is "function", "class", or "multi".
- `payload` is the per-problem dict from problems.json.
- `user_globals` is the dict produced by exec'ing the user's editor code.
"""
import time
from copy import deepcopy

from utils import TreeNode, ListNode, build_tree, build_list


def _revive(obj):
    if isinstance(obj, dict):
        if "__tree__" in obj:
            return build_tree(obj["__tree__"])
        if "__list__" in obj:
            return build_list([_revive(x) for x in obj["__list__"]])
        if "__set__" in obj:
            return {_revive(x) for x in obj["__set__"]}
        if "__tuple__" in obj:
            return tuple(_revive(x) for x in obj["__tuple__"])
        if "__ellipsis__" in obj:
            return Ellipsis
        return {k: _revive(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_revive(x) for x in obj]
    return obj


def _compare(r, e):
    # structural equality covers list/dict/set; TreeNode and ListNode need
    # a value walk because their __eq__ is identity.
    if isinstance(r, TreeNode) or isinstance(e, TreeNode):
        return _tree_eq(r, e)
    if isinstance(r, ListNode) or isinstance(e, ListNode):
        return _list_eq(r, e)
    return r == e


def _tree_eq(a, b):
    if a is None or b is None:
        return a is None and b is None
    if not (isinstance(a, TreeNode) and isinstance(b, TreeNode)):
        return False
    return a.val == b.val and _tree_eq(a.left, b.left) and _tree_eq(a.right, b.right)


def _list_eq(a, b):
    while a is not None and b is not None:
        if a.val != b.val:
            return False
        a, b = a.next, b.next
    return a is None and b is None


def _run_function(payload, user_globals):
    fn = user_globals.get("solution")
    if fn is None:
        print("✗ no `solution` function defined")
        return False
    cases = _revive(payload["cases"])
    mutates = payload.get("mutates_input", False)
    passed = 0
    total = len(cases)
    for i, case in enumerate(cases):
        args, expected = case[0], case[1]
        if mutates:
            args = deepcopy(args)
        call_args = args if isinstance(args, tuple) else (args,)
        try:
            start = time.perf_counter()
            result = fn(*call_args)
            elapsed_ms = (time.perf_counter() - start) * 1000
            ok = _compare(result, expected)
        except Exception as e:
            print(f"✗ Case {i}: RAISED {type(e).__name__}: {e}")
            continue
        if ok:
            passed += 1
            print(f"✓ Case {i} ({elapsed_ms:.2f}ms)")
        else:
            print(f"✗ Case {i} ({elapsed_ms:.2f}ms): got {result!r}, expected {expected!r}")
    print(f"\n{passed}/{total} passed")
    return passed == total


def _run_class(payload, user_globals):
    name = payload["class_name"]
    cls = user_globals.get(name)
    if cls is None:
        print(f"✗ no class `{name}` defined")
        return False
    cases = _revive(payload["cases"])
    passed = 0
    total = 0
    for ti, trace in enumerate(cases):
        init_args, ops = trace[0], trace[1]
        if not isinstance(init_args, tuple):
            init_args = tuple(init_args) if isinstance(init_args, list) else (init_args,)
        try:
            instance = cls(*init_args)
        except Exception as e:
            print(f"✗ Trace {ti}: __init__{init_args} RAISED {type(e).__name__}: {e}")
            total += len(ops)
            continue
        trace_passed = 0
        trace_total = len(ops)
        trace_start = time.perf_counter()
        for oi, op in enumerate(ops):
            method, args, expected = op[0], op[1], op[2]
            total += 1
            call_args = args if isinstance(args, tuple) else (args,)
            try:
                result = getattr(instance, method)(*call_args)
                ok = expected is Ellipsis or _compare(result, expected)
            except Exception as e:
                print(f"✗ Trace {ti}.op{oi} {method}{call_args}: RAISED {type(e).__name__}: {e}")
                continue
            if ok:
                passed += 1
                trace_passed += 1
            else:
                print(f"✗ Trace {ti}.op{oi} {method}{call_args}: got {result!r}, expected {expected!r}")
        trace_ms = (time.perf_counter() - trace_start) * 1000
        if trace_passed == trace_total:
            print(f"✓ Trace {ti} ({trace_total} ops, {trace_ms:.2f}ms)")
        else:
            print(f"  Trace {ti}: {trace_passed}/{trace_total} ops passed ({trace_ms:.2f}ms)")
    print(f"\n{passed}/{total} ops passed")
    return passed == total


def _run_multi(payload, user_globals):
    cases_by_name = _revive(payload["cases"])
    total_passed = 0
    total_cases = 0
    for name in payload["function_names"]:
        fn = user_globals.get(name)
        cases = cases_by_name.get(name, [])
        n = len(cases)
        passed = 0
        failures = []
        if fn is None:
            print(f"✗ {name}: not defined")
            total_cases += n
            continue
        for i, case in enumerate(cases):
            args, expected = case[0], case[1]
            call_args = args if isinstance(args, tuple) else (args,)
            try:
                result = fn(*call_args)
                ok = _compare(result, expected)
            except Exception as e:
                failures.append(f"    case {i}: RAISED {type(e).__name__}: {e}")
                continue
            if ok:
                passed += 1
            else:
                failures.append(f"    case {i} {call_args}: got {result!r}, expected {expected!r}")
        total_passed += passed
        total_cases += n
        marker = "✓" if passed == n else "✗"
        print(f"{marker} {name}: {passed}/{n}")
        for f in failures:
            print(f)
    print(f"\n{total_passed}/{total_cases} passed")
    return total_passed == total_cases


def run_problem(kind, payload, user_globals):
    if kind == "function":
        return _run_function(payload, user_globals)
    if kind == "class":
        return _run_class(payload, user_globals)
    if kind == "multi":
        return _run_multi(payload, user_globals)
    raise ValueError(f"unknown kind: {kind!r}")
