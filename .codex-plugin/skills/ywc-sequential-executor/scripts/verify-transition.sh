#!/usr/bin/env bash
# verify-transition.sh <integration-branch> <completed-task-name> [tasks-dir]

set -uo pipefail

INTEGRATION_BRANCH="${1:-}"
COMPLETED_TASK="${2:-}"
TASKS_DIR="${3:-tasks/}"

if [ -z "$INTEGRATION_BRANCH" ] || [ -z "$COMPLETED_TASK" ]; then
  echo "Usage: verify-transition.sh <integration-branch> <completed-task-name> [tasks-dir]" >&2
  exit 1
fi

FAILED=0

CURRENT=$(git branch --show-current 2>/dev/null || echo "")
if [ "$CURRENT" != "$INTEGRATION_BRANCH" ]; then
  echo "FAIL [1]: Current branch is '$CURRENT', expected '$INTEGRATION_BRANCH'"
  echo "  Fix: git checkout $INTEGRATION_BRANCH"
  FAILED=1
fi

FEATURE_BRANCH="feature/$COMPLETED_TASK"
if git branch --list "$FEATURE_BRANCH" | grep -q .; then
  echo "FAIL [2]: Feature branch '$FEATURE_BRANCH' still exists"
  echo "  Fix: re-invoke ywc-finish-branch or delete only after verifying merge"
  FAILED=1
fi

STATUS=$(git status --porcelain 2>/dev/null || echo "")
if [ -n "$STATUS" ]; then
  TRACKED=$(echo "$STATUS" | grep -v '^??' || true)
  UNTRACKED=$(echo "$STATUS" | grep '^??' || true)
  if [ -n "$TRACKED" ]; then
    echo "FAIL [3]: Working tree has tracked modifications:"
    echo "$TRACKED" | head -10 | sed 's/^/  /'
    FAILED=1
  elif [ -n "$UNTRACKED" ]; then
    echo "WARN [3]: Working tree has untracked files:"
    echo "$UNTRACKED" | head -5 | sed 's/^/  /'
  fi
fi

COMPLETED_DIR="${TASKS_DIR%/}/completed/$COMPLETED_TASK"
ACTIVE_DIR="${TASKS_DIR%/}/$COMPLETED_TASK"

if [ ! -d "$COMPLETED_DIR" ]; then
  echo "FAIL [4a]: '$COMPLETED_DIR' does not exist"
  FAILED=1
fi
if [ -e "$ACTIVE_DIR" ]; then
  echo "FAIL [4b]: '$ACTIVE_DIR' still exists"
  FAILED=1
fi

if [ "$FAILED" -eq 0 ]; then
  echo "PASS: All 4 pre-transition conditions satisfied"
  exit 0
fi

exit 1
