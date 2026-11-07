#!/usr/bin/env bash
# scan-secrets.sh [--staged] [--committed <base-branch>]
#
# Scans git diff for secret patterns across three phases:
#   Phase 1 — dangerous file names (.env, .pem, credentials.*, etc.)
#   Phase 2 — staged + unstaged diff content and untracked file content
#             (secret regex patterns)
#   Phase 3 — committed diff vs base branch, plus dangerous file names in
#             that range (when --committed is given)
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
# Binary content is not valid UTF-8 and makes awk abort; the patterns are ASCII.
export LC_ALL=C

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
# A name is matched after the status field's space, after a `/`, or at the
# start of a bare path (Phase 3 name list).
DANGEROUS_NAME_RE='(^|[/ ])\.env(\.|$)|credentials\.|secret\.|id_rsa|\.pem$|\.key$'
DANGEROUS=$(printf '%s\n' "$STATUS" | grep -iE "$DANGEROUS_NAME_RE" || true)

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
# Neither diff shows untracked files, and ywc-create-pr scans before its commit
# stages them, so each one is diffed against /dev/null. The NUL-separated list
# goes through a file so a failing ls-files is still caught. `--no-index` exits
# 1 when the files differ and 2+ on error. Directories (nested repos, dir
# symlinks) are skipped: git cannot read them as files and still exits 1. NUL
# bytes from binary content are dropped so bash does not warn about them.
UNTRACKED_LIST=$(mktemp) || {
  echo "ERROR: mktemp failed; nothing was scanned" >&2
  exit 2
}
trap 'rm -f "$UNTRACKED_LIST"' EXIT
git ls-files -z --others --exclude-standard > "$UNTRACKED_LIST" || {
  echo "ERROR: git ls-files --others failed; nothing was scanned" >&2
  exit 2
}
DIFF_UNTRACKED=""
while IFS= read -r -d '' UNTRACKED_FILE; do
  [ -d "$UNTRACKED_FILE" ] && continue
  RC=0
  FILE_DIFF=$(git diff "${DIFF_OPTS[@]}" --no-index -- /dev/null "$UNTRACKED_FILE" | tr -d '\0') || RC=$?
  if [ "$RC" -gt 1 ]; then
    echo "ERROR: git diff --no-index failed for an untracked file; nothing was scanned" >&2
    exit 2
  fi
  DIFF_UNTRACKED="$DIFF_UNTRACKED
$FILE_DIFF"
done < "$UNTRACKED_LIST"

DIFF_CONTENT="$DIFF_STAGED
$DIFF_UNSTAGED
$DIFF_UNTRACKED"

# ── Phase 3: committed diff vs base branch ────────────────────────────────────
if [ "$MODE" = "committed" ]; then
  # Phase 1 sees only the work tree, so a .env committed on the branch is
  # checked here. Walk every branch commit, not the net diff: a .env added and
  # then deleted is gone from BASE...HEAD but still in the pushed history.
  # --diff-filter=d skips deletions (removing a base .env is a cleanup), and
  # merge commits show no diff by default, so merging the base in adds nothing.
  COMMITTED_NAMES=$(git log --no-renames --diff-filter=d --name-only -z --format= "${BASE_BRANCH}..HEAD" | tr '\0' '\n') || {
    echo "ERROR: git log --name-only ${BASE_BRANCH}..HEAD failed; committed changes were not scanned" >&2
    exit 2
  }
  DANGEROUS_COMMITTED=$(printf '%s\n' "$COMMITTED_NAMES" | grep -iE "$DANGEROUS_NAME_RE" || true)
  if [ -n "$DANGEROUS_COMMITTED" ]; then
    echo "WARN: Potentially sensitive files committed since ${BASE_BRANCH}:"
    echo "$DANGEROUS_COMMITTED" | sed 's/^/  /'
    FOUND=1
  fi
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
  # Double-quoted so the apostrophe is literal (`\x27` is not an ERE escape).
  "password\\s*=\\s*[\"'][^\"']{4,}"
  'DATABASE_URL\s*='
)

# `+++ `/`--- ` are file headers only between a `diff ` line (`--git`, `--cc`)
# and the first `@@` hunk header; inside a hunk every `+` line is content, even
# one that reads `+++` because the added text starts with `++`.
ADDED_LINES=$(echo "$DIFF_CONTENT" | awk '/^diff /{h=0} /^@@/{h=1} h && /^\+/') || {
  echo "ERROR: filtering added lines failed; nothing was scanned" >&2
  exit 2
}

for PATTERN in "${SECRET_PATTERNS[@]}"; do
  MATCHES=$(echo "$ADDED_LINES" | grep -E "$PATTERN" || true)
  if [ -n "$MATCHES" ]; then
    echo "SECRET DETECTED (pattern: $PATTERN):"
    # One sed reads all input: `head` would close the pipe early and, under
    # pipefail, turn a large match set into exit 141 instead of "found".
    echo "$MATCHES" | sed -n '1,3s/^/  /p'
    FOUND=1
  fi
done

if [ "$FOUND" -eq 0 ]; then
  echo "OK: No secrets detected"
fi

exit "$FOUND"
