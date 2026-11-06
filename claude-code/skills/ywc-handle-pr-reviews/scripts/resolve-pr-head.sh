#!/usr/bin/env bash
# resolve-pr-head.sh <pr-number>
#
# Resolve and validate the head branch of a same-repository, OPEN pull request
# for `ywc-handle-pr-reviews --worktree`. The head branch name is chosen by
# whoever pushed it, so it is held in a variable and validated in-process
# before it reaches any command line.
#
# stdout: the validated head branch name (only on exit 0)
# exit 0 = validated; 1 = BLOCKED (reason on stderr); 2 = usage error
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: resolve-pr-head.sh <pr-number>" >&2
  exit 2
fi

blocked() { echo "BLOCKED: $1" >&2; exit 1; }

pr="$1"
# The PR number becomes the path segment pr-<N>; check it before gh sees it.
pr_re='^[0-9]+$'
[[ "$pr" =~ $pr_re ]] || blocked "PR number must be numeric"

# @tsv escapes tab, newline and backslash inside headRefName, so a hostile
# value cannot add fields or lines; the escapes then fail the allowlist below.
if ! fields="$(gh pr view "$pr" --json headRefName,isCrossRepository,state \
    --jq '[.state, (.isCrossRepository | tojson), .headRefName] | @tsv')"; then
  blocked "gh pr view failed for PR $pr"
fi
IFS=$'\t' read -r state cross head <<<"$fields" || true

[ "$state" = "OPEN" ] || blocked "PR is ${state:-unknown}"
# Fail closed: anything but the JSON boolean false (true, null, "false").
[ "$cross" = "false" ] || blocked "--worktree does not support fork PRs"

# Whole-string allowlist first (no shell call), then git's own ref rules.
head_re='^[A-Za-z0-9._/-]+$'
if [[ ! "$head" =~ $head_re ]] || [[ "$head" == -* ]] || [[ "$head" == *..* ]]; then
  blocked "invalid head branch name"
fi
git check-ref-format "refs/heads/$head" || blocked "invalid head branch name"

printf '%s\n' "$head"
