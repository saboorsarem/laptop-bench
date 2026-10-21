#!/usr/bin/env python3
"""Checks that every task is solvable: runs each check against its reference solution."""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
TASKS = os.path.join(ROOT, "tasks")
REFS = os.path.join(ROOT, "reference")

failed = 0
for name in sorted(os.listdir(TASKS)):
    task = os.path.join(TASKS, name)
    if not os.path.isdir(task):
        continue
    with tempfile.TemporaryDirectory() as workdir:
        for source in ("check.py",):
            with open(os.path.join(task, source), encoding="utf-8") as src:
                data = src.read()
            with open(os.path.join(workdir, source), "w", encoding="utf-8") as dst:
                dst.write(data)
        with open(os.path.join(REFS, name + ".py"), encoding="utf-8") as src:
            data = src.read()
        with open(os.path.join(workdir, "solution.py"), "w", encoding="utf-8") as dst:
            dst.write(data)
        done = subprocess.run([sys.executable, "check.py"], cwd=workdir, capture_output=True, text=True, timeout=30)
    if done.returncode != 0:
        failed += 1
        print(f"FAIL {name}: {(done.stderr or done.stdout).strip()[-300:]}")
    else:
        print(f"ok   {name}")

sys.exit(1 if failed else 0)
