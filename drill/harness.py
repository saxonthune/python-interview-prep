"""Reusable test runner. Import `run` and call it with your solution + cases."""
import time
from copy import deepcopy


def run(solution, cases, mutates_input=False, compare=None):
    """
    solution: the function to test
    cases: list of (args, expected) tuples. args can be a single value or a tuple.
    mutates_input: deepcopy args if the solution mutates them
    compare: optional custom comparison function (result, expected) -> bool
             (default: ==, but useful for trees/lists where you want structural equality)
    """
    if compare is None:
        compare = lambda r, e: r == e

    passed = 0
    total = len(cases)
    for i, (args, expected) in enumerate(cases):
        if mutates_input:
            args = deepcopy(args)
        # allow single-arg cases without forcing tuple syntax
        call_args = args if isinstance(args, tuple) else (args,)

        try:
            start = time.perf_counter()
            result = solution(*call_args)
            elapsed_ms = (time.perf_counter() - start) * 1000
            ok = compare(result, expected)
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


def run_class(cls, cases, compare=None):
    """
    For stateful design problems (LRU, rate limiter, etc.).

    cls: the class under test
    cases: list of traces. Each trace is (init_args, ops):
        - init_args: tuple of constructor args (use () for no-arg)
        - ops: list of (method_name, args, expected) triples.
            args follows the function-harness convention:
            tuple => splat, single value => wrapped.
            Use Ellipsis (...) as expected to skip the check.

    Each trace gets a fresh instance. Per-op failures print individually;
    a fully-passing trace collapses to one line.
    """
    if compare is None:
        compare = lambda r, e: r == e

    passed = 0
    total = 0
    for ti, (init_args, ops) in enumerate(cases):
        try:
            instance = cls(*init_args)
        except Exception as e:
            print(f"✗ Trace {ti}: __init__{tuple(init_args)} RAISED {type(e).__name__}: {e}")
            total += len(ops)
            continue

        trace_passed = 0
        trace_total = len(ops)
        trace_start = time.perf_counter()
        for oi, (method, args, expected) in enumerate(ops):
            total += 1
            call_args = args if isinstance(args, tuple) else (args,)
            try:
                result = getattr(instance, method)(*call_args)
                ok = expected is Ellipsis or compare(result, expected)
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
