#!/usr/bin/env bash
# cleanup-worktree.sh <task-name>
#
# Removes a parallel-executor worktree and its local feature branch, then
# verifies the result. Encodes all error-handling paths from Step 4g so the
# LLM receives a pass/fail exit code rather than parsing git output inline.
#
# Exit codes:
#   0  Cleanup verified — worktree removed, branch deleted, prune done
#   1  Cleanup failed — details on stdout; caller decides whether to force
#   2  Usage error
#
# Stdout:
#   One status line per action. On failure, includes a fix hint.
#
# Usage:
#   bash claude-code/skills/ywc-parallel-executor/scripts/cleanup-worktree.sh \
#     000001-010-db-create-users-table

set -euo pipefail

TASK_NAME="${1:-}"
if [ -z "$TASK_NAME" ]; then
  echo "Usage: cleanup-worktree.sh <task-name>" >&2
  exit 2
fi

WORKTREE_PATH="../worktree-${TASK_NAME}"
BRANCH="feature/${TASK_NAME}"
FAILED=0

# ── Step 1: Remove worktree ──────────────────────────────────────────────────
if [ -e "$WORKTREE_PATH" ]; then
  if git worktree remove "$WORKTREE_PATH" 2>/tmp/_wt_err; then
    echo "OK [1]: worktree removed: $WORKTREE_PATH"
  else
    ERR=$(cat /tmp/_wt_err)
    if echo "$ERR" | grep -q "contains modified or untracked files"; then
      echo "FAIL [1]: worktree '$WORKTREE_PATH' has modified or untracked files."
      echo "  Inspect: git -C $WORKTREE_PATH status"
      echo "  If build/log artifacts only: git worktree remove --force $WORKTREE_PATH"
      echo "  If real unstaged changes: stop and surface to user — do NOT force"
    elif echo "$ERR" | grep -q "is locked"; then
      echo "FAIL [1]: worktree '$WORKTREE_PATH' is locked."
      echo "  Fix: git worktree unlock $WORKTREE_PATH && git worktree remove $WORKTREE_PATH"
    else
      echo "FAIL [1]: git worktree remove failed: $ERR"
    fi
    FAILED=1
  fi
  # Directory persists after a successful remove (edge case)
  if [ "$FAILED" -eq 0 ] && [ -e "$WORKTREE_PATH" ]; then
    echo "WARN [1]: directory persists after worktree remove — running rm -rf"
    rm -rf "$WORKTREE_PATH"
    git worktree prune 2>/dev/null || true
  fi
else
  echo "INFO [1]: worktree path '$WORKTREE_PATH' not found — skipping remove"
fi

# ── Step 2: Delete local branch ──────────────────────────────────────────────
if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  if git branch -d "$BRANCH" 2>/tmp/_br_err; then
    echo "OK [2]: branch deleted: $BRANCH"
  else
    ERR=$(cat /tmp/_br_err)
    if echo "$ERR" | grep -q "not fully merged"; then
      echo "FAIL [2]: branch '$BRANCH' is not fully merged."
      echo "  This is a Step 4e (Wave Merge) failure — re-verify the merge commit."
      echo "  Do NOT use 'git branch -D' to bypass this safety check."
    else
      echo "FAIL [2]: git branch -d failed: $ERR"
    fi
    FAILED=1
  fi
else
  echo "INFO [2]: branch '$BRANCH' not found — skipping delete"
fi

# ── Step 3: Prune metadata ───────────────────────────────────────────────────
git worktree prune 2>/dev/null || true
echo "OK [3]: git worktree prune complete"

# ── Verification ─────────────────────────────────────────────────────────────
if [ "$FAILED" -eq 0 ]; then
  if [ -e "$WORKTREE_PATH" ]; then
    echo "FAIL [verify]: worktree directory still exists: $WORKTREE_PATH"
    FAILED=1
  fi
  if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
    echo "FAIL [verify]: branch still exists: $BRANCH"
    FAILED=1
  fi
fi

if [ "$FAILED" -eq 0 ]; then
  echo "PASS: cleanup verified for task '$TASK_NAME'"
fi

exit "$FAILED"
