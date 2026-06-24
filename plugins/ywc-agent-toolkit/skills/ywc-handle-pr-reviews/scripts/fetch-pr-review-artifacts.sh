#!/usr/bin/env bash
# fetch-pr-review-artifacts.sh [<owner/repo>] <pr-number>
#
# Emits normalized PR health artifacts: review feedback, CI status checks, and
# merge-readiness blockers. GitHub/API failures exit 3; usage errors exit 2.

set -euo pipefail

usage() {
  echo "Usage: fetch-pr-review-artifacts.sh [<owner/repo>] <pr-number>" >&2
}

REPO="${GH_REPO:-}"
PR_NUMBER=""

case "$#" in
  1)
    PR_NUMBER="$1"
    ;;
  2)
    REPO="$1"
    PR_NUMBER="$2"
    ;;
  *)
    usage
    exit 2
    ;;
esac

if [ -z "$PR_NUMBER" ]; then
  usage
  exit 2
fi

if [ -z "$REPO" ]; then
  REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null) || {
    echo "ERROR: unable to resolve repository from GH_REPO or gh repo view" >&2
    exit 3
  }
fi

CURRENT_USER=$(gh api user --jq .login 2>/dev/null) || {
  echo "ERROR: gh CLI not authenticated or API unreachable" >&2
  exit 3
}

COMMENTS_JSON=$(gh api "repos/${REPO}/pulls/${PR_NUMBER}/comments" --paginate 2>/dev/null) || {
  echo "ERROR: unable to fetch PR review comments" >&2
  exit 3
}

ISSUE_COMMENTS_JSON=$(gh api "repos/${REPO}/issues/${PR_NUMBER}/comments" --paginate 2>/dev/null) || {
  echo "ERROR: unable to fetch PR comments" >&2
  exit 3
}

REVIEWS_JSON=$(gh api "repos/${REPO}/pulls/${PR_NUMBER}/reviews" --paginate 2>/dev/null) || {
  echo "ERROR: unable to fetch PR reviews" >&2
  exit 3
}

PR_JSON=$(gh pr view "$PR_NUMBER" --repo "$REPO" \
  --json url,mergeable,mergeStateStatus,statusCheckRollup 2>/dev/null) || {
  echo "ERROR: unable to fetch PR status and merge readiness" >&2
  exit 3
}

jq -n \
  --arg me "$CURRENT_USER" \
  --argjson comments "$COMMENTS_JSON" \
  --argjson issue_comments "$ISSUE_COMMENTS_JSON" \
  --argjson reviews "$REVIEWS_JSON" \
  --argjson pr "$PR_JSON" '
  def marker_re: "<!--\\s*<review_comment_addressed:[^>]+>\\s*-->";
  def fingerprint($prefix; $id): "\($prefix)-\($id)";

  def review_threads:
    ($comments // [])
    | group_by(.in_reply_to_id // .id)
    | map(
        sort_by(.created_at)
        | {
            comments: .,
            root: .[0],
            addressed: (map(.body // "") | any(test(marker_re))),
            my_replies: (map(select(.user.login == $me)) | sort_by(.created_at)),
            reviewer_comments: (map(select(.user.login != $me)) | sort_by(.created_at))
          }
      )
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
    | map({
        artifact_type: "review_thread",
        fingerprint: fingerprint("review_thread"; .root.id),
        reply_api: "review_comment_reply",
        id: .root.id,
        in_reply_to_id: .root.in_reply_to_id,
        body: .root.body,
        path: .root.path,
        line: (.root.line // .root.original_line),
        user: .root.user.login,
        state: "unresolved",
        created_at: .root.created_at,
        thread_comment_count: (.comments | length)
      });

  def pr_comments:
    ($issue_comments // [])
    | map(select((.body // "" | test(marker_re)) | not))
    | map({
        artifact_type: "pr_comment",
        fingerprint: fingerprint("pr_comment"; .id),
        reply_api: "pr_comment",
        id: .id,
        body: .body,
        path: null,
        line: null,
        user: .user.login,
        state: "open",
        created_at: .created_at
      });

  def review_submissions:
    ($reviews // [])
    | map(select((.body // "") != "" and (.state | IN("COMMENTED", "CHANGES_REQUESTED"))))
    | map(select((.body // "" | test(marker_re)) | not))
    | map({
        artifact_type: "review_submission",
        fingerprint: fingerprint("review_submission"; .id),
        reply_api: "pr_comment",
        id: .id,
        body: .body,
        path: null,
        line: null,
        user: .user.login,
        state: .state,
        created_at: .submitted_at
      });

  def status_checks:
    ($pr.statusCheckRollup // [])
    | map(select((.conclusion // .status // "") | IN("SUCCESS", "COMPLETED", "SKIPPED", "NEUTRAL") | not))
    | map({
        artifact_type: "status_check",
        fingerprint: fingerprint("status_check"; (.name // .workflowName // .context // "unknown")),
        reply_api: "none",
        id: (.databaseId // .name // .context),
        body: (.name // .workflowName // .context // "status check"),
        path: null,
        line: null,
        user: "github",
        state: (.conclusion // .status // "UNKNOWN"),
        details_url: (.detailsUrl // .targetUrl // null)
      });

  def merge_readiness:
    if (($pr.mergeable == "MERGEABLE") and (($pr.mergeStateStatus // "UNKNOWN") | IN("CLEAN", "HAS_HOOKS"))) then
      []
    else
      [{
        artifact_type: "merge_readiness",
        fingerprint: "merge_readiness-\($pr.mergeable // "UNKNOWN")-\($pr.mergeStateStatus // "UNKNOWN")",
        reply_api: "none",
        id: "merge_readiness",
        body: "mergeable=\($pr.mergeable // "UNKNOWN"), mergeStateStatus=\($pr.mergeStateStatus // "UNKNOWN")",
        path: null,
        line: null,
        user: "github",
        state: ($pr.mergeStateStatus // "UNKNOWN"),
        pr_url: $pr.url
      }]
    end;

  review_threads + pr_comments + review_submissions + status_checks + merge_readiness
'
