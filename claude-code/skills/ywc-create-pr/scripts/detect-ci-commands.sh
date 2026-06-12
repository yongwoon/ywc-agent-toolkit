#!/usr/bin/env bash
# Detect candidate pre-push CI check commands for ywc-create-pr Step 5, in the
# documented priority order (workflows > CLAUDE.md > package.json > Makefile)
# plus the package manager from the lockfile. Best-effort extraction — the skill
# still selects and runs; this removes the per-run re-derivation of the same
# greps and the package-manager guess.
#
# Usage: bash claude-code/skills/ywc-create-pr/scripts/detect-ci-commands.sh [repo-dir]
set -uo pipefail

ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || { echo "error: cannot cd to $ROOT" >&2; exit 1; }

CHECK_RE='lint|format|typecheck|type-check|test|check'
EXCLUDE_RE='deploy|release|publish|docker[ _-]?(build|push)'

pm="unknown"
[ -f package-lock.json ] && pm="npm"
[ -f yarn.lock ] && pm="yarn"
[ -f pnpm-lock.yaml ] && pm="pnpm"
[ -f bun.lockb ] && pm="bun"
echo "package_manager: $pm"

# Command-runner tokens: lets us pick command lines out of `run: |` multi-line
# blocks (where the command sits on an indented line, not the `run:` line).
RUNNER_RE='npm |pnpm |yarn |bun |npx |make |go |cargo |pytest|tsc|eslint|ruff|golangci|jest|vitest|playwright|mvn |gradle|bash |sh '

echo "from_workflows:"
if [ -d .github/workflows ]; then
  grep -rhE "($RUNNER_RE)" .github/workflows 2>/dev/null \
    | sed -E 's/^[[:space:]]*(run:[[:space:]]*)?//; s/^[|>-][[:space:]]*//' \
    | grep -iE "$CHECK_RE" | grep -ivE "$EXCLUDE_RE" \
    | sort -u | head -15 | sed 's/^/  - /'
fi

echo "from_claude_md:"
if [ -f CLAUDE.md ]; then
  grep -niE "($CHECK_RE).*(command|: \`|npm |pnpm |yarn |make )" CLAUDE.md 2>/dev/null \
    | grep -ivE "$EXCLUDE_RE" | head -10 | sed 's/^/  L/'
fi

echo "from_package_json_scripts:"
if [ -f package.json ]; then
  # Extract "key": "value" pairs whose key matches a check category.
  grep -oE '"[A-Za-z:_-]+"[[:space:]]*:[[:space:]]*"[^"]*"' package.json 2>/dev/null \
    | grep -iE "^\"($CHECK_RE)" | grep -ivE "$EXCLUDE_RE" \
    | sed -E 's/^"([^"]+)".*/  - '"$pm"' run \1/' | sort -u
fi

echo "from_makefile:"
if [ -f Makefile ]; then
  grep -oE '^(lint|format|check|test)[A-Za-z_-]*:' Makefile 2>/dev/null \
    | sed -E 's/:$//; s/^/  - make /' | sort -u
fi
