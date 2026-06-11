#!/usr/bin/env bash
# Scaffold a task directory from the bundled templates.
#
# Creates <out>/<task-name>/{README.md,task.md} (and test.md with --with-test)
# from references/*.template, substituting the [TASK_NAME] placeholder. The
# generator fills the content; this script only lays down the deterministic
# structure so boilerplate is never hand-retyped per task.
#
# Usage:
#   bash claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh \
#     000017-010-db-create-user-table [--out tasks] [--with-test]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES="$SCRIPT_DIR/../references"

OUT="tasks"
WITH_TEST=0
TASK_NAME=""

while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT="${2:?--out needs a value}"; shift 2 ;;
    --with-test) WITH_TEST=1; shift ;;
    -*) echo "error: unknown flag: $1" >&2; exit 2 ;;
    *) TASK_NAME="$1"; shift ;;
  esac
done

[ -n "$TASK_NAME" ] || { echo "usage: scaffold-task-dir.sh <task-name> [--out dir] [--with-test]" >&2; exit 2; }

# Hard-block path traversal in the task name (it becomes a directory path).
case "$TASK_NAME" in
  */*|*..*) echo "error: invalid task name (no '/' or '..'): $TASK_NAME" >&2; exit 2 ;;
esac

# Warn (do not block) when the name diverges from PHASE-SEQUENCE-category-desc.
if ! [[ "$TASK_NAME" =~ ^[0-9]{6}-[0-9]{3}-[a-z]+-[a-z0-9-]+$ ]]; then
  echo "warning: '$TASK_NAME' does not match NNNNNN-NNN-category-description" >&2
fi

DEST="$OUT/$TASK_NAME"
[ -e "$DEST" ] && { echo "error: $DEST already exists" >&2; exit 1; }

for tpl in README.md.template task.md.template; do
  [ -f "$TEMPLATES/$tpl" ] || { echo "error: missing template $TEMPLATES/$tpl" >&2; exit 1; }
done

mkdir -p "$DEST"
subst() { sed "s/\[TASK_NAME\]/${TASK_NAME//\//\\/}/g" "$1" > "$2"; }

subst "$TEMPLATES/README.md.template" "$DEST/README.md"
subst "$TEMPLATES/task.md.template" "$DEST/task.md"
created="README.md, task.md"

if [ "$WITH_TEST" -eq 1 ]; then
  [ -f "$TEMPLATES/test.md.template" ] || { echo "error: missing test.md.template" >&2; exit 1; }
  subst "$TEMPLATES/test.md.template" "$DEST/test.md"
  created="$created, test.md"
fi

echo "created: $DEST ($created)"
