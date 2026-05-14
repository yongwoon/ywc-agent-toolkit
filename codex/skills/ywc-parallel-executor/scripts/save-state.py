#!/usr/bin/env python3
"""
Manual inspection and management utility for ywc-parallel-executor checkpoint state.

The executor writes .ywc-run-state.json automatically — use this script to inspect,
validate, or reset state from the command line.

Usage:
  python scripts/save-state.py           # Human-readable state summary
  python scripts/save-state.py --json    # Raw JSON dump
  python scripts/save-state.py --reset   # Delete state file (force fresh run)

Run from the project root (same directory as .ywc-run-state.json).
"""
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

STATE_FILE = Path(".ywc-run-state.json")

STATUS_ICON = {
    "completed": "✓",
    "in_progress": "▶",
    "planned": "○",
    "failed": "✗",
}


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
        description="ywc-parallel-executor state inspection utility"
    )
    parser.add_argument("--reset", action="store_true", help="Delete the state file")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Print raw JSON")
    args = parser.parse_args()

    if args.reset:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
            print("State file deleted. Next run will start fresh.")
        else:
            print("No state file found — already clean.")
        return

    if not STATE_FILE.exists():
        print("No checkpoint state found (.ywc-run-state.json does not exist).")
        print("The executor has not been run, or completed successfully and cleaned up.")
        return

    try:
        state = json.loads(STATE_FILE.read_text())
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

    print("=== ywc-parallel-executor checkpoint ===")
    print(f"  Executor    : {executor}")
    print(f"  Mode        : {mode}")
    print(f"  Tasks dir   : {state.get('tasks_dir', 'tasks/')}")
    print(f"  Started     : {started}")
    print(f"  Checkpoint  : {checkpoint}")
    print()

    if executor == "parallel":
        waves = state.get("waves", [])
        current_wave = state.get("current_wave", 0)
        print(f"  Current Wave: {current_wave}")
        print(f"  Waves:")
        for w in waves:
            wave_n = w.get("wave", "?")
            status = w.get("status", "unknown")
            tasks = w.get("tasks", [])
            merged = w.get("merged", [])
            pending = w.get("pending", [])
            icon = STATUS_ICON.get(status, "?")
            print(f"    {icon} Wave {wave_n:2d}: {status}")
            print(f"       Tasks  : {tasks}")
            if merged:
                print(f"       Merged : {merged}")
            if pending:
                print(f"       Pending: {pending}")
    else:
        print(f"  WARNING: executor='{executor}' is not 'parallel'.")
        print("  This state file may belong to ywc-sequential-executor.")

    print()
    print(f"  File: {STATE_FILE.resolve()}")
    print()
    print("Commands:")
    print("  python scripts/save-state.py --json    # raw JSON")
    print("  python scripts/save-state.py --reset   # delete state, force fresh run")


if __name__ == "__main__":
    main()
