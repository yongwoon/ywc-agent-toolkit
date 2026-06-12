#!/usr/bin/env bash
# scan-secrets.sh [--staged] [--committed <base-branch>]
#
# Scans git diff for secret patterns across three phases:
#   Phase 1 — dangerous file names (.env, .pem, credentials.*, etc.)
#   Phase 2 — staged + unstaged diff content (secret regex patterns)
#   Phase 3 — committed diff vs base branch (when --committed is given)
#
# Exit codes:
#   0  No secrets detected
#   1  Secrets or dangerous files found (details on stdout)
#   2  Usage error
#
# Usage:
#   # Scan staged + unstaged changes
#   bash codex/skills/ywc-create-pr/scripts/scan-secrets.sh --staged
#
#   # Also scan all commits vs base branch
#   bash codex/skills/ywc-create-pr/scripts/scan-secrets.sh --committed develop

set -uo pipefail

MODE="staged"
BASE_BRANCH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --staged)    MODE="staged"; shift ;;
    --committed) MODE="committed"; BASE_BRANCH="${2:-}"; shift 2 ;;
    *)           echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [ "$MODE" = "committed" ] && [ -z "$BASE_BRANCH" ]; then
  echo "Usage: scan-secrets.sh --committed <base-branch>" >&2
  exit 2
fi

FOUND=0

# ── Phase 1: dangerous file names ────────────────────────────────────────────
DANGEROUS=$(git status --short 2>/dev/null \
  | awk '{print $NF}' \
  | grep -iE '(^|\/)\.env(\.|$)|credentials\.|secret\.|id_rsa|\.pem$|\.key$' \
  || true)

if [ -n "$DANGEROUS" ]; then
  echo "WARN: Potentially sensitive files in changeset:"
  echo "$DANGEROUS" | sed 's/^/  /'
  FOUND=1
fi

# ── Phase 2: diff content (staged + unstaged) ─────────────────────────────────
DIFF_STAGED=$(git diff --cached 2>/dev/null || true)
DIFF_UNSTAGED=$(git diff 2>/dev/null || true)
DIFF_CONTENT="$DIFF_STAGED
$DIFF_UNSTAGED"

# ── Phase 3: committed diff vs base branch ────────────────────────────────────
if [ "$MODE" = "committed" ]; then
  DIFF_COMMITTED=$(git diff "${BASE_BRANCH}...HEAD" 2>/dev/null || true)
  DIFF_CONTENT="$DIFF_CONTENT
$DIFF_COMMITTED"
fi

# Secret patterns (applied to added lines only — lines starting with +)
SECRET_PATTERNS=(
  'AKIA[0-9A-Z]{16}'
  'sk-[a-zA-Z0-9]{32,}'
  'ghp_[a-zA-Z0-9]{36}'
  'github_pat_[a-zA-Z0-9]{82}'
  'xoxb-[0-9]{11}-[0-9]{11}-[a-zA-Z0-9]{24}'
  'xoxp-[0-9]{11}-'
  'AIza[0-9A-Za-z_\-]{35}'
  '\-\-\-\-\-BEGIN .* PRIVATE KEY\-\-\-\-\-'
  'password\s*=\s*["\x27][^"\x27]{4,}'
  'DATABASE_URL\s*='
)

ADDED_LINES=$(echo "$DIFF_CONTENT" | grep '^+' | grep -v '^+++' || true)

for PATTERN in "${SECRET_PATTERNS[@]}"; do
  MATCHES=$(echo "$ADDED_LINES" | grep -E "$PATTERN" || true)
  if [ -n "$MATCHES" ]; then
    echo "SECRET DETECTED (pattern: $PATTERN):"
    echo "$MATCHES" | head -3 | sed 's/^/  /'
    FOUND=1
  fi
done

if [ "$FOUND" -eq 0 ]; then
  echo "OK: No secrets detected"
fi

exit "$FOUND"
