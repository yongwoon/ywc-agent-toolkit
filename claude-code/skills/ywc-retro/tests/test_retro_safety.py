#!/usr/bin/env python3
"""Security checks for ywc-retro: execute the two bash blocks SKILL.md prescribes.

Block 1 creates the run scratchpad: it must land outside the repository (even
when TMPDIR points inside it) with mode 0700. Block 2 is the mechanical
redaction pass: every listed secret shape becomes `<REDACTED>`, benign text
such as `task-…` survives, and PEM state never leaks into the next file.

stdlib only, offline. Requires bash, git, perl.
"""

from __future__ import annotations

import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"
FAILURES: list[str] = []

SECRETS = {
    "github token": "ghp_" + "A" * 36,
    "openai key": "sk-" + "b" * 32,
    "aws key": "AKIA" + "ABCDEFGHIJKLMNOP",
    "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.c2lnbmF0dXJl",
    "bearer": "Bearer " + "x" * 24,
    "url userinfo": "postgres://admin:hunter2@db.example.com/app",
    "password assignment": "password=hunter2",
    "api key assignment": "API_KEY=abc123",
    "email": "alice@example.com",
    "github oauth token": "gho_" + "C" * 36,
    "github server token": "ghs_" + "D" * 36,
    "stripe live key": "sk_live_" + "c" * 24,
    "stripe restricted test key": "rk_test_" + "d" * 24,
    "gitlab pat": "glpat-" + "e" * 20,
    "npm token": "npm_" + "f" * 36,
    "slack app token": "xapp-1-A0B1C2D3E4-1234567890-" + "a1" * 10,
    "aws session key": "ASIA" + "QRSTUVWXYZ012345",
    "slack webhook": "https://hooks.slack.com/services/T00000000/B00000000/" + "X" * 24,
}
# JSON / quoted-key lines (transcripts are JSONL): line -> secret value that must disappear.
QUOTED = {
    '{"token": "s3cretTokenValue"}': "s3cretTokenValue",
    '{"password":"hunter2json"}': "hunter2json",
    "{'secret': 'singleQuotedVal'}": "singleQuotedVal",
}
BENIGN = "task-" + "a" * 30
BENIGN_WORD = "Asiapacificregionalhub"


def check(name: str, ok: bool) -> None:
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
    if not ok:
        FAILURES.append(name)


def bash_blocks(text: str) -> list[str]:
    return re.findall(r"^\s*```bash\n(.*?)^\s*```", text, re.S | re.M)


def scratchpad_case(block: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp, "repo").resolve()
        inner_tmp = repo / "tmp"
        inner_tmp.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        env = {**os.environ, "TMPDIR": str(inner_tmp)}
        done = subprocess.run(["bash", "-c", block], cwd=repo, env=env, capture_output=True, text=True)
        run = Path(done.stdout.strip().splitlines()[-1]) if done.stdout.strip() else None
        # Fails if the inside-repository fallback is removed: the scratchpad would sit in the repo.
        check("scratchpad created", done.returncode == 0 and run is not None and run.is_dir())
        if run is None or not run.is_dir():
            return
        try:
            check("scratchpad outside the repository", not str(run.resolve()).startswith(str(repo) + os.sep))
            # Fails if `chmod 700` is dropped (mktemp -d alone is 0700 on most systems, so also
            # guarded textually below).
            check("scratchpad mode 0700", stat.S_IMODE(run.stat().st_mode) == 0o700)
        finally:
            run.rmdir()
    check("scratchpad block keeps chmod 700", "chmod 700" in block)


def redaction_case(block: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp)
        secrets_file = run / "judgment.md"
        secrets_file.write_text(
            "\n".join(SECRETS.values()) + "\n" + "\n".join(QUOTED)
            + f"\nbenign: {BENIGN} {BENIGN_WORD}\nCookie: session=abc\nAuthorization: Basic Zm9vOmJhcg==\n"
            "inline -----BEGIN RSA PRIVATE KEY----- AAAA -----END RSA PRIVATE KEY----- tail\n"
            "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXk\n-----END OPENSSH PRIVATE KEY-----\n"
            "after pem\n-----BEGIN EC PRIVATE KEY-----\nunterminated-body\n",
            encoding="utf-8",
        )
        next_file = run / "tooling.md"
        next_file.write_text("next file survives\n", encoding="utf-8")
        command = block.replace('"<run>"', f'"{run}"')
        done = subprocess.run(["bash", "-c", command], capture_output=True, text=True)
        check("redaction exits 0", done.returncode == 0)
        out = secrets_file.read_text(encoding="utf-8")
        # Each fails if its pattern is removed from the perl regex.
        for name, value in SECRETS.items():
            check(f"redacted: {name}", value not in out)
        for line, value in QUOTED.items():
            check(f"redacted: quoted key {line}", value not in out)
        check("redacted: cookie line", "session=abc" not in out)
        check("redacted: authorization line", "Zm9vOmJhcg" not in out)
        check("redacted: inline PEM", "AAAA" not in out and "tail" in out)
        check("redacted: multi-line PEM", "b3BlbnNzaC1rZXk" not in out and "after pem" in out)
        check("redacted: unterminated PEM to EOF", "unterminated-body" not in out)
        # Fails if the `sk-` lookbehind is dropped.
        check("benign task- word kept", BENIGN in out)
        # Fails if the AWS prefix match becomes case-insensitive.
        check("benign Asia… word kept", BENIGN_WORD in out)
        # Fails if the per-file `$pem = 0` reset at eof is dropped.
        check("PEM state reset per file", next_file.read_text(encoding="utf-8") == "next file survives\n")
        check("hits reported on stderr", "judgment.md" in done.stderr)


def main() -> int:
    if not SKILL.is_file():
        print(f"FAIL: {SKILL} is missing")
        return 1
    blocks = bash_blocks(SKILL.read_text(encoding="utf-8"))
    scratch = next((b for b in blocks if "mktemp -d" in b), None)
    redact = next((b for b in blocks if "perl" in b), None)
    check("scratchpad block present", scratch is not None)
    check("redaction block present", redact is not None)
    if scratch:
        scratchpad_case(scratch)
    if redact:
        redaction_case(redact)
    if FAILURES:
        print(f"{len(FAILURES)} failure(s)", file=sys.stderr)
        return 1
    print("all retro safety checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
