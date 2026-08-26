#!/usr/bin/env bash
# Fixture suite for initials-scoped PHASE allocation in next-task-number.sh.
#
# Covers AC3 (legacy seed), AC4 (other-initials entries ignored), AC5 (linked
# worktree union + path normalization), AC11 (atomic git-ref reservation),
# AC12 (initials advisory list), and the A3 drift-scoping rule. Every fixture
# runs inside a throwaway scratch repository so reservation refs never touch
# the real repository's ledger.
set -euo pipefail

skill_dir="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
script="$skill_dir/scripts/next-task-number.sh"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/next-task-number-test.XXXXXX")"
# NOTE: deliberately NOT normalized with `pwd -P`. Doing so hid the symlinked-cwd
# bug (the union silently switched off) from this entire suite, because macOS
# $TMPDIR is itself a symlink. The symlink fixture at the end depends on this.
trap 'rm -rf "$tmpdir"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

# Scratch repository with exactly one commit so HEAD resolves. Built with
# plumbing (hash-object + commit-tree) so no working tree or identity config
# is required.
scratch_repo() {
  local repo="$tmpdir/$1" tree obj
  mkdir -p "$repo"
  git -C "$repo" init -q -b main >/dev/null 2>&1
  tree="$(git -C "$repo" hash-object -w -t tree /dev/null)"
  obj="$(GIT_AUTHOR_NAME=Test GIT_AUTHOR_EMAIL=t@example.com \
    GIT_COMMITTER_NAME=Test GIT_COMMITTER_EMAIL=t@example.com \
    git -C "$repo" commit-tree "$tree" -m init)"
  git -C "$repo" update-ref refs/heads/main "$obj"
  printf '%s\n' "$repo"
}

# --- AC3: legacy-only tree seeds from legacy max + 1 -------------------------
repo="$(scratch_repo ac3)"
mkdir -p "$repo/tasks/completed/000007-010-db-legacy" "$repo/tasks/000006-010-api-legacy"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000008-010" ] || fail "AC3 legacy seed returned '$out', expected 000008-010"

# A single entry carrying the resolved prefix disables the seed rule.
mkdir -p "$repo/tasks/yk-000002-010-db-first"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000003-010" ] || fail "AC3b prefixed entry did not disable the legacy seed (got '$out')"

# --- AC4: other collaborators' prefixes are out of scope ---------------------
repo="$(scratch_repo ac4)"
mkdir -p "$repo/tasks/completed/ab-000050-010-db-x"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000001-010" ] || fail "AC4 'ab-' entry leaked into yk numbering (got '$out')"

# ab- must neither raise the yk maximum nor satisfy the legacy seed rule.
mkdir -p "$repo/tasks/yk-000003-010-db-y"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000004-010" ] || fail "AC4 mixed-prefix scan returned '$out', expected 000004-010"

# --- AC5: linked worktree union ---------------------------------------------
repo="$(scratch_repo ac5)"
mkdir -p "$repo/tasks"
git -C "$repo" worktree add -q -b side "$tmpdir/ac5-side" >/dev/null 2>&1
side="$(CDPATH='' cd -- "$tmpdir/ac5-side" && pwd -P)"
mkdir -p "$side/tasks/completed/yk-000012-010-db-x"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000013-010" ] || fail "AC5 worktree union returned '$out', expected 000013-010"

# An absolute tasks-dir must be relativized before the worktree join (A6).
out="$(cd "$repo" && bash "$script" "$repo/tasks" yk 2>/dev/null)"
[ "$out" = "000014-010" ] || fail "AC5 absolute tasks-dir union returned '$out', expected 000014-010"

# A tasks-dir outside the repository skips the union entirely (A6).
mkdir -p "$tmpdir/outside/tasks"
out="$(cd "$repo" && bash "$script" "$tmpdir/outside/tasks" yk 2>/dev/null)"
[ "$out" = "000001-010" ] || fail "AC5 out-of-repo tasks-dir did not skip the union (got '$out')"

git -C "$repo" worktree remove --force "$side" >/dev/null 2>&1
[ ! -d "$side" ] || fail "AC5 throwaway worktree was not removed"

# --- AC11: reservation is an atomic create-if-absent CAS ---------------------
repo="$(scratch_repo ac11)"
branches_before="$(git -C "$repo" branch -a)"
git -C "$repo" update-ref refs/ywc/task-phase/yk/000099 HEAD '' \
  || fail "AC11 first update-ref failed, expected exit 0"
set +e
git -C "$repo" update-ref refs/ywc/task-phase/yk/000099 HEAD '' 2>/dev/null
repeat_status=$?
set -e
[ "$repeat_status" -ne 0 ] || fail "AC11 repeated update-ref succeeded, expected non-zero"
[ "$(git -C "$repo" branch -a)" = "$branches_before" ] || fail "AC11 reservation polluted the branch list"

# A reserved (burned) PHASE must push the next allocation to N+1.
mkdir -p "$repo/tasks"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000001-010" ] || fail "AC11 first allocation returned '$out', expected 000001-010"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000002-010" ] || fail "AC11 burned PHASE was reused (got '$out')"

# --- AC12: initials advisory list -------------------------------------------
repo="$(scratch_repo ac12)"
mkdir -p "$repo/tasks"
out="$(cd "$repo" && bash "$script" tasks --list-initials)"
[ -z "$out" ] || fail "AC12 empty tree reported prefixes: '$out'"
mkdir -p "$repo/tasks/yk-000001-010-db-x" "$repo/tasks/completed/yk-000002-010-api-y" \
  "$repo/tasks/completed/ab-000005-010-db-z" "$repo/tasks/completed/000009-010-db-legacy"
out="$(cd "$repo" && bash "$script" tasks --list-initials)"
[ "$(printf '%s\n' "$out" | grep -c '^yk 2$')" -eq 1 ] || fail "AC12 expected 'yk 2', got: $out"
[ "$(printf '%s\n' "$out" | grep -c '^ab 1$')" -eq 1 ] || fail "AC12 expected 'ab 1', got: $out"
[ "$(printf '%s\n' "$out" | wc -l | tr -d '[:space:]')" -eq 2 ] || fail "AC12 legacy entry leaked into the list: $out"

# --- Drift cross-check scoping (spec A3) ------------------------------------
repo="$(scratch_repo drift)"
mkdir -p "$repo/tasks/completed/000007-010-db-legacy"
cat > "$repo/tasks/dependency-graph.md" <<'GRAPH'
# Dependency Graph

## Phase 000007

- `000007-010-db-legacy` — done
GRAPH
(cd "$repo" && bash "$script" tasks yk >/dev/null 2>"$tmpdir/drift.err")
[ ! -s "$tmpdir/drift.err" ] \
  || fail "drift warning emitted for a graph with zero yk entries: $(cat "$tmpdir/drift.err")"

# The unscoped legacy path must still warn on a real drift.
mkdir -p "$repo/tasks/completed/000009-010-db-legacy"
(cd "$repo" && bash "$script" tasks >/dev/null 2>"$tmpdir/drift-legacy.err")
[ -s "$tmpdir/drift-legacy.err" ] || fail "legacy drift check unexpectedly silent"

# --- Invalid initials rejected ----------------------------------------------
set +e
(cd "$repo" && bash "$script" tasks TOOLONG) > "$tmpdir/invalid.log" 2>&1
invalid_status=$?
set -e
[ "$invalid_status" -eq 1 ] || fail "invalid initials accepted (exit $invalid_status)"
grep -q 'invalid initials' "$tmpdir/invalid.log" || fail "no invalid-initials error message"


# --- Legacy seed with a FOREIGN prefix present (contract: neither satisfies ---
# nor disables). Without this, AC4's fixture has no legacy entry, so the seed
# rule could not have fired either way and its assertion is vacuous.
repo="$(scratch_repo seed_foreign)"
mkdir -p "$repo/tasks/000007-010-db-legacy" "$repo/tasks/ab-000050-010-db-x"
out="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"
[ "$out" = "000008-010" ] \
  || fail "foreign prefix broke the legacy seed: got '$out', expected 000008-010"

# --- A symlinked cwd must not disable the worktree union --------------------
# `git rev-parse --show-toplevel` is physical, so a logical `pwd` through a
# symlink made the path compare as "outside the repository" and skipped the
# union — returning a LOW number, i.e. failing open into the exact cross-worktree
# collision this scan prevents. Each run reserves its phase, so the two probes
# need independent repositories.
repo="$(scratch_repo symlink_a)"
mkdir -p "$repo/tasks"
git -C "$repo" worktree add -q -b sym_a "$tmpdir/symlink-a-side" >/dev/null 2>&1
mkdir -p "$tmpdir/symlink-a-side/tasks/yk-000012-010-db-x"
direct="$(cd "$repo" && bash "$script" tasks yk 2>/dev/null)"

repo="$(scratch_repo symlink_b)"
mkdir -p "$repo/tasks"
git -C "$repo" worktree add -q -b sym_b "$tmpdir/symlink-b-side" >/dev/null 2>&1
mkdir -p "$tmpdir/symlink-b-side/tasks/yk-000012-010-db-x"
ln -s symlink_b "$tmpdir/symlink-link"
through="$(cd "$tmpdir/symlink-link" && bash "$script" tasks yk 2>/dev/null)"

[ "$direct" = "000013-010" ] \
  || fail "symlink baseline: direct run returned '$direct', expected 000013-010"
[ "$through" = "$direct" ] \
  || fail "symlinked cwd disabled the union: got '$through', expected '$direct'"

echo "PASS: next-task-number.sh initials fixtures"
