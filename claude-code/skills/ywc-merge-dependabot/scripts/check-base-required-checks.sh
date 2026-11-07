#!/usr/bin/env bash
# check-base-required-checks.sh <pr-number>
#
# Parallel-auto prerequisite (Mode Selection): confirms that the PR's base
# branch has at least one REQUIRED status check, so `gh pr merge --auto`
# waits for CI instead of merging an already-mergeable PR immediately.
#
# `baseRefName` is set by the remote and is treated as hostile input: it is
# read here (never pasted into a command line by the caller) and must pass
# `^[A-Za-z0-9._/-]+$`, no leading `-`, no `..`, not `HEAD`, and
# `git check-ref-format "refs/heads/$base"` before it reaches any `gh api` path.
# It is only ever used as a quoted variable.
#
# stdout (last line): CONFIRMED=<0|1> BASE=<validated base, or empty>
#
# Exit codes:
#   0  confirmed — the PR may join the `--auto` queue
#   1  cannot confirm (unreadable or invalid base, gh failure, zero required
#      checks) — exclude the PR from `--auto`, handle it in the sequential pass
#   2  usage error

set -euo pipefail

[ $# -eq 1 ] && [[ "$1" =~ ^[0-9]+$ ]] || { echo "usage: check-base-required-checks.sh <pr-number>" >&2; exit 2; }
PR="$1"

cannot_confirm() {
  echo "cannot confirm a required status check for PR $PR: $1" >&2
  echo "CONFIRMED=0 BASE=$2"
  exit 1
}

base="$(gh pr view "$PR" --json baseRefName --jq .baseRefName 2>/dev/null)" || base=""
# The leading-dash test runs before git so the value can never be read as an option.
if [ -z "$base" ] || [[ ! "$base" =~ ^[A-Za-z0-9._/-]+$ ]] || [[ "$base" == -* ]] \
   || [[ "$base" == *..* ]] || [ "$base" = HEAD ] || ! git check-ref-format "refs/heads/$base" >/dev/null 2>&1; then
  cannot_confirm "baseRefName is unreadable or not a safe branch name" ""
fi

# Prints nothing; succeeds only when the query returns an integer greater than 0.
positive_count() {
  local n
  n="$(gh api "$1" --jq "$2" 2>/dev/null)" || return 1
  [[ "$n" =~ ^[0-9]+$ ]] && [ "$n" -gt 0 ]
}

if positive_count "repos/{owner}/{repo}/branches/$base/protection/required_status_checks" \
     '(.contexts | length) + (.checks | length)' \
   || positive_count "repos/{owner}/{repo}/rules/branches/$base" \
     '[.[] | select(.type == "required_status_checks")] | length'; then
  echo "CONFIRMED=1 BASE=$base"
  exit 0
fi
cannot_confirm "no required status check found on $base (or the lookup failed)" "$base"
