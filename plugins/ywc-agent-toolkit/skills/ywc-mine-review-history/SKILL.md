---
name: ywc-mine-review-history
description: >-
  (ywc) Use when batch-mining bot review comments across many already-merged
  PRs to find recurring defect classes and propose durable review learnings.
  Triggers: "mine review history", "batch mine PR reviews", "recurring defect
  sweep", "PR 리뷰 이력 스캔", "レビュー履歴マイニング". Do not use for a
  single PR (use ywc-handle-pr-reviews or ywc-review-learnings), an open review,
  an incident postmortem, or implementation review.
---

# ywc-mine-review-history

**Announce at start:** "I'm using the ywc-mine-review-history skill to batch-mine bot review comments across merged PRs and surface recurring defect classes."

This is a bounded, retrospective producer. It never edits `docs/review-learnings.md`,
`references/recurring-defects.md`, or a packaged catalog. Project-local writes are
delegated to `$ywc-review-learnings --mode update --source mining` after one complete
user-confirmed changeset.

## Arguments

| Argument | Default | Meaning |
|---|---:|---|
| `--repo <owner/repo>` | current repository | Repository scope for every GitHub request |
| `--limit <n>` | required unless `--since` | First N merged PRs in `gh pr list` returned order |
| `--since <YYYY-MM-DD>` | — | Inclusive UTC lower bound on `mergedAt`; alone uses limit 200 |
| `--min-recurrence <n>` | `3` | Distinct-PR threshold for a maintainer proposal |
| `--dry-run` | off | Present the changeset and stop before delegation |

`--limit` and `--min-recurrence` are positive integers. Duplicate flags and
invalid dates are usage errors. At least one scope bound is required.

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "Scan all history by default" | A scope is mandatory; unbounded GitHub scans are unsafe and non-repeatable. |
| "Two comments in one PR prove recurrence" | Recurrence is counted by distinct PR, with each PR contributing at most once. |
| "Raw NDJSON proves the bot was accepted" | Resolution, human dismissal, and later-fix evidence are separate checks. |
| "Write directly to review-learnings or the catalog" | The local owner owns durable writes; shared-catalog output is proposal-only. |
| "Missing evidence can be inferred" | Drop and account for ambiguous, incomplete, null-anchor, renamed, or unrelated evidence. |

## Workflow

1. **Scope.** Resolve `--repo` with `gh repo view` when omitted. Require a bound,
   confirm the selected PR count and the returned-order/date-window semantics.
2. **Fetch.** Run `scripts/fetch-bulk-review-comments.sh <owner/repo> ...`.
   Its NDJSON contains only `pr`, `id`, `path`, `line`, `body`, and
   `in_reply_to_id`; it does not contain resolution or human-reply evidence.
3. **Evidence.** For every candidate, use repository-scoped GraphQL with
   `repository(owner:, name:)`, paginate both `reviewThreads` and nested
   `comments`, map the database id to `isResolved`, `createdAt`, and a
   non-bot reply. If pagination or mapping is incomplete, account and drop.
4. **Later fix.** A resolved comment is `DO` only when a later commit has the
   same filename and an exact `+start,count` hunk whose inclusive new-line range
   contains the non-null comment line. Missing/outdated anchors, renames,
   unrelated hunks, or unavailable API evidence are drops. A reasoned non-bot
   dismissal is `FALSE-POSITIVE`.
5. **Cluster.** Generalize accepted findings by class and polarity. Count each
   class once per distinct PR. Report below-threshold classes; do not promote them.
6. **Route.** Read the project-local learning owner for duplicates. For each
   candidate, prepare rule, why, polarity, target, representative evidence, and
   distinct PR provenance. For a shared-catalog threshold, read the full catalog,
   report covering entries, or render an `A-NNN` maintainer proposal without
   modifying the catalog.
7. **Confirm and report.** Present the whole changeset before any write. On
   confirmation, delegate local entries to `$ywc-review-learnings --mode update
   --source mining`; `--dry-run` stops before this delegation. Always report PRs
   scanned, date range, fetched/classified/dropped counts, classes, thresholds,
   and proposal status.

## Safety and validation

Use the exact anchored bot allowlist
`^(coderabbitai|chatgpt-codex-connector|github-actions)\[bot\]$`.
Every GitHub request must carry the resolved repository. Propagate per-PR API
failures while continuing later PRs, and return a nonzero final status. Never
create an `Appended entries` section or modify generated marketplace files by
hand.
