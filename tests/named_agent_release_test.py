#!/usr/bin/env python3
"""Gate: every batch-dispatch callout must carry its Release clause.

A named subagent stays `idle` after finishing until it is stopped, so a SKILL.md
that dispatches a concurrent batch must tell the orchestrator to `TaskStop` each
lane. The shared reference alone is not enough (it is rarely read mid-run), so the
clause has to live on the callout line in the SKILL.md body.

Rule: in every `claude-code/skills/*/SKILL.md`, EACH physical line that matches
`Action required.*subagent-async-monitoring\\.md` must also match
`Release.*TaskStop`. Checking per line (not per file) catches a second batch in the
same skill (impl-review Step 4.5, spec-validate Council) that omits Release. A
callout wrapped so `Action required` and the link sit on different lines (same
blank-line-delimited block) is reported as a violation too.

Known limit (FM-2, accepted): a skill that cites the contract only in prose, with
no `Action required` callout, is treated as a single dispatch and is not bound.
A new fan-out skill must use the callout form to be covered.

stdlib only, offline.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "claude-code/skills"

CALLOUT = re.compile(r"Action required.*subagent-async-monitoring\.md")
RELEASE = re.compile(r"Release.*TaskStop")

LINK = (
    "[../references/subagent-async-monitoring.md]"
    "(../references/subagent-async-monitoring.md)"
)
CALLOUT_ONLY = f"> **Action required**: Read {LINK} now — one batch.\n"
RELEASE_CLAUSE = " **Release (mechanical gate)**: call `TaskStop` once per lane.\n"
PROSE_CITE = f"For the contract see {LINK}.\n"


def paragraphs(text: str) -> list[list[tuple[int, str]]]:
    """Split text into blank-line separated blocks of (line number, line)."""
    blocks: list[list[tuple[int, str]]] = [[]]
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip():
            blocks[-1].append((number, line))
        elif blocks[-1]:
            blocks.append([])
    return [block for block in blocks if block]


def find_violations(skills_dir: Path) -> tuple[int, list[str]]:
    """Return (callout count, violations as `path:line`) under skills_dir."""
    callouts = 0
    violations: list[str] = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        rel = skill_md.relative_to(skills_dir.parent.parent)
        for block in paragraphs(skill_md.read_text(encoding="utf-8")):
            for index, (number, line) in enumerate(block):
                if "Action required" not in line:
                    continue
                if CALLOUT.search(line):
                    callouts += 1
                    if not RELEASE.search(line):
                        violations.append(f"{rel}:{number}")
                    continue
                # Each callout is judged on its own: join only the lines up to the next
                # `Action required`, so a wrapped callout cannot hide behind a complete one.
                tail = [line]
                for _, following in block[index + 1 :]:
                    if "Action required" in following:
                        break
                    tail.append(following)
                if CALLOUT.search(" ".join(tail)):
                    callouts += 1
                    violations.append(f"{rel}:{number} (callout wrapped across lines)")
    return callouts, violations


def run_synthetic(name: str, body: str, expected_callouts: int, expected_violations: int) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        skills = Path(tmp) / "claude-code/skills"
        target = skills / "ywc-thing/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("# Skill\n\n" + body, encoding="utf-8")
        callouts, violations = find_violations(skills)
    if (callouts, len(violations)) != (expected_callouts, expected_violations):
        print(
            f"FAIL: {name}: expected {expected_callouts} callout(s)/{expected_violations} "
            f"violation(s), got {callouts}/{len(violations)}",
            file=sys.stderr,
        )
        return False
    print(f"PASS: {name}")
    return True


def self_check() -> bool:
    cases = [
        ("callout without release is a violation", CALLOUT_ONLY, 1, 1),
        ("release on the same line passes", CALLOUT_ONLY.rstrip("\n") + RELEASE_CLAUSE, 1, 0),
        ("release on a different line is a violation", CALLOUT_ONLY + "\n" + RELEASE_CLAUSE.lstrip(), 1, 1),
        (
            "two callouts with only one release: the bare one is a violation",
            CALLOUT_ONLY.rstrip("\n") + RELEASE_CLAUSE + "\n" + CALLOUT_ONLY,
            2,
            1,
        ),
        ("prose citation is out of scope", PROSE_CITE, 0, 0),
        (
            "callout wrapped before the link is a violation",
            "> **Action required**: Read\n> " + LINK + " now — one batch." + RELEASE_CLAUSE,
            1,
            1,
        ),
        (
            "wrapped callout next to a complete one in the same block is still a violation",
            CALLOUT_ONLY.rstrip("\n")
            + RELEASE_CLAUSE
            + "> **Action required**: Read\n> "
            + LINK
            + " now — one batch."
            + RELEASE_CLAUSE,
            2,
            1,
        ),
    ]
    return all([run_synthetic(*case) for case in cases])


def main() -> int:
    ok = self_check()

    callouts, violations = find_violations(SKILLS_DIR)
    if callouts == 0:
        print(f"FAIL: no `Action required` callouts found under {SKILLS_DIR} (vacuous pass)", file=sys.stderr)
        ok = False
    for violation in violations:
        print(f"FAIL: callout without a same-line `Release … TaskStop` clause: {violation}", file=sys.stderr)
        ok = False

    if ok:
        print(f"All checks passed ({callouts} callout lines, 0 violations).")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
