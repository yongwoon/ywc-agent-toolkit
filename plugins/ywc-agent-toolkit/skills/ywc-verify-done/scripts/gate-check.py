#!/usr/bin/env python3
"""Fail-closed optional Gate Ledger checker for ywc-verify-done."""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import os
import re
import selectors
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


CHECK_TIMEOUT_SECONDS = 120
OUTPUT_LIMIT_BYTES = 64 * 1024
EXPECT_TIMEOUT_SECONDS = 5

HEADER_RE = re.compile(r"^-\s*\[[^\]]\]\s*(.+)$")
FIELD_RE = re.compile(r"^\s*(CHECK|EXPECT|EVIDENCE):( ?)(.*)$")
CACHE_RE = re.compile(
    r"^PASS; exit=0; fingerprint=sha256:([0-9a-f]{64}); decisive=(.+)$"
)


class LedgerError(ValueError):
    """A malformed ledger that must fail before any CHECK executes."""


@dataclass
class Field:
    name: str
    value: str
    line_index: int


@dataclass
class Gate:
    gate_id: str
    header_index: int
    fields: dict[str, Field] = field(default_factory=dict)

    @property
    def check(self) -> Optional[str]:
        item = self.fields.get("CHECK")
        return item.value if item else None

    @property
    def expect(self) -> Optional[str]:
        item = self.fields.get("EXPECT")
        return item.value if item else None

    @property
    def evidence(self) -> Optional[str]:
        item = self.fields.get("EVIDENCE")
        return item.value if item else None

    @property
    def manual(self) -> bool:
        return self.check is None and self.expect is None


def _line_text(line: str) -> str:
    return line[:-2] if line.endswith("\r\n") else line.rstrip("\n")


def _regex_expect(value: str) -> Optional[tuple[str, int]]:
    if not (value.startswith("/") and value.count("/") >= 2):
        return None
    end = value.rfind("/")
    pattern = value[1:end]
    flags_text = value[end + 1 :]
    flags = 0
    mapping = {"i": re.IGNORECASE, "m": re.MULTILINE, "s": re.DOTALL}
    for flag in flags_text:
        if flag not in mapping:
            raise LedgerError(
                f"unsupported regex flag {flag!r}; only i, m, and s are allowed"
            )
        if flags & mapping[flag]:
            raise LedgerError(f"duplicate regex flag {flag!r}")
        flags |= mapping[flag]
    try:
        re.compile(pattern, flags)
    except re.error as exc:
        raise LedgerError(f"invalid regex EXPECT: {exc}") from exc
    return pattern, flags


def parse_ledger(text: str) -> tuple[list[str], list[Gate]]:
    lines = text.splitlines(keepends=True)
    gates: list[Gate] = []
    current: Optional[Gate] = None
    seen_ids: set[str] = set()
    fenced = False

    for index, line in enumerate(lines):
        raw = _line_text(line)
        if raw.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        header = HEADER_RE.match(raw)
        if header:
            content = header.group(1)
            colon = content.find(":")
            if colon <= 0 or not content[:colon].strip():
                continue
            gate_id = content[:colon].strip()
            if gate_id in seen_ids:
                raise LedgerError(f"duplicate gate ID: {gate_id}")
            seen_ids.add(gate_id)
            current = Gate(gate_id, index)
            gates.append(current)
            continue
        if current is not None:
            match = FIELD_RE.match(raw)
            if match:
                name = match.group(1)
                current.fields[name] = Field(name, match.group(3), index)

    if not gates:
        raise LedgerError("ledger contains zero gates")
    for gate in gates:
        has_check = gate.check is not None
        has_expect = gate.expect is not None
        if has_check != has_expect:
            raise LedgerError(
                f"gate {gate.gate_id} must contain both CHECK and EXPECT, or neither"
            )
        if has_check and (not gate.check or not gate.expect):
            raise LedgerError(f"gate {gate.gate_id} has an empty CHECK or EXPECT")
        if gate.expect is not None:
            _regex_expect(gate.expect)
    return lines, gates


def fingerprint(check: str, expect: str) -> str:
    digest = hashlib.sha256(check.encode("utf-8") + b"\0" + expect.encode("utf-8"))
    return digest.hexdigest()


def cached_pass(gate: Gate) -> bool:
    if not gate.evidence or not gate.check or not gate.expect:
        return False
    match = CACHE_RE.fullmatch(gate.evidence)
    if not match or match.group(1) != fingerprint(gate.check, gate.expect):
        return False
    try:
        decisive = json.loads(match.group(2))
    except json.JSONDecodeError:
        return False
    return isinstance(decisive, str)


def _kill_group(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGTERM)
            time.sleep(0.05)
            os.killpg(process.pid, signal.SIGKILL)
        except (PermissionError, ProcessLookupError):
            process.kill()
    else:
        process.kill()


def run_check(command: str) -> tuple[int, bytes]:
    kwargs: dict[str, object] = {
        "shell": True,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
    }
    if os.name == "posix":
        kwargs["start_new_session"] = True
    process = subprocess.Popen(command, **kwargs)  # type: ignore[arg-type]
    output = bytearray()
    stream = process.stdout
    if stream is None:
        return process.wait(), b""
    selector = selectors.DefaultSelector()
    selector.register(stream, selectors.EVENT_READ)
    deadline = time.monotonic() + CHECK_TIMEOUT_SECONDS
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                _kill_group(process)
                process.wait()
                return 124, bytes(output)
            events = selector.select(min(remaining, 0.1))
            for key, _ in events:
                chunk = os.read(key.fd, 4096)
                if not chunk:
                    selector.unregister(stream)
                    stream.close()
                    stream = None
                    break
                remaining_capacity = OUTPUT_LIMIT_BYTES - len(output)
                if len(chunk) > remaining_capacity:
                    output.extend(chunk[:remaining_capacity])
                    _kill_group(process)
                    process.wait()
                    return 125, bytes(output)
                output.extend(chunk)
            if process.poll() is not None and stream is None:
                break
        return process.returncode or 0, bytes(output)
    finally:
        selector.close()
        if stream is not None:
            stream.close()
        if process.poll() is None:
            _kill_group(process)
            process.wait()


def _regex_worker(pattern: str, flags: int, output: str, connection) -> None:
    try:
        connection.send(bool(re.search(pattern, output, flags)))
    except BaseException as exc:  # pragma: no cover - defensive child boundary
        connection.send(exc)
    finally:
        connection.close()


def matches_expect(expect: str, output: str) -> bool:
    regex = _regex_expect(expect)
    if regex is None:
        return expect in output
    pattern, flags = regex
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(False)
    process = context.Process(target=_regex_worker, args=(pattern, flags, output, sender))
    process.start()
    sender.close()
    try:
        if receiver.poll(EXPECT_TIMEOUT_SECONDS):
            result = receiver.recv()
            if isinstance(result, BaseException):
                raise LedgerError(f"regex evaluation failed: {result}")
            return bool(result)
        process.terminate()
        process.join(1)
        if process.is_alive():
            process.kill()
            process.join()
        raise LedgerError("regex EXPECT timed out after 5 seconds")
    finally:
        receiver.close()
        if process.is_alive():
            process.terminate()
        process.join()


def evidence_line(gate: Gate, exit_code: int, output: bytes, passed: bool) -> str:
    output_digest = hashlib.sha256(output).hexdigest()
    decisive = (
        f"exit={exit_code}; matched={str(passed).lower()}; "
        f"output_sha256=sha256:{output_digest}"
    )
    encoded = json.dumps(decisive, ensure_ascii=False)
    if passed:
        return f"PASS; exit=0; fingerprint=sha256:{fingerprint(gate.check or '', gate.expect or '')}; decisive={encoded}"
    return f"FAIL; exit={exit_code}; decisive={encoded}"


def rewrite_evidence(path: Path, lines: list[str], gates: list[Gate], updates: dict[str, str]) -> None:
    newline = "\r\n" if any(line.endswith("\r\n") for line in lines) else "\n"
    operations: list[tuple[int, Optional[str], str]] = []
    for gate in gates:
        if gate.gate_id not in updates or gate.manual:
            continue
        value = updates[gate.gate_id]
        if "EVIDENCE" in gate.fields:
            operations.append((gate.fields["EVIDENCE"].line_index, value, newline))
        else:
            operations.append((gate.fields["EXPECT"].line_index + 1, None, f"  EVIDENCE: {value}{newline}"))
    for index, replacement, payload in sorted(operations, reverse=True):
        if replacement is not None:
            if lines[index].endswith("\r\n"):
                ending = "\r\n"
            elif lines[index].endswith("\n"):
                ending = "\n"
            else:
                ending = ""
            prefix = lines[index][: len(lines[index]) - len(lines[index].lstrip())]
            lines[index] = prefix + "EVIDENCE: " + replacement + ending
        else:
            previous = index - 1
            if previous >= 0 and not lines[previous].endswith(("\n", "\r\n")):
                lines[previous] += newline
            lines.insert(index, payload)
    path.write_text("".join(lines), encoding="utf-8", newline="")


def status(gates: list[Gate]) -> int:
    for gate in gates:
        if gate.manual:
            state = "MANUAL"
        elif cached_pass(gate):
            state = "PASS"
        elif gate.evidence and gate.evidence.startswith("FAIL;"):
            state = "FAIL"
        else:
            state = "PENDING"
        print(f"{gate.gate_id}: {state}")
        if gate.check is not None:
            print(f"  CHECK: {gate.check}")
            print(f"  EXPECT: {gate.expect}")
    return 0


def execute(path: Path, lines: list[str], gates: list[Gate], reverify: bool) -> int:
    updates: dict[str, str] = {}
    failed = False
    for gate in gates:
        if gate.manual:
            print(f"{gate.gate_id}: MANUAL (skipped)")
            continue
        if not reverify and cached_pass(gate):
            print(f"{gate.gate_id}: PASS (cached)")
            continue
        try:
            exit_code, output_bytes = run_check(gate.check or "")
            output = output_bytes.decode("utf-8", errors="replace")
            matched = exit_code == 0 and matches_expect(gate.expect or "", output)
            if exit_code == 0 and not matched:
                exit_code = 1
            updates[gate.gate_id] = evidence_line(gate, exit_code, output_bytes, matched)
            print(f"{gate.gate_id}: {'PASS' if matched else 'FAIL'}")
            failed = failed or not matched
        except LedgerError as exc:
            updates[gate.gate_id] = evidence_line(gate, 1, str(exc).encode("utf-8"), False)
            print(f"{gate.gate_id}: FAIL ({exc})")
            failed = True
    if updates:
        rewrite_evidence(path, lines, gates, updates)
    return 1 if failed else 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--status", action="store_true")
    mode.add_argument("--reverify", action="store_true")
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args(argv)
    try:
        text = args.ledger.read_bytes().decode("utf-8")
        lines, gates = parse_ledger(text)
        if args.status:
            return status(gates)
        return execute(args.ledger, lines, gates, args.reverify)
    except (OSError, UnicodeError, LedgerError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
