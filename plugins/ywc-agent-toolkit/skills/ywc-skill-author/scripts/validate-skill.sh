#!/usr/bin/env bash
# Mechanical authoring gate for a single ywc-* skill directory — the
# deterministic subset of the ywc-skill-author A1–A14 checklist. Complements the
# repo-wide scripts/validate.sh (which only checks frontmatter presence + README
# set across all skills) by enforcing the per-skill authoring rules at edit time.
# Exit 1 on any failure.
#
# Usage: bash "${CODEX_HOME:-$HOME/.codex}/skills/ywc-skill-author/scripts/validate-skill.sh" <skill-dir>
set -uo pipefail

DIR="${1:-}"
[ -n "$DIR" ] || { echo "usage: validate-skill.sh <skill-dir>" >&2; exit 2; }
DIR="${DIR%/}"
SKILL="$DIR/SKILL.md"
name="$(basename "$DIR")"
errs=0
fail() { echo "FAIL: $1"; errs=$((errs + 1)); }

[ -f "$SKILL" ] || { echo "FAIL: $SKILL not found"; exit 1; }

# --- Frontmatter ---
if ! printf '%s' "$name" | grep -qE '^ywc-[a-z0-9]+(-[a-z0-9]+)*$'; then
  fail "directory name '$name' is not ywc-<kebab-case> (lowercase letters/digits, hyphen-separated)"
fi
declared="$(sed -n 's/^name:[[:space:]]*//p' "$SKILL" | head -1)"
[ "$declared" = "$name" ] || fail "frontmatter name '$declared' != directory '$name'"
# The description may be inline (text on the `description:` line) or a folded
# block scalar (>-, text on wrapped indented lines). Join the whole value into
# one space-normalized string before matching, so phrases that wrap across lines
# ("Do not use\n  for") and inline single-line descriptions both match.
desc_text="$(awk '
  /^description:/ { sub(/^description:[[:space:]]*[>|]?-?[[:space:]]*/, ""); f=1; print; next }
  f && /^[A-Za-z_]+:/ { f=0 }
  f { print }
' "$SKILL" | tr '\n' ' ' | tr -s ' ')"
# Opener: "(ywc) Use <when|before|after|during ...>". Anti-triggers: "Do not
# use|invoke <for|during|to ...>". Match the stable stem, not a fixed preposition.
case "$desc_text" in *"(ywc) Use "*) ;; *) fail "description missing '(ywc) Use ...' opener" ;; esac
case "$desc_text" in
  *"Do not use "*|*"Do not invoke "*) ;;
  *) fail "description missing 'Do not use/invoke ...' anti-triggers" ;;
esac

# --- Body ---
grep -qE '^\*\*Announce at start:\*\*' "$SKILL" || fail "missing '**Announce at start:**' line"
grep -q '## Rationalization Defense' "$SKILL"    || fail "missing '## Rationalization Defense' section"
if grep -qE '@ywc-[a-z]' "$SKILL"; then
  fail "contains '@ywc-...' force-load cross-reference (reference by name only)"
fi
lines="$(wc -l < "$SKILL" | tr -d ' ')"
[ "$lines" -le 500 ] || fail "SKILL.md is $lines lines (> 500 cap; extract to references/)"

# --- Filesystem: README locale set ---
for f in README.md README.en.md README.ja.md README.ko.md; do
  [ -f "$DIR/$f" ] || fail "missing $f"
done

# --- references/ hygiene: each must be pointed to, none under 30 lines ---
if [ -d "$DIR/references" ]; then
  for ref in "$DIR"/references/*.md; do
    [ -f "$ref" ] || continue
    base="$(basename "$ref")"
    # A pointer may live in SKILL.md or another body/reference file (not the ref itself).
    if ! grep -rqF "$base" "$DIR" --include='*.md' --exclude="$base" 2>/dev/null; then
      fail "reference '$base' has no pointer from any skill .md file"
    fi
    rlines="$(wc -l < "$ref" | tr -d ' ')"
    [ "$rlines" -ge 30 ] || fail "reference '$base' is $rlines lines (< 30; over-extraction)"
  done
fi

if [ "$errs" -eq 0 ]; then
  echo "PASS: $name ($lines lines) — all mechanical checks passed"
else
  echo ""
  echo "$errs check(s) failed for $name"
  exit 1
fi
