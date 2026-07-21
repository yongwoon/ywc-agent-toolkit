#!/usr/bin/env bash
# poll-pr-reviews.sh <pr-number>
#
# Output contract (the caller MUST parse the last line, not a bare integer):
#   BOT_COUNT=<n> WINDOW=complete    exit 0 -> bots posted; handle reviews
#   BOT_COUNT=0 WINDOW=complete      exit 1 -> full window elapsed, no bots; merge allowed
#   BOT_COUNT=0 WINDOW=degraded      exit 3 -> every gh query failed; NOT evidence of zero bots
#
# If no `WINDOW=complete` line is printed, the poll did not finish (Bash tool
# timeout, kill, network death). That is never evidence of BOT_COUNT==0 —
# the caller must retry, and must not merge.

set -euo pipefail

PR_NUMBER="${1:-}"
if [ -z "$PR_NUMBER" ]; then
  echo "Usage: poll-pr-reviews.sh <pr-number>" >&2
  exit 2
fi

BOT_RE='coderabbitai|coderabbit|codex|claude|anthropic|github-actions'

# Two sources are required. `gh pr view --json` has no `reviewThreads` field —
# passing one makes the whole call fail — yet line-level review comments (the
# most common bot output) live only there. They come from the REST endpoint.
fetch_bot_count() {
  local top line
  top=$(gh pr view "$PR_NUMBER" --json reviews,comments \
    --jq "[ .reviews[], .comments[] ]
          | map(select(.author.login | test(\"$BOT_RE\"; \"i\")))
          | length") || return 1
  line=$(gh api --paginate "repos/{owner}/{repo}/pulls/$PR_NUMBER/comments" \
    --jq ".[] | select(.user.login | test(\"$BOT_RE\"; \"i\")) | .id" \
    | wc -l | tr -d ' ') || return 1
  case "$top$line" in ''|*[!0-9]*) return 1 ;; esac
  echo $((top + line))
}

POLL_COUNT=0
BOT_COUNT=0
QUERY_OK=0
QUERY_FAILURES=0

until [ "$BOT_COUNT" -gt 0 ] || [ "$POLL_COUNT" -ge 11 ]; do
  if [ "$POLL_COUNT" -eq 0 ]; then
    sleep 60
  else
    sleep 30
  fi

  if RESULT=$(fetch_bot_count); then
    BOT_COUNT="$RESULT"
    QUERY_OK=1
  else
    QUERY_FAILURES=$((QUERY_FAILURES + 1))
    echo "Failed to fetch review artifacts for PR #${PR_NUMBER} (attempt ${QUERY_FAILURES})" >&2
  fi

  POLL_COUNT=$((POLL_COUNT + 1))
done

if [ "$QUERY_OK" -eq 0 ]; then
  echo "BOT_COUNT=0 WINDOW=degraded"
  exit 3
fi

echo "BOT_COUNT=$BOT_COUNT WINDOW=complete"
[ "$BOT_COUNT" -gt 0 ]
