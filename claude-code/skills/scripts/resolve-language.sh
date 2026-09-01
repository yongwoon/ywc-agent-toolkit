#!/usr/bin/env bash
# resolve-language.sh — deterministic output-language resolution.
#
# Precedence (references/language-resolution.md:22-33):
#   --lang flag -> project CLAUDE.md ## Language Policy ->
#   user ~/.claude/CLAUDE.md ## Language Policy -> UNRESOLVED
# The reference's 4th rung ("each consuming skill's existing fallback") is
# each caller's own responsibility, not this script's — the terminal rung
# here is deliberately UNRESOLVED, never a hardcoded 'en'.
#
# Usage:
#   resolve-language.sh [--lang <code-or-full-name>]
#   resolve-language.sh --emit-section <code>
#
# Prints one of ko|ja|en|es|zh|UNRESOLVED (or, for --emit-section, the
# canonical "## Language Policy" block) to stdout. Always exits 0 — a
# malformed, duplicate, or absent policy is never an error, it just falls
# through to the next rung (E1, E3).
#
# YWC_PROJECT_CLAUDE_MD / YWC_USER_CLAUDE_MD override the default paths,
# for tests using fixture directories. Per "Bundled Execution Scripts" in
# claude-code/skills/CLAUDE.md, scripts run from the repo root in
# production, so the project default is the repo-root CLAUDE.md.
set -uo pipefail

PROJECT_CLAUDE_MD="${YWC_PROJECT_CLAUDE_MD:-./CLAUDE.md}"
USER_CLAUDE_MD="${YWC_USER_CLAUDE_MD:-$HOME/.claude/CLAUDE.md}"

# normalize <value> — case-insensitive code-or-full-name -> code, per
# language-resolution.md:61-67. Prints the code and returns 0 on match;
# prints nothing and returns 1 when unrecognized.
normalize() {
  local input
  input=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
  case "$input" in
    ko|korean) echo ko ;;
    ja|japanese) echo ja ;;
    en|english) echo en ;;
    es|spanish) echo es ;;
    zh|chinese) echo zh ;;
    *) return 1 ;;
  esac
}

# emit_section <code> — print the canonical block from
# language-resolution.md:47-53 with <code> substituted verbatim.
emit_section() {
  cat <<EOF
## Language Policy

- **Output language**: $1   <!-- one of: ko | ja | en | es | zh -->
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
EOF
}

# language_policy_code <file> — read the sole "## Language Policy" section
# of <file> and print its normalized Output-language code (return 0), or
# return 1 (no stdout) when the file is missing, has zero or 2+ such
# sections (E3), or the Output-language value is missing/unrecognized
# (E1) — every one of those cases is "absent", never an error.
language_policy_code() {
  local file="$1" count section value
  [ -f "$file" ] || return 1
  count=$(grep -c '^## Language Policy[[:space:]]*$' "$file" 2>/dev/null)
  case "$count" in '' | *[!0-9]*) count=0 ;; esac
  [ "$count" -eq 1 ] || return 1
  section=$(awk '
    /^## Language Policy[ \t]*$/ { found=1; next }
    found && /^## / { exit }
    found { print }
  ' "$file")
  value=$(printf '%s\n' "$section" | grep -i 'output language' | head -n1 |
    sed -E 's/^[^:]*:[[:space:]]*//; s/<!--.*-->//; s/\*//g' | tr -d '[:space:]')
  [ -n "$value" ] || return 1
  normalize "$value"
}

LANG_FLAG=""
EMIT_MODE=0
EMIT_CODE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --lang)
      LANG_FLAG="${2:-}"
      shift
      [ $# -gt 0 ] && shift
      ;;
    --emit-section)
      EMIT_MODE=1
      EMIT_CODE="${2:-}"
      shift
      [ $# -gt 0 ] && shift
      ;;
    *)
      echo "resolve-language.sh: ignoring unrecognized argument: $1" >&2
      shift
      ;;
  esac
done

if [ "$EMIT_MODE" -eq 1 ] && [ -n "$EMIT_CODE" ]; then
  emit_section "$EMIT_CODE"
  exit 0
fi

if [ -n "$LANG_FLAG" ]; then
  CODE=$(normalize "$LANG_FLAG") && [ -n "$CODE" ] && { echo "$CODE"; exit 0; }
fi

CODE=$(language_policy_code "$PROJECT_CLAUDE_MD") && [ -n "$CODE" ] && { echo "$CODE"; exit 0; }
CODE=$(language_policy_code "$USER_CLAUDE_MD") && [ -n "$CODE" ] && { echo "$CODE"; exit 0; }

echo "UNRESOLVED"
exit 0
