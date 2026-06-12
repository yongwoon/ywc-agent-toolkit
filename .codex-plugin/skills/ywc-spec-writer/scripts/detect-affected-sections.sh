#!/usr/bin/env bash
# Maps changed file paths to spec sections that need updating.
# Input:  git diff --name-only output via stdin
# Output: newline-separated spec section filenames (e.g., "02-features.md\n03-data.md")
# Exit 0: one or more sections detected
# Exit 1: no spec-relevant changes found
#
# Usage:
#   git diff HEAD~1 --name-only | bash detect-affected-sections.sh
#   git diff --cached --name-only | bash detect-affected-sections.sh

declare -A seen

add_section() {
  local section="$1"
  if [[ -z "${seen[$section]}" ]]; then
    seen[$section]=1
    echo "$section"
  fi
}

while IFS= read -r file; do
  # Skip spec files themselves and pure documentation
  [[ "$file" == docs/specification/* ]] && continue
  [[ "$file" =~ ^(README|CLAUDE|AGENTS|CODEX)\.md$ ]] && continue
  [[ "$file" == docs/ywc-plans/* ]] && continue

  case "$file" in
    # Data model: schema, migrations, models, entities
    *schema* | *migration* | prisma/* | */migrations/* | *model* | *entity* | *entities/*)
      add_section "03-data.md"
      ;;
    # External interfaces: routes, API, controllers, endpoints
    *routes/* | */api/* | *endpoint* | *controller* | *handler*)
      add_section "04-interfaces.md"
      add_section "02-features.md"
      ;;
    # User flows: UI components, pages, views, screens
    *component* | *page* | *view* | *screen* | */ui/* | */frontend/*)
      add_section "05-user-flows.md"
      add_section "02-features.md"
      ;;
    # Business logic: services, usecases, domain
    *service* | *usecase* | */domain/* | */application/*)
      add_section "02-features.md"
      ;;
    # Non-functional: infra, config, env, CI/CD
    *infra/* | *deploy/* | *.env* | *config* | *settings* | *.yml | *.yaml)
      add_section "06-requirements.md"
      ;;
    # Any other code file -> features
    *.ts | *.tsx | *.js | *.jsx | *.py | *.go | *.rs | *.java | *.kt | *.rb | *.php | *.cs)
      add_section "02-features.md"
      ;;
  esac
done

if [[ ${#seen[@]} -gt 0 ]]; then
  exit 0
else
  exit 1
fi
