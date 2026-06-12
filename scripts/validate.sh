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

rewrite_packaged_skill_paths() {
  local dest_dir="$1"
  local file tmp_file mode

  while IFS= read -r -d '' file; do
    tmp_file="$file.tmp"
    if mode="$(stat -f '%Lp' "$file" 2>/dev/null)"; then
      :
    else
      mode="$(stat -c '%a' "$file")"
    fi
    sed -E \
      -e 's#bash codex/skills/([^[:space:]]+)#bash "${CODEX_HOME:-$HOME/.codex}/skills/\1"#g' \
      -e 's#python codex/skills/([^[:space:]]+)#python "${CODEX_HOME:-$HOME/.codex}/skills/\1"#g' \
      -e 's#cp codex/skills/([^[:space:]]+)#cp "${CODEX_HOME:-$HOME/.codex}/skills/\1"#g' \
      "$file" > "$tmp_file"
    chmod "$mode" "$tmp_file"
    mv "$tmp_file" "$file"
  done < <(find "$dest_dir" -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' \) -print0)
}

build_expected_codex_plugin_skills() {
  local dest_dir="$1"

  mkdir -p "$dest_dir"
  (
    cd codex/skills
    tar -cf - .
  ) | (
    cd "$dest_dir"
    tar -xf -
  )
  rewrite_packaged_skill_paths "$dest_dir"
}

check_path_under_codex_plugin() {
  local field="$1"
  local path="$2"

  [ -n "$path" ] || return 0
  path="${path#./}"
  if [ ! -f ".codex-plugin/$path" ]; then
    echo "ERROR: .codex-plugin/plugin.json references missing interface.$field path: $path"
    ERRORS=$((ERRORS + 1))
  fi
}

check_codex_plugin_manifest() {
  local manifest=".codex-plugin/plugin.json"
  local required field value tmp_dir expected_dir diff_output

  if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: jq is required to validate .codex-plugin/plugin.json"
    ERRORS=$((ERRORS + 1))
    return
  fi

  if [ ! -f "$manifest" ]; then
    echo "ERROR: .codex-plugin/plugin.json is missing"
    ERRORS=$((ERRORS + 1))
    return
  fi

  if ! jq empty "$manifest" >/dev/null 2>&1; then
    echo "ERROR: .codex-plugin/plugin.json is not valid JSON"
    ERRORS=$((ERRORS + 1))
    return
  fi

  required=(name version description author repository license keywords skills interface)
  for field in "${required[@]}"; do
    if ! jq -e --arg field "$field" 'has($field)' "$manifest" >/dev/null; then
      echo "ERROR: .codex-plugin/plugin.json is missing required field: $field"
      ERRORS=$((ERRORS + 1))
    fi
  done

  if [ "$(jq -r '.skills // empty' "$manifest")" != "./skills/" ]; then
    echo "ERROR: .codex-plugin/plugin.json skills must be ./skills/"
    ERRORS=$((ERRORS + 1))
  fi

  required=(displayName shortDescription longDescription developerName category capabilities defaultPrompt websiteURL brandColor)
  for field in "${required[@]}"; do
    if ! jq -e --arg field "$field" '.interface | type == "object" and has($field)' "$manifest" >/dev/null; then
      echo "ERROR: .codex-plugin/plugin.json interface is missing required field: $field"
      ERRORS=$((ERRORS + 1))
    fi
  done

  if ! jq -e '.keywords | type == "array" and length > 0' "$manifest" >/dev/null; then
    echo "ERROR: .codex-plugin/plugin.json keywords must be a non-empty array"
    ERRORS=$((ERRORS + 1))
  fi

  if ! jq -e '.interface.capabilities | type == "array" and length > 0' "$manifest" >/dev/null; then
    echo "ERROR: .codex-plugin/plugin.json interface.capabilities must be a non-empty array"
    ERRORS=$((ERRORS + 1))
  fi

  for field in icon logo composerIcon; do
    value="$(jq -r --arg field "$field" '.interface[$field] // empty' "$manifest")"
    check_path_under_codex_plugin "$field" "$value"
  done

  while IFS= read -r value; do
    check_path_under_codex_plugin "screenshots" "$value"
  done < <(jq -r '.interface.screenshots[]? | strings' "$manifest")

  if [ ! -d .codex-plugin/skills ]; then
    echo "ERROR: .codex-plugin/skills is missing"
    ERRORS=$((ERRORS + 1))
    return
  fi

  if [ ! -f .codex-plugin/skills/ywc-plan/SKILL.md ]; then
    echo "ERROR: .codex-plugin/skills/ywc-plan/SKILL.md is missing"
    ERRORS=$((ERRORS + 1))
  fi

  if [ -n "$(find .codex-plugin/skills -type l -print -quit)" ]; then
    echo "ERROR: .codex-plugin/skills must not contain symlinks"
    ERRORS=$((ERRORS + 1))
  fi

  if rg -n '(bash|python|cp) codex/skills/' .codex-plugin/skills >/tmp/ywc-plugin-unsafe-paths.txt; then
    echo "ERROR: .codex-plugin/skills contains workspace-relative executable command paths"
    sed -n '1,20p' /tmp/ywc-plugin-unsafe-paths.txt
    ERRORS=$((ERRORS + 1))
  fi
  rm -f /tmp/ywc-plugin-unsafe-paths.txt

  if [ -f codex/skills/ywc-plan/SKILL.md ] && [ -f .codex-plugin/skills/ywc-plan/SKILL.md ]; then
    if ! diff -u \
      <(sed -n '/^---$/,/^---$/p' codex/skills/ywc-plan/SKILL.md) \
      <(sed -n '/^---$/,/^---$/p' .codex-plugin/skills/ywc-plan/SKILL.md) >/dev/null; then
      echo "ERROR: .codex-plugin/skills/ywc-plan/SKILL.md frontmatter does not match source codex/skills/ywc-plan/SKILL.md"
      ERRORS=$((ERRORS + 1))
    fi
  fi

  tmp_dir="$(mktemp -d)"
  expected_dir="$tmp_dir/skills"
  build_expected_codex_plugin_skills "$expected_dir"

  if ! diff_output="$(diff -qr "$expected_dir" .codex-plugin/skills)"; then
    echo "ERROR: .codex-plugin/skills is stale; run: bash scripts/sync-codex-plugin.sh"
    printf '%s\n' "$diff_output" | sed -n '1,20p'
    ERRORS=$((ERRORS + 1))
  fi

  if ! diff -u \
    <(find codex/skills -type f -perm -111 | sed 's#^codex/skills/##' | sort) \
    <(find .codex-plugin/skills -type f -perm -111 | sed 's#^.codex-plugin/skills/##' | sort) >/dev/null; then
    echo "ERROR: .codex-plugin/skills executable file modes do not match codex/skills"
    ERRORS=$((ERRORS + 1))
  fi

  rm -rf "$tmp_dir"
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

echo "==> Validating codex skills..."
for dir in codex/skills/*/; do
  [ -d "$dir" ] || continue
  is_skill_dir "$dir" || continue
  check_codex_skill_dir "$dir"
done
check_codex_support_dirs
check_codex_plan_handoff

echo "==> Validating Codex plugin package..."
check_codex_plugin_manifest

echo "==> Checking install script (dry run)..."
bash scripts/install.sh --list > /dev/null

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "Validation failed: $ERRORS error(s) found."
  exit 1
fi

echo "All checks passed."
