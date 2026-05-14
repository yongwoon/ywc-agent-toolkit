#!/usr/bin/env python3
"""
Validate checkpoint state and determine the resume point for ywc-sequential-executor.

Exit codes:
  0  Valid, non-stale state exists — safe to resume
  1  No state, stale state (>48h), mismatched executor, or unrecoverable inconsistency

Output (stdout):
  Human-readable summary by default.
  JSON when --json is passed (suitable for scripting).

JSON schema (exit 0):
  {
    "status": "valid",
    "resume_task": "<task-directory-name>",
    "resume_step": <1-8>,
    "branch": "<feature/...>" | null,
    "completed": ["<task-1>", ...],
    "remaining": ["<task-N>", ...],
    "mode": "local-merge|draft|skip-ci-wait|normal",
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


def git_branch_exists(branch: str) -> bool:
    result = subprocess.run(
        ["git", "branch", "--list", branch],
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def completed_on_disk(tasks_dir: str) -> list[str]:
    completed_path = Path(tasks_dir) / "completed"
    if not completed_path.exists():
        return []
    return [d.name for d in completed_path.iterdir() if d.is_dir()]


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
        description="Validate ywc-sequential-executor checkpoint for safe resume"
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
    if executor != "sequential":
        fail(
            f"State file belongs to '{executor}', not 'sequential'",
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
    warnings: list[str] = []

    # Cross-validate completed tasks
    state_completed = set(state.get("completed", []))
    disk_completed = set(completed_on_disk(tasks_dir))
    missing_from_disk = state_completed - disk_completed
    extra_on_disk = disk_completed - state_completed
    if missing_from_disk:
        warnings.append(
            f"Tasks marked 'completed' in state but absent from {tasks_dir}completed/: "
            f"{sorted(missing_from_disk)}"
        )
    if extra_on_disk:
        warnings.append(
            f"Tasks present in {tasks_dir}completed/ but not tracked in state: "
            f"{sorted(extra_on_disk)} — treating as completed."
        )
        state_completed |= extra_on_disk

    # Cross-validate branch
    branch = state.get("branch")
    step = state.get("current_step", 0)
    current_task = state.get("current_task")

    if branch and step >= 2:
        if not git_branch_exists(branch):
            warnings.append(
                f"Branch '{branch}' no longer exists (merged or manually deleted). "
                f"Will resume from Step 1 of task '{current_task}'."
            )
            branch = None
            step = 1

    # Determine where to resume
    task_range = state.get("range", [])
    remaining = [t for t in task_range if t not in state_completed]

    if not remaining:
        fail(
            "All tasks are already completed — nothing to resume",
            args.as_json,
            "Delete .ywc-run-state.json if the run is truly finished.",
        )

    resume_task = current_task if current_task in remaining else remaining[0]
    resume_step = step if (current_task == resume_task and step >= 1) else 1

    result = {
        "status": "valid",
        "resume_task": resume_task,
        "resume_step": resume_step,
        "branch": branch,
        "completed": sorted(state_completed),
        "remaining": remaining,
        "mode": state.get("mode", "unknown"),
        "tasks_dir": tasks_dir,
        "warnings": warnings,
    }

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    print("=== Resume Validation ===")
    print(f"  Status      : VALID — safe to resume")
    print(f"  Resume at   : task='{resume_task}', step={resume_step}")
    if branch:
        print(f"  Branch      : {branch} (exists)")
    print(f"  Completed   : {len(state_completed)} / {len(task_range)}")
    print(f"  Remaining   : {len(remaining)} tasks")
    print(f"  Mode        : {result['mode']}")
    if warnings:
        print()
        print("  Warnings:")
        for w in warnings:
            print(f"    ⚠ {w}")
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
