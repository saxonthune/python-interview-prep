#!/usr/bin/env python3
"""Print the path of a random problem directory."""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS = ROOT / "problems"

problems = [
    p for topic in PROBLEMS.iterdir() if topic.is_dir()
    for p in topic.iterdir() if p.is_dir()
]

if not problems:
    raise SystemExit("no problems found")

print(random.choice(problems).relative_to(ROOT))
