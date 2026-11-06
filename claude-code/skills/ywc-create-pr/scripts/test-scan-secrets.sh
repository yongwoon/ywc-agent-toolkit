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
# A failed fixture step aborts the suite: a half-built repo would let the
# exit-2 cases pass without testing anything.
g() {
  (cd "$REPO" && GIT_CEILING_DIRECTORIES="$TMP_ROOT" no_git_env git -c user.name=t -c user.email=t@example.invalid "$@" >/dev/null 2>&1) \
    || { echo "FIXTURE FAIL: git $*" >&2; exit 1; }
}
g init -q -b main
echo clean > "$REPO/a.txt"; g add a.txt; g commit -q -m base
g checkout -q -b clean-feat
echo "still clean" >> "$REPO/a.txt"; g commit -q -am clean
g checkout -q -b feat main
echo "key=AKIA""ABCDEFGHIJKLMNOP" > "$REPO/b.txt"; g add b.txt; g commit -q -m secret

# The three guards (allowlist, rev-parse --verify, checked diff) back each
# other up, so each is isolated with a `git` shim on PATH:
#   SHIM_MODE=faildiff  — only the Phase 3 `git diff <base>...HEAD` fails
#   SHIM_MODE=passdiff  — only that diff always succeeds (empty output)
#   SHIM_MODE=passall   — `rev-parse --verify` and that diff always succeed
SHIM="$TMP_ROOT/shim"; mkdir -p "$SHIM"
REAL_GIT="$(command -v git)"
cat > "$SHIM/git" <<EOF
#!/usr/bin/env bash
case "\${SHIM_MODE:-}:\$1:\$*" in
  faildiff:diff:*...HEAD*) exit 1 ;;
  passall:diff:*...HEAD*|passdiff:diff:*...HEAD*) exit 0 ;;
  passall:rev-parse:*--verify*) exit 0 ;;
esac
exec "$REAL_GIT" "\$@"
EOF
chmod +x "$SHIM/git"

ERR="$TMP_ROOT/scan.err"
# run_committed <shim-mode> [args...] — prints the exit code; stderr kept in $ERR.
run_committed() {
  local mode="$1"; shift
  (cd "$REPO" && SHIM_MODE="$mode" PATH="$SHIM:$PATH" GIT_CEILING_DIRECTORIES="$TMP_ROOT" \
    no_git_env bash "$TARGET" --committed "$@" >/dev/null 2>"$ERR")
  echo $?
}
assert_committed() {
  local desc="$1" expected="$2"; shift 2
  local before=$FAIL
  assert_eq "$desc" "$expected" "$(run_committed "$@")"
  [ "$FAIL" -eq "$before" ] || sed 's/^/    stderr: /' "$ERR" >&2
}

# Fails if `shift 2` with a missing value exits 1 ("secrets found") under set -e.
assert_committed "--committed without a base" "2" ""
assert_committed "--committed unknown base" "2" "" no-such-branch
# Fails only if the rev-parse --verify guard is removed (passdiff diffs nothing).
assert_committed "--committed unknown base, diff succeeds" "2" passdiff no-such-branch
# Fails if Phase 3 swallows the diff error (`|| true`) again.
assert_committed "--committed diff failure" "2" faildiff main
# Each fails only if its own allowlist clause is removed (passall bypasses git).
assert_committed "--committed leading-dash base" "2" passall -x
assert_committed "--committed dot-dot base" "2" passall 'main..feat'
# shellcheck disable=SC2016  # the literal `$(id)` is the input under test
assert_committed "--committed shell-metachar base" "2" passall 'main$(id)'
# Positive cases: a resolvable base still detects (1) and still passes (0).
assert_committed "--committed secret vs valid base" "1" "" main
g checkout -q clean-feat
assert_committed "--committed clean vs valid base" "0" "" main

echo ""
echo "test-scan-secrets.sh: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
