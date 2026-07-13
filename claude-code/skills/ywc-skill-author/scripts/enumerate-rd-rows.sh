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
# Sourceable: guarded by the __main__ check at the bottom of this file, so
# build-variant.sh can `source` this file and call enumerate_rows directly
# instead of carrying a second copy of the classification logic.
enumerate_rows() {
  awk '
    # infm: frontmatter state machine (0 = before frontmatter, 1 = inside,
    # 2 = past the closing fence / in body). Only body (infm==2) is scanned,
    # matching score.py::split_frontmatter()s (fm, body) split.
    NR == 1 && /^---[[:space:]]*$/ { infm = 1; next }
    infm == 1 && /^---[[:space:]]*$/ { infm = 2; next }
    infm != 2 { next }
    # insection: true from the "## Rationalization Defense" heading up to
    # (not including) the next "## " heading, mirroring score.py::
    # _rationalization_data_rows()s body[idx:next-"## "-or-EOF] slice.
    !insection && /^## Rationalization Defense/ { insection = 1; found_section = 1; next }
    insection && /^## / { insection = 0; next }
    !insection { next }
    {
      trimmed = $0
      sub(/^[ \t]+/, "", trimmed)
      sub(/[ \t]+$/, "", trimmed)
      if (trimmed !~ /^\|/) next
      # is_sep: a markdown table separator row ("|---|---|") contains only
      # pipe/dash/colon/space characters once trimmed.
      is_sep = (trimmed ~ /^[|: -]*$/)
      # header_seen: one-shot latch — the first non-separator pipe row is
      # the table header and is excluded, exactly like score.pys
      # "data -= 1  # drop the header row".
      if (!header_seen && !is_sep) { header_seen = 1; next }
      if (is_sep) next
      data_rows++
      print NR "-" NR
    }
    END {
      if (data_rows + 0 == 0) {
        if (infm != 2) print "WARNING: no closed frontmatter fence found (0 rows emitted)" > "/dev/stderr"
        else if (!found_section) print "WARNING: no \"## Rationalization Defense\" section found (0 rows emitted)" > "/dev/stderr"
        else print "WARNING: \"## Rationalization Defense\" section found but has 0 data rows" > "/dev/stderr"
      }
    }
  ' "$1"
}

self_check() {
  local total=0 mismatches=0 d skill_md ours canonical
  for d in "$REPO_ROOT"/claude-code/skills/ywc-*/; do
    skill_md="${d}SKILL.md"
    [ -f "$skill_md" ] || continue
    total=$((total + 1))
    ours="$(enumerate_rows "$skill_md" 2>/dev/null | wc -l | tr -d ' ')"
    if ! canonical="$(python3 -c "
import sys
sys.path.insert(0, '$REPO_ROOT/.claude/skills/ywc-toolkit-eval/scripts')
from score import split_frontmatter, _rationalization_data_rows
text = open('$skill_md', encoding='utf-8').read()
_, body = split_frontmatter(text)
print(_rationalization_data_rows(body))
" 2>&1)"; then
      echo "FAIL: could not invoke canonical scorer (score.py) for $skill_md: $canonical" >&2
      mismatches=$((mismatches + 1))
      continue
    fi
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

# __main__ guard: only run the CLI dispatch when executed directly, so
# build-variant.sh can `source` this file for enumerate_rows() alone.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  [ "$#" -eq 1 ] || usage

  if [ "$1" = "--self-check" ]; then
    self_check
    exit $?
  fi

  DIR="${1%/}"
  SKILL="$DIR/SKILL.md"
  [ -f "$SKILL" ] || { echo "FAIL: $SKILL not found" >&2; exit 1; }
  enumerate_rows "$SKILL"
fi
