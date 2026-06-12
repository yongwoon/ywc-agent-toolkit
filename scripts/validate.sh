#!/usr/bin/env bash
# Local validation script — mirrors the logic in .github/workflows/validate.yml.
# Usage: bash scripts/validate.sh
set -euo pipefail

ERRORS=0

is_skill_dir() {
  [ -f "$1/SKILL.md" ]
}

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

check_codex_support_dirs() {
  local ref

  if [ ! -d codex/skills/references ]; then
    echo "ERROR: codex/skills/references is missing"
    ERRORS=$((ERRORS + 1))
  fi

  if [ ! -d codex/skills/scripts ]; then
    echo "ERROR: codex/skills/scripts is missing"
    ERRORS=$((ERRORS + 1))
  fi

  if [ ! -x codex/skills/scripts/poll-pr-reviews.sh ]; then
    echo "ERROR: codex/skills/scripts/poll-pr-reviews.sh is missing or not executable"
    ERRORS=$((ERRORS + 1))
  fi

  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    if [ ! -f "codex/skills/references/$ref" ]; then
      echo "ERROR: codex shared reference is missing: references/$ref"
      ERRORS=$((ERRORS + 1))
    fi
  done < <(
    {
      rg -o '\.\./references/[A-Za-z0-9._-]+' codex/skills || true
      rg -o 'codex/skills/references/[A-Za-z0-9._-]+' codex/skills || true
    } | sed -E 's#^.*references/##' | sort -u
  )
}

check_codex_plan_handoff() {
  local file="codex/skills/ywc-plan/SKILL.md"

  if [ ! -f "$file" ]; then
    return
  fi

  if rg -n '/ywc-(spec-validate|task-generator|code-gen|sequential-executor|parallel-executor)' "$file"; then
    echo "ERROR: codex/skills/ywc-plan/SKILL.md must use Codex-style \$ywc-* handoff commands, not Claude Code slash commands"
    ERRORS=$((ERRORS + 1))
  fi
}

check_agent_file() {
  local file="$1"
  local base
  base="$(basename "$file" .md)"

  if ! grep -q "^name:" "$file"; then
    echo "ERROR: agents/$base.md is missing 'name:' in frontmatter"
    ERRORS=$((ERRORS + 1))
    return
  fi

  if ! grep -q "^description:" "$file"; then
    echo "ERROR: agents/$base.md is missing 'description:' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  local declared_name
  declared_name="$(sed -n 's/^name:[[:space:]]*//p' "$file" | head -n 1)"
  if [ "$declared_name" != "$base" ]; then
    echo "ERROR: agents/$base.md name '$declared_name' does not match filename"
    ERRORS=$((ERRORS + 1))
  fi
}

check_cc_support_dirs() {
  local ref

  if [ ! -d claude-code/skills/references ]; then
    echo "ERROR: claude-code/skills/references is missing"
    ERRORS=$((ERRORS + 1))
  fi

  if [ ! -d claude-code/skills/scripts ]; then
    echo "ERROR: claude-code/skills/scripts is missing"
    ERRORS=$((ERRORS + 1))
  fi

  if [ ! -x claude-code/skills/scripts/poll-pr-reviews.sh ]; then
    echo "ERROR: claude-code/skills/scripts/poll-pr-reviews.sh is missing or not executable"
    ERRORS=$((ERRORS + 1))
  fi

  # Every ../references/<file> link must resolve relative to the file that
  # contains it. From a SKILL.md this points at the shared references dir; from
  # a skill-local references/*.md it points back at that same local dir. We
  # resolve per-source-file so both cases are validated without false positives.
  # This catches the broken-link regression class that frontmatter checks miss.
  local file link target
  while IFS= read -r file; do
    [ -n "$file" ] || continue
    while IFS= read -r link; do
      [ -n "$link" ] || continue
      target="$(dirname "$file")/$link"
      if [ ! -f "$target" ]; then
        echo "ERROR: broken reference link in ${file#./}: $link"
        ERRORS=$((ERRORS + 1))
      fi
    done < <(grep -oE '(\.\./)+references/[A-Za-z0-9._-]+\.md' "$file" | sort -u)
  done < <(grep -rlE '(\.\./)+references/[A-Za-z0-9._-]+\.md' claude-code/skills --include='*.md')
}

check_cc_agents() {
  local dir=claude-code/agents
  [ -d "$dir" ] || return 0

  # Catalog README locale set must be present
  local file
  for file in README.md README.en.md README.ja.md README.ko.md; do
    if [ ! -f "$dir/$file" ]; then
      echo "ERROR: claude-code/agents is missing $file"
      ERRORS=$((ERRORS + 1))
    fi
  done

  # Each ywc-*.md agent file must have valid frontmatter
  for file in "$dir"/ywc-*.md; do
    [ -f "$file" ] || continue
    check_agent_file "$file"
  done
}

echo "==> Validating claude-code skills..."
for dir in claude-code/skills/*/; do
  [ -d "$dir" ] || continue
  is_skill_dir "$dir" || continue
  check_skill_dir "$dir"
  check_readme_set "$dir"
done

echo "==> Validating claude-code agents..."
check_cc_agents
check_cc_support_dirs

echo "==> Validating codex skills..."
for dir in codex/skills/*/; do
  [ -d "$dir" ] || continue
  is_skill_dir "$dir" || continue
  check_codex_skill_dir "$dir"
done
check_codex_support_dirs
check_codex_plan_handoff

echo "==> Checking install script (dry run)..."
bash scripts/install.sh --list > /dev/null

# Mirror the CI mechanical-regression gate locally so a score drop is caught
# before push, not only in CI (.github/workflows/validate.yml runs the same gate).
if [ -f .claude/skills/ywc-toolkit-eval/scripts/score.py ]; then
  echo "==> Running ywc-toolkit-eval mechanical regression gate..."
  python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci || ERRORS=$((ERRORS + 1))
fi

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "Validation failed: $ERRORS error(s) found."
  exit 1
fi

echo "All checks passed."
