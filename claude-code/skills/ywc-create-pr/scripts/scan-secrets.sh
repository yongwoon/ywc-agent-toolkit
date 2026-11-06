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
#   2  Usage error, not inside a git work tree, or (--committed) an invalid or
#      unresolvable base branch (nothing was scanned)
#
# Usage:
#   # Scan staged + unstaged changes
#   bash claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh --staged
#
#   # Also scan all commits vs base branch
#   bash claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh --committed develop

set -euo pipefail

MODE="staged"
BASE_BRANCH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    # Phases 1-2 always run; --staged must never downgrade an earlier
    # --committed, or Phase 3 is skipped and committed secrets report as OK.
    --staged)    shift ;;
    # A missing value must reach the usage check (exit 2); `shift 2` would
    # fail under set -e and exit 1, which callers read as "secrets found".
    --committed) MODE="committed"; BASE_BRANCH="${2:-}"; shift $(( $# >= 2 ? 2 : 1 )) ;;
    *)           echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

# Outside a work tree every git call below fails silently and reports "clean".
# A bare repository exits 0 but prints "false", so the output is checked too.
if [ "$(git rev-parse --is-inside-work-tree 2>/dev/null)" != "true" ]; then
  echo "ERROR: not inside a git work tree; nothing was scanned" >&2
  exit 2
fi

# diff.relative=true limits every diff to the current directory, so scan from
# the top of the work tree.
TOP=$(git rev-parse --show-toplevel) && cd "$TOP" || {
  echo "ERROR: cannot enter the work tree root; nothing was scanned" >&2
  exit 2
}

if [ "$MODE" = "committed" ] && [ -z "$BASE_BRANCH" ]; then
  echo "Usage: scan-secrets.sh --committed <base-branch>" >&2
  exit 2
fi

# An unresolvable base would make Phase 3 diff nothing and report "clean".
# The allowlist runs in-process before git sees the value (no option-like or
# shell-metachar names, no `..` range syntax).
if [ "$MODE" = "committed" ]; then
  if ! [[ "$BASE_BRANCH" =~ ^[A-Za-z0-9._/-]+$ ]] || [[ "$BASE_BRANCH" == -* ]] || [[ "$BASE_BRANCH" == *..* ]]; then
    echo "ERROR: invalid base branch name; nothing was scanned" >&2
    exit 2
  fi
  if ! git rev-parse --verify --quiet "${BASE_BRANCH}^{commit}" >/dev/null; then
    echo "ERROR: base branch '$BASE_BRANCH' does not resolve to a commit; nothing was scanned" >&2
    exit 2
  fi
fi

FOUND=0

# The user's git config must not change what is scanned: color codes before
# "+" defeat the `^+` match, and an external diff driver or textconv replaces
# the patch text; `--text` keeps paths marked binary (`-diff`) from collapsing
# to "Binary files differ". `--porcelain` is never colored, and
# `--untracked-files=all` overrides status.showUntrackedFiles=no.
DIFF_OPTS=(--no-color --no-ext-diff --no-textconv --text)

# ── Phase 1: dangerous file names ────────────────────────────────────────────
# A failing git call means nothing was scanned (exit 2); `|| true` is kept only
# on grep, where exit 1 just means "no match". `-z` disables path quoting
# (spaces, non-ASCII), so each entry is matched as written; a name is matched
# after the status field's space or after a `/`.
STATUS=$(git status --porcelain -z --untracked-files=all | tr '\0' '\n') || {
  echo "ERROR: git status failed; nothing was scanned" >&2
  exit 2
}
DANGEROUS=$(printf '%s\n' "$STATUS" \
  | grep -iE '(^|[/ ])\.env(\.|$)|credentials\.|secret\.|id_rsa|\.pem$|\.key$' \
  || true)

if [ -n "$DANGEROUS" ]; then
  echo "WARN: Potentially sensitive files in changeset:"
  echo "$DANGEROUS" | sed 's/^/  /'
  FOUND=1
fi

# ── Phase 2: diff content (staged + unstaged) ─────────────────────────────────
DIFF_STAGED=$(git diff "${DIFF_OPTS[@]}" --cached) || {
  echo "ERROR: git diff --cached failed; nothing was scanned" >&2
  exit 2
}
DIFF_UNSTAGED=$(git diff "${DIFF_OPTS[@]}") || {
  echo "ERROR: git diff failed; nothing was scanned" >&2
  exit 2
}
DIFF_CONTENT="$DIFF_STAGED
$DIFF_UNSTAGED"

# ── Phase 3: committed diff vs base branch ────────────────────────────────────
if [ "$MODE" = "committed" ]; then
  DIFF_COMMITTED=$(git diff "${DIFF_OPTS[@]}" "${BASE_BRANCH}...HEAD") || {
    echo "ERROR: git diff ${BASE_BRANCH}...HEAD failed; committed changes were not scanned" >&2
    exit 2
  }
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
