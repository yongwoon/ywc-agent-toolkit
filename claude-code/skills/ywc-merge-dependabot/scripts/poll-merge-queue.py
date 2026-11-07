#!/usr/bin/env python3
"""Poll the parallel-auto merge queue for one chunk (Step 3b Stage 2).

One invocation = one chunk of at most 540 s of polling, so it fits a single
Bash call with `timeout: 600000`. All cross-chunk state lives in the --state
JSON file, written after every chunk:

    {"deadline": 1761200000, "remaining": [101, 105],
     "status": {"107": "merged"}, "rebase_commented": [105]}

- deadline: absolute epoch seconds, computed ONCE (first chunk = now + 1800)
  and never recomputed. If the state file is lost, pass the original
  --deadline when known instead of starting a fresh 30 minutes.
- Each poll: one `gh pr view <pr> --json state,mergeStateStatus` per PR,
  bounded to 20 s. MERGED → "merged", CLOSED → "closed",
  CONFLICTING/DIRTY → comment `@dependabot rebase` once per PR (recorded only
  when the comment posted, so a failed post is retried) and re-queue;
  anything else, including a failed or timed-out query, → re-queue.
- 60 s between polls, clamped so a sleep never runs past the chunk.
- When the overall deadline has passed, every remaining PR is marked
  "stalled". A chunk that ends before the deadline never marks anything stalled.

Usage:
    poll-merge-queue.py --state <file> --prs <n> [<n> ...] [--deadline <epoch>]
    poll-merge-queue.py --state <file>        # resume the next chunk

stdout: one JSON object {"done": bool, "deadline": int, "remaining": [...], "status": {...}}

The first chunk must use a fresh --state path (e.g. from `mktemp`): --prs
together with an existing parseable state file is refused, so a leftover file
from an earlier run never replaces the new PR list.

Exit codes:
    0  queue finished: no PR remaining, or the deadline passed (stalled marked)
    2  usage error, no usable state and no --prs to start from, or --prs given
       while --state already holds queue state
    3  chunk ended before the deadline with PRs remaining — run again with
       the same --state
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

TOTAL_SECONDS = 1800
CHUNK_SECONDS = int(os.environ.get("YWC_MQ_CHUNK_SECONDS", "540"))  # env override is for tests only
POLL_SECONDS = int(os.environ.get("YWC_MQ_POLL_SECONDS", "60"))  # env override is for tests only
GH_TIMEOUT_SECONDS = 20


def load_state(path: str) -> dict | None:
    try:
        with open(path) as f:
            state = json.load(f)
        return {
            "deadline": int(state["deadline"]),
            "remaining": [int(n) for n in state["remaining"]],
            "status": {str(k): str(v) for k, v in state.get("status", {}).items()},
            "rebase_commented": [int(n) for n in state.get("rebase_commented", [])],
        }
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def save_state(path: str, state: dict) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".mq-state-")
    with os.fdopen(fd, "w") as f:
        json.dump(state, f)
    os.replace(tmp, path)


def gh(*args: str) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(["gh", *args], capture_output=True, text=True, timeout=GH_TIMEOUT_SECONDS)
    except (subprocess.TimeoutExpired, OSError):
        return None


def pr_state(pr: int) -> tuple[str, str]:
    r = gh("pr", "view", str(pr), "--json", "state,mergeStateStatus")
    if r is None or r.returncode != 0:
        return "UNKNOWN", "UNKNOWN"
    try:
        data = json.loads(r.stdout)
        return str(data.get("state", "UNKNOWN")), str(data.get("mergeStateStatus", "UNKNOWN"))
    except (ValueError, AttributeError):
        return "UNKNOWN", "UNKNOWN"


def poll_once(state: dict, chunk_deadline: float) -> None:
    next_remaining = []
    for pr in state["remaining"]:
        if time.time() >= chunk_deadline:  # slow gh calls must not outlive the chunk
            next_remaining.append(pr)
            continue
        status, merge_status = pr_state(pr)
        if status == "MERGED":
            state["status"][str(pr)] = "merged"
        elif status == "CLOSED":
            state["status"][str(pr)] = "closed"
        else:
            if merge_status in ("CONFLICTING", "DIRTY") and pr not in state["rebase_commented"]:
                r = gh("pr", "comment", str(pr), "--body", "@dependabot rebase")
                if r is not None and r.returncode == 0:
                    state["rebase_commented"].append(pr)
            next_remaining.append(pr)
    state["remaining"] = next_remaining


def run_chunk(state: dict) -> bool:
    """Poll until drained, the deadline, or the chunk end. Return True when finished."""
    chunk_deadline = time.time() + CHUNK_SECONDS
    while state["remaining"] and time.time() < state["deadline"] and time.time() < chunk_deadline:
        poll_once(state, chunk_deadline)
        left = chunk_deadline - time.time()
        if state["remaining"] and left > 0:
            time.sleep(min(left, POLL_SECONDS))
    if state["remaining"] and time.time() >= state["deadline"]:
        for pr in state["remaining"]:
            state["status"][str(pr)] = "stalled"
        state["remaining"] = []
    return not state["remaining"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll the Dependabot auto-merge queue for one chunk.")
    parser.add_argument("--state", required=True)
    parser.add_argument("--prs", type=int, nargs="+")
    parser.add_argument("--deadline", type=int)
    args = parser.parse_args()

    state = load_state(args.state)
    if state is not None and args.prs:
        # A leftover state file must never silently replace a new PR list.
        print(f"{args.state} already holds queue state — omit --prs to resume it, "
              "or start a new run with a fresh --state path", file=sys.stderr)
        return 2
    if state is None:
        if not args.prs:
            print("no usable state file and no --prs to start from", file=sys.stderr)
            return 2
        # An empty file is a fresh `mktemp` path, not lost state — warn only on real content.
        if os.path.exists(args.state) and os.path.getsize(args.state) > 0 and not args.deadline:
            print(f"{args.state} is unparsable and no --deadline was given — starting a fresh "
                  f"{TOTAL_SECONDS} s deadline; pass --deadline <original epoch> if it is known",
                  file=sys.stderr)
        deadline = args.deadline if args.deadline else int(time.time()) + TOTAL_SECONDS
        state = {"deadline": deadline, "remaining": list(dict.fromkeys(args.prs)),
                 "status": {}, "rebase_commented": []}

    done = run_chunk(state)
    save_state(args.state, state)
    print(json.dumps({"done": done, "deadline": state["deadline"],
                      "remaining": state["remaining"], "status": state["status"]}))
    return 0 if done else 3


if __name__ == "__main__":
    sys.exit(main())
