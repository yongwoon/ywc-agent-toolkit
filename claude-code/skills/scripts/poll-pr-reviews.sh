#!/usr/bin/env bash
# poll-pr-reviews.sh <pr-number>
#
# Output contract (the caller MUST parse the last line, not a bare integer):
#   BOT_COUNT=<n> WINDOW=complete    exit 0 -> bots posted; handle reviews
#   BOT_COUNT=0 WINDOW=complete      exit 1 -> full window elapsed, no bots; merge allowed
#   BOT_COUNT=0 WINDOW=degraded      exit 3 -> a gh query failed; NOT evidence of zero bots
#
# A zero-bot verdict requires a window in which EVERY query succeeded. One
# failed query anywhere in the window degrades it, even if an earlier query
# already succeeded and reported zero.
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

# Overrides exist so the verdict branches are testable without waiting out the
# real window. Defaults are the production 60s + 10 x 30s contract.
INITIAL_WAIT_SECONDS="${YWC_POLL_INITIAL_WAIT_SECONDS:-60}"
INTERVAL_SECONDS="${YWC_POLL_INTERVAL_SECONDS:-30}"
MAX_POLLS="${YWC_POLL_MAX_POLLS:-11}"

POLL_COUNT=0
BOT_COUNT=0
QUERY_FAILURES=0

until [ "$BOT_COUNT" -gt 0 ] || [ "$POLL_COUNT" -ge "$MAX_POLLS" ]; do
  if [ "$POLL_COUNT" -eq 0 ]; then
    sleep "$INITIAL_WAIT_SECONDS"
  else
    sleep "$INTERVAL_SECONDS"
  fi

  if RESULT=$(fetch_bot_count); then
    BOT_COUNT="$RESULT"
  else
    QUERY_FAILURES=$((QUERY_FAILURES + 1))
    echo "Failed to fetch review artifacts for PR #${PR_NUMBER} (attempt ${QUERY_FAILURES})" >&2
  fi

  POLL_COUNT=$((POLL_COUNT + 1))
done

# Only a zero count needs a clean window: BOT_COUNT > 0 is positive evidence
# that survives a later failed query, but BOT_COUNT == 0 is an absence claim and
# any failed query in the window makes that absence unproven.
if [ "$BOT_COUNT" -eq 0 ] && [ "$QUERY_FAILURES" -gt 0 ]; then
  echo "BOT_COUNT=0 WINDOW=degraded"
  exit 3
fi

echo "BOT_COUNT=$BOT_COUNT WINDOW=complete"
[ "$BOT_COUNT" -gt 0 ]
