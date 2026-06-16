#!/usr/bin/env python3
"""
Manual inspection and management utility for ywc-sequential-executor checkpoint state.

The executor writes .ywc-run-state.json automatically — use this script to inspect,
validate, or reset state from the command line.

Usage:
  python scripts/inspect-state.py           # Human-readable state summary
  python scripts/inspect-state.py --json    # Raw JSON dump
  python scripts/inspect-state.py --state-file <path>
  python scripts/inspect-state.py --reset   # Delete state file (force fresh run)

Run from the project root (same directory as .ywc-run-state.json).
"""
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

STATE_FILE = Path(".ywc-run-state.json")


def fmt_age(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
        secs = (datetime.now(timezone.utc) - dt).total_seconds()
        if secs < 3600:
            return f"{int(secs / 60)}m ago"
        elif secs < 86400:
            return f"{secs / 3600:.1f}h ago"
        else:
            return f"{secs / 86400:.1f}d ago"
    except Exception:
        return iso_str or "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ywc-sequential-executor state inspection utility"
    )
    parser.add_argument("--reset", action="store_true", help="Delete the state file")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Print raw JSON")
    parser.add_argument(
        "--state-file",
        type=Path,
        default=STATE_FILE,
        help="Checkpoint file to inspect. Defaults to .ywc-run-state.json in the current directory.",
    )
    args = parser.parse_args()
    state_file = args.state_file

    if args.reset:
        if state_file.exists():
            state_file.unlink()
            print(f"State file deleted: {state_file}. Next run will start fresh.")
        else:
            print("No state file found — already clean.")
        return

    if not state_file.exists():
        print(f"No checkpoint state found ({state_file} does not exist).")
        print("The executor has not been run, or completed successfully and cleaned up.")
        return

    try:
        state = json.loads(state_file.read_text())
    except json.JSONDecodeError as exc:
        print(f"ERROR: Cannot parse state file: {exc}")
        print("Run with --reset to delete the corrupted file.")
        sys.exit(1)

    if args.as_json:
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return

    executor = state.get("executor", "unknown")
    mode = state.get("mode", "unknown")
    started = fmt_age(state.get("started_at", ""))
    checkpoint = fmt_age(state.get("last_checkpoint", ""))

    print("=== ywc-sequential-executor checkpoint ===")
    print(f"  Executor    : {executor}")
    print(f"  Mode        : {mode}")
    print(f"  Tasks dir   : {state.get('tasks_dir', 'tasks/')}")
    print(f"  Started     : {started}")
    print(f"  Checkpoint  : {checkpoint}")
    print()

    if executor == "sequential":
        task_range = state.get("range", [])
        completed = state.get("completed", [])
        current = state.get("current_task")
        step = state.get("current_step", 0)
        branch = state.get("branch")
        remaining = [t for t in task_range if t not in completed]

        print(f"  Progress    : {len(completed)} / {len(task_range)} tasks completed")

        if completed:
            print(f"  Completed   :")
            for t in completed:
                print(f"    ✓ {t}")

        if current:
            print(f"  In Progress : {current}")
            print(f"    Step      : {step} / 8")
            if branch:
                print(f"    Branch    : {branch}")
        elif remaining:
            print(f"  Next Task   : {remaining[0]}")
        else:
            print("  Status      : All tasks complete (state file should have been deleted)")

        if remaining and not current:
            print(f"  Remaining   : {len(remaining)} tasks")
    else:
        print(f"  WARNING: executor='{executor}' is not 'sequential'.")
        print("  This state file may belong to ywc-parallel-executor.")

    print()
    if state.get("worktree_mode"):
        print(f"  Worktree    : {state.get('worktree_path', 'unknown')}")
        print(f"  Integration : {state.get('integration_branch', 'unknown')}")
        print(f"  Run task    : {state.get('run_task_name', 'unknown')}")

    print(f"  File: {state_file.resolve()}")
    print()
    print("Commands:")
    print("  python scripts/inspect-state.py --json    # raw JSON")
    print("  python scripts/inspect-state.py --reset   # delete state, force fresh run")


if __name__ == "__main__":
    main()
