#!/usr/bin/env python3
"""
Validate checkpoint state and determine the resume point for ywc-parallel-executor.

Exit codes:
  0  Valid, non-stale state exists — safe to resume
  1  No state, stale state (>48h), mismatched executor, or unrecoverable inconsistency

Output (stdout):
  Human-readable summary by default.
  JSON when --json is passed (suitable for scripting).

JSON schema (exit 0):
  {
    "status": "valid",
    "resume_wave": <wave number>,
    "pending_tasks": ["<task-1>", ...],
    "merged_in_wave": ["<task-N>", ...],
    "mode": "local-merge|draft|per-task-pr",
    "worktree_root": "<absolute resolved root>",
    "root_kind": "standard|legacy",
    "warnings": ["<warning text>", ...]
  }

Run from the project root (same directory as .ywc-run-state.json).
"""
import json
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone

STATE_FILE = Path(".ywc-run-state.json")
MAX_AGE_HOURS = 48


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def age_hours(iso_str: str) -> float:
    try:
        dt = datetime.fromisoformat(iso_str)
        return (now_utc() - dt).total_seconds() / 3600
    except Exception:
        return float("inf")


def worktree_exists(path: str) -> bool:
    return Path(path).exists()


def completed_on_disk(tasks_dir: str) -> list[str]:
    completed_path = Path(tasks_dir) / "completed"
    if not completed_path.exists():
        return []
    return [d.name for d in completed_path.iterdir() if d.is_dir()]


def git_repo_root() -> Path:
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if output:
            return Path(output)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return Path.cwd()


def trim(value: str) -> str:
    return value.strip()


def claude_worktree_root(repo_root: Path) -> str:
    claude_md = repo_root / "CLAUDE.md"
    if not claude_md.exists():
        return ""

    for line in claude_md.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("worktree_root"):
            continue
        key, sep, value = stripped.partition(":")
        if sep and key.strip() == "worktree_root":
            return trim(value)
    return ""


def absolute_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return repo_root / path


def resolve_worktree_root(state: dict) -> tuple[Path, str]:
    repo_root = git_repo_root()

    recorded_root = state.get("worktree_root")
    if recorded_root:
        return absolute_path(repo_root, str(recorded_root)), state.get("root_kind", "standard")

    in_repo_root = repo_root / ".worktrees"
    if in_repo_root.is_dir():
        return in_repo_root.resolve(), "standard"

    claude_root = claude_worktree_root(repo_root)
    if claude_root:
        return absolute_path(repo_root, claude_root), "standard"

    return repo_root.parent, "legacy"


def worktree_path_for(task: str, worktree_root: Path, root_kind: str) -> Path:
    if root_kind == "legacy":
        return worktree_root / f"worktree-{task}"
    return worktree_root / task


def fail(msg: str, as_json: bool, hint: str = "") -> None:
    if as_json:
        print(json.dumps({"status": "error", "reason": msg, "hint": hint}))
    else:
        print(f"CANNOT RESUME: {msg}")
        if hint:
            print(f"  → {hint}")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate ywc-parallel-executor checkpoint for safe resume"
    )
    parser.add_argument("--json", dest="as_json", action="store_true")
    args = parser.parse_args()

    if not STATE_FILE.exists():
        fail("No .ywc-run-state.json found", args.as_json, "This is a fresh run.")

    try:
        state = json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError as exc:
        fail(f"Cannot parse state file: {exc}", args.as_json, "Run: rm .ywc-run-state.json")

    executor = state.get("executor")
    if executor != "parallel":
        fail(
            f"State file belongs to '{executor}', not 'parallel'",
            args.as_json,
            "Delete .ywc-run-state.json manually if you want to start fresh.",
        )

    checkpoint_ts = state.get("last_checkpoint") or state.get("started_at", "")
    age = age_hours(checkpoint_ts)
    if age > MAX_AGE_HOURS:
        fail(
            f"State is {age:.1f}h old (limit: {MAX_AGE_HOURS}h)",
            args.as_json,
            "Delete .ywc-run-state.json to start fresh.",
        )

    tasks_dir = state.get("tasks_dir", "tasks/")
    worktree_root, root_kind = resolve_worktree_root(state)
    warnings: list[str] = []

    waves = state.get("waves", [])

    # Find the wave to resume from
    in_progress = next((w for w in waves if w.get("status") == "in_progress"), None)
    if in_progress:
        resume_wave = in_progress["wave"]
        pending = in_progress.get("pending", [])
        merged_in_wave = in_progress.get("merged", [])

        # Validate worktrees for pending tasks
        for task in pending:
            wt_path = worktree_path_for(task, worktree_root, root_kind)
            if not worktree_exists(wt_path):
                warnings.append(
                    f"Worktree for '{task}' not found at {wt_path}. "
                    f"May need to recreate worktree (Step 4a) before resuming this task."
                )
    else:
        # Find the next planned wave
        planned = next((w for w in waves if w.get("status") == "planned"), None)
        if planned:
            resume_wave = planned["wave"]
            pending = planned.get("tasks", [])
            merged_in_wave = []
        else:
            fail(
                "No in-progress or planned waves found — all waves may be complete",
                args.as_json,
                "Delete .ywc-run-state.json if the run is finished.",
            )

    # Cross-validate completed wave tasks against disk
    completed_waves = [w for w in waves if w.get("status") == "completed"]
    disk_completed = set(completed_on_disk(tasks_dir))
    for w in completed_waves:
        for task in w.get("tasks", []):
            if task not in disk_completed:
                warnings.append(
                    f"Task '{task}' in a completed wave but absent from {tasks_dir}completed/."
                )

    result = {
        "status": "valid",
        "resume_wave": resume_wave,
        "pending_tasks": pending,
        "merged_in_wave": merged_in_wave,
        "mode": state.get("mode", "unknown"),
        "tasks_dir": tasks_dir,
        "worktree_root": str(worktree_root),
        "root_kind": root_kind,
        "warnings": warnings,
    }

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    print("=== Resume Validation ===")
    print(f"  Status       : VALID — safe to resume")
    print(f"  Resume at    : Wave {resume_wave}")
    if merged_in_wave:
        print(f"  Already done : {merged_in_wave} (merged in this wave)")
    print(f"  Pending      : {pending}")
    print(f"  Mode         : {result['mode']}")
    print(f"  Worktree root: {worktree_root} ({root_kind})")
    if warnings:
        print()
        print("  Warnings:")
        for w in warnings:
            print(f"    ⚠ {w}")
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
