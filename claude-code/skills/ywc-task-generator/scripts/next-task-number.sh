#!/usr/bin/env bash
# Compute the starting task number for a NEW batch.
#
# Scans BOTH <tasks-dir> and <tasks-dir>/completed (executors archive finished
# tasks into completed/, so scanning the live dir alone risks reusing a number
# that was already used and archived). Takes the highest 6-digit PHASE across
# the union and returns the next phase with SEQUENCE reset to 010.
#
# Usage:
#   bash claude-code/skills/ywc-task-generator/scripts/next-task-number.sh [tasks-dir]
#
# Output: the next batch prefix, e.g. "000017-010" (or "000001-010" when empty).
set -euo pipefail

TASKS_DIR="${1:-tasks}"
max=0

scan() {
  local dir="$1" entry name phase
  [ -d "$dir" ] || return 0
  for entry in "$dir"/*; do
    [ -e "$entry" ] || continue
    name="$(basename "$entry")"
    if [[ "$name" =~ ^([0-9]{6})-[0-9]{3}- ]]; then
      phase=$((10#${BASH_REMATCH[1]}))
      (( phase > max )) && max=$phase
    fi
  done
}

scan "$TASKS_DIR"
scan "$TASKS_DIR/completed"

printf '%06d-010\n' $((max + 1))
