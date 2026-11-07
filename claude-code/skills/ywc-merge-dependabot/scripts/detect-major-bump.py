#!/usr/bin/env python3
"""
detect-major-bump.py --title "<dependabot PR title>"
detect-major-bump.py           (reads "<number>\\t<title>" or "<title>" lines from stdin)

Decides whether a Dependabot PR is a MAJOR version bump — the gate that
ywc-merge-dependabot Step 2 uses to skip a PR for human review. The judgement
is deterministic, so it lives in a script rather than in LLM arithmetic: an
LLM routinely mis-calls the subtle 0.x case (0.2.0 -> 0.3.0 IS breaking,
1.2.0 -> 1.3.0 is NOT), and a wrong call here merges a breaking change to main.

Rule — "the leftmost non-zero version segment changed":
  1.2.3 -> 2.0.0   major   (major segment 1->2)
  1.2.3 -> 1.3.0   minor   (leftmost non-zero 1 unchanged)
  0.2.0 -> 0.3.0   major   (leftmost non-zero is the 2, and 2->3)
  0.2.0 -> 0.2.5   minor   (leftmost non-zero 0.2 unchanged)
  0.9.0 -> 1.0.0   major
  0.0.3 -> 0.0.4   major   (conservative under 0.0.x: every release may break)

Titles that do not yield two comparable semver versions (group updates,
git-sha action bumps, unparseable strings) are returned with
`major_bump: null` and a reason so the LLM can decide.

Output: one JSON object per input, single line each (NDJSON), to stdout.

  {"number": 130, "name": "webpack", "from": "4.46.0", "to": "5.90.0",
   "major_bump": true, "reason": "major segment 4 -> 5"}

Exit codes:
  0  At least one input processed (per-line major_bump may be null)
  1  No input provided
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# "Bump X from A to B", optionally prefixed by a conventional-commit scope
# (e.g. "build(deps): bump axios from 1.6.0 to 1.7.2"). Case-insensitive.
BUMP_RE = re.compile(
    r"\bbump\s+(?P<name>\S+)\s+from\s+(?P<from>\S+)\s+to\s+(?P<to>\S+)",
    re.IGNORECASE,
)
# A semver-ish version: digits and dots, optional leading v, optional -prerelease.
VERSION_RE = re.compile(r"^v?(?P<core>\d+(?:\.\d+)*)(?P<pre>[-+].*)?$")


def parse_core(version: str) -> list[int] | None:
    """Return the numeric segments of a version, or None if it is not semver-ish."""
    match = VERSION_RE.match(version.strip())
    if not match:
        return None
    return [int(seg) for seg in match.group("core").split(".")]


def leftmost_nonzero_index(parts: list[int]) -> int:
    for index, value in enumerate(parts):
        if value != 0:
            return index
    return len(parts) - 1  # all-zero version → compare the last segment


def classify(from_v: str, to_v: str) -> tuple[bool | None, str]:
    """Return (is_major_bump, reason). is_major_bump is None when undecidable."""
    from_parts = parse_core(from_v)
    to_parts = parse_core(to_v)
    if from_parts is None or to_parts is None:
        return None, f"unparseable version(s): {from_v!r} -> {to_v!r}"

    # Pad to equal length so index comparison is well-defined (1.2 vs 1.2.0).
    width = max(len(from_parts), len(to_parts))
    from_parts += [0] * (width - len(from_parts))
    to_parts += [0] * (width - len(to_parts))

    pivot = min(leftmost_nonzero_index(from_parts), leftmost_nonzero_index(to_parts))
    if from_parts[: pivot + 1] != to_parts[: pivot + 1]:
        return True, (
            f"leftmost non-zero segment changed at index {pivot}: "
            f"{'.'.join(map(str, from_parts))} -> {'.'.join(map(str, to_parts))}"
        )
    return False, "leftmost non-zero segment unchanged"


def process(title: str, number: int | None) -> dict[str, object]:
    record: dict[str, object] = {"number": number, "title": title}
    match = BUMP_RE.search(title)
    if not match:
        record.update(major_bump=None, reason="no 'bump X from A to B' pattern found")
        return record
    name, from_v, to_v = match.group("name"), match.group("from"), match.group("to")
    is_major, reason = classify(from_v, to_v)
    record.update(name=name, **{"from": from_v}, to=to_v, major_bump=is_major, reason=reason)
    return record


def read_inputs(title_arg: str | None) -> list[tuple[int | None, str]]:
    if title_arg is not None:
        return [(None, title_arg)]
    if sys.stdin.isatty():
        return []
    inputs: list[tuple[int | None, str]] = []
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        if "\t" in line:
            num_str, _, title = line.partition("\t")
            number = int(num_str) if num_str.strip().lstrip("#").isdigit() else None
            inputs.append((number, title))
        else:
            inputs.append((None, line))
    return inputs


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Detect Dependabot major version bumps")
    parser.add_argument("--title", help="A single PR title to classify")
    args = parser.parse_args(argv[1:])

    inputs = read_inputs(args.title)
    if not inputs:
        print(
            "usage: detect-major-bump.py --title \"Bump X from A to B\"   "
            "(or pipe '<number>\\t<title>' lines on stdin)",
            file=sys.stderr,
        )
        return 1

    for number, title in inputs:
        print(json.dumps(process(title, number), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
