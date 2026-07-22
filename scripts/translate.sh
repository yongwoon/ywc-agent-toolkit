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
#   - claude CLI, signed in (`claude auth status` must report loggedIn)
#   - jq (brew install jq)
#
# Runs on the Claude subscription via `claude -p`. This script deliberately does
# NOT use ANTHROPIC_API_KEY or call api.anthropic.com directly — project policy
# is subscription-only operation.
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
  command -v jq >/dev/null 2>&1 || die "jq is required (brew install jq)"
  [ -f "$TRANSLATIONS_JSON" ]    || die "translations.json not found at $TRANSLATIONS_JSON"
  $DRY_RUN && return 0

  command -v claude >/dev/null 2>&1 || die "claude CLI is required (subscription-based translation)"

  # Fail fast on auth rather than after N wasted invocations. `auth status` is a
  # local read — it costs no model usage.
  local auth
  auth="$(claude auth status 2>/dev/null)" \
    || die "could not read 'claude auth status' — is the CLI installed correctly?"
  [ "$(printf '%s' "$auth" | jq -r '.loggedIn // false')" = "true" ] \
    || die "claude CLI is not signed in. Run: claude auth login"
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

  local instruction
  instruction="Translate the Markdown documentation supplied on stdin into ${lang_label}.

Rules:
- Keep all code blocks, file paths, command examples, and YAML frontmatter exactly as-is
- Translate only natural language text (headings, paragraphs, table cells, list items)
- Preserve all Markdown formatting (headers, bold, italics, tables, lists)
- Do not add explanatory text or notes
- Output only the translated Markdown, nothing else"

  # The document goes over stdin rather than as an argument: READMEs are
  # arbitrarily large, and this sidesteps ARG_MAX and every quoting hazard.
  #
  # --disable-slash-commands: translation needs no skill. Without it the whole
  # installed skill catalogue is loaded into context on every call, which is
  # pure cost for a text-transform task.
  local response status
  set +e
  response="$(printf '%s' "$content" \
    | claude -p "$instruction" \
        --model "$MODEL" \
        --disable-slash-commands \
        --output-format json 2>/dev/null)"
  status=$?
  set -e

  if [ $status -ne 0 ]; then
    echo "claude CLI exited $status while translating to ${lang_label}" >&2
    return 1
  fi

  if [ "$(printf '%s' "$response" | jq -r '.is_error // false')" = "true" ]; then
    echo "translation failed (${lang_label}): $(printf '%s' "$response" | jq -r '.result // "unknown"')" >&2
    return 1
  fi

  local text
  text="$(printf '%s' "$response" | jq -r '.result // empty')"
  [ -n "$text" ] || {
    echo "translation returned no content (${lang_label})" >&2
    return 1
  }

  printf '%s' "$text"
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
  sed -n '3,18p' "$0" | sed 's/^# \{0,1\}//'
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
