#!/usr/bin/env bash
# poll-pr-reviews.sh [--verify] <pr-number>

set -euo pipefail

VERIFY_ONLY=false
if [ "${1:-}" = "--verify" ]; then
  VERIFY_ONLY=true
  shift
fi

PR_NUMBER="${1:-}"
if [ -z "$PR_NUMBER" ] || [ "$#" -ne 1 ]; then
  echo "Usage: poll-pr-reviews.sh [--verify] <pr-number>" >&2
  exit 2
fi

require_nonnegative_integer() {
  case "$2" in
    ''|*[!0-9]*)
      echo "$1 must be a non-negative integer; got: $2" >&2
      exit 2
      ;;
  esac
}

require_nonnegative_integer PR_NUMBER "$PR_NUMBER"

artifact_path() {
  git rev-parse --git-path "ywc-bot-review-polls/${PR_NUMBER}.json"
}

ARTIFACT_PATH="$(artifact_path)"

if [ "$VERIFY_ONLY" = true ]; then
  if [ ! -s "$ARTIFACT_PATH" ]; then
    echo "No completed bot-review polling artifact for PR #${PR_NUMBER}: $ARTIFACT_PATH" >&2
    exit 4
  fi

  if ! jq -e --arg pr_number "$PR_NUMBER" \
    '.pr_number == $pr_number and .complete == true' "$ARTIFACT_PATH" >/dev/null; then
    echo "Invalid bot-review polling artifact for PR #${PR_NUMBER}: $ARTIFACT_PATH" >&2
    exit 4
  fi

  ARTIFACT_HEAD_REF_OID="$(jq -r '.head_ref_oid // empty' "$ARTIFACT_PATH")"
  if ! CURRENT_HEAD_REF_OID="$(gh pr view "$PR_NUMBER" --json headRefOid --jq '.headRefOid')" \
    || [ -z "$ARTIFACT_HEAD_REF_OID" ] \
    || [ "$ARTIFACT_HEAD_REF_OID" != "$CURRENT_HEAD_REF_OID" ]; then
    echo "Bot-review polling artifact is stale for PR #${PR_NUMBER}; poll again after the latest push." >&2
    exit 4
  fi

  cat "$ARTIFACT_PATH"
  exit 0
fi

# Environment overrides make the script testable without changing production
# semantics. Normal invocations use the 60s + 10 x 30s wait contract.
INITIAL_WAIT_SECONDS="${YWC_POLL_INITIAL_WAIT_SECONDS:-60}"
INTERVAL_SECONDS="${YWC_POLL_INTERVAL_SECONDS:-30}"
MAX_POLLS="${YWC_POLL_MAX_POLLS:-11}"
MAX_FETCH_FAILURES="${YWC_POLL_MAX_FETCH_FAILURES:-3}"
require_nonnegative_integer YWC_POLL_INITIAL_WAIT_SECONDS "$INITIAL_WAIT_SECONDS"
require_nonnegative_integer YWC_POLL_INTERVAL_SECONDS "$INTERVAL_SECONDS"
require_nonnegative_integer YWC_POLL_MAX_POLLS "$MAX_POLLS"
require_nonnegative_integer YWC_POLL_MAX_FETCH_FAILURES "$MAX_FETCH_FAILURES"
if [ "$MAX_POLLS" -eq 0 ] || [ "$MAX_FETCH_FAILURES" -eq 0 ]; then
  echo "YWC_POLL_MAX_POLLS and YWC_POLL_MAX_FETCH_FAILURES must be greater than zero" >&2
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

# A stale successful artifact must never satisfy a later merge gate.
rm -f "$ARTIFACT_PATH"

POLL_COUNT=0
BOT_COUNT=0
FETCH_FAILURES=0

while [ "$BOT_COUNT" -eq 0 ] && [ "$POLL_COUNT" -lt "$MAX_POLLS" ]; do
  if [ "$POLL_COUNT" -eq 0 ]; then
    sleep "$INITIAL_WAIT_SECONDS"
  else
    sleep "$INTERVAL_SECONDS"
  fi

  if BOT_COUNT=$(fetch_bot_count); then
    require_nonnegative_integer "gh bot-comment count" "$BOT_COUNT"
    FETCH_FAILURES=0
    POLL_COUNT=$((POLL_COUNT + 1))
  else
    FETCH_FAILURES=$((FETCH_FAILURES + 1))
    echo "Failed to fetch review artifacts for PR #${PR_NUMBER} (${FETCH_FAILURES}/${MAX_FETCH_FAILURES}); retrying" >&2
    if [ "$FETCH_FAILURES" -ge "$MAX_FETCH_FAILURES" ]; then
      echo "Bot-review polling did not complete; refusing to create a merge-gate artifact." >&2
      exit 3
    fi
  fi
done

mkdir -p "$(dirname "$ARTIFACT_PATH")"
if ! HEAD_REF_OID="$(gh pr view "$PR_NUMBER" --json headRefOid --jq '.headRefOid')" \
  || [ -z "$HEAD_REF_OID" ]; then
  echo "Could not determine the PR head SHA; refusing to create a merge-gate artifact." >&2
  exit 3
fi
TEMP_ARTIFACT="$(mktemp "${ARTIFACT_PATH}.tmp.XXXXXX")"
trap 'rm -f "$TEMP_ARTIFACT"' EXIT
cat > "$TEMP_ARTIFACT" <<EOF
{
  "pr_number": "${PR_NUMBER}",
  "complete": true,
  "bot_count": ${BOT_COUNT},
  "poll_count": ${POLL_COUNT},
  "head_ref_oid": "${HEAD_REF_OID}",
  "completed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
mv "$TEMP_ARTIFACT" "$ARTIFACT_PATH"
trap - EXIT

echo "$BOT_COUNT"
[ "$BOT_COUNT" -gt 0 ]
