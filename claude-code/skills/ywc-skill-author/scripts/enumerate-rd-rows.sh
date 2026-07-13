#!/usr/bin/env bash
# Enumerate the absolute file line range of each data row in a skill's
# "## Rationalization Defense" table. Outputs one "<start>-<end>" per data
# row (1-indexed, inclusive; start == end for a normal single-line row).
#
# Mirrors score.py::_rationalization_data_rows()'s line-filtering logic
# (frontmatter-bounded body, section-bounded to the next "## " heading,
# pipe-row / separator-row / header-row classification) but preserves line
# position instead of discarding it, because sampling and variant-building
# both need "<start>-<end>" ranges that score.py's int-only counter drops.
#
# Usage:
#   enumerate-rd-rows.sh <skill-dir>
#   enumerate-rd-rows.sh --self-check
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

usage() {
  echo "usage: enumerate-rd-rows.sh <skill-dir> | enumerate-rd-rows.sh --self-check" >&2
  exit 2
}

# Reads a SKILL.md path on $1, prints one "<line>-<line>" per RD data row.
enumerate_rows() {
  awk '
    NR == 1 && /^---[[:space:]]*$/ { infm = 1; next }
    infm == 1 && /^---[[:space:]]*$/ { infm = 2; next }
    infm != 2 { next }
    !insection && /^## Rationalization Defense/ { insection = 1; next }
    insection && /^## / { insection = 0; next }
    !insection { next }
    {
      trimmed = $0
      sub(/^[ \t]+/, "", trimmed)
      sub(/[ \t]+$/, "", trimmed)
      if (trimmed !~ /^\|/) next
      is_sep = (trimmed ~ /^[|: -]*$/)
      if (!header_seen && !is_sep) { header_seen = 1; next }
      if (is_sep) next
      print NR "-" NR
    }
  ' "$1"
}

self_check() {
  local total=0 mismatches=0 d skill_md ours canonical
  for d in "$REPO_ROOT"/claude-code/skills/ywc-*/; do
    skill_md="${d}SKILL.md"
    [ -f "$skill_md" ] || continue
    total=$((total + 1))
    ours="$(enumerate_rows "$skill_md" | wc -l | tr -d ' ')"
    canonical="$(python3 -c "
import sys
sys.path.insert(0, '$REPO_ROOT/.claude/skills/ywc-toolkit-eval/scripts')
from score import split_frontmatter, _rationalization_data_rows
text = open('$skill_md', encoding='utf-8').read()
_, body = split_frontmatter(text)
print(_rationalization_data_rows(body))
")"
    if [ "$ours" != "$canonical" ]; then
      echo "MISMATCH: $(basename "$d") ours=$ours canonical=$canonical" >&2
      mismatches=$((mismatches + 1))
    fi
  done
  if [ "$mismatches" -eq 0 ]; then
    echo "PARITY OK: $total/$total"
    return 0
  fi
  echo "PARITY FAIL: $mismatches/$total mismatched" >&2
  return 1
}

[ "$#" -eq 1 ] || usage

if [ "$1" = "--self-check" ]; then
  self_check
  exit $?
fi

DIR="${1%/}"
SKILL="$DIR/SKILL.md"
[ -f "$SKILL" ] || { echo "FAIL: $SKILL not found" >&2; exit 1; }
enumerate_rows "$SKILL"
