#!/usr/bin/env bash
# test-scan-secrets.sh — assert-based, no framework.
# Checks that scan-secrets.sh never reports "clean" when it could not scan:
# outside a git work tree and in a bare repository it must exit 2, and an
# unresolved script path must surface as a non-0/1 exit the caller reads as
# BLOCKED.
#
# Every git and scan call runs through no_git_env: the pre-commit hook runs
# scripts/validate.sh with GIT_DIR / GIT_INDEX_FILE / GIT_WORK_TREE set, and an
# inherited GIT_DIR would point these checks at the hook's repository.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/scan-secrets.sh"

PASS=0
FAIL=0

# Every throwaway directory lives under TMP_ROOT, removed on any exit.
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

no_git_env() {
  env -u GIT_DIR -u GIT_INDEX_FILE -u GIT_WORK_TREE "$@"
}

assert_eq() {
  local desc="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
    echo "FAIL: $desc — expected [$expected], got [$actual]" >&2
  fi
}

# Runs the scan from directory $1; GIT_CEILING_DIRECTORIES stops git from
# discovering a repository above TMP_ROOT (e.g. when TMPDIR is inside one).
run_scan() {
  (cd "$1" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env bash "$TARGET" --staged >/dev/null 2>&1)
  echo $?
}

# Fails if the not-a-work-tree guard is removed: every git call errors
# silently and the scan reports "OK" with exit 0.
NOREPO="$(mktemp -d "$TMP_ROOT/norepo.XXXXXX")"
assert_eq "outside a git work tree" "2" "$(run_scan "$NOREPO")"

# Fails if the guard only checks rev-parse's exit status: in a bare repo it
# exits 0 but prints "false".
BARE="$(mktemp -d "$TMP_ROOT/bare.XXXXXX")"
no_git_env git init -q --bare "$BARE/r.git"
assert_eq "bare repository" "2" "$(run_scan "$BARE/r.git")"

# Fails if callers could mistake an unresolved script path for a scan result:
# bash must exit 127 (not 0/1), which SKILL.md treats as BLOCKED. A nonexistent
# directory under TMP_ROOT stands in for the unresolved variable — an empty one
# would expand to /scan-secrets.sh, which depends on the host root.
UNRESOLVED="$TMP_ROOT/unresolved-skill-dir"
assert_eq "unresolved script path" "127" "$( (no_git_env bash "$UNRESOLVED/scan-secrets.sh" --staged >/dev/null 2>&1); echo $?)"

# --committed <base>: a base that cannot be scanned must exit 2, never "OK".
# Fixture: main has a clean commit; branch "feat" adds an AWS-key-shaped line
# (assembled at runtime so this file itself never contains the pattern).
REPO="$(mktemp -d "$TMP_ROOT/repo.XXXXXX")"
g() { (cd "$REPO" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env git -c user.name=t -c user.email=t@example.invalid "$@" >/dev/null 2>&1); }
g init -q -b main
echo clean > "$REPO/a.txt"; g add a.txt; g commit -q -m base
g checkout -q -b clean-feat
echo "still clean" >> "$REPO/a.txt"; g commit -q -am clean
g checkout -q -b feat main
echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/b.txt"; g add b.txt; g commit -q -m secret

run_committed() {
  (cd "$REPO" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env bash "$TARGET" --committed "$1" >/dev/null 2>&1)
  echo $?
}

# Fails if Phase 3 swallows the diff error (`|| true`): the committed key is
# never seen and the scan reports OK / exit 0.
assert_eq "--committed unknown base" "2" "$(run_committed no-such-branch)"
# Fails if the base is not allowlisted: git reads it as an option.
assert_eq "--committed option-like base" "2" "$(run_committed --output=x)"
# shellcheck disable=SC2016  # the literal `$(id)` is the input under test
assert_eq "--committed shell-metachar base" "2" "$(run_committed 'main$(id)')"
assert_eq "--committed dot-dot base" "2" "$(run_committed 'main..feat')"
# Positive cases: a resolvable base still detects (1) and still passes (0).
assert_eq "--committed secret vs valid base" "1" "$(run_committed main)"
g checkout -q clean-feat
assert_eq "--committed clean vs valid base" "0" "$(run_committed main)"

echo ""
echo "test-scan-secrets.sh: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
