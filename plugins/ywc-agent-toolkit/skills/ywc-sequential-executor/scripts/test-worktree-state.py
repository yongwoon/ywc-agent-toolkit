#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RESUME = SCRIPT_DIR / "resume-state.py"
INSPECT = SCRIPT_DIR / "inspect-state.py"


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
      raise AssertionError(
          f"command failed: {' '.join(cmd)}\nstdout={result.stdout}\nstderr={result.stderr}"
      )
    return result


def write_state(path: Path, worktree_path: Path) -> None:
    now = datetime.now(timezone.utc).isoformat()
    state = {
        "executor": "sequential",
        "args": "000001-010 --worktree",
        "mode": "normal",
        "tasks_dir": "tasks/",
        "range": ["000001-010-example"],
        "completed": [],
        "current_task": "000001-010-example",
        "current_step": 0,
        "branch": None,
        "started_at": now,
        "last_checkpoint": now,
        "worktree_mode": True,
        "worktree_path": str(worktree_path),
        "integration_branch": "integration/run-000001-010",
        "start_point": "main",
        "run_task_name": "run-000001-010",
    }
    path.write_text(json.dumps(state), encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="ywc-sequential-worktree-state.") as raw:
        repo = Path(raw)
        run(["git", "init", "-q", "-b", "main"], cwd=repo)
        run(["git", "config", "user.name", "Test User"], cwd=repo)
        run(["git", "config", "user.email", "test@example.com"], cwd=repo)
        (repo / "README.md").write_text("test\n", encoding="utf-8")
        run(["git", "add", "README.md"], cwd=repo)
        run(["git", "commit", "-q", "-m", "init"], cwd=repo)

        (repo / ".worktrees").mkdir()
        worktree = repo / ".worktrees" / "run-000001-010"
        run(
            [
                "git",
                "worktree",
                "add",
                "-q",
                str(worktree),
                "-b",
                "integration/run-000001-010",
            ],
            cwd=repo,
        )
        write_state(worktree / ".ywc-run-state.json", worktree)

        resume = run([sys.executable, str(RESUME), "--json"], cwd=repo)
        resume_payload = json.loads(resume.stdout)
        assert resume_payload["status"] == "valid"
        assert resume_payload["resume_task"] == "000001-010-example"
        assert resume_payload["worktree_path"] == str(worktree)
        assert resume_payload["integration_branch"] == "integration/run-000001-010"

        inspect = run(
            [
                sys.executable,
                str(INSPECT),
                "--state-file",
                str(worktree / ".ywc-run-state.json"),
                "--json",
            ],
            cwd=repo,
        )
        inspect_payload = json.loads(inspect.stdout)
        assert inspect_payload["worktree_mode"] is True
        assert inspect_payload["run_task_name"] == "run-000001-010"

    print("PASS: worktree state discovery and inspection")


if __name__ == "__main__":
    main()
