#!/usr/bin/env bash
# Assertions for resolve-initials.sh covering AC4-AC5 from
# tasks/yw-000012-030-infra-resolve-initials-script/task.md.
#
# Each case runs the script inside an isolated temp git repo with an
# isolated global/system config, so results never depend on the machine's
# real ~/.gitconfig identity.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOLVE="$SCRIPT_DIR/resolve-initials.sh"

FAILURES=0

# assert_case <label> <expected_stdout> <email-or-empty> [extra script args...]
assert_case() {
  local label="$1" expected="$2" email="$3"
  shift 3

  local tmp actual status
  tmp="$(mktemp -d)"

  export GIT_CONFIG_GLOBAL="$tmp/gitconfig-empty"
  export GIT_CONFIG_SYSTEM="$tmp/gitconfig-empty"
  : > "$GIT_CONFIG_GLOBAL"

  git init -q "$tmp/repo"
  if [ -n "$email" ]; then
    git -C "$tmp/repo" config user.email "$email"
  fi

  set +e
  actual="$(cd "$tmp/repo" && bash "$RESOLVE" "$@")"
  status=$?
  set -e

  unset GIT_CONFIG_GLOBAL GIT_CONFIG_SYSTEM
  rm -rf "$tmp"

  if [ "$status" -ne 0 ]; then
    echo "FAIL [$label]: exit code $status, expected 0" >&2
    FAILURES=$((FAILURES + 1))
    return
  fi
  if [ "$actual" != "$expected" ]; then
    echo "FAIL [$label]: got '$actual', expected '$expected'" >&2
    FAILURES=$((FAILURES + 1))
    return
  fi
  echo "PASS [$label]"
}

# AC4: no flag, no CLAUDE.md section, user.email = yongwoon.kim@example.com
#      -> NEEDS_CONFIRM yk, exit 0.
assert_case "AC4: derive from email" \
  "NEEDS_CONFIRM yk" "yongwoon.kim@example.com"

# AC5: no flag, no CLAUDE.md section, no resolvable git identity -> NONE, exit 0.
assert_case "AC5: no resolvable identity" \
  "NONE" ""

# Extra coverage: rung 1 explicit valid flag wins outright.
assert_case "flag: valid --initials wins" \
  "RESOLVED yk" "" --initials yk

# Extra coverage: an invalid flag falls through to derivation instead of
# erroring (this script never exits non-zero).
assert_case "flag: invalid --initials falls through to derivation" \
  "NEEDS_CONFIRM yk" "yongwoon.kim@example.com" --initials TOOLONG5

# Regression: --initials as the very last argv token (no value following)
# must not crash under `set -e` -- it falls through to derivation like any
# other unsatisfied rung-1 attempt.
assert_case "flag: dangling --initials (no value) falls through" \
  "NEEDS_CONFIRM yk" "yongwoon.kim@example.com" --initials

# E6: a single-segment local-part whose first-char join is < 2 chars falls
# back to the first 2-4 lowercase alphanumeric characters of the source.
assert_case "E6: sub-2-char join falls back to alnum prefix" \
  "NEEDS_CONFIRM ab" "ab@example.com"

# E5: user.email unset, user.name set -- derive from name instead.
assert_case_name() {
  local label="$1" expected="$2" name="$3"
  local tmp actual status

  tmp="$(mktemp -d)"
  export GIT_CONFIG_GLOBAL="$tmp/gitconfig-empty"
  export GIT_CONFIG_SYSTEM="$tmp/gitconfig-empty"
  : > "$GIT_CONFIG_GLOBAL"

  git init -q "$tmp/repo"
  git -C "$tmp/repo" config user.name "$name"

  set +e
  actual="$(cd "$tmp/repo" && bash "$RESOLVE")"
  status=$?
  set -e

  unset GIT_CONFIG_GLOBAL GIT_CONFIG_SYSTEM
  rm -rf "$tmp"

  if [ "$status" -ne 0 ]; then
    echo "FAIL [$label]: exit code $status, expected 0" >&2
    FAILURES=$((FAILURES + 1))
    return
  fi
  if [ "$actual" != "$expected" ]; then
    echo "FAIL [$label]: got '$actual', expected '$expected'" >&2
    FAILURES=$((FAILURES + 1))
    return
  fi
  echo "PASS [$label]"
}
assert_case_name "E5: derive from user.name when email unset" \
  "NEEDS_CONFIRM as" "alice.smith"

if [ "$FAILURES" -gt 0 ]; then
  echo "$FAILURES case(s) failed" >&2
  exit 1
fi

echo "all cases passed"
exit 0
