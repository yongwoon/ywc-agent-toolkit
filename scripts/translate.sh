#!/usr/bin/env bash
#
# AI-assisted translation script for ywc-agent-toolkit
#
# Usage:
#   bash scripts/translate.sh                          Translate all skills (tier2 languages)
#   bash scripts/translate.sh --lang es               Translate to Spanish only
#   bash scripts/translate.sh --skill ywc-plan        Translate a single skill
#   bash scripts/translate.sh --codex                 Translate Codex skills only
#   bash scripts/translate.sh --dry-run               Print what would be translated
#
# Requirements:
#   - ANTHROPIC_API_KEY env var must be set
#   - jq (brew install jq)
#   - curl
#
# Language codes are read from translations.json (tier2.codes).
# Generated files are marked with an auto-translation notice at the top.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRANSLATIONS_JSON="$REPO_ROOT/translations.json"
CC_SRC="$REPO_ROOT/claude-code/skills"
CODEX_SRC="$REPO_ROOT/codex/skills"
MODEL="claude-haiku-4-5-20251001"
DRY_RUN=false
TARGET_LANG=""
TARGET_SKILL=""
CODEX_ONLY=false

# ---- helpers ----------------------------------------------------------------

die() { echo "ERROR: $*" >&2; exit 1; }

check_deps() {
  command -v jq   >/dev/null 2>&1 || die "jq is required (brew install jq)"
  command -v curl >/dev/null 2>&1 || die "curl is required"
  $DRY_RUN || [ -n "${ANTHROPIC_API_KEY:-}" ] || die "ANTHROPIC_API_KEY is not set"
  [ -f "$TRANSLATIONS_JSON" ]      || die "translations.json not found at $TRANSLATIONS_JSON"
}

lang_name() {
  case "$1" in
    es) echo "Spanish" ;;
    zh) echo "Chinese (Simplified)" ;;
    fr) echo "French" ;;
    de) echo "German" ;;
    pt) echo "Portuguese" ;;
    *)  echo "$1" ;;
  esac
}

auto_notice() {
  local lang="$1"
  cat <<EOF
<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: $(lang_name "$lang") -->

EOF
}

translate_content() {
  local content="$1"
  local lang="$2"
  local lang_label
  lang_label="$(lang_name "$lang")"

  local payload
  payload="$(jq -n \
    --arg model "$MODEL" \
    --arg lang "$lang_label" \
    --arg content "$content" \
    '{
      model: $model,
      max_tokens: 4096,
      messages: [{
        role: "user",
        content: ("Translate the following Markdown documentation into " + $lang + ".\n\nRules:\n- Keep all code blocks, file paths, command examples, and YAML frontmatter exactly as-is\n- Translate only natural language text (headings, paragraphs, table cells, list items)\n- Preserve all Markdown formatting (headers, bold, italics, tables, lists)\n- Do not add explanatory text or notes\n- Output only the translated Markdown, nothing else\n\n" + $content)
      }]
    }')"

  local response
  response="$(curl -s https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$payload")"

  echo "$response" | jq -r '.content[0].text // empty' || {
    echo "API error: $(echo "$response" | jq -r '.error.message // "unknown"')" >&2
    return 1
  }
}

translate_file() {
  local src="$1"
  local lang="$2"
  local dest
  dest="$(dirname "$src")/README.${lang}.md"

  if $DRY_RUN; then
    echo "[dry-run] Would translate: $src → $dest"
    return
  fi

  echo "  Translating $(basename "$(dirname "$src")")/README.en.md → README.${lang}.md ..."
  local content
  content="$(cat "$src")"

  local translated
  translated="$(translate_content "$content" "$lang")" || return 1

  { auto_notice "$lang"; echo "$translated"; } > "$dest"
  echo "  ✓ Written: $dest"
}

# ---- main -------------------------------------------------------------------

usage() {
  sed -n '3,15p' "$0" | sed 's/^# \{0,1\}//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lang)    TARGET_LANG="$2"; shift 2 ;;
    --skill)   TARGET_SKILL="$2"; shift 2 ;;
    --codex)   CODEX_ONLY=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help|-h) usage; exit 0 ;;
    *) die "Unknown option: $1. Use --help for usage." ;;
  esac
done

check_deps

# Determine languages to process
if [ -n "$TARGET_LANG" ]; then
  LANGS=("$TARGET_LANG")
else
  mapfile -t LANGS < <(jq -r '.languages.tier2.codes[]' "$TRANSLATIONS_JSON")
fi

echo "Languages: ${LANGS[*]}"
echo ""

# ---- skill translation ------------------------------------------------------

translate_skill_tree() {
  local label="$1"
  local src_root="$2"

  echo "=== $label skills ==="
  local found=false
  local skill_dir
  for skill_dir in "$src_root"/*/; do
    [ -d "$skill_dir" ] || continue

    local skill_name
    skill_name="$(basename "$skill_dir")"
    [ -n "$TARGET_SKILL" ] && [ "$skill_name" != "$TARGET_SKILL" ] && continue

    local src="${skill_dir%/}/README.en.md"
    [ -f "$src" ] || continue

    found=true
    echo "[$skill_name]"
    for lang in "${LANGS[@]}"; do
      translate_file "$src" "$lang"
    done
  done

  if ! $found && [ -n "$TARGET_SKILL" ]; then
    echo "  ! $TARGET_SKILL not found under $src_root" >&2
  fi
  echo ""
}

if $CODEX_ONLY; then
  translate_skill_tree "Codex" "$CODEX_SRC"
else
  translate_skill_tree "Codex" "$CODEX_SRC"
  translate_skill_tree "Claude Code" "$CC_SRC"
fi

echo ""
echo "Done."
