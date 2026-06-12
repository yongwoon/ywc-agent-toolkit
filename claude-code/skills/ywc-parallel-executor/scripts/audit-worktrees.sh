#!/usr/bin/env bash
# audit-worktrees.sh [--prune] [--expect <task1,task2,...>]
#
# Lists parallel-executor worktrees (paths matching /worktree-/).
# Used at Pre-flight to detect stale leftovers and after each wave to
# detect drift — unexpected live worktrees.
#
# Options:
#   --prune              Run 'git worktree prune' before auditing
#   --expect <tasks>     Comma-separated task names expected to still have
#                        worktrees (preserved failures). Unlisted entries
#                        are reported as DRIFT.
#
# Exit codes:
#   0  No unexpected worktrees (clean or only expected preserved failures)
#   1  Stale / drifted worktrees detected — details on stdout
#   2  Usage error
#
# Usage:
#   # Pre-flight: prune stale metadata first, then report any remaining
#   bash claude-code/skills/ywc-parallel-executor/scripts/audit-worktrees.sh --prune
#
#   # Wave-end audit with preserved failures
#   bash claude-code/skills/ywc-parallel-executor/scripts/audit-worktrees.sh \
#     --expect 000001-010-db-create-users,000001-020-add-indexes

set -euo pipefail

DO_PRUNE=0
EXPECT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prune)   DO_PRUNE=1; shift ;;
    --expect)  EXPECT="${2:-}"; shift 2 ;;
    *)         echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [ "$DO_PRUNE" -eq 1 ]; then
  git worktree prune --verbose 2>&1 || true
fi

WORKTREES=$(git worktree list --porcelain 2>/dev/null \
  | awk '/^worktree /{print $2}' \
  | grep -E '/worktree-' || true)

if [ -z "$WORKTREES" ]; then
  echo "OK: no parallel-executor worktrees found"
  exit 0
fi

# Build expected set from comma-separated task names
declare -A EXPECTED_MAP
if [ -n "$EXPECT" ]; then
  IFS=',' read -ra EXPECTED_LIST <<< "$EXPECT"
  for TASK in "${EXPECTED_LIST[@]}"; do
    EXPECTED_MAP["worktree-${TASK}"]=1
  done
fi

FOUND_UNEXPECTED=0
while IFS= read -r WT_PATH; do
  WT_BASENAME=$(basename "$WT_PATH")
  if [ -n "$EXPECT" ] && [ "${EXPECTED_MAP[$WT_BASENAME]+_}" ]; then
    echo "OK (preserved failure): $WT_PATH"
  else
    echo "DRIFT: unexpected worktree: $WT_PATH"
    echo "  Investigate before proceeding to next wave."
    echo "  If already merged: git worktree remove --force $WT_PATH"
    echo "  If in-progress work: stop and surface to user"
    FOUND_UNEXPECTED=1
  fi
done <<< "$WORKTREES"

exit "$FOUND_UNEXPECTED"
