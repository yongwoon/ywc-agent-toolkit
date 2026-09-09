#!/usr/bin/env bash
# fetch-bulk-review-comments.sh --limit <n> | --since <date>
#
# Batch-fetches bot review comments (CodeRabbit / Codex Review / Claude
# Review / anthropic / github-actions) across N already-merged PRs and
# emits them as NDJSON (one line per comment, tagged with its source PR
# number) to stdout.
#
# Ported from develop-with-llm commit 93129bd89756fad8e4fa17000e9d8e54325280fb,
# adapted to this repo's broader bot-login allowlist (see SKILL.md's
# Bot-login allowlist decision — reuses the regex from
# claude-code/skills/scripts/poll-pr-reviews.sh, kept inline here per the
# existing per-site convention, not extracted to a shared constant).
#
# Exit codes:
#   0  Success (including zero merged PRs in the selected window)
#   1  gh pr list / gh api failure (propagated, never swallowed with || true)
#   2  Usage error (missing/invalid --limit or --since)
#
# Usage:
#   bash claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh --limit 50
#   bash claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh --since 2026-01-01
#   bash claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh --limit 50 --since 2026-01-01

set -euo pipefail

LIMIT=""
SINCE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --limit) LIMIT="${2:-}"; shift 2 ;;
    --since) SINCE="${2:-}"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$LIMIT" && -z "$SINCE" ]]; then
  echo "Usage: fetch-bulk-review-comments.sh --limit <n> | --since <date>" >&2
  echo "At least one of --limit or --since is required (no unbounded scan)." >&2
  exit 2
fi

if [[ -n "$LIMIT" && ! "$LIMIT" =~ ^[0-9]+$ ]]; then
  echo "error: --limit must be a positive integer, got: $LIMIT" >&2
  exit 2
fi

if [[ -n "$SINCE" && ! "$SINCE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "error: --since must be YYYY-MM-DD, got: $SINCE" >&2
  exit 2
fi

# Anchored bot-login allowlist (^(...)$-equivalent via test(), not a bare
# substring match) — carried over from the upstream fix in commit 93129bd.
# GitHub bot accounts carry a literal "[bot]" suffix in user.login, so the
# regex must match it explicitly or every real bot comment is dropped.
BOT_RE='^(coderabbitai|coderabbit|codex|claude|anthropic|github-actions)\[bot\]$'

SEARCH="is:merged"
[[ -n "$SINCE" ]] && SEARCH="$SEARCH merged:>=$SINCE"

FETCH_LIMIT="${LIMIT:-1000}"
PR_NUMBERS=$(gh pr list --state merged --search "$SEARCH" --limit "$FETCH_LIMIT" --json number --jq '.[].number')

if [[ -z "$PR_NUMBERS" ]]; then
  # Zero merged PRs in the selected window is not an error (see Edge Cases).
  exit 0
fi

while IFS= read -r pr; do
  [[ -z "$pr" ]] && continue
  # shellcheck disable=SC2016 # jq's own $re/$pr (bound via --arg), not shell expansion
  gh api --paginate "repos/{owner}/{repo}/pulls/$pr/comments" |
    jq -c --arg pr "$pr" --arg re "$BOT_RE" \
      '.[] | select(.user.login | test($re; "i")) | {pr: ($pr | tonumber), id, path, line, body, in_reply_to_id}'
done <<< "$PR_NUMBERS"
