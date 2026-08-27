#!/usr/bin/env bash
# fetch-nitpick-comments.sh <owner/repo> <pr-number>
#
# Fetches all CodeRabbit reviews on a PR, pipes each review body through
# extract-nitpick-comments.py (Task 010) to extract Nitpick pseudo-comments,
# merges the results across reviews, and excludes items already marked
# addressed via a PR-level `<!-- nitpick-addressed:<hash> -->` comment.
# Outputs a JSON array to stdout.
#
# Exit codes:
#   0  Success — JSON array on stdout (may be [])
#   1  gh CLI error (not authenticated, PR not found, API failure)
#   2  Usage error
#
# Output format (JSON array):
#   [{"hash":"9dd61764f7e5cfad48b73fc4","path":"apps/backend/src/foo.ts",
#     "line_start":134,"line_end":168,"title":"...","body":"...",
#     "severity":"nitpick","parse_status":"ok","review_id":123456,
#     "review_submitted_at":"2026-01-01T00:00:00Z"}, ...]
#
# Usage:
#   bash claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh \
#     owner/repo 123

set -euo pipefail

REPO="${1:-}"
PR_NUMBER="${2:-}"

if [ -z "$REPO" ] || [ -z "$PR_NUMBER" ]; then
  echo "Usage: fetch-nitpick-comments.sh <owner/repo> <pr-number>" >&2
  exit 2
fi

if ! [[ "$REPO" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]]; then
  echo "ERROR: invalid repository format: expected <owner>/<repo>" >&2
  exit 2
fi

if ! [[ "$PR_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "ERROR: invalid PR number: expected digits only" >&2
  exit 2
fi

PARSER="$(dirname "$0")/extract-nitpick-comments.py"

CURRENT_USER=$(gh api user --jq .login 2>/dev/null) || {
  echo "ERROR: gh CLI not authenticated or API unreachable" >&2
  exit 1
}

# 1. Fetch all reviews, filter to CodeRabbit only (before any body is parsed,
#    so a human reviewer's prose is never misparsed as a Nitpick block).
REVIEWS_JSON=$(gh api "repos/${REPO}/pulls/${PR_NUMBER}/reviews" --paginate --slurp 2>/dev/null) || {
  echo "ERROR: failed to fetch reviews for ${REPO}#${PR_NUMBER}" >&2
  exit 1
}
CODERABBIT_REVIEWS=$(printf '%s' "$REVIEWS_JSON" | jq -c '[(add // [])[] | select(.user.login == "coderabbitai[bot]")]')

# 2+3. Pipe each review's body to the parser, tag with review_id/
#      review_submitted_at, and merge all per-review arrays into one.
TMP_ITEMS=$(mktemp)
trap 'rm -f "$TMP_ITEMS"' EXIT

if [ "$(printf '%s' "$CODERABBIT_REVIEWS" | jq 'length')" -gt 0 ]; then
  printf '%s' "$CODERABBIT_REVIEWS" | jq -c '.[]' | while IFS= read -r REVIEW; do
    REVIEW_ID=$(printf '%s' "$REVIEW" | jq -r '.id')
    REVIEW_SUBMITTED_AT=$(printf '%s' "$REVIEW" | jq -r '.submitted_at')
    printf '%s' "$REVIEW" | jq -r '.body' \
      | python3 "$PARSER" \
      | jq -c \
          --argjson review_id "$REVIEW_ID" \
          --arg review_submitted_at "$REVIEW_SUBMITTED_AT" \
          'map(. + {review_id: $review_id, review_submitted_at: $review_submitted_at})' \
      >> "$TMP_ITEMS"
  done
fi


# Same Nitpick can re-appear in a later review before it's addressed; keep
# only the most recent review's copy. Empty-hash raw_fallback items are
# distinct per-occurrence, so they are excluded from hash-based dedup.
MERGED_ITEMS=$(jq -s '
  (add // [])
  | sort_by(.review_submitted_at)
  | (map(select(.hash != "")) | group_by(.hash) | map(last))
    + map(select(.hash == ""))
' "$TMP_ITEMS")

# 4. Amendment A: exclude items whose hash already appears in a
#    <!-- nitpick-addressed:<hash> --> marker in an existing PR-level issue
#    comment authored by the authenticated user only. A marker that was later
#    edited/deleted is simply absent from this scan, so its hash safely
#    re-surfaces (Amendment A's safe-default).
ADDRESSED_COMMENTS=$(gh api "repos/${REPO}/issues/${PR_NUMBER}/comments" --paginate --slurp 2>/dev/null) || {
  echo "ERROR: failed to fetch PR-level comments for ${REPO}#${PR_NUMBER}" >&2
  exit 1
}
ADDRESSED_HASHES=$(printf '%s' "$ADDRESSED_COMMENTS" | jq -c --arg me "$CURRENT_USER" '
  [(add // [])[] | select(.user.login == $me) | .body]
  | join("\n")
  | [scan("nitpick-addressed:([0-9a-fA-F]+)")]
  | map(.[0])
')

# 5. Emit the final filtered JSON array. Empty-hash raw_fallback items are
#    never eligible for this exclusion (Amendment B) -- $addressed never
#    contains "", so they always pass through unaffected.
printf '%s' "$MERGED_ITEMS" | jq --argjson addressed "$ADDRESSED_HASHES" '
  map(select(.hash as $h | ($addressed | index($h)) | not))
'
