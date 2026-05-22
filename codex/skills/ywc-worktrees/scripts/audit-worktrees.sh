#!/usr/bin/env bash
# audit-worktrees.sh [--root <path>] [--prune] [--expect <task1,task2,...>]
#
# Audits the project worktree root used by ywc-worktrees. Resolution order:
# .worktrees/ > CLAUDE.md worktree_root > --root > legacy ../worktree-<task>.
#
# Exit codes:
#   0  Clean: no unexpected, stale, leaked, or missing worktrees
#   1  Audit failed: findings printed on stdout
#   2  Usage error

set -uo pipefail

DO_PRUNE=0
EXPECT=""
ROOT_ARG=""

usage() {
  echo "Usage: audit-worktrees.sh [--root <path>] [--prune] [--expect <task1,task2,...>]" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prune)   DO_PRUNE=1; shift ;;
    --expect)
      if [ -z "${2:-}" ]; then usage; exit 2; fi
      EXPECT="$2"; shift 2
      ;;
    --root)
      if [ -z "${2:-}" ]; then usage; exit 2; fi
      ROOT_ARG="$2"; shift 2
      ;;
    -h|--help) usage; exit 0 ;;
    *)         echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

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

append_line() {
  local current="$1"
  local value="$2"
  if [ -z "$current" ]; then
    printf '%s\n' "$value"
  else
    printf '%s\n%s\n' "$current" "$value"
  fi
}

contains_line() {
  local list="$1"
  local value="$2"
  [ -n "$list" ] && printf '%s\n' "$list" | grep -Fx -- "$value" >/dev/null 2>&1
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

if [ "$DO_PRUNE" -eq 1 ]; then
  git worktree prune --verbose 2>&1 || true
fi

ALL_WORKTREES=$(git worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2}' || true)
REGISTERED=""
STALE=""
while IFS= read -r WT_PATH; do
  [ -z "$WT_PATH" ] && continue
  case "$ROOT_KIND:$WT_PATH" in
    legacy:*/worktree-*) ;;
    standard:"$ROOT_ABS"/*) ;;
    *) continue ;;
  esac

  REGISTERED=$(append_line "$REGISTERED" "$WT_PATH")
  if [ ! -d "$WT_PATH" ]; then
    STALE=$(append_line "$STALE" "$WT_PATH")
  fi
done <<< "$ALL_WORKTREES"

EXPECTED_PATHS=""
EXPECTED_TASKS=""
if [ -n "$EXPECT" ]; then
  IFS=',' read -ra EXPECTED_LIST <<< "$EXPECT"
  for TASK in "${EXPECTED_LIST[@]}"; do
    TASK=$(trim "$TASK")
    [ -z "$TASK" ] && continue
    EXPECTED_TASKS=$(append_line "$EXPECTED_TASKS" "$TASK")
    if [ "$ROOT_KIND" = "legacy" ]; then
      EXPECTED_PATHS=$(append_line "$EXPECTED_PATHS" "$ROOT_ABS/worktree-${TASK}")
    else
      EXPECTED_PATHS=$(append_line "$EXPECTED_PATHS" "$ROOT_ABS/${TASK}")
    fi
  done
fi

UNREGISTERED=""
if [ -d "$ROOT_ABS" ]; then
  if [ "$ROOT_KIND" = "legacy" ]; then
    DIRS=$(find "$ROOT_ABS" -mindepth 1 -maxdepth 1 -type d -name 'worktree-*' 2>/dev/null || true)
  else
    DIRS=$(find "$ROOT_ABS" -mindepth 1 -maxdepth 1 -type d 2>/dev/null || true)
  fi
  while IFS= read -r DIR_PATH; do
    [ -z "$DIR_PATH" ] && continue
    if ! contains_line "$REGISTERED" "$DIR_PATH"; then
      UNREGISTERED=$(append_line "$UNREGISTERED" "$DIR_PATH")
    fi
  done <<< "$DIRS"
fi

MISSING=""
if [ -n "$EXPECTED_PATHS" ]; then
  while IFS= read -r EXPECTED_PATH; do
    [ -z "$EXPECTED_PATH" ] && continue
    if ! contains_line "$REGISTERED" "$EXPECTED_PATH"; then
      MISSING=$(append_line "$MISSING" "$EXPECTED_PATH")
    fi
  done <<< "$EXPECTED_PATHS"
fi

LEAKED=""
if [ -n "$REGISTERED" ]; then
  while IFS= read -r WT_PATH; do
    [ -z "$WT_PATH" ] && continue
    if [ -n "$EXPECTED_PATHS" ]; then
      contains_line "$EXPECTED_PATHS" "$WT_PATH" || LEAKED=$(append_line "$LEAKED" "$WT_PATH")
    else
      LEAKED=$(append_line "$LEAKED" "$WT_PATH")
    fi
  done <<< "$REGISTERED"
fi

FAILED=0
if [ -n "$STALE" ]; then
  echo "STALE: registered worktree paths no longer exist"
  printf '%s\n' "$STALE" | sed 's/^/  - /'
  FAILED=1
fi
if [ -n "$UNREGISTERED" ]; then
  echo "DRIFT: directories under worktree root are not registered with git"
  printf '%s\n' "$UNREGISTERED" | sed 's/^/  - /'
  FAILED=1
fi
if [ -n "$MISSING" ]; then
  echo "MISSING: expected worktrees are not registered"
  printf '%s\n' "$MISSING" | sed 's/^/  - /'
  FAILED=1
fi
if [ -n "$LEAKED" ]; then
  if [ -n "$EXPECTED_TASKS" ]; then
    echo "LEAKED: registered worktrees are not in --expect"
  else
    echo "DRIFT: unexpected worktrees found"
  fi
  printf '%s\n' "$LEAKED" | sed 's/^/  - /'
  FAILED=1
fi

if [ "$FAILED" -eq 0 ]; then
  echo "OK: worktree audit clean (root: $ROOT_ABS, mode: $ROOT_KIND)"
fi

exit "$FAILED"
