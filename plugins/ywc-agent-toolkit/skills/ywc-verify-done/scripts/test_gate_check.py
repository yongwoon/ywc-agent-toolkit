#!/usr/bin/env python3
"""Hermetic standard-library regression suite for gate-check.py."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHECKER = Path(__file__).with_name("gate-check.py")


def fail(message: str) -> None:
    raise AssertionError(message)


def run(checker: Path, *args: str, timeout: float = 20) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(checker), *args],
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def ledger(tmp: Path, body: str, name: str = "ledger.md") -> Path:
    path = tmp / name
    path.write_text(body, encoding="utf-8")
    return path


def evidence(path: Path) -> str:
    match = re.findall(r"^\s*EVIDENCE: (.*)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return match[-1] if match else ""


def digest_from_evidence(path: Path) -> str:
    match = re.search(r'output_sha256=sha256:([0-9a-f]{64})', evidence(path))
    if not match:
        fail(f"missing output digest in {path.read_text()!r}")
    return match.group(1)


def assert_status_read_only(tmp: Path) -> None:
    sentinel = tmp / "status-sentinel"
    path = ledger(
        tmp,
        f"- [ ] G1: status\n  CHECK: touch {shlex.quote(str(sentinel))}\n  EXPECT: done\n",
    )
    before = path.read_bytes()
    result = run(CHECKER, "--status", str(path))
    assert result.returncode == 0, result
    assert "G1: PENDING" in result.stdout, result.stdout
    assert "CHECK: touch" in result.stdout and "EXPECT: done" in result.stdout
    assert not sentinel.exists(), "--status executed CHECK"
    assert path.read_bytes() == before, "--status rewrote the ledger"


def assert_parser_and_manual(tmp: Path) -> None:
    cases = [
        ("missing", tmp / "missing.md", "No such file or directory"),
        ("zero", ledger(tmp, "documentation only\n", "zero.md"), "zero gates"),
        ("duplicate", ledger(tmp, "- [ ] G: one\n- [x] G: two\n", "duplicate.md"), "duplicate gate ID"),
        ("partial", ledger(tmp, "- [ ] G: partial\n  CHECK: printf ok\n", "partial.md"), "both CHECK and EXPECT"),
        ("empty", ledger(tmp, "- [ ] G: empty\n  CHECK:\n  EXPECT: ok\n", "empty.md"), "empty CHECK or EXPECT"),
        ("flag", ledger(tmp, "- [ ] G: flag\n  CHECK: printf ok\n  EXPECT: /ok/z\n", "flag.md"), "unsupported regex flag"),
        ("regex", ledger(tmp, "- [ ] G: regex\n  CHECK: printf ok\n  EXPECT: /(/i\n", "regex.md"), "invalid regex"),
    ]
    for name, path, expected in cases:
        result = run(CHECKER, "--status", str(path))
        assert result.returncode == 2, (name, result)
        assert expected in result.stderr, (name, result.stderr)

    sentinel = tmp / "malformed-sentinel"
    malformed = ledger(
        tmp,
        f"- [ ] A: side effect\n  CHECK: touch {shlex.quote(str(sentinel))}\n  EXPECT: done\n"
        "- [ ] A: duplicate\n",
        "malformed-execution.md",
    )
    result = run(CHECKER, str(malformed))
    assert result.returncode == 2 and not sentinel.exists(), result

    path = ledger(
        tmp,
        """```markdown
- [ ] Fenced: never
  CHECK: touch SHOULD_NOT_EXIST
  EXPECT: never
```
- [ ] MANUAL: human review
text that is inert
""",
        "manual.md",
    )
    result = run(CHECKER, str(path))
    assert result.returncode == 0, result
    assert "MANUAL: MANUAL" in result.stdout, result.stdout
    assert "Fenced" not in result.stdout


def assert_literal_regex_and_last_field(tmp: Path) -> None:
    path = ledger(
        tmp,
        """- [ ] L: literal
  CHECK: printf 'alpha'
  EXPECT: alpha
- [ ] R: regex
  CHECK: printf 'ALPHA'
  EXPECT: /alpha/i
- [ ] D: duplicate fields
  CHECK: printf old
  CHECK: printf final
  EXPECT: old
  EXPECT: final
""",
        "matches.md",
    )
    result = run(CHECKER, str(path))
    assert result.returncode == 0, result
    assert result.stdout.count("PASS") >= 3, result.stdout
    assert "CHECK: printf final" in run(CHECKER, "--status", str(path)).stdout


def assert_cache_reverify_and_fingerprint(tmp: Path) -> None:
    path = ledger(tmp, "- [ ] G1: cache\n  CHECK: printf one\n  EXPECT: one\n", "cache.md")
    first = run(CHECKER, str(path))
    assert first.returncode == 0, first
    saved = path.read_bytes()
    cached = run(CHECKER, str(path))
    assert cached.returncode == 0 and "cached" in cached.stdout, cached
    assert path.read_bytes() == saved
    fresh = run(CHECKER, "--reverify", str(path))
    assert fresh.returncode == 0 and "PASS" in fresh.stdout, fresh
    text = path.read_text()
    expected_fingerprint = hashlib.sha256(b"printf one" + bytes([0]) + b"one").hexdigest()
    assert f"fingerprint=sha256:{expected_fingerprint}" in text

    changed = ledger(tmp, text.replace("EXPECT: one", "EXPECT: two"), "changed.md")
    result = run(CHECKER, str(changed))
    assert result.returncode == 1 and "FAIL" in result.stdout, result

    fingerprint = re.search(r"fingerprint=sha256:([0-9a-f]{64})", text).group(1)
    invalid_cache = [
        f"PASS; exit=0; fingerprint=sha256:{fingerprint}; decisive=not-json",
        f"PASS; exit=0; fingerprint=sha256:{'0' * 64}; decisive=\"ok\"",
        f"PASS; exit=0; fingerprint=sha256:{fingerprint}; decisive=123",
    ]
    for index, cached_evidence in enumerate(invalid_cache):
        candidate = ledger(
            tmp,
            "- [ ] G1: cache variant\n  CHECK: printf one\n  EXPECT: one\n"
            f"  EVIDENCE: {cached_evidence}\n",
            f"invalid-cache-{index}.md",
        )
        status_result = run(CHECKER, "--status", str(candidate))
        assert "G1: PENDING" in status_result.stdout, status_result


def assert_rewrite_and_bytes(tmp: Path) -> None:
    path = ledger(tmp, "- [ ] G1: insert\n  CHECK: printf pass\n  EXPECT: pass", "insert.md")
    result = run(CHECKER, str(path))
    assert result.returncode == 0, result
    assert "EXPECT: pass\n  EVIDENCE: PASS;" in path.read_text()
    assert run(CHECKER, "--status", str(path)).stdout.startswith("G1: PASS")

    crlf = tmp / "crlf.md"
    crlf.write_bytes(b"- [ ] G1: crlf\r\n  CHECK: printf pass\r\n  EXPECT: pass\r\n")
    result = run(CHECKER, str(crlf))
    assert result.returncode == 0, result
    assert b"\r\n  EVIDENCE: PASS;" in crlf.read_bytes()
    assert b"\n" not in crlf.read_bytes().replace(b"\r\n", b"")

    replacement = ledger(
        tmp,
        "- [ ] G1: replacement\n  CHECK: printf pass\n  EXPECT: pass\n"
        "  EVIDENCE: FAIL; old\n  EVIDENCE: FAIL; final\n  tail: keep\n",
        "replacement.md",
    )
    result = run(CHECKER, str(replacement))
    assert result.returncode == 0, result
    replacement_text = replacement.read_text()
    assert "EVIDENCE: FAIL; old" in replacement_text
    assert replacement_text.count("EVIDENCE:") == 2 and "tail: keep" in replacement_text

    raw = ledger(tmp, "- [ ] G1: raw\n  CHECK: python3 -c \"import sys; sys.stdout.buffer.write(bytes([255]))\"\n  EXPECT: nope\n", "raw.md")
    result = run(CHECKER, str(raw))
    assert result.returncode == 1, result
    assert digest_from_evidence(raw) == hashlib.sha256(b"\xff").hexdigest()


def copy_with_limits(tmp: Path, **replacements: str) -> Path:
    copied = tmp / "gate-check-copy.py"
    text = CHECKER.read_text(encoding="utf-8")
    for name, value in replacements.items():
        text = re.sub(rf"^{name} = .*?$", f"{name} = {value}", text, flags=re.MULTILINE)
    copied.write_text(text, encoding="utf-8")
    return copied


def assert_bounds_and_cleanup(tmp: Path) -> None:
    nonzero = ledger(
        tmp,
        "- [ ] G1: nonzero\n  CHECK: python3 -c \"raise SystemExit(7)\"\n  EXPECT: never\n",
        "nonzero.md",
    )
    result = run(CHECKER, str(nonzero))
    assert result.returncode == 1 and "FAIL; exit=7;" in evidence(nonzero), result

    exact = ledger(
        tmp,
        "- [ ] G1: exact cap\n  CHECK: python3 -c \"import sys; sys.stdout.write('x'*65536)\"\n  EXPECT: x\n",
        "exact-cap.md",
    )
    result = run(CHECKER, str(exact))
    assert result.returncode == 0 and "PASS" in result.stdout, result

    output = ledger(
        tmp,
        "- [ ] G1: cap\n  CHECK: python3 -c \"import sys; sys.stdout.write('x'*70000)\"\n  EXPECT: x\n",
        "cap.md",
    )
    result = run(CHECKER, str(output))
    assert result.returncode == 1 and "FAIL" in result.stdout, result
    assert "exit=125" in evidence(output)
    assert digest_from_evidence(output) == hashlib.sha256(b"x" * 65536).hexdigest()

    timeout_checker = copy_with_limits(tmp, CHECK_TIMEOUT_SECONDS="1")
    timed = ledger(tmp, "- [ ] G1: timeout\n  CHECK: sleep 3\n  EXPECT: done\n", "timeout.md")
    result = run(timeout_checker, str(timed), timeout=8)
    assert result.returncode == 1 and "exit=124" in evidence(timed), result

    regex_checker = copy_with_limits(tmp, EXPECT_TIMEOUT_SECONDS="0.2")
    catastrophic = ledger(
        tmp,
        "- [ ] G1: regex timeout\n  CHECK: python3 -c \"import sys; sys.stdout.write('a'*30000+'!')\"\n  EXPECT: /(a+)+$/\n",
        "regex-timeout.md",
    )
    started = time.monotonic()
    result = run(regex_checker, str(catastrophic), timeout=8)
    elapsed = time.monotonic() - started
    assert result.returncode == 1, result
    assert elapsed < 4, f"regex bound exceeded: {elapsed:.2f}s"
    assert "FAIL; exit=1;" in evidence(catastrophic)
    assert digest_from_evidence(catastrophic) == hashlib.sha256(b"a" * 30000 + b"!").hexdigest()

    if os.name != "posix":
        print("POSIX descendant cleanup: SKIP (non-POSIX)")
        return
    child_file = tmp / "child.pid"
    child_code = (
        "import os,signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); "
        f"open({str(child_file)!r},'w').write(str(os.getpid())); time.sleep(30)"
    )
    parent_code = (
        "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c'," + repr(child_code) + "]); time.sleep(30)"
    )
    cleanup_checker = copy_with_limits(tmp, CHECK_TIMEOUT_SECONDS="1")
    cleanup = ledger(
        tmp,
        f"- [ ] G1: cleanup\n  CHECK: {shlex.quote(sys.executable)} -c {shlex.quote(parent_code)}\n  EXPECT: done\n",
        "cleanup.md",
    )
    result = run(cleanup_checker, str(cleanup), timeout=8)
    assert result.returncode == 1 and "exit=124" in evidence(cleanup), result
    deadline = time.monotonic() + 1
    while not child_file.exists() and time.monotonic() < deadline:
        time.sleep(0.02)
    assert child_file.exists(), "cleanup fixture never started its child"
    child_pid = int(child_file.read_text())
    for _ in range(20):
        try:
            os.kill(child_pid, 0)
        except ProcessLookupError:
            break
        time.sleep(0.05)
    else:
        fail("SIGTERM-ignoring descendant survived process-group cleanup")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="gate-check-tests-") as directory:
        tmp = Path(directory)
        assert_status_read_only(tmp)
        assert_parser_and_manual(tmp)
        assert_literal_regex_and_last_field(tmp)
        assert_cache_reverify_and_fingerprint(tmp)
        assert_rewrite_and_bytes(tmp)
        assert_bounds_and_cleanup(tmp)
    print("gate-check regression suite: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
