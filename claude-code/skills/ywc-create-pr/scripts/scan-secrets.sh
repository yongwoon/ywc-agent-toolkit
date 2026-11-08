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
#   1  Secrets or dangerous files found (details on stdout; matched values are
#      shown as [REDACTED])
#   2  Nothing (or not everything) was scanned: usage error, not inside a git
#      work tree, (--committed) an invalid or unresolvable base branch, or a
#      failed step — git status / diff / ls-files / log, mktemp, reading an
#      untracked file, or the added-line filter. Never read 2 as "clean".
#
# Usage:
#   # Scan staged + unstaged changes
#   bash claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh --staged
#
#   # Also scan all commits vs base branch
#   bash claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh --committed develop

set -Eeuo pipefail
# Any unguarded failure (a full TMPDIR, a sed error) would otherwise exit 1,
# which callers read as "secrets found": every such exit is 2.
trap 'exit 2' ERR
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
# grep exits 1 for "no match" and 2 for an error; only 1 is "nothing found".
grep_or_none() { local rc=0; grep "$@" || rc=$?; [ "$rc" -le 1 ] || { echo "ERROR: grep failed; nothing was scanned" >&2; exit 2; }; }
DANGEROUS=$(printf '%s\n' "$STATUS" | grep_or_none -iE "$DANGEROUS_NAME_RE")

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
# stages them. Every line of an untracked file is added, so the files are read
# with one `cat` and prefixed with `+` under a synthetic hunk header (a
# `git diff --no-index` per file took ~65 ms each and hit the 120 s Bash
# timeout around 1,800 files). The NUL-separated lists go through files so a
# failing ls-files is still caught. A symlink contributes its target path, as
# git would commit it; directories (nested repos, dir symlinks) and other
# non-regular files are skipped. NUL bytes from binary content are dropped so
# bash does not warn about them.
UNTRACKED_LIST=$(mktemp) && REGULAR_LIST=$(mktemp) || {
  echo "ERROR: mktemp failed; nothing was scanned" >&2
  exit 2
}
trap 'rm -f "$UNTRACKED_LIST" "$REGULAR_LIST"' EXIT
git ls-files -z --others --exclude-standard > "$UNTRACKED_LIST" || {
  echo "ERROR: git ls-files --others failed; nothing was scanned" >&2
  exit 2
}
SYMLINK_TARGETS=""
while IFS= read -r -d '' UNTRACKED_FILE; do
  if [ -L "$UNTRACKED_FILE" ]; then
    LINK_TARGET=$(readlink -- "$UNTRACKED_FILE") || {
      echo "ERROR: readlink failed for untracked symlink '$UNTRACKED_FILE'; nothing was scanned" >&2
      exit 2
    }
    SYMLINK_TARGETS="$SYMLINK_TARGETS$LINK_TARGET
"
  elif [ -f "$UNTRACKED_FILE" ]; then
    # ./ so a file named `-` is not read as stdin.
    printf './%s\0' "$UNTRACKED_FILE" >> "$REGULAR_LIST"
  fi
done < "$UNTRACKED_LIST"
UNTRACKED_CONTENT=""
if [ -s "$REGULAR_LIST" ]; then
  # cat names any file it cannot read on stderr.
  UNTRACKED_CONTENT=$(xargs -0 cat -- < "$REGULAR_LIST" | tr -d '\0') || {
    echo "ERROR: reading untracked files failed (see the cat error above); nothing was scanned" >&2
    exit 2
  }
fi
DIFF_UNTRACKED=$(printf '%s\n%s' "$UNTRACKED_CONTENT" "$SYMLINK_TARGETS" | sed 's/^/+/') || {
  echo "ERROR: preparing untracked content failed; nothing was scanned" >&2
  exit 2
}
DIFF_UNTRACKED="diff untracked-files
@@
$DIFF_UNTRACKED"

DIFF_CONTENT="$DIFF_STAGED
$DIFF_UNSTAGED
$DIFF_UNTRACKED"

# ── Phase 3: committed diff vs base branch ────────────────────────────────────
if [ "$MODE" = "committed" ]; then
  # Phase 1 sees only the work tree, so a .env committed on the branch is
  # checked here. Walk every branch commit, not the net diff: a .env added and
  # then deleted is gone from BASE...HEAD but still in the pushed history.
  # --diff-filter=d skips deletions (removing a base .env is a cleanup). --cc
  # lists a merge's file only when it differs from every parent, so a file
  # added while resolving a merge is caught but files from the base are not.
  COMMITTED_NAMES=$(git log --cc --no-renames --diff-filter=d --name-only -z --format= "${BASE_BRANCH}..HEAD" | tr '\0' '\n') || {
    echo "ERROR: git log --name-only ${BASE_BRANCH}..HEAD failed; committed changes were not scanned" >&2
    exit 2
  }
  DANGEROUS_COMMITTED=$(printf '%s\n' "$COMMITTED_NAMES" | grep_or_none -iE "$DANGEROUS_NAME_RE")
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
# POSIX ERE only ([[:space:]], not \s): the same pattern also drives the sed
# redaction below, and BSD sed has no \s.
SECRET_PATTERNS=(
  'AKIA[0-9A-Z]{16}'
  'sk-[a-zA-Z0-9]{32,}'
  'sk-ant-[A-Za-z0-9_-]{20,}'
  'sk-proj-[A-Za-z0-9_-]{20,}'
  'gh[pousr]_[a-zA-Z0-9]{36}'
  'github_pat_[a-zA-Z0-9_]{82}'
  'glpat-[A-Za-z0-9_-]{20}'
  'sk_live_[A-Za-z0-9]{24,}'
  'xoxb-[0-9]{11}-[0-9]{11}-[a-zA-Z0-9]{24}'
  'xoxp-[0-9]{11}-'
  'AIza[0-9A-Za-z_-]{35}'
  # RSA / EC / OPENSSH / ENCRYPTED and the bare PKCS#8 header.
  '-----BEGIN ([A-Z0-9]+ )*PRIVATE KEY-----'
  # Double-quoted so the apostrophe is literal (`\x27` is not an ERE escape).
  "password[[:space:]]*=[[:space:]]*[\"'][^\"']{4,}"
  'DATABASE_URL[[:space:]]*='
)

# `+++ `/`--- ` are file headers only between a `diff ` line (`--git`, `--cc`)
# and the first `@@` hunk header; inside a hunk every `+` line is content, even
# one that reads `+++` because the added text starts with `++`. A combined diff
# (`diff --cc`, e.g. the unstaged diff of a conflicted merge) has one marker
# column per parent, counted from the `@@@` header: a line is added when any
# marker column holds a `+` (`++`, `+ `, ` +`); `+` and `-` never share a line.
ADDED_LINES=$(echo "$DIFF_CONTENT" | awk '
  /^diff /{h=0}
  /^@@/{match($0, /^@+/); n=RLENGTH-1; h=1; next}
  h && index(substr($0, 1, n), "+")') || {
  echo "ERROR: filtering added lines failed; nothing was scanned" >&2
  exit 2
}

# Every pattern redacts every printed line, so a second secret earlier on the
# same line is never shown either.
REDACT=()
for PATTERN in "${SECRET_PATTERNS[@]}"; do REDACT+=(-e "s#${PATTERN}.*#[REDACTED]#"); done

for PATTERN in "${SECRET_PATTERNS[@]}"; do
  # -e: the private-key pattern starts with `-`.
  MATCHES=$(echo "$ADDED_LINES" | grep_or_none -E -e "$PATTERN")
  if [ -n "$MATCHES" ]; then
    echo "SECRET DETECTED (pattern: $PATTERN):"
    # Never echo the secret: everything from the match to the end of the line is
    # redacted. One sed reads all input: `head` would close the pipe early and,
    # under pipefail, turn a large match set into exit 141 instead of "found".
    echo "$MATCHES" | sed -n '1,3p' | sed -E "${REDACT[@]}" -e 's/^/  /'
    FOUND=1
  fi
done

if [ "$FOUND" -eq 0 ]; then
  echo "OK: No secrets detected"
fi

exit "$FOUND"
