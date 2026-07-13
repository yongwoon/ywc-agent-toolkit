#!/usr/bin/env bash
# Mechanical authoring gate for a single ywc-* skill directory — the
# deterministic subset of the ywc-skill-author A1–A14 checklist. Complements the
# repo-wide scripts/validate.sh (which only checks frontmatter presence + README
# set across all skills) by enforcing the per-skill authoring rules at edit time.
# Exit 1 on any failure.
#
# Usage: bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh <skill-dir>
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
#
# Bounded to the frontmatter block (stops at the closing `---`) and matches
# hyphenated top-level keys (e.g. `allowed-tools:`), mirroring
# score.py::split_frontmatter() + parse_yaml_lite(). Without both, a skill
# whose `description:` is the last frontmatter key swallows the entire body,
# and a hyphenated key immediately after `description:` gets swallowed into
# the value.
desc_text="$(awk '
  /^---[[:space:]]*$/ { infm++; if (infm == 2) { exit }; next }
  infm != 1 { next }
  /^description:/ { sub(/^description:[[:space:]]*[>|]?-?[[:space:]]*/, ""); f=1; print; next }
  f && /^[A-Za-z_][A-Za-z0-9_-]*:/ { f=0 }
  f { print }
' "$SKILL" | tr '\n' ' ' | tr -s ' ')"
# Trim leading/trailing whitespace so the awk-joined text matches score.py's
# str.startswith() exactly (a leading space from folded-scalar joining would
# otherwise desync this check from the canonical CI judge).
desc_text="$(printf '%s' "$desc_text" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

# Strip a single pair of matching outer quotes, mirroring score.py's
# _unquote_scalar. Some skills (e.g. ywc-project-docs, ywc-e2e-test-strategy)
# use a quoted single-line `description: "..."` scalar; without this, desc_text
# starts with a literal '"' and every check below silently desyncs from the
# canonical CI judge (A2's startswith match fails on a value that is actually
# well-formed).
case "$desc_text" in
  \"*\") desc_text="${desc_text#\"}"; desc_text="${desc_text%\"}"; desc_text="${desc_text//\\\"/\"}" ;;
  \'*\') desc_text="${desc_text#\'}"; desc_text="${desc_text%\'}"; desc_text="${desc_text//\'\'/\'}" ;;
esac

# A2/A3 (unified with score.py:286-287, the canonical CI judge — 000059-020).
# Opener must start with the literal stem "(ywc) Use when" (not a substring
# match, not "Use before/after/during"). Anti-trigger must match
# "Do not use (for|during|when|in)" — "Do not invoke" is no longer accepted;
# it passed here previously but always failed score.py's A3.
case "$desc_text" in "(ywc) Use when"*) ;; *) fail "description does not start with '(ywc) Use when' (A2)" ;; esac
printf '%s' "$desc_text" | grep -qE 'Do not use (for|during|when|in)\b' \
  || fail "description missing 'Do not use (for|during|when|in) ...' anti-trigger (A3)"

# A15 (description word cap, FR-5/AC12 — 000059-020). Boundary inclusive:
# 80 PASS, 81 FAIL. Word count via bash IFS splitting (locale-independent,
# unlike `wc -w`, which disagrees with itself across locales on CJK-heavy
# text). Enforcement mode follows the skill-pruning-pilot evidence gate
# (docs/ywc-plans/prune-report-rationalization-defense.md): the pilot run
# concluded INCONCLUSIVE (pooled floor_rate 0.5333 > 0.25 ceiling), so this
# check is advisory (warn, do not fail the build) until a future pilot run
# reaches a VALID ceiling and passes AC9's evidence gate.
# shellcheck disable=SC2086 # intentional word-splitting for a locale-independent count
set -- $desc_text
word_count="$#"
if [ "$word_count" -gt 80 ]; then
  echo "WARN: description is $word_count words (> 80 word cap) [advisory — skill-pruning-pilot run was INCONCLUSIVE, see docs/ywc-plans/prune-report-rationalization-defense.md]"
fi

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
