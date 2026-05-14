#!/usr/bin/env bash
# Local validation script — mirrors the logic in .github/workflows/validate.yml.
# Usage: bash scripts/validate.sh
set -euo pipefail

ERRORS=0

check_skill_dir() {
  local dir="$1"
  local name
  name="$(basename "$dir")"
  local skill_md="${dir}SKILL.md"

  if [ ! -f "$skill_md" ]; then
    echo "ERROR: $name is missing SKILL.md"
    ERRORS=$((ERRORS + 1))
    return
  fi

  if ! grep -q "^name:" "$skill_md"; then
    echo "ERROR: $name/SKILL.md is missing 'name:' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  if ! grep -q "^description:" "$skill_md"; then
    echo "ERROR: $name/SKILL.md is missing 'description:' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  local declared_name
  declared_name="$(sed -n 's/^name:[[:space:]]*//p' "$skill_md" | head -n 1)"
  if [ "$declared_name" != "$name" ]; then
    echo "ERROR: $name/SKILL.md name '$declared_name' does not match directory name"
    ERRORS=$((ERRORS + 1))
  fi
}

check_readme_set() {
  local dir="$1"
  local name
  name="$(basename "$dir")"
  local file
  for file in README.md README.en.md README.ja.md README.ko.md; do
    if [ ! -f "$dir$file" ]; then
      echo "ERROR: $name is missing $file"
      ERRORS=$((ERRORS + 1))
    fi
  done
}

check_codex_skill_dir() {
  local dir="$1"
  local name
  name="$(basename "$dir")"

  check_skill_dir "$dir"
  check_readme_set "$dir"

  if [ ! -f "${dir}agents/openai.yaml" ]; then
    echo "ERROR: $name is missing agents/openai.yaml"
    ERRORS=$((ERRORS + 1))
  fi

  local frontmatter
  frontmatter="$(awk '
    NR == 1 && $0 == "---" { in_fm = 1; next }
    in_fm && $0 == "---" { exit }
    in_fm { print }
  ' "${dir}SKILL.md")"
  if printf '%s\n' "$frontmatter" | grep -Eq '^(version|category|phase|requires|advisor_budget|allowed tools):'; then
    echo "ERROR: $name/SKILL.md has non-Codex frontmatter fields"
    ERRORS=$((ERRORS + 1))
  fi
}

echo "==> Validating claude-code skills..."
for dir in claude-code/skills/*/; do
  if [ -d "$dir" ]; then
    check_skill_dir "$dir"
    check_readme_set "$dir"
  fi
done

echo "==> Validating codex skills..."
for dir in codex/skills/*/; do
  [ -d "$dir" ] && check_codex_skill_dir "$dir"
done

echo "==> Checking install script (dry run)..."
bash scripts/install.sh --list > /dev/null

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "Validation failed: $ERRORS error(s) found."
  exit 1
fi

echo "All checks passed."
