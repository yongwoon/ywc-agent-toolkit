#!/usr/bin/env python3
"""
group-by-ecosystem.py <pr> [<pr> ...]
group-by-ecosystem.py            (reads whitespace-separated PR numbers from stdin)

Classifies Dependabot PRs by the lockfile / manifest ecosystem they touch.
Used by ywc-merge-dependabot's parallel-auto mode to decide which PRs may
progress in parallel (different ecosystems → no lockfile collision) versus
which must serialize (same ecosystem → identical lockfile → race).

For each input PR, calls `gh pr view <pr> --json files` and classifies based
on file paths touched. A PR touching files from a single recognised ecosystem
joins that group; a PR touching multiple ecosystem markers (or none) goes to
"mixed" and is handled by a final sequential pass to avoid hidden conflicts.

Output: single-line JSON to stdout.

  {
    "groups": {
      "npm":            [101, 105],
      "github-actions": [102],
      "python":         [103],
      "go":             [],
      "cargo":          [],
      "maven":          [],
      "gradle":         [],
      "docker":         [],
      "mixed":          [115]
    },
    "errors": []
  }

Exit codes:
  0  Classification completed (groups may be empty; errors may be non-empty)
  1  No PR identifiers provided, or every gh call failed
"""

from __future__ import annotations

import json
import re
import subprocess
import sys


ECOSYSTEMS: dict[str, list[re.Pattern[str]]] = {
    "npm": [
        re.compile(r"(^|/)(package(-lock)?\.json|yarn\.lock|pnpm-lock\.yaml|npm-shrinkwrap\.json)$"),
    ],
    "github-actions": [
        re.compile(r"^\.github/workflows/.+\.ya?ml$"),
        re.compile(r"^\.github/actions/.+/action\.ya?ml$"),
    ],
    "python": [
        re.compile(r"(^|/)(requirements[^/]*\.txt|pyproject\.toml|poetry\.lock|uv\.lock|Pipfile(\.lock)?|setup\.py|setup\.cfg)$"),
    ],
    "go": [
        re.compile(r"(^|/)(go\.mod|go\.sum)$"),
    ],
    "cargo": [
        re.compile(r"(^|/)Cargo\.(toml|lock)$"),
    ],
    "maven": [
        re.compile(r"(^|/)pom\.xml$"),
    ],
    "gradle": [
        re.compile(r"(^|/)(build\.gradle(\.kts)?|settings\.gradle(\.kts)?|gradle/libs\.versions\.toml)$"),
    ],
    "docker": [
        re.compile(r"(^|/)(Dockerfile[^/]*|docker-compose(\.[^/]+)?\.ya?ml)$"),
    ],
}


def classify_pr(pr: str) -> tuple[set[str], str | None]:
    """Return (ecosystems_touched, error_message).

    ecosystems_touched is empty when the PR touched no recognised marker file;
    callers treat that case as "mixed" to stay on the safe side.
    """
    try:
        result = subprocess.run(
            ["gh", "pr", "view", pr, "--json", "files"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        return set(), f"PR #{pr}: gh pr view failed: {exc.stderr.strip() or exc}"
    except FileNotFoundError:
        return set(), "gh CLI not found in PATH"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return set(), f"PR #{pr}: invalid JSON from gh: {exc}"

    touched: set[str] = set()
    for entry in data.get("files") or []:
        path = entry.get("path", "")
        for ecosystem, patterns in ECOSYSTEMS.items():
            if any(pattern.search(path) for pattern in patterns):
                touched.add(ecosystem)
                break
    return touched, None


def read_pr_args(argv: list[str]) -> list[str]:
    if len(argv) >= 2:
        return argv[1:]
    if not sys.stdin.isatty():
        return [token for token in sys.stdin.read().split() if token]
    return []


def main(argv: list[str]) -> int:
    pr_args = read_pr_args(argv)
    if not pr_args:
        print(
            "usage: group-by-ecosystem.py <pr> [<pr> ...]   "
            "(or pipe whitespace-separated PR numbers on stdin)",
            file=sys.stderr,
        )
        return 1

    groups: dict[str, list[int]] = {ecosystem: [] for ecosystem in ECOSYSTEMS}
    groups["mixed"] = []
    errors: list[str] = []
    classified = 0

    for raw in pr_args:
        token = raw.lstrip("#")
        if not token.isdigit():
            errors.append(f"PR identifier '{raw}' is not numeric — skipped")
            continue
        pr_num = int(token)
        touched, error = classify_pr(str(pr_num))
        if error:
            errors.append(error)
            continue
        classified += 1
        if len(touched) == 1:
            groups[next(iter(touched))].append(pr_num)
        else:
            # No marker, or multiple markers — both are unsafe for parallel grouping.
            groups["mixed"].append(pr_num)

    payload = {"groups": groups, "errors": errors}
    print(json.dumps(payload))

    if classified == 0 and errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
