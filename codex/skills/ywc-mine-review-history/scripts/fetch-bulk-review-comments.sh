#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <owner/repo> --limit <positive-integer> [--since YYYY-MM-DD]" >&2
  echo "       $0 <owner/repo> --since YYYY-MM-DD [--limit <positive-integer>]" >&2
}

if [[ $# -lt 1 ]]; then usage; exit 2; fi
REPO=$1
shift
if [[ ! "$REPO" =~ ^[^/]+/[^/]+$ ]]; then
  echo "error: repository must be owner/name" >&2
  exit 2
fi
LIMIT=""
SINCE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --limit)
      [[ -z "$LIMIT" && $# -ge 2 ]] || { echo "error: duplicate or missing --limit" >&2; exit 2; }
      LIMIT=$2; shift 2
      ;;
    --since)
      [[ -z "$SINCE" && $# -ge 2 ]] || { echo "error: duplicate or missing --since" >&2; exit 2; }
      SINCE=$2; shift 2
      ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done
if [[ -z "$LIMIT" && -z "$SINCE" ]]; then usage; exit 2; fi
if [[ -n "$LIMIT" && ( ! "$LIMIT" =~ ^[1-9][0-9]*$ ) ]]; then
  echo "error: --limit must be a positive integer" >&2; exit 2
fi
if [[ -n "$SINCE" && ! "$SINCE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "error: --since must be YYYY-MM-DD" >&2; exit 2
fi
command -v gh >/dev/null 2>&1 || { echo "error: gh is required" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }

LIMIT=${LIMIT:-200}
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT
pr_json="$tmp_dir/prs.json"
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" --json number,mergedAt >"$pr_json" || {
  echo "error: unable to list merged PRs for $REPO" >&2
  exit 1
}
BOT_RE='^(coderabbitai|chatgpt-codex-connector|github-actions)\[bot\]$'
failure=0
while IFS=$'\t' read -r pr merged_at; do
  [[ -n "$pr" ]] || continue
  if [[ -n "$SINCE" && "$merged_at" < "${SINCE}T00:00:00Z" ]]; then continue; fi
  comments_json="$tmp_dir/comments-$pr.json"
  if ! gh api --paginate "repos/$REPO/pulls/$pr/comments" >"$comments_json"; then
    echo "error: failed to fetch review comments for $REPO#$pr" >&2
    failure=1
    continue
  fi
  jq -c --arg pr "$pr" --arg re "$BOT_RE" \
    '.[] | select((.user.login // "") | test($re; "i")) |
     {pr: ($pr | tonumber), id, path, line, body, in_reply_to_id}' "$comments_json"
done < <(jq -r '.[] | [.number, (.mergedAt // "")] | @tsv' "$pr_json")
exit "$failure"
