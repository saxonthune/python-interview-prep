#!/usr/bin/env python3
"""Minimal pywebview UI for drill: browse problems, reset, promote."""
import importlib.util
from pathlib import Path

import webview

# The repo has both a `drill/` package and a `drill.py` script at the root.
# The package shadows the script on plain `import drill`, so load the script
# directly by file path under a distinct module name.
_DRILL_PY = Path(__file__).parent / "drill.py"
_spec = importlib.util.spec_from_file_location("drill_cli", _DRILL_PY)
drill_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drill_cli)

PROBLEMS = drill_cli.PROBLEMS
EXAMPLE_RE = drill_cli.EXAMPLE_RE
iter_problem_dirs = drill_cli.iter_problem_dirs
load_spec = drill_cli.load_spec
reset_solution = drill_cli.reset_solution
promote_solution = drill_cli.promote_solution
build_solution_content = drill_cli.build_solution_content


def _strip_boilerplate(content):
    """Strip the template header (sys.path / imports) and the __main__ footer,
    leaving the solution + any user-added helpers."""
    if not content:
        return content
    lines = content.splitlines()
    # Find start: first line after the last `from _spec import ...`, else after
    # `from utils import *`, else line 0.
    start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("from _spec import") or stripped.startswith("from drill.harness import"):
            start = i + 1
        elif stripped.startswith("from utils import") and start == 0:
            start = i + 1
    # Find end: first `if __name__ == "__main__":` line.
    end = len(lines)
    for i, line in enumerate(lines):
        if line.strip().startswith('if __name__ == "__main__"'):
            end = i
            break
    return "\n".join(lines[start:end]).strip("\n")


def _is_modified(problem_dir):
    """True if solution.py differs from a fresh template."""
    solution_file = problem_dir / "solution.py"
    if not solution_file.exists():
        return False
    try:
        fresh = build_solution_content(problem_dir)
    except Exception:
        return False
    if fresh is None:
        return False
    try:
        current = solution_file.read_text()
    except Exception:
        return False
    return current != fresh


def _title_for(problem_dir):
    try:
        s = load_spec(problem_dir / "_spec.py")
        return getattr(s, "TITLE", problem_dir.name)
    except Exception:
        return problem_dir.name


def _build_tree():
    root = {"name": "", "sections": {}, "problems": []}
    for d in sorted(iter_problem_dirs()):
        rel = d.relative_to(PROBLEMS)
        parts = rel.parts
        node = root
        for part in parts[:-1]:
            node = node["sections"].setdefault(
                part, {"name": part, "sections": {}, "problems": []}
            )
        node["problems"].append({
            "path": str(rel).replace("\\", "/"),
            "title": _title_for(d),
            "modified": _is_modified(d),
        })

    def finalize(node):
        return {
            "name": node["name"],
            "sections": [finalize(v) for _, v in sorted(node["sections"].items())],
            "problems": node["problems"],
        }

    return finalize(root)


class Api:
    def get_tree(self):
        return _build_tree()

    def get_problem(self, path):
        problem_dir = PROBLEMS / path
        spec_file = problem_dir / "_spec.py"
        if not spec_file.exists():
            return {"error": f"No spec at {spec_file}"}
        s = load_spec(spec_file)
        example_count = sum(
            1 for f in problem_dir.iterdir() if EXAMPLE_RE.match(f.name)
        )
        solution_file = problem_dir / "solution.py"
        solution = solution_file.read_text() if solution_file.exists() else ""
        solution = _strip_boilerplate(solution)
        lastrun_file = problem_dir / "lastrun.log"
        lastrun = lastrun_file.read_text() if lastrun_file.exists() else ""
        return {
            "path": path,
            "title": getattr(s, "TITLE", problem_dir.name),
            "description": getattr(s, "DESCRIPTION", "").strip(),
            "constraints": getattr(s, "CONSTRAINTS", "").strip(),
            "example_count": example_count,
            "solution": solution,
            "modified": _is_modified(problem_dir),
            "lastrun": lastrun,
        }

    def reset(self, path):
        try:
            ok = reset_solution(PROBLEMS / path)
            return {"ok": bool(ok), "error": None if ok else "reset_solution returned False"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def promote(self, path):
        try:
            ok = promote_solution(PROBLEMS / path)
            return {"ok": bool(ok), "error": None if ok else "promote_solution returned False (no solution.py?)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}


HTML = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Interview Drill</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: system-ui, -apple-system, sans-serif; font-size: 14px; color: #222; }
  .app { display: flex; height: 100vh; }
  .left {
    width: 340px; border-right: 1px solid #ddd; overflow: auto;
    padding: 12px; background: #fafafa;
  }
  .right { flex: 1; overflow: auto; padding: 24px; }
  h1 { margin: 0 0 12px; font-size: 22px; }
  ul { list-style: none; padding-left: 16px; margin: 4px 0; }
  .left > ul { padding-left: 0; }
  details > summary { cursor: pointer; padding: 2px 0; font-weight: 600; }
  details { margin: 2px 0; }
  .problem {
    cursor: pointer; padding: 3px 6px; border-radius: 3px;
    display: block;
  }
  .problem:hover { background: #e8eef7; }
  .problem.active { background: #d3e1f5; }
  .dot {
    display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: #2a6df4; margin-left: 6px; vertical-align: middle;
  }
  pre {
    background: #f4f4f4; padding: 10px; border-radius: 4px;
    white-space: pre-wrap; font-size: 13px; margin: 6px 0 0;
  }
  .detail details { margin: 10px 0; }
  .detail summary { font-weight: 600; }
  .badge {
    display: inline-block; background: #eef; color: #336;
    padding: 2px 8px; border-radius: 10px; font-size: 12px;
    margin: 8px 0;
  }
  .actions { margin-top: 18px; }
  button {
    font-size: 14px; padding: 6px 14px; margin-right: 8px;
    cursor: pointer; border: 1px solid #888; background: #fff;
    border-radius: 3px;
  }
  button:hover:not(:disabled) { background: #eee; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  pre.solution {
    background: #1e1e1e; color: #d4d4d4;
    max-height: 500px; overflow: auto;
    font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 12px;
  }
  .status { margin-top: 10px; font-size: 13px; min-height: 18px; }
  .status.ok { color: #2a7a2a; }
  .status.err { color: #b33; }
  .empty { color: #999; }
  .path { color: #888; font-family: monospace; font-size: 12px; }
</style>
</head>
<body>
<div class="app">
  <div class="left" id="tree">loading…</div>
  <div class="right" id="detail"><div class="empty">Select a problem on the left.</div></div>
</div>

<script>
let currentPath = null;

function esc(s) {
  return (s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderTreeNode(node, isRoot) {
  const parts = [];
  for (const section of node.sections) {
    parts.push(
      `<details open><summary>${esc(section.name)}</summary>` +
      renderTreeNode(section, false) +
      `</details>`
    );
  }
  for (const p of node.problems) {
    const dot = p.modified ? `<span class="dot" title="solution.py has modifications"></span>` : "";
    parts.push(
      `<a class="problem" data-path="${esc(p.path)}">${esc(p.title)}${dot}</a>`
    );
  }
  return `<ul>${parts.map(x => `<li>${x}</li>`).join("")}</ul>`;
}

async function loadTree() {
  const tree = await pywebview.api.get_tree();
  document.getElementById("tree").innerHTML = renderTreeNode(tree, true);
  document.querySelectorAll(".problem").forEach(el => {
    el.addEventListener("click", () => selectProblem(el.dataset.path));
    if (el.dataset.path === currentPath) el.classList.add("active");
  });
}

async function selectProblem(path) {
  currentPath = path;
  document.querySelectorAll(".problem").forEach(el => {
    el.classList.toggle("active", el.dataset.path === path);
  });
  await renderDetail();
}

async function renderDetail() {
  if (!currentPath) return;
  const d = await pywebview.api.get_problem(currentPath);
  const root = document.getElementById("detail");
  if (d.error) {
    root.innerHTML = `<div class="status err">${esc(d.error)}</div>`;
    return;
  }
  root.innerHTML = `
    <div class="detail">
      <h1>${esc(d.title)}</h1>
      <div class="path">${esc(d.path)}</div>
      <details open><summary>Description</summary><pre>${esc(d.description)}</pre></details>
      <details open><summary>Constraints</summary><pre>${esc(d.constraints)}</pre></details>
      <details ${d.modified ? "open" : ""}><summary>Solution${d.modified ? " (modified)" : ""}</summary><pre class="solution">${esc(d.solution)}</pre></details>
      ${d.lastrun ? `<details open><summary>Last run</summary><pre class="solution">${esc(d.lastrun)}</pre></details>` : ""}
      <div class="badge">archived examples: ${d.example_count}</div>
      <div class="actions">
        <button id="btn-reset" ${d.modified ? "" : "disabled"}>Reset</button>
        <button id="btn-promote" ${d.modified ? "" : "disabled"}>Promote</button>
      </div>
      <div id="status" class="status"></div>
    </div>
  `;
  document.getElementById("btn-reset").addEventListener("click", onReset);
  document.getElementById("btn-promote").addEventListener("click", onPromote);
}

function setStatus(msg, ok) {
  const s = document.getElementById("status");
  s.textContent = msg;
  s.className = "status " + (ok ? "ok" : "err");
}

async function onReset() {
  const r = await pywebview.api.reset(currentPath);
  if (r.ok) {
    await loadTree();
    setStatus("Reset ok", true);
  } else {
    setStatus("Error: " + (r.error || "unknown"), false);
  }
}

async function onPromote() {
  const r = await pywebview.api.promote(currentPath);
  if (r.ok) {
    await renderDetail();
    await loadTree();
    setStatus("Promote ok", true);
  } else {
    setStatus("Error: " + (r.error || "unknown"), false);
  }
}

window.addEventListener("pywebviewready", loadTree);
</script>
</body>
</html>
"""


if __name__ == "__main__":
    api = Api()
    window = webview.create_window(
        "Interview Drill", html=HTML, js_api=api, width=1400, height=950
    )
    webview.start()
