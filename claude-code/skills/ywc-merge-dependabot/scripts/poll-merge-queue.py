#!/usr/bin/env python3
"""Poll the parallel-auto merge queue for one chunk (Step 3b Stage 2).

One invocation = one chunk of at most 540 s of polling, so it fits a single
Bash call with `timeout: 600000`. All cross-chunk state lives in the --state
JSON file, written after every chunk:

    {"deadline": 1761200000, "remaining": [101, 105],
     "heads": {"101": "<sha>", "105": "<sha>", "107": "<sha>"},
     "status": {"107": "merged"}, "rebase_commented": [105], "query_failed": [101],
     "requeues": {"105": 1}}

- deadline: absolute epoch seconds, computed ONCE (first chunk = now + 1800)
  and never recomputed. If the state file is lost, pass the original
  --deadline when known instead of starting a fresh 30 minutes.
- heads: the head SHA each PR was queued with (`--prs <n>:<sha>`).
- Each poll: one `gh pr view <pr> --json state,mergeStateStatus,headRefOid`
  per PR, bounded to 20 s. MERGED → "merged", CLOSED → "closed".
  An OPEN head that differs from the queued head → `gh pr merge --disable-auto`;
  once that succeeds → "head-moved" and the chunk ends at once (exit 3, or 0
  when nothing else remains) so the caller can re-run the Step 2 checks on the
  new head and re-queue it pinned with --requeue; a failed disable is retried
  on the next poll. CONFLICTING/DIRTY → comment
  `@dependabot rebase` once per PR (recorded only when the comment posted, so a
  failed post is retried) and re-queue; anything else → re-queue.
- A failed or timed-out query (or a reply without a 40-hex head) re-queues the
  PR, prints gh's error to stderr and adds the PR to query_failed; the next
  successful query removes it.
- 60 s between polls, clamped so a sleep never runs past the chunk.
- When the overall deadline has passed, every remaining PR is marked
  "unreadable" when its latest query failed (after one final read) (an auth or rate-limit outage is
  not a stalled queue), else "stalled". A chunk that ends before the deadline
  never marks anything.

Usage:
    poll-merge-queue.py --state <file> --prs <n>:<sha> [<n>:<sha> ...] [--deadline <epoch>]
    poll-merge-queue.py --state <file>        # resume the next chunk
    poll-merge-queue.py --state <file> --requeue <n>:<sha> [...]
        # resume after re-queueing head-moved PRs on their new heads. At most
        # MAX_REQUEUES per PR; past that the PR is left "head-moved" with a
        # warning and the caller hands it to the sequential pass.

stdout: one JSON object {"done": bool, "deadline": int, "remaining": [...], "status": {...},
        "requeues": {...}} — check requeues[<n>] < MAX_REQUEUES before re-enabling auto-merge.

The first chunk must use a fresh --state path (e.g. from `mktemp`): --prs
together with an existing parseable state file is refused, so a leftover file
from an earlier run never replaces the new PR list.

Exit codes:
    0  queue finished: no PR remaining, or the deadline passed (stalled or
       unreadable marked)
    2  usage error, no usable state and no --prs to start from, --prs given
       while --state already holds queue state, or --requeue for a PR that is
       not "head-moved"
    3  chunk ended before the deadline with PRs remaining — run again with
       the same --state
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

TOTAL_SECONDS = 1800
CHUNK_SECONDS = int(os.environ.get("YWC_MQ_CHUNK_SECONDS", "540"))  # env override is for tests only
POLL_SECONDS = int(os.environ.get("YWC_MQ_POLL_SECONDS", "60"))  # env override is for tests only
GH_TIMEOUT_SECONDS = int(os.environ.get("YWC_MQ_GH_TIMEOUT_SECONDS", "20"))  # env override is for tests only
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
FINAL_POLL_SECONDS = 40  # fits the 600 s Bash cap after a 540 s chunk
MAX_REQUEUES = 2  # same cap as the sequential flow's "at most 2 restarts"


def load_state(path: str) -> dict | None:
    try:
        with open(path) as f:
            state = json.load(f)
        loaded = {
            "deadline": int(state["deadline"]),
            "remaining": [int(n) for n in state["remaining"]],
            "heads": {str(k): str(v) for k, v in state["heads"].items()},
            "status": {str(k): str(v) for k, v in state.get("status", {}).items()},
            "rebase_commented": [int(n) for n in state.get("rebase_commented", [])],
            "query_failed": [int(n) for n in state.get("query_failed", [])],
            "requeues": {str(k): int(v) for k, v in state.get("requeues", {}).items()},
        }
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None
    # Without its queued head a remaining PR cannot be checked for a moved head.
    if not all(SHA_RE.match(loaded["heads"].get(str(n), "")) for n in loaded["remaining"]):
        return None
    return loaded


def save_state(path: str, state: dict) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".mq-state-")
    with os.fdopen(fd, "w") as f:
        json.dump(state, f)
    os.replace(tmp, path)


def gh(*args: str) -> subprocess.CompletedProcess | None:
    """Run gh; on failure print why to stderr and return None."""
    try:
        r = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=GH_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        print(f"gh {' '.join(args[:3])} timed out after {GH_TIMEOUT_SECONDS} s", file=sys.stderr)
        return None
    except OSError as e:
        print(f"gh {' '.join(args[:3])} could not run: {e}", file=sys.stderr)
        return None
    if r.returncode != 0:
        err = (r.stderr.strip().splitlines() or ["no error output"])[-1]
        print(f"gh {' '.join(args[:3])} failed (exit {r.returncode}): {err}", file=sys.stderr)
        return None
    return r


def pr_state(pr: int) -> tuple[str, str, str] | None:
    """(state, mergeStateStatus, headRefOid), or None when the query failed."""
    r = gh("pr", "view", str(pr), "--json", "state,mergeStateStatus,headRefOid")
    if r is None:
        return None
    try:
        data = json.loads(r.stdout)
        head = str(data.get("headRefOid", ""))
        state = str(data.get("state", "UNKNOWN")), str(data.get("mergeStateStatus", "UNKNOWN")), head
    except (ValueError, AttributeError):
        print(f"gh pr view {pr} returned unparsable output", file=sys.stderr)
        return None
    if state[0] == "OPEN" and not SHA_RE.match(head):
        print(f"gh pr view {pr} returned no 40-hex head: {head!r}", file=sys.stderr)
        return None
    return state


def poll_once(state: dict, chunk_deadline: float) -> bool:
    """One pass over the remaining PRs. Return True when a PR became head-moved."""
    moved = False
    next_remaining = []
    for pr in state["remaining"]:
        if time.time() >= chunk_deadline:  # slow gh calls must not outlive the chunk
            next_remaining.append(pr)
            continue
        read = pr_state(pr)
        if read is None:
            if pr not in state["query_failed"]:
                state["query_failed"].append(pr)
            next_remaining.append(pr)
            continue
        if pr in state["query_failed"]:
            state["query_failed"].remove(pr)
        status, merge_status, head = read
        if status == "MERGED":
            state["status"][str(pr)] = "merged"
        elif status == "CLOSED":
            state["status"][str(pr)] = "closed"
        elif head != state["heads"][str(pr)]:
            # A head pushed after --auto skipped the Step 2 checks: stop auto-merge before
            # GitHub merges it. The caller re-checks the new head; a failed disable is retried.
            if gh("pr", "merge", str(pr), "--disable-auto") is not None:
                state["status"][str(pr)] = "head-moved"
                moved = True
            else:
                next_remaining.append(pr)
        else:
            if merge_status in ("CONFLICTING", "DIRTY") and pr not in state["rebase_commented"]:
                if gh("pr", "comment", str(pr), "--body", "@dependabot rebase") is not None:
                    state["rebase_commented"].append(pr)
            next_remaining.append(pr)
    state["remaining"] = next_remaining
    return moved


def run_chunk(state: dict) -> bool:
    """Poll until drained, the deadline, or the chunk end. Return True when finished."""
    chunk_deadline = time.time() + CHUNK_SECONDS
    while state["remaining"] and time.time() < state["deadline"] and time.time() < chunk_deadline:
        if poll_once(state, chunk_deadline):
            break  # hand the moved head to the caller now, not at the chunk end
        left = chunk_deadline - time.time()
        if state["remaining"] and left > 0:
            time.sleep(min(left, POLL_SECONDS))
    if state["remaining"] and time.time() >= state["deadline"]:
        # One last read, so a PR that merged or closed during the final sleep keeps its real
        # outcome instead of being reported stalled. Bounded to FINAL_POLL_SECONDS.
        poll_once(state, time.time() + FINAL_POLL_SECONDS)
        for pr in state["remaining"]:
            state["status"][str(pr)] = "unreadable" if pr in state["query_failed"] else "stalled"
        state["remaining"] = []
    return not state["remaining"]


def pr_with_head(value: str) -> tuple[int, str]:
    number, _, head = value.partition(":")
    if not number.isdecimal() or not SHA_RE.match(head):
        raise argparse.ArgumentTypeError(f"expected <pr-number>:<40-hex head>, got {value!r}")
    return int(number), head


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll the Dependabot auto-merge queue for one chunk.")
    parser.add_argument("--state", required=True)
    parser.add_argument("--prs", type=pr_with_head, nargs="+", metavar="N:SHA")
    parser.add_argument("--requeue", type=pr_with_head, nargs="+", metavar="N:SHA")
    parser.add_argument("--deadline", type=int)
    args = parser.parse_args()

    state = load_state(args.state)
    if state is not None and args.prs:
        # A leftover state file must never silently replace a new PR list.
        print(f"{args.state} already holds queue state — omit --prs to resume it, "
              "or start a new run with a fresh --state path", file=sys.stderr)
        return 2
    if args.requeue:
        if state is None or args.prs:
            print("--requeue resumes an existing --state and cannot be combined with --prs", file=sys.stderr)
            return 2
        if len({n for n, _ in args.requeue}) != len(args.requeue):
            print("--requeue lists a PR twice", file=sys.stderr)
            return 2
        for number, head in args.requeue:
            key = str(number)
            if state["status"].get(key) != "head-moved":
                print(f"PR {number} is not head-moved — only a moved head can be re-queued", file=sys.stderr)
                return 2
        for number, head in args.requeue:
            key = str(number)
            if state["requeues"].get(key, 0) >= MAX_REQUEUES:
                # The caller re-enabled auto-merge before asking; turn it off again so a PR
                # left out of the poll can never merge an unchecked head.
                if gh("pr", "merge", key, "--disable-auto") is None:
                    print(f"PR {number}: auto-merge may still be enabled — disable it manually", file=sys.stderr)
                print(f"PR {number} already re-queued {MAX_REQUEUES} times — left head-moved; "
                      "hand it to the sequential pass", file=sys.stderr)
                continue
            state["requeues"][key] = state["requeues"].get(key, 0) + 1
            state["heads"][key] = head
            del state["status"][key]
            state["remaining"].append(number)
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
        heads = {}
        for number, head in args.prs:
            if heads.setdefault(number, head) != head:
                print(f"PR {number} given with two different heads", file=sys.stderr)
                return 2
        state = {"deadline": deadline, "remaining": list(heads),
                 "heads": {str(n): h for n, h in heads.items()},
                 "status": {}, "rebase_commented": [], "query_failed": [], "requeues": {}}

    done = run_chunk(state)
    save_state(args.state, state)
    print(json.dumps({"done": done, "deadline": state["deadline"],
                      "remaining": state["remaining"], "status": state["status"],
                      "requeues": state["requeues"]}))
    return 0 if done else 3


if __name__ == "__main__":
    sys.exit(main())
