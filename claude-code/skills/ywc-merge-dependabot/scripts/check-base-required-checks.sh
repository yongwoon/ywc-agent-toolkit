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
#   1  validated base with zero required checks (a lookup answering HTTP 404 —
#      branch not protected / no rulesets — counts as zero), or an unreadable or
#      invalid base (empty BASE=) — exclude the PR from `--auto`
#   2  usage error
#   3  unresolved — a lookup failed (403, rate limit, other gh error) or returned a
#      non-integer, and no lookup confirmed a required check; nothing is confirmed
#      or denied — exclude the PR from `--auto`, never treat it as zero checks

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

# ponytail: a 404 caused by missing permission looks like "not protected"; the caller's
# all-checks fallback still gates such a PR on every check.
# Prints the required-check count; HTTP 404 is a count of 0. Fails when gh fails any
# other way or the output (stderr included, so a stray warning is never trusted) is
# not an integer.
required_count() {
  local out
  if out="$(gh api "$1" --jq "$2" 2>&1)"; then
    [[ "$out" =~ ^[0-9]+$ ]] || return 1
    echo "$out"
  elif [[ "$out" == *"(HTTP 404)"* ]]; then
    echo 0
  else
    return 1
  fi
}

# Exits 0 on a positive count; records a failed lookup so zero is never inferred from it.
unresolved=0
check_lookup() {
  local n
  if ! n="$(required_count "$1" "$2")"; then
    unresolved=1
  elif [ "$n" -gt 0 ]; then
    echo "CONFIRMED=1 BASE=$base"
    exit 0
  fi
}
check_lookup "repos/{owner}/{repo}/branches/$base/protection/required_status_checks" \
  '(.contexts | length) + (.checks | length)'
check_lookup "repos/{owner}/{repo}/rules/branches/$base" \
  '[.[] | select(.type == "required_status_checks")] | length'
if [ "$unresolved" -eq 1 ]; then
  echo "required status checks on $base are unresolved for PR $PR: a lookup failed or returned unparseable output" >&2
  echo "CONFIRMED=0 BASE=$base"
  exit 3
fi
cannot_confirm "no required status check found on $base" "$base"
