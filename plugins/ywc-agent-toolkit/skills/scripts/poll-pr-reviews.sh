#!/usr/bin/env bash
# poll-pr-reviews.sh <pr-number>

set -euo pipefail

PR_NUMBER="${1:-}"
if [ -z "$PR_NUMBER" ]; then
  echo "Usage: poll-pr-reviews.sh <pr-number>" >&2
  exit 2
fi

POLL_COUNT=0
BOT_COUNT=0

until [ "$BOT_COUNT" -gt 0 ] || [ "$POLL_COUNT" -ge 11 ]; do
  if [ "$POLL_COUNT" -eq 0 ]; then
    sleep 60
  else
    sleep 30
  fi

  BOT_COUNT=$(gh pr view "$PR_NUMBER" --json reviews,comments,reviewThreads \
    --jq '
      [ .reviews[],
        .comments[],
        (.reviewThreads[]?.comments[]?)
      ]
      | map(select(.author.login
          | test("coderabbitai|coderabbit|codex|claude|anthropic|github-actions"; "i")))
      | length
    ' 2>/dev/null || echo "0")

  POLL_COUNT=$((POLL_COUNT + 1))
done

echo "$BOT_COUNT"
[ "$BOT_COUNT" -gt 0 ]
