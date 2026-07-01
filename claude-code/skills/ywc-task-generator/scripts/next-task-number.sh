#!/usr/bin/env bash
# Compute the starting task number for a NEW batch.
#
# The task DIRECTORIES are the single source of truth for number allocation.
# Scans BOTH <tasks-dir> and <tasks-dir>/completed (executors archive finished
# tasks into completed/, so scanning the live dir alone risks reusing a number
# that was already used and archived). Takes the highest 6-digit PHASE across
# the union and returns the next phase with SEQUENCE reset to 010.
#
# Cross-check (advisory only): if <tasks-dir>/dependency-graph.md exists, the
# highest PHASE referenced by a full `NNNNNN-NNN-` task ID in it is parsed and
# compared against the directory result. A mismatch means the derived graph has
# drifted from the authoritative directories; a warning is emitted to STDERR but
# the directory result still wins. The graph NEVER overrides directory scan.
#
# Usage:
#   bash claude-code/skills/ywc-task-generator/scripts/next-task-number.sh [tasks-dir]
#
# Output (STDOUT): the next batch prefix, e.g. "000017-010" (or "000001-010" when empty).
# Warnings (STDERR): drift notice when the dependency graph disagrees.
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
      # Use `if` (not `(( )) && ...`): under `set -e` a false `(( ))` returns 1
      # as the loop's last command, which would exit before the final printf.
      if (( phase > max )); then max=$phase; fi
    fi
  done
}

scan "$TASKS_DIR"
scan "$TASKS_DIR/completed"

# Advisory cross-check against the derived dependency graph. Only full task IDs
# of the form NNNNNN-NNN- count; bare "depends on 000001" phase references (no
# SEQUENCE) are intentionally excluded so partial mentions never inflate the max.
graph="$TASKS_DIR/dependency-graph.md"
if [ -f "$graph" ]; then
  graph_max=0
  while IFS= read -r phase; do
    [ -n "$phase" ] || continue
    phase=$((10#$phase))
    if (( phase > graph_max )); then graph_max=$phase; fi
  done < <(grep -oE '[0-9]{6}-[0-9]{3}-' "$graph" | cut -d- -f1 | sort -u)
  if (( graph_max != max )); then
    printf 'WARN: dependency-graph.md highest PHASE (%06d) disagrees with task directories (%06d); directories win. Graph may have drifted — reconcile before generating.\n' \
      "$graph_max" "$max" >&2
  fi
fi

printf '%06d-010\n' $((max + 1))
