#!/usr/bin/env bash
# cleanup-worktree.sh [--root <path>] [--branch <branch>] [--force] [--keep-branch] <task-name>
#
# Removes the resolved task worktree, deletes or preserves the local branch,
# prunes stale metadata, and verifies the result.
#
# Exit codes:
#   0  Cleanup verified
#   1  Cleanup failed; details printed on stdout
#   2  Usage error

set -uo pipefail

ROOT_ARG=""
BRANCH=""
FORCE=0
KEEP_BRANCH=0
TASK_NAME=""

usage() {
  echo "Usage: cleanup-worktree.sh [--root <path>] [--branch <branch>] [--force] [--keep-branch] <task-name>" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      if [ -z "${2:-}" ]; then usage; exit 2; fi
      ROOT_ARG="$2"; shift 2
      ;;
    --branch)
      if [ -z "${2:-}" ]; then usage; exit 2; fi
      BRANCH="$2"; shift 2
      ;;
    --force)
      FORCE=1; shift
      ;;
    --keep-branch)
      KEEP_BRANCH=1; shift
      ;;
    -h|--help)
      usage; exit 0
      ;;
    -*)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
    *)
      if [ -n "$TASK_NAME" ]; then
        echo "Unexpected extra argument: $1" >&2
        usage
        exit 2
      fi
      TASK_NAME="$1"; shift
      ;;
  esac
done

if [ -z "$TASK_NAME" ]; then
  usage
  exit 2
fi

# Reject task names that could enable path traversal or shell metacharacter
# injection. WORKTREE_PATH and BRANCH are derived from TASK_NAME, and
# WORKTREE_PATH later flows into `git worktree remove` / `rm -rf` via
# `git worktree remove --force`, so an unvalidated task name (e.g. containing
# `..`, `/`, `\\`, or shell metacharacters) could resolve outside the worktree
# root or break later parsing. Allowlist: alphanumeric, hyphen, underscore.
if [[ ! "$TASK_NAME" =~ ^[A-Za-z0-9_-]+$ ]]; then
  echo "FAIL: invalid task name: '$TASK_NAME'" >&2
  echo "  Allowed characters: A-Z, a-z, 0-9, '-', '_' (no path separators, no '..')" >&2
  exit 2
fi

if [ -z "$BRANCH" ]; then
  BRANCH="feature/${TASK_NAME}"
fi

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
  echo "FAIL: not inside a git repository"
  exit 1
fi
cd "$REPO_ROOT" || exit 1

trim() {
  printf '%s' "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

absolute_path() {
  local path="${1%/}"
  if [ "${path#/}" != "$path" ]; then
    printf '%s\n' "$path"
  else
    printf '%s\n' "$REPO_ROOT/$path"
  fi
}

canonical_dir() {
  local path="$1"
  if [ -d "$path" ]; then
    (cd "$path" && pwd -P)
  else
    absolute_path "$path"
  fi
}

CLAUDE_ROOT=""
if [ -f CLAUDE.md ]; then
  CLAUDE_ROOT=$(awk -F: '/^[[:space:]]*worktree_root[[:space:]]*:/ {print $2; exit}' CLAUDE.md)
  CLAUDE_ROOT=$(trim "$CLAUDE_ROOT")
fi

ROOT_KIND="standard"
if [ -d .worktrees ]; then
  RESOLVED_ROOT=".worktrees"
elif [ -n "$CLAUDE_ROOT" ]; then
  RESOLVED_ROOT="$CLAUDE_ROOT"
elif [ -n "$ROOT_ARG" ]; then
  RESOLVED_ROOT="$ROOT_ARG"
else
  RESOLVED_ROOT=".."
  ROOT_KIND="legacy"
fi

ROOT_ABS=$(canonical_dir "$RESOLVED_ROOT")
if [ "$ROOT_KIND" = "standard" ]; then
  if [ ! -d "$ROOT_ABS" ]; then
    echo "FAIL: resolved worktree root does not exist: $ROOT_ABS"
    exit 1
  fi
  if [ ! -w "$ROOT_ABS" ]; then
    echo "FAIL: resolved worktree root is not writable: $ROOT_ABS"
    exit 1
  fi
fi

if [ "$ROOT_KIND" = "legacy" ]; then
  WORKTREE_PATH="$ROOT_ABS/worktree-${TASK_NAME}"
else
  WORKTREE_PATH="$ROOT_ABS/${TASK_NAME}"
fi

case "$WORKTREE_PATH" in
  "$ROOT_ABS"/*) ;;
  *)
    echo "FAIL: resolved worktree path is outside root"
    echo "  root: $ROOT_ABS"
    echo "  path: $WORKTREE_PATH"
    exit 1
    ;;
esac

FAILED=0
ERR_FILE=$(mktemp "${TMPDIR:-/tmp}/ywc-worktree-cleanup.XXXXXX")
trap 'rm -f "$ERR_FILE"' EXIT

# ── Step 1: Remove worktree ──────────────────────────────────────────────────
if [ -e "$WORKTREE_PATH" ]; then
  REMOVE_ARGS=("$WORKTREE_PATH")
  if [ "$FORCE" -eq 1 ]; then
    REMOVE_ARGS=(--force "$WORKTREE_PATH")
  fi
  if git worktree remove "${REMOVE_ARGS[@]}" 2>"$ERR_FILE"; then
    echo "OK [1]: worktree removed: $WORKTREE_PATH"
  else
    ERR=$(cat "$ERR_FILE")
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
else
  echo "INFO [1]: worktree path '$WORKTREE_PATH' not found — skipping remove"
fi

# ── Step 2: Delete or preserve local branch ─────────────────────────────────
if [ "$KEEP_BRANCH" -eq 1 ]; then
  if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
    echo "OK [2]: branch preserved: $BRANCH"
  else
    echo "FAIL [2]: branch '$BRANCH' not found; cannot preserve missing branch"
    FAILED=1
  fi
elif git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  if git branch -d "$BRANCH" 2>"$ERR_FILE"; then
    echo "OK [2]: branch deleted: $BRANCH"
  else
    ERR=$(cat "$ERR_FILE")
    if echo "$ERR" | grep -q "not fully merged"; then
      echo "FAIL [2]: branch '$BRANCH' is not fully merged."
      echo "  This is a Step 4e (Wave Merge) failure — re-verify the merge commit."
      echo "  Do NOT use 'git branch -D' to bypass this safety check."
    elif echo "$ERR" | grep -q "checked out"; then
      echo "FAIL [2]: branch '$BRANCH' is still checked out in another worktree."
      echo "  Inspect: git worktree list"
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
  if git worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2}' | grep -Fx -- "$WORKTREE_PATH" >/dev/null; then
    echo "FAIL [verify]: worktree metadata still exists: $WORKTREE_PATH"
    FAILED=1
  fi
  if [ "$KEEP_BRANCH" -eq 1 ]; then
    if ! git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
      echo "FAIL [verify]: preserved branch is missing: $BRANCH"
      FAILED=1
    fi
  elif git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
    echo "FAIL [verify]: branch still exists: $BRANCH"
    FAILED=1
  fi
fi

if [ "$FAILED" -eq 0 ]; then
  echo "PASS: cleanup verified for task '$TASK_NAME'"
fi

exit "$FAILED"
