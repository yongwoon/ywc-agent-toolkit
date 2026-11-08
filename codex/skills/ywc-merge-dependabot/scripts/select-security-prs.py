#!/usr/bin/env python3
"""
select-security-prs.py <owner/repo> < prs.json

Security scope for ywc-merge-dependabot. Reads the output of
`gh pr list --json number,title,body,files` on stdin and reads the
repository's open Dependabot alerts with `gh api`.

A PR is a security update only when an open Dependabot alert matches it:
the PR changes the alert's manifest file, and the alert's package name
appears in the PR title (or, for a grouped PR, its body). PR text alone never
makes a PR a security update, because the body embeds upstream release notes
that can mention any CVE, GHSA or package.

Output: one line of JSON on stdout.

  {"security": [101], "other": [102], "advisories": {"101": ["GHSA-xxxx-xxxx-xxxx"]}}

Exit codes:
  0  Classified
  1  Bad arguments or input
  2  Alerts could not be read (Dependabot alerts disabled, the token cannot
     read them, `gh` is missing or timed out, or a row is malformed).
     stdout is {"unresolved": [<every PR>], "error": "..."}
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

GH_TIMEOUT_SECONDS = 60
GROUP_TITLE = re.compile(r"\bgroup\b", re.IGNORECASE)
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ALERT_FIELDS = ".[] | [.dependency.package.name, .dependency.manifest_path, .security_advisory.ghsa_id] | @json"


def mentions(text: str, name: str) -> bool:
    """True when `name` appears as a whole package name, so `lodash` does not match `lodash.merge`."""
    pattern = r"(?<![\w.@/-])" + re.escape(name) + r"(?![\w@/-]|\.\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def searchable_text(pr: dict) -> str:
    """A single-package PR names its package in the title; only a grouped PR lists packages in the body.

    The body of a single-package PR embeds upstream release notes, which can name any other package.
    """
    title = pr.get("title") or ""
    return f"{title}\n{pr.get('body') or ''}" if GROUP_TITLE.search(title) else title


def parse_alert_row(line: str) -> tuple[str, str, str]:
    row = json.loads(line)
    if not (isinstance(row, list) and len(row) == 3 and all(isinstance(v, str) and v for v in row)):
        raise RuntimeError(f"unexpected alert row: {line[:80]}")
    return row[0], row[1], row[2]


def read_alerts(repo: str) -> list[tuple[str, str, str]]:
    try:
        result = subprocess.run(
            ["gh", "api", "--paginate", f"repos/{repo}/dependabot/alerts?state=open&per_page=100", "--jq", ALERT_FIELDS],
            capture_output=True, text=True, timeout=GH_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(f"gh api failed: {exc}") from exc
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh api exited {result.returncode}")
    return [parse_alert_row(line) for line in result.stdout.splitlines() if line.strip()]


def classify(prs: list[dict], alerts: list[tuple[str, str, str]]) -> dict:
    security, other, advisories = [], [], {}
    for pr in prs:
        paths = {f["path"] for f in pr.get("files") or []}
        text = searchable_text(pr)
        ids = sorted({ghsa for name, manifest, ghsa in alerts if manifest in paths and mentions(text, name)})
        if ids:
            security.append(pr["number"])
            advisories[str(pr["number"])] = ids
        else:
            other.append(pr["number"])
    return {"security": sorted(security), "other": sorted(other), "advisories": advisories}


def main() -> int:
    if len(sys.argv) != 2 or not REPO.match(sys.argv[1]):
        print("usage: select-security-prs.py <owner/repo> < prs.json", file=sys.stderr)
        return 1
    try:
        prs = json.load(sys.stdin)
        numbers = [int(pr["number"]) for pr in prs]
    except (ValueError, KeyError, TypeError) as exc:
        print(f"invalid PR list: {exc}", file=sys.stderr)
        return 1
    try:
        alerts = read_alerts(sys.argv[1])
    except (RuntimeError, ValueError) as exc:
        print(json.dumps({"unresolved": sorted(numbers), "error": str(exc)}))
        return 2
    print(json.dumps(classify(prs, alerts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
