#!/usr/bin/env bash
# verify-transition.sh <base-branch> <completed-task-name> [tasks-dir]
#
# Runs the 4-condition pre-transition state check between tasks in range mode.
# All four conditions must pass before moving to the next task.
#
# Conditions checked:
#   1. Current branch == base branch
#   2. Feature branch feature/<completed-task> no longer exists
#   3. Working tree is clean (tracked modifications → FAIL; untracked only → WARN)
#   4. tasks-dir/completed/<completed-task> exists AND tasks-dir/<completed-task> is gone
#
# Exit codes:
#   0  PASS — all conditions satisfied
#   1  FAIL — one or more conditions failed (details on stdout)
#
# Usage:
#   bash claude-code/skills/ywc-sequential-executor/scripts/verify-transition.sh \
#     <base-branch> <completed-task-name> [tasks-dir]
#   tasks-dir defaults to "tasks/"

set -euo pipefail

BASE_BRANCH="${1:-}"
COMPLETED_TASK="${2:-}"
TASKS_DIR="${3:-tasks/}"

if [ -z "$BASE_BRANCH" ] || [ -z "$COMPLETED_TASK" ]; then
  echo "Usage: verify-transition.sh <base-branch> <completed-task-name> [tasks-dir]" >&2
  exit 1
fi

FAILED=0

# ── Condition 1: current branch must equal base branch ──────────────────────
CURRENT=$(git branch --show-current 2>/dev/null || echo "")
if [ "$CURRENT" != "$BASE_BRANCH" ]; then
  echo "FAIL [1]: Current branch is '$CURRENT', expected '$BASE_BRANCH'"
  echo "  Fix: git checkout $BASE_BRANCH"
  FAILED=1
fi

# ── Condition 2: feature branch must be deleted ──────────────────────────────
FEATURE_BRANCH="feature/$COMPLETED_TASK"
if git branch --list "$FEATURE_BRANCH" | grep -q .; then
  echo "FAIL [2]: Feature branch '$FEATURE_BRANCH' still exists (not deleted by ywc-finish-branch)"
  echo "  Fix: git branch -d $FEATURE_BRANCH"
  FAILED=1
fi

# ── Condition 3: working tree must be clean ───────────────────────────────────
STATUS=$(git status --porcelain 2>/dev/null || echo "")
if [ -n "$STATUS" ]; then
  TRACKED=$(echo "$STATUS" | grep -v '^??' || true)
  UNTRACKED=$(echo "$STATUS" | grep '^??' || true)
  if [ -n "$TRACKED" ]; then
    echo "FAIL [3]: Working tree has tracked modifications:"
    echo "$TRACKED" | head -10 | sed 's/^/  /'
    echo "  Fix: commit or stash these changes before transitioning"
    FAILED=1
  elif [ -n "$UNTRACKED" ]; then
    echo "WARN [3]: Working tree has untracked files (likely build/log artifacts)"
    echo "$UNTRACKED" | head -5 | sed 's/^/  /'
    echo "  If safe: git clean -fd to clear"
  fi
fi

# ── Condition 4: task directory moved to completed/ ──────────────────────────
COMPLETED_DIR="${TASKS_DIR%/}/completed/$COMPLETED_TASK"
ACTIVE_DIR="${TASKS_DIR%/}/$COMPLETED_TASK"

if [ ! -d "$COMPLETED_DIR" ]; then
  echo "FAIL [4a]: '$COMPLETED_DIR' does not exist"
  echo "  Mark Task Complete (ywc-finish-branch Step 7) may not have run"
  FAILED=1
fi
if [ -e "$ACTIVE_DIR" ]; then
  echo "FAIL [4b]: '$ACTIVE_DIR' still exists — task was not moved to completed/"
  FAILED=1
fi

# ── Result ────────────────────────────────────────────────────────────────────
if [ "$FAILED" -eq 0 ]; then
  echo "PASS: All 4 pre-transition conditions satisfied — safe to start next task"
  exit 0
else
  exit 1
fi
