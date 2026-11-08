#!/usr/bin/env python3
"""
select-security-prs.py <owner/repo> < prs.json

Security scope for ywc-merge-dependabot. Reads the output of
`gh pr list --json number,title,body,files` on stdin and reads the
repository's open Dependabot alerts with `gh api`.

A PR is a security update only when an open Dependabot alert matches it:
the PR changes the alert's manifest file, and the alert's package name
appears in the PR title or body. PR text alone never makes a PR a security
update, because the body embeds upstream release notes that can mention any
CVE or GHSA.

Output: one line of JSON on stdout.

  {"security": [101], "other": [102], "advisories": {"101": ["GHSA-xxxx-xxxx-xxxx"]}}

Exit codes:
  0  Classified
  1  Bad arguments or input
  2  Alerts could not be read (Dependabot alerts disabled, or the token
     cannot read them). stdout is {"unresolved": [<every PR>], "error": "..."}
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ALERT_FIELDS = ".[] | [.dependency.package.name, .dependency.manifest_path, .security_advisory.ghsa_id] | @json"


def mentions(text: str, name: str) -> bool:
    """True when `name` appears as a whole package name, so `lodash` does not match `lodash.merge`."""
    pattern = r"(?<![\w.@/-])" + re.escape(name) + r"(?![\w@/-]|\.\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def read_alerts(repo: str) -> list[tuple[str, str, str]]:
    result = subprocess.run(
        ["gh", "api", "--paginate", f"repos/{repo}/dependabot/alerts?state=open&per_page=100", "--jq", ALERT_FIELDS],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh api exited {result.returncode}")
    return [tuple(json.loads(line)) for line in result.stdout.splitlines() if line.strip()]


def classify(prs: list[dict], alerts: list[tuple[str, str, str]]) -> dict:
    security, other, advisories = [], [], {}
    for pr in prs:
        paths = {f["path"] for f in pr.get("files") or []}
        text = f"{pr.get('title') or ''}\n{pr.get('body') or ''}"
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
    except (RuntimeError, ValueError, TypeError) as exc:
        print(json.dumps({"unresolved": sorted(numbers), "error": str(exc)}))
        return 2
    print(json.dumps(classify(prs, alerts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
