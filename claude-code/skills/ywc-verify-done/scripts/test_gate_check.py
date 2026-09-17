#!/usr/bin/env python3
"""Bundled self-check for gate-check.py — stdlib-only, assert-based, no pytest.

Run directly: `python3 claude-code/skills/ywc-verify-done/scripts/test_gate_check.py`
Exit 0 = pass. Mirrors tools/scripts/test_pyyaml_bootstrap.py's convention.

Covers AC1 (--status executes zero CHECK commands), AC2 (pass / failing-exit /
EXPECT-mismatch branches), AC3 (every malformed-ledger case, including a
nonexistent path with a message distinguishable from malformed-ledger
messages), and AC4 (--reverify re-flips a previously-met gate to FAIL).
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "gate-check.py"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


def write_ledger(tmp: Path, content: str) -> Path:
    path = tmp / "ledger.md"
    with open(path, "w", newline="") as f:
        f.write(content)
    return path


def check_status_executes_nothing(tmp: Path) -> None:
    sentinel = tmp / "sentinel"
    ledger = write_ledger(
        tmp,
        f"- [ ] G1: creates sentinel\n"
        f"  CHECK: touch {sentinel}\n"
        f"  EXPECT: ok\n"
        f"  EVIDENCE: pending\n",
    )
    result = run("--status", str(ledger))
    assert result.returncode == 0, f"--status on well-formed ledger should exit 0: {result.stderr}"
    assert not sentinel.exists(), "--status executed a CHECK command (AC1 regressed)"
    print("PASS: --status executes zero CHECK commands")


def check_passing_gate(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: prints ok\n"
        "  CHECK: echo ok\n"
        "  EXPECT: ok\n"
        "  EVIDENCE: pending\n",
    )
    result = run(str(ledger))
    assert result.returncode == 0, f"passing gate should yield exit 0: {result.stdout} {result.stderr}"
    assert "G1: PASS" in result.stdout
    assert "PASS" in ledger.read_text()
    print("PASS: passing gate marked met")


def check_failing_exit_code_gate(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: fails\n"
        "  CHECK: exit 1\n"
        "  EXPECT: ok\n"
        "  EVIDENCE: pending\n",
    )
    result = run(str(ledger))
    assert result.returncode == 1, "failing-exit-code gate should yield exit 1"
    assert "G1: FAIL" in result.stdout
    print("PASS: failing exit-code gate marked unmet")


def check_expect_mismatch_gate(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: wrong output\n"
        "  CHECK: echo nope\n"
        "  EXPECT: ok\n"
        "  EVIDENCE: pending\n",
    )
    result = run(str(ledger))
    assert result.returncode == 1, "EXPECT-mismatch gate should yield exit 1 even with exit 0 CHECK"
    assert "G1: FAIL" in result.stdout
    assert "expect=no-match" in ledger.read_text()
    print("PASS: EXPECT-mismatch gate marked unmet despite exit 0")


def check_reverify_flips_to_fail(tmp: Path) -> None:
    flag = tmp / "flag"
    flag.write_text("1")
    ledger = write_ledger(
        tmp,
        f"- [ ] G1: conditional\n"
        f"  CHECK: test -f {flag} && echo ok\n"
        f"  EXPECT: ok\n"
        f"  EVIDENCE: pending\n",
    )
    first = run(str(ledger))
    assert first.returncode == 0, "gate should pass while flag file exists"
    assert "PASS" in ledger.read_text()

    flag.unlink()
    default_rerun = run(str(ledger))
    assert default_rerun.returncode == 0, "default run must skip an already-met gate, not re-execute it"
    assert "skipped, fingerprint matched" in default_rerun.stdout

    reverified = run("--reverify", str(ledger))
    assert reverified.returncode == 1, "--reverify must re-execute and flip the now-failing gate"
    assert "G1: FAIL" in reverified.stdout
    print("PASS: --reverify re-flips a previously-met gate to FAIL")


def check_fingerprint_invalidates_stale_pass(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: cached\n  CHECK: echo ok\n  EXPECT: ok\n  EVIDENCE: pending\n",
    )
    first = run(str(ledger))
    assert first.returncode == 0
    assert "fingerprint=sha256:" in ledger.read_text()

    cached = run(str(ledger))
    assert cached.returncode == 0
    assert "skipped, fingerprint matched" in cached.stdout

    changed = ledger.read_text().replace("EXPECT: ok", "EXPECT: changed")
    ledger.write_text(changed)
    assert "PASS" in ledger.read_text(), "test setup: stale EVIDENCE line must still read PASS"

    rerun = run(str(ledger))
    assert rerun.returncode == 1, "changed EXPECT must invalidate the stale fingerprinted PASS and re-execute"
    assert "G1: FAIL" in rerun.stdout
    print("PASS: stale EVIDENCE with a mismatched fingerprint is not trusted as cached PASS")


def check_zero_gates(tmp: Path) -> None:
    ledger = write_ledger(tmp, "# Just prose, no gates here\n")
    result = run("--status", str(ledger))
    assert result.returncode == 1
    assert "zero gates" in result.stderr
    print("PASS: zero-gate ledger fails closed")


def check_duplicate_id(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: first\n"
        "  CHECK: echo ok\n"
        "  EXPECT: ok\n"
        "- [ ] G1: second\n"
        "  CHECK: echo ok\n"
        "  EXPECT: ok\n",
    )
    result = run("--status", str(ledger))
    assert result.returncode == 1
    assert "duplicate id" in result.stderr and "G1" in result.stderr
    print("PASS: duplicate gate id fails closed")


def check_missing_expect(tmp: Path) -> None:
    ledger = write_ledger(tmp, "- [ ] G1: only has CHECK\n  CHECK: echo ok\n")
    result = run("--status", str(ledger))
    assert result.returncode == 1
    assert "G1" in result.stderr and "EXPECT" in result.stderr
    print("PASS: runnable gate missing EXPECT fails closed")


def check_missing_check(tmp: Path) -> None:
    ledger = write_ledger(tmp, "- [ ] G1: only has EXPECT\n  EXPECT: ok\n")
    result = run("--status", str(ledger))
    assert result.returncode == 1
    assert "G1" in result.stderr and "CHECK" in result.stderr
    print("PASS: runnable gate missing CHECK fails closed")


def check_empty_expect(tmp: Path) -> None:
    ledger = write_ledger(tmp, "- [ ] G1: empty expect\n  CHECK: echo ok\n  EXPECT: \n")
    result = run("--status", str(ledger))
    assert result.returncode == 1
    assert "G1" in result.stderr and "empty" in result.stderr.lower()
    print("PASS: empty EXPECT value fails closed at --status time")


def check_nonexistent_path(tmp: Path) -> None:
    result = run("--status", str(tmp / "does-not-exist.md"))
    assert result.returncode == 1
    assert "not found" in result.stderr.lower()
    assert "zero gates" not in result.stderr and "duplicate" not in result.stderr, (
        "nonexistent-path message must be distinguishable from malformed-ledger messages"
    )
    print("PASS: nonexistent ledger path fails closed with a distinct message")


def check_expect_regex_case_insensitive(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: regex case-insensitive\n"
        "  CHECK: echo SUCCESS\n"
        "  EXPECT: /success/i\n"
        "  EVIDENCE: pending\n",
    )
    result = run(str(ledger))
    assert result.returncode == 0, f"regex EXPECT with /i should match: {result.stdout} {result.stderr}"
    assert "G1: PASS" in result.stdout
    print("PASS: regex EXPECT with /i flag matches case-insensitively")


def check_expect_regex_multiline_dotall(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: regex dotall across lines\n"
        "  CHECK: printf 'line1\\nline2'\n"
        "  EXPECT: /line1.*line2/s\n"
        "  EVIDENCE: pending\n",
    )
    result = run(str(ledger))
    assert result.returncode == 0, f"regex EXPECT with /s should match across newlines: {result.stdout} {result.stderr}"
    assert "G1: PASS" in result.stdout
    print("PASS: regex EXPECT with /s flag matches across newlines")


def check_invalid_regex_flag(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: unsupported flag\n"
        "  CHECK: echo hi\n"
        "  EXPECT: /hi/g\n"
        "  EVIDENCE: pending\n",
    )
    result = run("--status", str(ledger))
    assert result.returncode == 1
    assert "G1" in result.stderr and "unsupported" in result.stderr.lower()
    print("PASS: unsupported EXPECT regex flag fails closed at --status time")


def check_invalid_regex_syntax(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: unclosed char class\n"
        "  CHECK: echo hi\n"
        "  EXPECT: /[unclosed/\n"
        "  EVIDENCE: pending\n",
    )
    result = run("--status", str(ledger))
    assert result.returncode == 1
    assert "G1" in result.stderr and "invalid" in result.stderr.lower()
    print("PASS: invalid EXPECT regex syntax fails closed at --status time")


def check_evidence_insertion_no_initial_line(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: no evidence line yet\n  CHECK: echo ok\n  EXPECT: ok\n",
    )
    assert "EVIDENCE" not in ledger.read_text()
    result = run(str(ledger))
    assert result.returncode == 0, f"gate should pass: {result.stdout} {result.stderr}"
    content = ledger.read_text()
    assert "EVIDENCE: PASS" in content
    assert "CHECK: echo ok" in content and "EXPECT: ok" in content, (
        "inserting the EVIDENCE line must not corrupt the surrounding CHECK/EXPECT lines"
    )
    print("PASS: missing EVIDENCE line is auto-inserted without corrupting the gate")


def check_manual_gate_neither_check_nor_expect(tmp: Path) -> None:
    ledger = write_ledger(tmp, "- [ ] G1: manual_task\n  a human verifies this by hand\n")
    status_result = run("--status", str(ledger))
    assert status_result.returncode == 0, f"a manual gate alone is well-formed: {status_result.stderr}"
    assert "G1: manual" in status_result.stdout

    run_result = run(str(ledger))
    assert run_result.returncode == 0, "a manual-only gate is vacuously met (nothing runnable to fail)"
    assert "G1: manual (skipped)" in run_result.stdout
    print("PASS: a gate with neither CHECK nor EXPECT is treated as manual, not malformed")


def check_timeout_on_hung_command(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: hangs\n"
        "  CHECK: sleep 5\n"
        "  EXPECT: ok\n"
        "  EVIDENCE: pending\n",
    )
    original = SCRIPT.read_text()
    patched = original.replace("TIMEOUT_SECONDS = 120", "TIMEOUT_SECONDS = 1")
    assert patched != original, "TIMEOUT_SECONDS constant not found to patch for the timeout test"
    patched_script = tmp / "gate-check-short-timeout.py"
    patched_script.write_text(patched)

    result = subprocess.run(
        [sys.executable, str(patched_script), str(ledger)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 1, "a gate whose CHECK exceeds the timeout must be reported FAIL"
    assert "G1: FAIL" in result.stdout
    assert "TIMEOUT" in ledger.read_text()
    print("PASS: a CHECK command that exceeds the per-gate timeout is marked FAIL, not hung forever")


def check_output_cap_64kb(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: huge output\n"
        "  CHECK: python3 -c \"print('x' * 200000)\"\n"
        "  EXPECT: /x{100,}/\n"
        "  EVIDENCE: pending\n",
    )
    result = run(str(ledger))
    assert result.returncode == 1, "output exceeding the 64 KB cap must fail closed, not match within the cap"
    content = ledger.read_text()
    assert "OUTPUT_LIMIT" in content
    evidence_line = next(line for line in content.splitlines() if "EVIDENCE:" in line)
    assert len(evidence_line) < 65 * 1024, "EVIDENCE line must not embed the full uncapped output"
    print("PASS: gate output exceeding 64 KB fails closed instead of buffering it in full")


def check_sigterm_ignoring_descendant_is_killed(tmp: Path) -> None:
    if os.name != "posix":
        print("SKIP: SIGTERM-ignoring descendant test requires POSIX process groups")
        return
    marker = tmp / "grandchild_done"
    ledger = write_ledger(
        tmp,
        "- [ ] G1: spawns a SIGTERM-ignoring descendant\n"
        f"  CHECK: (trap '' TERM; sleep 3; touch {marker}) & sleep 100\n"
        "  EXPECT: ok\n"
        "  EVIDENCE: pending\n",
    )
    original = SCRIPT.read_text()
    patched = original.replace("TIMEOUT_SECONDS = 120", "TIMEOUT_SECONDS = 1")
    assert patched != original, "TIMEOUT_SECONDS constant not found to patch for the SIGTERM test"
    patched_script = tmp / "gate-check-short-timeout-sigterm.py"
    patched_script.write_text(patched)

    result = subprocess.run(
        [sys.executable, str(patched_script), str(ledger)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 1, "the hung CHECK must still be reported FAIL"
    time.sleep(3.5)
    assert not marker.exists(), (
        "a background descendant that ignores SIGTERM must still be SIGKILLed "
        "with the rest of the process group, not left running past the timeout"
    )
    print("PASS: a SIGTERM-ignoring background descendant is killed with the process group")


def check_expect_regex_catastrophic_backtracking_bounded(tmp: Path) -> None:
    ledger = write_ledger(
        tmp,
        "- [ ] G1: pathological EXPECT pattern\n"
        "  CHECK: python3 -c \"print('a' * 40 + '!')\"\n"
        "  EXPECT: /(a+)+b/\n"
        "  EVIDENCE: pending\n",
    )
    started = time.monotonic()
    result = run(str(ledger))
    elapsed = time.monotonic() - started
    assert result.returncode == 1, "an EXPECT that never matches must fail the gate"
    assert elapsed < 30, (
        f"EXPECT regex matching must be bounded, not block the checker "
        f"indefinitely (took {elapsed:.1f}s)"
    )
    print("PASS: catastrophic-backtracking EXPECT patterns are bounded, not left to hang")


CHECKS = [
    check_status_executes_nothing,
    check_passing_gate,
    check_failing_exit_code_gate,
    check_expect_mismatch_gate,
    check_reverify_flips_to_fail,
    check_fingerprint_invalidates_stale_pass,
    check_zero_gates,
    check_duplicate_id,
    check_missing_expect,
    check_missing_check,
    check_empty_expect,
    check_nonexistent_path,
    check_expect_regex_case_insensitive,
    check_expect_regex_multiline_dotall,
    check_invalid_regex_flag,
    check_invalid_regex_syntax,
    check_evidence_insertion_no_initial_line,
    check_manual_gate_neither_check_nor_expect,
    check_timeout_on_hung_command,
    check_output_cap_64kb,
    check_sigterm_ignoring_descendant_is_killed,
    check_expect_regex_catastrophic_backtracking_bounded,
]


def main() -> int:
    for check in CHECKS:
        with tempfile.TemporaryDirectory(prefix="gate-check-selfcheck-") as tmp_str:
            check(Path(tmp_str))
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
