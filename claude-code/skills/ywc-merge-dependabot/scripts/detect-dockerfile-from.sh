#!/usr/bin/env bash
# detect-dockerfile-from.sh <pr-number>
#
# Decides whether a Dependabot PR changes a `FROM` line inside a Dockerfile.
# The `FROM` line is matched only inside the hunks of a changed `Dockerfile*` /
# `*.dockerfile` file — a `FROM` added to a README or shell file never counts.
# The patch is fetched first so a `gh` failure is reported as unresolved,
# never mistaken for "no match".
#
# Exit codes:
#   0  FROM change in a Dockerfile → `Skipped (Dockerfile)`
#   1  no Dockerfile FROM change
#   2  usage error
#   3  unresolved — `gh pr diff` failed; never treat as "no change"

set -euo pipefail

[ $# -eq 1 ] && [[ "$1" =~ ^[0-9]+$ ]] || { echo "usage: detect-dockerfile-from.sh <pr-number>" >&2; exit 2; }

if ! patch="$(gh pr diff "$1")"; then
  echo "UNRESOLVED: gh pr diff $1 failed" >&2
  exit 3
fi

printf '%s\n' "$patch" | awk '
  /^diff --git /{ p = $0; sub(/^.* b\//, "", p)   # the b/ path; field splitting would cut paths with spaces
                  df = (p ~ /(^|\/)(Dockerfile[^\/]*|[^\/]*\.dockerfile)$/) }
  df && /^[+-][[:space:]]*FROM[[:space:]]/{ found=1 }
  END{ exit !found }'
