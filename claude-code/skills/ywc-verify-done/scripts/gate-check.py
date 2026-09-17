#!/usr/bin/env python3
"""
gate-check.py --status|--reverify <ledger.md>

Deterministic gate-ledger checker for ywc-verify-done's optional high-stakes
completion-claim escalation. Parses a markdown gate ledger (ID / CHECK: /
EXPECT: / EVIDENCE:), and either reports it (--status), executes every unmet
runnable gate (default, no flag), or force re-executes every runnable gate
(--reverify). A runnable gate passes only when its CHECK command exits 0 AND
its combined stdout+stderr matches EXPECT (substring, or /regex/flags with
only i/m/s recognized). See
docs/ywc-plans/20260917-verify-done-gate-ledger-port.md for the full spec.

Ledger format:

  - [ ] G1: <outcome>
    CHECK: <shell command>
    EXPECT: <substring or /regex/flags>
    EVIDENCE: pending

A gate with neither CHECK nor EXPECT is manual/non-runnable and is never
auto-marked met. A gate with exactly one of the two is a malformed ledger
(fails closed). CHECK/EXPECT/EVIDENCE lines belong to the most recently seen
gate header until the next header or EOF. A line that starts with a
triple-backtick fence marker (bare, or with a trailing language tag such as
```markdown) toggles a "skip parsing" state so a ledger's own documentation
examples are not parsed as live gates; an unterminated fence is implicitly
closed at EOF.

Python 3 stdlib only (score-gate.py convention). Plain-text stdout, not
JSON — read interactively by a human running verification, never
machine-chained by another script.

Exit codes:
  0  --status: well-formed ledger / default+--reverify: all runnable gates met
  1  --status: malformed ledger or bad path /
     default+--reverify: >=1 unmet gate, malformed ledger, or bad path
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import selectors
import signal
import multiprocessing
import queue as queue_mod
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

TIMEOUT_SECONDS = 120
EXPECT_TIMEOUT_SECONDS = 5
OUTPUT_CAP_BYTES = 64 * 1024
GATE_HEADER_RE = re.compile(r"^-\s*\[.?\]\s*([^:]+):\s*(.*)$")
FIELD_RE = re.compile(r"^(\s*)(CHECK|EXPECT|EVIDENCE):\s?(.*)$")
REGEX_WRAP_RE = re.compile(r"^/(.*)/([A-Za-z]*)$", re.S)
FLAG_MAP = {"i": re.IGNORECASE, "m": re.MULTILINE, "s": re.DOTALL}
PASS_RE = re.compile(
    r"^PASS; exit=0; fingerprint=sha256:([0-9a-f]{64}); decisive=(.+)$"
)


@dataclass
class Gate:
    id: str
    header_idx: int
    check: str | None = None
    check_idx: int | None = None
    expect: str | None = None
    expect_idx: int | None = None
    evidence: str | None = None
    evidence_idx: int | None = None
    indent: str = "  "
    runnable: bool = False


def split_line(line: str) -> tuple[str, str]:
    """Split a splitlines(keepends=True) line into (body, terminator)."""
    m = re.match(r"^(.*?)(\r\n|\r|\n)?$", line, re.S)
    return m.group(1), m.group(2) or ""


def parse_ledger(lines: list[str]) -> tuple[dict[str, Gate], list[str], list[str]]:
    """Parse ledger lines. Returns (gates_by_id, id_order, errors)."""
    gates: dict[str, Gate] = {}
    order: list[str] = []
    errors: list[str] = []
    current: Gate | None = None
    skip = False

    for i, line in enumerate(lines):
        body, _ = split_line(line)
        if body.strip().startswith("```"):
            skip = not skip
            continue
        if skip:
            continue

        header_match = GATE_HEADER_RE.match(body)
        if header_match:
            gid = header_match.group(1).strip()
            if not gid:
                errors.append(f"line {i + 1}: gate header has an empty id")
                current = None
                continue
            if gid in gates:
                errors.append(f"gate '{gid}': duplicate id")
                current = None
                continue
            gate = Gate(id=gid, header_idx=i)
            gates[gid] = gate
            order.append(gid)
            current = gate
            continue

        field_match = FIELD_RE.match(body)
        if field_match and current is not None:
            indent, key, value = field_match.groups()
            current.indent = indent or current.indent
            if key == "CHECK":
                current.check, current.check_idx = value, i
            elif key == "EXPECT":
                current.expect, current.expect_idx = value, i
            elif key == "EVIDENCE":
                current.evidence, current.evidence_idx = value, i

    if not gates:
        errors.append("ledger has zero gates")

    for gid in order:
        gate = gates[gid]
        has_check = gate.check is not None
        has_expect = gate.expect is not None
        if has_check != has_expect:
            missing = "EXPECT" if has_check else "CHECK"
            errors.append(f"gate '{gid}': runnable gate missing {missing}")
            continue
        if not has_check and not has_expect:
            continue  # manual gate: not runnable, not an error
        if gate.expect == "":
            errors.append(f"gate '{gid}': EXPECT value is empty")
            continue
        wrap = REGEX_WRAP_RE.match(gate.expect)
        if wrap:
            pattern, flag_chars = wrap.groups()
            bad_flags = sorted(set(flag_chars) - set(FLAG_MAP))
            if bad_flags:
                errors.append(
                    f"gate '{gid}': unsupported EXPECT regex flag(s) "
                    f"{''.join(bad_flags)!r} (only i/m/s recognized)"
                )
                continue
            try:
                re.compile(pattern)
            except re.error as exc:
                errors.append(f"gate '{gid}': invalid EXPECT regex — {exc}")
                continue
        gate.runnable = True

    return gates, order, errors


def fingerprint(gate: Gate) -> str:
    value = (gate.check or "").encode() + b"\0" + (gate.expect or "").encode()
    return hashlib.sha256(value).hexdigest()


def evidence_is_cached_pass(gate: Gate) -> bool:
    if gate.evidence is None:
        return False
    match = PASS_RE.fullmatch(gate.evidence.strip())
    if not match or match.group(1) != fingerprint(gate):
        return False
    try:
        value = json.loads(match.group(2))
    except json.JSONDecodeError:
        return False
    return isinstance(value, str)


def evidence_status(gate: Gate) -> str:
    if gate.runnable and evidence_is_cached_pass(gate):
        return "PASS"
    value = (gate.evidence or "pending").strip()
    if value.upper().startswith("FAIL"):
        return "FAIL"
    return "PENDING"


def _regex_search_worker(
    pattern: str, output: str, flags: int, queue: "multiprocessing.Queue[str | None]"
) -> None:
    m = re.search(pattern, output, flags)
    queue.put(m.group(0) if m else None)


def matches_expect(expect: str, output: str) -> tuple[bool, str]:
    wrap = REGEX_WRAP_RE.match(expect)
    if wrap:
        pattern, flag_chars = wrap.groups()
        flags = 0
        for ch in flag_chars:
            flags |= FLAG_MAP[ch]
        # A pathological pattern (catastrophic backtracking) must not block
        # the checker indefinitely. re.search holds the GIL for the whole
        # match, so a thread cannot be interrupted — a separate process is
        # required to bound and kill a runaway match.
        queue: "multiprocessing.Queue[str | None]" = multiprocessing.Queue()
        worker = multiprocessing.Process(
            target=_regex_search_worker, args=(pattern, output, flags, queue), daemon=True
        )
        worker.start()
        try:
            matched = queue.get(timeout=EXPECT_TIMEOUT_SECONDS)
        except queue_mod.Empty:
            matched = None
        finally:
            if worker.is_alive():
                worker.terminate()
            worker.join()
        return (matched is not None, matched or "")
    return (expect in output, expect if expect in output else "")


def stop_process_group(process: subprocess.Popen[bytes]) -> None:
    """Terminate, then kill, the process group started for a CHECK command.

    process.wait() reaps only the top-level shell; if it exits before a
    backgrounded grandchild that ignores SIGTERM, the wait succeeds while
    that grandchild is still alive in the group. SIGKILL is therefore sent
    to the group unconditionally after the grace period, not only on a
    wait() timeout. On POSIX this must run even when the top-level shell
    has already been reaped (process.poll() is not None) — a descendant can
    still hold the stdout pipe open in that case, and skipping the signal
    would leave it running past the deadline.
    """
    if os.name != "posix" and process.poll() is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=0.5)
    except subprocess.TimeoutExpired:
        pass
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except ProcessLookupError:
        pass


def run_check(gate: Gate) -> tuple[int | str, bool, str]:
    """Execute gate.check. Returns (exit_code, expect_ok, decisive_output).

    Streams stdout+stderr incrementally with a bounded buffer instead of
    buffering the full output in memory, and runs the shell command in its
    own process group so a timeout or output-cap breach can terminate the
    whole subtree, not just the top-level shell.
    """
    kwargs: dict[str, object] = {
        "shell": True,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
    }
    if os.name == "posix":
        kwargs["start_new_session"] = True
    process = subprocess.Popen(gate.check, **kwargs)  # type: ignore[arg-type]
    output = bytearray()
    limited = False
    timed_out = False
    selector = selectors.DefaultSelector()
    assert process.stdout is not None
    selector.register(process.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + TIMEOUT_SECONDS
    try:
        while True:
            if not timed_out and time.monotonic() >= deadline:
                timed_out = True
                stop_process_group(process)
                break
            events = selector.select(timeout=0.05)
            for key, _ in events:
                chunk = key.fileobj.read1(4096)  # type: ignore[attr-defined]
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                remaining = OUTPUT_CAP_BYTES - len(output)
                output.extend(chunk[:remaining])
                if len(chunk) > remaining:
                    limited = True
                    stop_process_group(process)
            if process.poll() is not None and not selector.get_map():
                break
            if (timed_out or limited) and process.poll() is not None:
                selector.close()
                break
    finally:
        selector.close()
        if process.poll() is None:
            stop_process_group(process)
        try:
            process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            stop_process_group(process)
            process.communicate()

    decoded = bytes(output).decode("utf-8", errors="replace")
    if timed_out:
        return "timeout", False, f"TIMEOUT after {TIMEOUT_SECONDS}s"
    if limited:
        return "output_limit", False, f"OUTPUT_LIMIT exceeded ({OUTPUT_CAP_BYTES} bytes)"
    returncode = process.returncode if process.returncode is not None else 1
    expect_ok, matched = matches_expect(gate.expect, decoded)
    if returncode == 0 and expect_ok:
        return returncode, True, matched
    out_lines = decoded.splitlines()
    return returncode, False, out_lines[0] if out_lines else "(no output)"


def write_evidence(path: Path, lines: list[str], edits: list[tuple[str, int, str]]) -> None:
    """Apply replace/insert_after edits, highest line index first, then write.

    Applying in descending index order means an insertion never shifts the
    index of an edit still pending lower in the file.
    """
    for kind, idx, new_body in sorted(edits, key=lambda e: e[1], reverse=True):
        if kind == "replace":
            _, term = split_line(lines[idx])
            lines[idx] = new_body + (term or "\n")
        else:  # insert_after
            term = split_line(lines[idx])[1] or "\n"
            lines.insert(idx + 1, new_body + term)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(lines))


def execute_gates(
    path: Path, lines: list[str], gates: dict[str, Gate], order: list[str], force: bool
) -> tuple[int, list[str]]:
    report: list[str] = []
    edits: list[tuple[str, int, str]] = []
    all_met = True

    for gid in order:
        gate = gates[gid]
        if not gate.runnable:
            report.append(f"{gid}: manual (skipped)")
            continue
        if not force and evidence_is_cached_pass(gate):
            report.append(f"{gid}: PASS (skipped, fingerprint matched)")
            continue

        exit_code, expect_ok, decisive = run_check(gate)
        passed = exit_code == 0 and expect_ok
        if not passed:
            all_met = False

        if passed:
            digest = fingerprint(gate)
            decisive_json = json.dumps(decisive, ensure_ascii=False)
            new_line = (
                f"{gate.indent}EVIDENCE: PASS; exit=0; "
                f"fingerprint=sha256:{digest}; decisive={decisive_json}"
            )
            report.append(f"{gid}: PASS (exit=0, expect=match)")
        else:
            detail = f'exit={exit_code} expect={"match" if expect_ok else "no-match"} decisive="{decisive}"'
            new_line = f"{gate.indent}EVIDENCE: FAIL; {detail}"
            report.append(f"{gid}: FAIL ({detail})")

        if gate.evidence_idx is not None:
            edits.append(("replace", gate.evidence_idx, new_line))
        else:
            anchor = gate.expect_idx if gate.expect_idx is not None else gate.check_idx
            edits.append(("insert_after", anchor, new_line))

    if edits:
        write_evidence(path, lines, edits)

    return (0 if all_met else 1), report


def print_status_report(gates: dict[str, Gate], order: list[str]) -> None:
    for gid in order:
        gate = gates[gid]
        kind = "runnable" if gate.runnable else "manual"
        print(f"{gid}: {kind}, {evidence_status(gate).lower()}")
    runnable_count = sum(1 for g in gates.values() if g.runnable)
    print(f"{len(order)} gate(s), {runnable_count} runnable, {len(order) - runnable_count} manual")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Deterministic gate-ledger checker for ywc-verify-done")
    parser.add_argument("ledger", help="path to the gate ledger markdown file")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--status", action="store_true", help="parse and report only; execute nothing")
    mode.add_argument("--reverify", action="store_true", help="force re-execute every runnable gate")
    args = parser.parse_args(argv[1:])

    path = Path(args.ledger)
    if not path.is_file():
        print(f"gate-check.py: file not found: {args.ledger}", file=sys.stderr)
        return 1

    with open(path, "r", encoding="utf-8", newline="") as f:
        content = f.read()
    lines = content.splitlines(keepends=True)

    gates, order, errors = parse_ledger(lines)
    if errors:
        for err in errors:
            print(f"gate-check.py: malformed ledger — {err}", file=sys.stderr)
        return 1

    if args.status:
        print_status_report(gates, order)
        return 0

    exit_code, report = execute_gates(path, lines, gates, order, force=args.reverify)
    for line in report:
        print(line)
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
