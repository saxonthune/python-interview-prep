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
  harness.py        # run(...) for functions, run_class(...) for class designs,
                    # run_many(...) for multi-function drills
  scaffold.py       # generates solution.py from _spec.py
utils/
build/              # web build pipeline (see "Web layer" below)
web/                # Astro static site
Makefile            # transform / dev / build / clean targets
```

Topic directories and problem directories are both numbered (`01-`, `02-`, …)
to give a stable order. When adding a new problem, pick the next number in the
chosen topic.

## Three problem styles

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

**Multi-function drill** (small-prompt practice sets like comprehensions):
- `_spec.py` exposes `STUBS = [(section_or_None, signature, prompt), ...]`
  and `CASES` as a `dict` keyed by function name.
- The scaffold emits one stub per `STUBS` entry plus a `DRILLS` list, and
  `solution.py` calls `run_many(DRILLS)`.
- Use this when the unit of practice is a one-line expression and you want
  ~10–20 prompts together in one file, not full problems.

Pick the style that matches the problem. Class-style is only for problems that
are inherently about designing a stateful object. Multi-function drills are for
syntax/idiom practice where each prompt is too small to merit its own
directory. Everything else is function-style, even when it lives under a
"design"-flavored topic.

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
- **Do not hand-write `solution.py`.** The spec is the single source of truth;
  generate `solution.py` via:
  ```
  python drill/scaffold.py problems/<topic>/<slug>/ [--force]
  ```
  This emits the standard bootstrap, the signature(s) from the spec, the
  per-function docstring prompt(s), and the appropriate `__main__` block.
  Use `--force` to regenerate (overwrites in-progress work, so warn the user).
- For multi-function drills, type hints belong in the `STUBS` signature
  strings in `_spec.py` — never hand-add them to `solution.py`. Re-run the
  scaffold to propagate changes.

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
5. After adding or editing a spec, run `make transform` to regenerate
   `web/public/problems.json` so the web layer picks up the change.
   The CLI workflow doesn't need this step.

## Web layer

The repo also ships as a static site at `web/`. Specs are the single
source of truth for both the CLI and the web layer — never hand-edit
`web/public/problems.json` or anything under `web/public/` that the
build produces.

**Pipeline** (`build/transform.py`):
- Imports every `problems/**/_spec.py`, normalizes it to JSON, and writes
  `web/public/problems.json`. Detects style from the spec attrs (`STUBS`
  → multi, `CLASS_NAME` → class, else function).
- Regenerates the skeleton from the spec (not from `solution.py`), so
  in-progress user code in `solution.py` never leaks to the published
  site.
- Copies `build/web_harness.py` → `web/public/web_harness.py` and
  `utils/__init__.py` → `web/public/utils.py` for the in-Pyodide runtime.

**Special CASES values** (`build/encoders.py` ↔ `build/web_harness.py`):
- `set`, `TreeNode`, `ListNode`, `tuple`, and `Ellipsis` are encoded with
  `{"__set__": ...}` / `{"__tree__": ...}` / `{"__list__": ...}` /
  `{"__tuple__": ...}` / `{"__ellipsis__": true}` markers and revived in
  the worker before tests run.
- If you introduce a new Python-only type in CASES, add it to both
  files together.

**Runtime** (`web/`):
- Astro static site, one route per problem via `getStaticPaths()`.
- CodeMirror 6 editor; Pyodide runs in a Web Worker
  (`web/public/pyodide.worker.js`) so wasm compile doesn't block the
  main thread.
- User solutions are persisted to `localStorage` keyed by problem id,
  with a SHA-1 of the current skeleton stored alongside for "skeleton
  changed" detection.

**Workflow**:
- `make transform` — regenerate the published JSON (do this after any
  `_spec.py` change).
- `make dev` — runs transform then `astro dev`.
- `make build` — runs transform then `astro build` (output: `web/dist`).
- Deploys to GitHub Pages on `v*` tag push or manual
  `workflow_dispatch` (`.github/workflows/deploy.yml`).
