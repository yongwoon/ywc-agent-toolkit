#!/usr/bin/env python3
"""Deterministic checkpoint mutations for ywc-sequential / ywc-parallel-executor.

The executors otherwise hand-edit ``.ywc-run-state.json`` via the Write tool on
every wave / task event. That is pure deterministic JSON mutation (move a task
``pending`` -> ``merged``, flip a wave ``status``, append to ``completed``, bump
``last_checkpoint``), and doing it by hand risks malformed JSON, stale
timestamps, and dropped fields. This script applies exactly one mutation, stamps
``last_checkpoint`` with the current UTC time, and writes atomically. The
read-only inspection / resume helpers already prove the schema.

Run from the project root (same directory as ``.ywc-run-state.json``).

Subcommands:
  init-parallel    --mode M --tasks-dir D --waves '<json-array>'
  init-sequential  --mode M --tasks-dir D --range '<json-array>' [--current-task T] [--branch B]
  wave-start       N
  task-merged      WAVE TASK
  wave-complete    N
  task-step        TASK STEP [--branch B]
  task-complete    TASK
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone

STATE_FILE = Path(".ywc-run-state.json")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load() -> dict:
    if not STATE_FILE.exists():
        die(f"{STATE_FILE} not found — run an init-* subcommand first")
    try:
        return json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError as exc:
        die(f"cannot parse {STATE_FILE}: {exc}")
    return {}  # unreachable


def save(state: dict) -> None:
    """Stamp the checkpoint and write atomically (temp file + os.replace)."""
    state["last_checkpoint"] = now_iso()
    fd, tmp = tempfile.mkstemp(dir=".", prefix=".ywc-run-state.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(state, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, STATE_FILE)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise


def parse_json_list(raw: str, label: str) -> list:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        die(f"--{label} is not valid JSON: {exc}")
    if not isinstance(value, list):
        die(f"--{label} must be a JSON array")
    return value


def require_executor(state: dict, expected: str, sub: str) -> None:
    actual = state.get("executor")
    if actual != expected:
        die(f"'{sub}' requires executor='{expected}', but state is '{actual}'")


def find_wave(state: dict, n: int) -> dict:
    for wave in state.get("waves", []):
        if wave.get("wave") == n:
            return wave
    die(f"wave {n} not found in state")
    return {}  # unreachable


# --- subcommand handlers -----------------------------------------------------

def cmd_init_parallel(args: argparse.Namespace) -> None:
    waves = parse_json_list(args.waves, "waves")
    for wave in waves:
        if (not isinstance(wave, dict)
                or not isinstance(wave.get("wave"), int)
                or not isinstance(wave.get("tasks"), list)):
            die('each --waves element must be a {"wave": <int>, "tasks": [<task>...]} object')
        wave.setdefault("status", "planned")
        wave.setdefault("merged", [])
        wave.setdefault("pending", list(wave["tasks"]))
    save({
        "executor": "parallel",
        "mode": args.mode,
        "tasks_dir": args.tasks_dir,
        "started_at": now_iso(),
        "current_wave": 0,
        "waves": waves,
    })
    print(f"initialized parallel state: {len(waves)} wave(s)")


def cmd_init_sequential(args: argparse.Namespace) -> None:
    task_range = parse_json_list(args.range, "range")
    save({
        "executor": "sequential",
        "mode": args.mode,
        "tasks_dir": args.tasks_dir,
        "started_at": now_iso(),
        "range": task_range,
        "completed": [],
        "current_task": args.current_task or (task_range[0] if task_range else None),
        "current_step": 1,
        "branch": args.branch,
    })
    print(f"initialized sequential state: {len(task_range)} task(s)")


def cmd_wave_start(args: argparse.Namespace) -> None:
    state = load()
    require_executor(state, "parallel", "wave-start")
    wave = find_wave(state, args.n)
    wave["status"] = "in_progress"
    if not wave.get("pending"):
        wave["pending"] = list(wave.get("tasks", []))
    state["current_wave"] = args.n
    save(state)
    print(f"wave {args.n} -> in_progress")


def cmd_task_merged(args: argparse.Namespace) -> None:
    state = load()
    require_executor(state, "parallel", "task-merged")
    wave = find_wave(state, args.wave)
    if args.task not in wave.get("tasks", []):
        die(f"task '{args.task}' is not in wave {args.wave}'s task list {wave.get('tasks', [])}")
    if args.task in wave.get("pending", []):
        wave["pending"].remove(args.task)
    if args.task not in wave.setdefault("merged", []):
        wave["merged"].append(args.task)
    save(state)
    print(f"wave {args.wave}: '{args.task}' merged ({len(wave['pending'])} pending)")


def cmd_wave_complete(args: argparse.Namespace) -> None:
    state = load()
    require_executor(state, "parallel", "wave-complete")
    wave = find_wave(state, args.n)
    if wave.get("pending"):
        die(f"wave {args.n} still has pending tasks: {wave['pending']}")
    wave["status"] = "completed"
    # Advance current_wave to the lowest-numbered not-yet-completed wave so an
    # interruption right after wave-complete resumes at the next wave, not the
    # one just finished. If every wave is done, keep the last completed number.
    remaining = [w["wave"] for w in state.get("waves", []) if w.get("status") != "completed"]
    state["current_wave"] = min(remaining) if remaining else args.n
    save(state)
    print(f"wave {args.n} -> completed (current_wave={state['current_wave']})")


def cmd_task_step(args: argparse.Namespace) -> None:
    state = load()
    require_executor(state, "sequential", "task-step")
    state["current_task"] = args.task
    state["current_step"] = args.step
    if args.branch is not None:
        state["branch"] = args.branch
    save(state)
    print(f"current: task='{args.task}' step={args.step}")


def cmd_task_complete(args: argparse.Namespace) -> None:
    state = load()
    require_executor(state, "sequential", "task-complete")
    completed = state.setdefault("completed", [])
    if args.task not in completed:
        completed.append(args.task)
    remaining = [t for t in state.get("range", []) if t not in completed]
    state["current_task"] = remaining[0] if remaining else None
    state["current_step"] = 1
    state["branch"] = None
    save(state)
    print(f"'{args.task}' completed ({len(completed)} done, {len(remaining)} remaining)")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    ip = sub.add_parser("init-parallel")
    ip.add_argument("--mode", required=True)
    ip.add_argument("--tasks-dir", default="tasks/")
    ip.add_argument("--waves", required=True, help='JSON array of {"wave":N,"tasks":[...]}')
    ip.set_defaults(func=cmd_init_parallel)

    iseq = sub.add_parser("init-sequential")
    iseq.add_argument("--mode", required=True)
    iseq.add_argument("--tasks-dir", default="tasks/")
    iseq.add_argument("--range", required=True, help="JSON array of task-directory names")
    iseq.add_argument("--current-task", default=None)
    iseq.add_argument("--branch", default=None)
    iseq.set_defaults(func=cmd_init_sequential)

    ws = sub.add_parser("wave-start")
    ws.add_argument("n", type=int)
    ws.set_defaults(func=cmd_wave_start)

    tm = sub.add_parser("task-merged")
    tm.add_argument("wave", type=int)
    tm.add_argument("task")
    tm.set_defaults(func=cmd_task_merged)

    wc = sub.add_parser("wave-complete")
    wc.add_argument("n", type=int)
    wc.set_defaults(func=cmd_wave_complete)

    ts = sub.add_parser("task-step")
    ts.add_argument("task")
    ts.add_argument("step", type=int)
    ts.add_argument("--branch", default=None)
    ts.set_defaults(func=cmd_task_step)

    tc = sub.add_parser("task-complete")
    tc.add_argument("task")
    tc.set_defaults(func=cmd_task_complete)

    return p


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
