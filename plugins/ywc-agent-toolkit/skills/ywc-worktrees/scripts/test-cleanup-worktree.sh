#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
CLEANUP="$REPO_ROOT/codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh"

TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/ywc-worktree-cleanup-test.XXXXXX")
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$TMP_DIR"
git init -q
git config user.name "Test User"
git config user.email "test@example.com"

echo "base" >README.md
git add README.md
git commit -q -m "init"

mkdir .worktrees
git worktree add -q .worktrees/sample-task -b feature/sample-task

"$CLEANUP" --keep-branch sample-task >"$TMP_DIR/keep-branch.log"

test ! -e .worktrees/sample-task
! git worktree list --porcelain | grep -Fx "worktree $TMP_DIR/.worktrees/sample-task" >/dev/null
git show-ref --verify --quiet refs/heads/feature/sample-task

git worktree add -q .worktrees/delete-task -b feature/delete-task
"$CLEANUP" delete-task >"$TMP_DIR/default-delete.log"

test ! -e .worktrees/delete-task
! git worktree list --porcelain | grep -Fx "worktree $TMP_DIR/.worktrees/delete-task" >/dev/null
! git show-ref --verify --quiet refs/heads/feature/delete-task

echo "PASS: cleanup removes worktrees and respects branch preservation mode"
