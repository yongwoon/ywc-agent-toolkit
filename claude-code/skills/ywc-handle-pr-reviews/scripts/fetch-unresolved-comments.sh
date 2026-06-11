#!/usr/bin/env bash
# fetch-unresolved-comments.sh <owner/repo> <pr-number>
#
# Fetches all PR review comments (paginated) and filters out already-addressed
# ones. Outputs a JSON array of actionable comment objects to stdout so the
# LLM can process them without re-implementing the filtering logic.
#
# A comment thread is SKIPPED when:
#   - Any comment in the thread contains <!-- <review_comment_addressed> -->
#   - The authenticated user already replied AND the reply is newer than the
#     latest non-user comment in the thread
#
# Exit codes:
#   0  Success — JSON array on stdout (may be [])
#   1  gh CLI error (not authenticated, PR not found, API failure)
#   2  Usage error
#
# Output format (JSON array):
#   [{"id":123,"in_reply_to_id":null,"body":"...","path":"src/foo.ts",
#     "line":42,"user":"reviewer","created_at":"2025-01-01T00:00:00Z",
#     "thread_comment_count":3}, ...]
#
# Usage:
#   bash claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh \
#     owner/repo 123

set -euo pipefail

REPO="${1:-}"
PR_NUMBER="${2:-}"

if [ -z "$REPO" ] || [ -z "$PR_NUMBER" ]; then
  echo "Usage: fetch-unresolved-comments.sh <owner/repo> <pr-number>" >&2
  exit 2
fi

CURRENT_USER=$(gh api user --jq .login 2>/dev/null) || {
  echo "ERROR: gh CLI not authenticated or API unreachable" >&2
  exit 1
}

gh api "repos/${REPO}/pulls/${PR_NUMBER}/comments" --paginate 2>/dev/null \
  | jq --arg me "$CURRENT_USER" '
    # Group comments into threads by in_reply_to_id.
    # Root comments (null in_reply_to_id) form their own thread keyed by id.
    group_by(.in_reply_to_id // .id)
    | map(
        sort_by(.created_at)
        | {
            comments: .,
            root: .[0],
            addressed: (map(.body) | any(test("<!--\\s*<review_comment_addressed>\\s*-->"))),
            my_replies: (map(select(.user.login == $me)) | sort_by(.created_at)),
            reviewer_comments: (map(select(.user.login != $me)) | sort_by(.created_at))
          }
      )
    # Keep only unresolved threads
    | map(select(
        .addressed == false
        and (
          (.my_replies | length) == 0
          or (
            (.reviewer_comments | length) > 0
            and (.my_replies | last | .created_at) < (.reviewer_comments | last | .created_at)
          )
        )
      ))
    # Return root comment of each unresolved thread with thread context
    | map({
        id: .root.id,
        in_reply_to_id: .root.in_reply_to_id,
        body: .root.body,
        path: .root.path,
        line: (.root.line // .root.original_line),
        user: .root.user.login,
        created_at: .root.created_at,
        thread_comment_count: (.comments | length)
      })
  '
