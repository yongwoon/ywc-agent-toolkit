#!/usr/bin/env bash
# Detect candidate pre-push CI check commands for ywc-create-pr Step 5, in the
# documented priority order (workflows > CLAUDE.md > package.json > Makefile)
# plus the package manager from the lockfile. Best-effort extraction — the skill
# still selects and runs; this removes the per-run re-derivation of the same
# greps and the package-manager guess.
#
# Usage: bash codex/skills/ywc-create-pr/scripts/detect-ci-commands.sh [repo-dir]
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
  # Parse only the "scripts" object (not the whole file) so non-script keys
  # never become bogus `pm run <key>` candidates. Silent no-op if python3 or
  # the JSON is unavailable.
  python3 - "$pm" "$CHECK_RE" "$EXCLUDE_RE" <<'PY' 2>/dev/null
import json, re, sys
pm, check_re, exclude_re = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    scripts = json.load(open("package.json")).get("scripts", {})
except Exception:
    scripts = {}
check = re.compile(check_re, re.I)
exclude = re.compile(exclude_re, re.I)
for key in sorted(scripts):
    if check.search(key) and not exclude.search(key):
        print(f"  - {pm} run {key}")
PY
fi

echo "from_makefile:"
if [ -f Makefile ]; then
  grep -oE '^(lint|format|check|test)[A-Za-z_-]*:' Makefile 2>/dev/null \
    | sed -E 's/:$//; s/^/  - make /' | sort -u
fi
