#!/usr/bin/env bash
# Mark a task complete: move <tasks-dir>/<task> into completed/, write the
# mandatory marker commit, and verify. Shared by ywc-parallel-executor (Step 4e)
# and ywc-finish-branch (Step 7), where this exact block was inlined verbatim.
#
# The marker form depends on whether <tasks-dir> is gitignored: `git mv` cannot
# stage a path inside a gitignored dir (no diff to commit), so that case uses a
# plain `mv` plus an --allow-empty marker commit. Either way the
# "chore: mark <task> as completed" commit is mandatory — it is the git-log
# audit boundary every downstream consumer (resume, replay, Completion Report)
# relies on.
#
# Usage:
#   bash claude-code/skills/scripts/mark-complete.sh <tasks-dir> <task-name> [--push | --defer-push]
#
# Push defaults to OFF (deferred). Pass --push to push the current branch after
# the marker commit (local-merge / normal-pr without --defer-push). The caller
# owns the branch context; --push runs `git push` on the current branch.
set -euo pipefail

TASKS_DIR="${1:-}"
TASK="${2:-}"
if [ -z "$TASKS_DIR" ] || [ -z "$TASK" ]; then
  echo "usage: mark-complete.sh <tasks-dir> <task-name> [--push | --defer-push]" >&2
  exit 2
fi
shift 2

PUSH=0
while [ $# -gt 0 ]; do
  case "$1" in
    --push) PUSH=1; shift ;;
    --defer-push) PUSH=0; shift ;;
    *) echo "error: unknown flag: $1" >&2; exit 2 ;;
  esac
done

# Path-traversal guard — the task name becomes a filesystem path.
case "$TASK" in
  */*|*..*) echo "error: invalid task name (no '/' or '..'): $TASK" >&2; exit 2 ;;
esac

# Tasks-dir guard — both executors pass a repo-relative dir; reject absolute
# paths and '..' so the move/commit can never escape the working tree.
case "$TASKS_DIR" in
  /*)    echo "error: tasks-dir must be repo-relative, not absolute: $TASKS_DIR" >&2; exit 2 ;;
  *..*)  echo "error: tasks-dir must not contain '..': $TASKS_DIR" >&2; exit 2 ;;
esac

TASKS_DIR="${TASKS_DIR%/}"
SRC="$TASKS_DIR/$TASK"
DEST="$TASKS_DIR/completed/$TASK"
MSG="chore: mark $TASK as completed"

[ -d "$SRC" ]  || { echo "error: source task dir not found: $SRC" >&2; exit 1; }
[ -e "$DEST" ] && { echo "error: destination already exists: $DEST" >&2; exit 1; }

mkdir -p "$TASKS_DIR/completed"

if git check-ignore -q "$SRC" 2>/dev/null; then
  # Gitignored tasks/ — git mv cannot track the move; plain mv + empty marker.
  mv "$SRC" "$DEST"
  git commit --allow-empty -m "$MSG"
else
  # Tracked tasks/ — git mv stages the rename; the commit content IS the move.
  git mv "$SRC" "$DEST"
  git commit -m "$MSG"
fi

# Post-move verification (do not skip).
if [ ! -d "$DEST" ] || [ -e "$SRC" ]; then
  echo "error: move verification failed ($SRC -> $DEST)" >&2
  exit 1
fi
last_subject="$(git log -1 --format='%s')"
if [ "$last_subject" != "$MSG" ]; then
  echo "error: marker commit is not at HEAD (HEAD subject: '$last_subject')" >&2
  exit 1
fi

if [ "$PUSH" -eq 1 ]; then
  git push
  echo "marked complete + pushed: $TASK"
else
  echo "marked complete (push deferred): $TASK"
fi
