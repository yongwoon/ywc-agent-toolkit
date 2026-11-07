#!/usr/bin/env bash
# test-audit-worktrees.sh — assert-based checks for both copies of
# ywc-worktrees/scripts/audit-worktrees.sh. Throwaway repos only, no network.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COPIES=(
  "$ROOT/claude-code/skills/ywc-worktrees/scripts/audit-worktrees.sh"
  "$ROOT/codex/skills/ywc-worktrees/scripts/audit-worktrees.sh"
)
PASS=0; FAIL=0
TMP_ROOT="$(cd "$(mktemp -d)" && pwd -P)"
trap 'rm -rf "$TMP_ROOT"' EXIT

check() {
  if [ "$2" = "$3" ]; then PASS=$((PASS + 1)); else FAIL=$((FAIL + 1)); echo "FAIL: $1 — expected [$2], got [$3]" >&2; fi
}
# Hooks export GIT_DIR / GIT_INDEX_FILE; they must not leak into the fixtures.
g() { env -u GIT_DIR -u GIT_INDEX_FILE -u GIT_WORK_TREE git -c user.name=t -c user.email=t@example.invalid "$@" >/dev/null 2>&1; }

for AUDIT in "${COPIES[@]}"; do
  NAME="${AUDIT#"$ROOT"/}"
  BASE="$(mktemp -d "$TMP_ROOT/case.XXXXXX")"
  REPO="$BASE/repo"
  mkdir -p "$REPO" && g -C "$REPO" init -q -b main && g -C "$REPO" commit -q --allow-empty -m base
  mkdir -p "$REPO/.worktrees"
  run() { (cd "$REPO" && env -u GIT_DIR -u GIT_INDEX_FILE -u GIT_WORK_TREE bash "$AUDIT" "$@" >"$BASE/out" 2>&1); echo $?; }

  check "$NAME: empty .worktrees root is clean" "0" "$(run)"
  # A worktree from the legacy ../worktree-<task> convention, made before
  # .worktrees/ existed, must still be reported once .worktrees/ wins.
  g -C "$REPO" worktree add -q -b feature/pr-7 "$BASE/worktree-pr-7"
  check "$NAME: legacy ../worktree-pr-7 is reported under .worktrees" "1" "$(run)"
  check "$NAME: the report names the legacy path" "1" "$(grep -c "$BASE/worktree-pr-7" "$BASE/out")"
  check "$NAME: --expect pr-7 still fails on the legacy path" "1" "$(run --expect pr-7)"
  check "$NAME: the legacy worktree is LEAKED against --expect" "1" "$(grep -c '^LEAKED:' "$BASE/out")"
  # An unrelated sibling worktree outside both conventions stays out of scope.
  g -C "$REPO" worktree remove "$BASE/worktree-pr-7"
  g -C "$REPO" worktree add -q -b scratch "$BASE/scratch"
  check "$NAME: sibling worktree outside the conventions is ignored" "0" "$(run)"
  # A main checkout whose own name is worktree-* is not a legacy worktree.
  NAMED="$BASE/worktree-tools"
  mkdir -p "$NAMED/.worktrees" && g -C "$NAMED" init -q -b main && g -C "$NAMED" commit -q --allow-empty -m base
  check "$NAME: a repo cloned as ../worktree-tools does not report itself" "0" \
    "$( (cd "$NAMED" && env -u GIT_DIR -u GIT_INDEX_FILE -u GIT_WORK_TREE bash "$AUDIT" >"$BASE/out" 2>&1); echo $?)"
done

echo "test-audit-worktrees.sh: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
