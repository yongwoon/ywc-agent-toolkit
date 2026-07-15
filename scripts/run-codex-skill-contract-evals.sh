#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
ERRORS=0

fail() {
  echo "ERROR: $1"
  ERRORS=$((ERRORS + 1))
}

require_file() {
  local file="$1"
  [ -f "$file" ] || {
    fail "missing file: ${file#$ROOT/}"
    return 1
  }
}

require_json_shape() {
  local file="$1"
  local rel="${file#$ROOT/}"

  require_file "$file" || return 0

  if ! jq empty "$file" >/dev/null 2>&1; then
    fail "$rel is not valid JSON"
    return 0
  fi

  if ! jq -e '.skill_name | type == "string" and length > 0' "$file" >/dev/null 2>&1; then
    fail "$rel is missing a non-empty skill_name"
  fi

  if ! jq -e '.evals | type == "array"' "$file" >/dev/null 2>&1; then
    fail "$rel is missing an evals array"
  fi

  if ! jq -e '
    .evals
    | all(
        (.id | type == "number")
        and (.prompt | type == "string" and length > 0)
      )
  ' "$file" >/dev/null 2>&1; then
    fail "$rel has an eval item without numeric id or non-empty prompt"
  fi

  if ! jq -e '
    (.evals | map(.id) | length) == (.evals | map(.id) | unique | length)
  ' "$file" >/dev/null 2>&1; then
    fail "$rel contains duplicate eval ids"
  fi

  if ! jq -e '
    all(
      .evals[];
      (
        (.files? == null or (.files | type == "array"))
        and (.expected_behavior? == null or (.expected_behavior | type == "array"))
        and (.anti_behavior? == null or (.anti_behavior | type == "array"))
        and (.expectations? == null or (.expectations | type == "array"))
        and (.context? == null or (.context | type == "object"))
      )
    )
  ' "$file" >/dev/null 2>&1; then
    fail "$rel contains an eval item with an invalid optional field type"
  fi
}

require_tokens() {
  local file="$1"
  shift
  local rel="${file#$ROOT/}"
  local raw

  require_file "$file" || return 0
  raw="$(cat "$file")"
  for token in "$@"; do
    if ! printf '%s' "$raw" | grep -Fq -- "$token"; then
      fail "$rel is missing required token: $token"
    fi
  done
}

check_all_eval_json() {
  local file
  while IFS= read -r file; do
    [ -n "$file" ] || continue
    require_json_shape "$file"
  done < <(find "$ROOT/codex/skills" -path '*/evals/evals.json' -type f | sort)
}

check_preview_contracts() {
  local tg_skill="$ROOT/codex/skills/ywc-task-generator/SKILL.md"
  local tg_evals="$ROOT/codex/skills/ywc-task-generator/evals/evals.json"
  local agentic_skill="$ROOT/codex/skills/ywc-agentic/SKILL.md"
  local agentic_evals="$ROOT/codex/skills/ywc-agentic/evals/evals.json"

  if grep -Fq -- '--preview-only' "$tg_skill"; then
    require_tokens "$tg_evals" "--preview-only" "--spec" "NEEDS_CONTEXT"
  fi

  if grep -Fq -- '--approve-preview' "$tg_skill"; then
    require_tokens "$tg_evals" "--approve-preview" "digest" "revision"
  fi

  if grep -Fq -- '--approve-preview' "$agentic_skill"; then
    require_tokens "$agentic_evals" "--spec" "preview" "NEEDS_CONTEXT"
  fi
}

check_wayfinder_contracts() {
  local wayfinder_dir="$ROOT/codex/skills/ywc-wayfinder"
  local wayfinder_evals="$wayfinder_dir/evals/evals.json"
  local plan_evals="$ROOT/codex/skills/ywc-plan/evals/evals.json"
  local brainstorm_evals="$ROOT/codex/skills/ywc-brainstorm/evals/evals.json"

  [ -d "$wayfinder_dir" ] || return 0

  require_json_shape "$wayfinder_evals"
  require_tokens "$wayfinder_evals" "active ticket" "NEEDS_CONTEXT" "DONE"

  if grep -Fq -- 'ywc-wayfinder' "$plan_evals"; then
    require_tokens "$plan_evals" "ywc-wayfinder"
  else
    echo "INFO: wayfinder routing eval tokens are deferred in ywc-plan until routing catalog assets land."
  fi

  if grep -Fq -- 'ywc-wayfinder' "$brainstorm_evals"; then
    require_tokens "$brainstorm_evals" "ywc-wayfinder"
  else
    echo "INFO: wayfinder routing eval tokens are deferred in ywc-brainstorm until routing catalog assets land."
  fi
}

check_research_persistence_contracts() {
  local skill="$ROOT/codex/skills/ywc-tech-research/SKILL.md"
  local evals="$ROOT/codex/skills/ywc-tech-research/evals/evals.json"

  if grep -Fq -- '--output' "$skill"; then
    require_tokens "$evals" "--output" "overwrite" "provenance"
  fi

  if grep -Fq -- '--confirm-overwrite' "$skill"; then
    require_tokens "$evals" "--confirm-overwrite" "--non-interactive"
  fi
}

check_all_eval_json
check_wayfinder_contracts
check_preview_contracts
check_research_persistence_contracts

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "Contract eval validation failed: $ERRORS error(s) found."
  exit 1
fi

echo "PASS: Codex skill contract evals are structurally valid."
