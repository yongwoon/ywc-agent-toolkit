#!/usr/bin/env bash
# Write a variant of <skill-dir>/SKILL.md with the given inclusive line
# range deleted, to a fresh temp path, and print that path. Never mutates
# the source file (AC2 global invariant) and never writes anything to disk
# on a refusal.
#
# Refuses (exit 1, no write, no output path) on:
#   - inverted range (start > end)
#   - out-of-bounds range (start < 1 or end > file line count)
#   - header orphan: the deletion would leave the "## Rationalization
#     Defense" table with 0 remaining data rows (per
#     enumerate-rd-rows.sh's row classification)
#
# Determinism is the contract: re-running with the same skill-dir/start/end
# produces byte-identical output content every time (`cmp` exit 0).
#
# Usage: build-variant.sh <skill-dir> <start> <end>
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=enumerate-rd-rows.sh
source "$SCRIPT_DIR/enumerate-rd-rows.sh"

usage() {
  echo "usage: build-variant.sh <skill-dir> <start> <end>" >&2
  exit 2
}

[ "$#" -eq 3 ] || usage
DIR="${1%/}"
START="$2"
END="$3"
SKILL="$DIR/SKILL.md"

[ -f "$SKILL" ] || { echo "FAIL: $SKILL not found" >&2; exit 1; }

case "$START" in ''|*[!0-9]*) echo "FAIL: start must be a positive integer, got '$START'" >&2; exit 1 ;; esac
case "$END" in ''|*[!0-9]*) echo "FAIL: end must be a positive integer, got '$END'" >&2; exit 1 ;; esac

TOTAL="$(wc -l < "$SKILL" | tr -d ' ')"

if [ "$START" -gt "$END" ]; then
  echo "FAIL: inverted range ($START > $END)" >&2
  exit 1
fi
if [ "$START" -lt 1 ] || [ "$END" -gt "$TOTAL" ]; then
  echo "FAIL: out-of-bounds range ($START-$END, file has $TOTAL lines)" >&2
  exit 1
fi

# Header-orphan check reuses enumerate-rd-rows.sh's enumerate_rows() (sourced
# above) via process substitution, rather than carrying a second copy of the
# classification awk that could silently drift from the self-check-pinned
# original. Diagnostics from enumerate_rows's own empty-output warning are
# irrelevant here (this script emits its own header-orphan message), so
# stderr is discarded for this call only.
REMAINING="$(enumerate_rows <(awk -v s="$START" -v e="$END" 'NR < s || NR > e' "$SKILL") 2>/dev/null | wc -l | tr -d ' ')"
if [ "$REMAINING" -eq 0 ]; then
  echo "FAIL: deleting lines $START-$END would leave the Rationalization Defense table with 0 data rows (header orphan)" >&2
  exit 1
fi

OUT="$(mktemp)"
awk -v s="$START" -v e="$END" 'NR < s || NR > e' "$SKILL" > "$OUT"
echo "$OUT"
