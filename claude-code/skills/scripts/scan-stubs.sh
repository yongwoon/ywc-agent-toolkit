#!/usr/bin/env bash
# Scan files for banned stub / placeholder patterns that make generated code a
# runtime error rather than deferred work. Shared by ywc-code-gen (Banned Output
# Patterns) and ywc-sequential-executor (Completeness Gate). Exit 1 if any found.
#
# Usage:
#   bash claude-code/skills/scripts/scan-stubs.sh <file> [<file>...]
#   bash claude-code/skills/scripts/scan-stubs.sh --range <git-ref>   # files changed since <ref>
#
# Only high-confidence comment/marker stubs are gated here. Bare `...` / `pass`
# and prose shortcuts ("for brevity...") are deliberately NOT grepped — they
# false-positive on legitimate Python stubs and documentation, so the reviewer
# judges those.
set -uo pipefail

files=""
if [ "${1:-}" = "--range" ]; then
  base="${2:-}"
  [ -n "$base" ] || { echo "usage: scan-stubs.sh --range <git-ref>" >&2; exit 2; }
  # Validate the ref first — otherwise an invalid base yields an empty file list
  # and the gate exits 0 (false pass), silently disabling stub detection.
  git rev-parse --verify "$base^{commit}" >/dev/null 2>&1 || {
    echo "error: invalid git ref: $base" >&2; exit 2
  }
  if ! files="$(git diff --name-only "$base"...HEAD)"; then
    echo "error: failed to collect changed files for range $base...HEAD" >&2; exit 2
  fi
elif [ "$#" -gt 0 ]; then
  printf -v files '%s\n' "$@"
else
  echo "usage: scan-stubs.sh <file>... | --range <git-ref>" >&2
  exit 2
fi

# ERE of high-confidence code-stub markers across common languages.
pattern='TODO:[[:space:]]*implement|FIXME|Not implemented|NotImplementedError|todo!\(\)|unimplemented!\(\)|YOUR_VALUE_HERE|<replace_me>|//[[:space:]]*\.\.\.[[:space:]]*rest of code|//[[:space:]]*same as|//[[:space:]]*follows the same pattern'

found=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  [ -f "$f" ] || continue
  if matches="$(grep -nE "$pattern" "$f" 2>/dev/null)" && [ -n "$matches" ]; then
    printf '%s\n' "$matches" | sed "s|^|$f:|"
    found=1
  fi
done <<EOF
$files
EOF

if [ "$found" -eq 0 ]; then
  echo "no stub patterns found"
fi
exit "$found"
