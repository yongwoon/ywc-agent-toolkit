#!/usr/bin/env bash
# fetch-unresolved-comments.sh <owner/repo> <pr-number>
#
# Deprecated compatibility wrapper. Runtime instructions use
# fetch-pr-review-artifacts.sh, which emits review artifacts, CI status, and
# merge-readiness blockers.
#
# Usage:
#   bash codex/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh \
#     owner/repo 123

set -euo pipefail

REPO="${1:-}"
PR_NUMBER="${2:-}"

if [ -z "$REPO" ] || [ -z "$PR_NUMBER" ]; then
  echo "Usage: fetch-unresolved-comments.sh <owner/repo> <pr-number>" >&2
  exit 2
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"${SCRIPT_DIR}/fetch-pr-review-artifacts.sh" "$REPO" "$PR_NUMBER" \
  | jq '[.[] | select(.artifact_type == "review_thread")]'
