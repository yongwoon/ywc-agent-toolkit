---
name: ywc-mine-review-history
description: >-
  (ywc) Use when the user wants to batch-mine bot review comments (CodeRabbit
  / Codex Review / Claude Review) across many already-merged PRs and surface
  recurring defect classes as candidate durable learnings — a retrospective
  sweep of PR history that predates review-learnings adoption. Triggers:
  "review history 마이닝", "PR 리뷰 이력 스캔", "batch mine PR reviews", "recurring
  defect sweep", "PR 리뷰 히스토리 분석", "レビュー履歴マイニング", "mine review history",
  "PR 리뷰 일괄 수집". Do not use for a single already-open PR's review comments
  (use ywc-handle-pr-reviews), a single already-merged PR's on-demand
  bot-comment harvest (use ywc-review-learnings --mode update --source pr),
  or a single incident's postmortem (use ywc-incident-postmortem) — this
  skill's value is specifically the batch/retrospective sweep across N PRs,
  not any single-PR or single-incident capture.
---

# ywc-mine-review-history

**Announce at start:** "I'm using the ywc-mine-review-history skill to batch-mine bot review comments across merged PRs and surface recurring defect classes."

This skill fetches bot review comments (CodeRabbit / Codex Review / Claude Review) across N already-merged PRs, classifies each comment accept-vs-dismiss using the same rule `ywc-review-learnings --source pr` already applies to a single PR, clusters classified comments into defect classes, and offers classes that recur across `--min-recurrence` distinct PRs to `ywc-review-learnings --mode update --source pr` as promotion candidates. It closes the gap between `ywc-review-learnings` (single PR, on demand) and `ywc-incident-postmortem` (single incident) — neither covers a batch sweep of PR history that predates either skill's adoption.

This skill never writes `docs/review-learnings.md` or `references/recurring-defects.md` directly. Its only write path is delegating to `ywc-review-learnings --mode update --source pr`, which applies its own confirmation-gated CHANGESET before any write. `references/recurring-defects.md`-style cross-project append infrastructure is out of scope — that reference stays read-only in this repository.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "Skip --limit/--since, just scan everything" | Unbounded scans risk `gh api` rate-limit exhaustion on large repos (NFR: Performance). FR-1 requires at least one bound — the fetch script refuses to run with neither. |
| "This defect class only hit 2 PRs, promote it anyway since it looks important" | The `--min-recurrence` gate (default 3, `count >= threshold`) exists precisely to separate real recurring patterns from noise. Below-threshold classes are still reported, never silently dropped — but never auto-promoted either. |
| "Count raw comment occurrences toward recurrence, more comments = more signal" | FR-4 counts **distinct PRs**, not comments — two comments in one PR count once. Counting raw comments inflates a false recurrence signal. |
| "Write the promoted learnings straight to docs/review-learnings.md, skip the confirmation gate" | This skill never writes `docs/review-learnings.md` directly (AC5) — every promotion candidate goes through `ywc-review-learnings --mode update --source pr`'s own confirmation-gated CHANGESET, no exceptions even for a high-recurrence class. |
| "A gh api call failed mid-sweep, treat it as zero comments for that PR and continue" | Swallowing a failed `gh api` call as an empty result silently understates the mined evidence set (NFR: Reliability). The fetch script propagates the failure (non-zero exit) — never `\|\| true` it. |
| "Use the narrower capture-sources.md bot regex, it's the existing convention there" | The Bot-login allowlist decision deliberately widens to the shared executor regex (`coderabbitai\|coderabbit\|codex\|claude\|anthropic\|github-actions`) — under-detecting a bot login in a batch sweep silently shrinks the mined evidence set; false positives are already absorbed by the accept/dismiss classification step. |
| "This is a batch retrospective task like ywc-incident-postmortem, treat it the same way" | `ywc-incident-postmortem` covers one incident with one root cause. This skill covers a corpus of N merged PRs with no single triggering incident — different scope, different report shape, different promotion source. |

**Violating the letter of these rules is violating the spirit.** A batch sweep that under-counts recurrence, bypasses the confirmation gate, or silently drops evidence produces exactly the noisy, unconfirmed learnings this skill family exists to avoid.

## Arguments

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| `--limit` | `--limit <n>` | — | Most-recent N merged PRs to sweep. At least one of `--limit` / `--since` is required (FR-1) |
| `--since` | `--since <date>` | — | Merged-after date (`YYYY-MM-DD`). At least one of `--limit` / `--since` is required (FR-1) |
| `--min-recurrence` | `--min-recurrence <n>` | `3` | Distinct-PR recurrence threshold for promotion (FR-5). A class meeting or exceeding this is a promotion candidate; a class below it is reported only |

## Procedure

### Step 1 — Scope selection (FR-1)

Confirm at least one of `--limit` or `--since` was given. If neither was given, stop and ask — this skill never runs an unbounded "scan everything" sweep (NFR: Performance).

### Step 2 — Batch fetch (FR-2)

```bash
bash claude-code/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh --limit <n>
# or: --since <date>, or both together
```

The script iterates the selected merged PRs and emits NDJSON to stdout — one line per bot review comment, tagged with its source PR number (`{pr, id, path, line, body, in_reply_to_id}`). It reuses the same `gh api --paginate` query shape as `ywc-review-learnings`'s `--source pr` path (see [references/capture-sources.md](../ywc-review-learnings/references/capture-sources.md#--source-pr-bot-comment-harvest)), with the broader anchored bot-login regex documented in the script header. `gh api` / `gh pr list` failures propagate as a non-zero exit — treat any failure as a hard stop, never as "zero comments for that PR."

### Step 3 — Accept/dismiss classification (FR-3)

For each fetched comment, apply the identical rule `ywc-review-learnings`'s `--source pr` path already uses (see [capture-sources.md](../ywc-review-learnings/references/capture-sources.md#--source-pr-bot-comment-harvest)'s classification table):

| Outcome signal | Classification |
|---|---|
| Thread resolved and the fix appears in a later commit | `DO` |
| A reply states the comment was wrong / not applicable | `FALSE-POSITIVE` |
| Open, no resolution, no reply | skip |

Apply this per comment across the whole NDJSON stream, not per individual PR.

### Step 4 — Defect-class clustering and recurrence count (FR-4)

Cluster classified (`DO` / `FALSE-POSITIVE`) comments into defect classes by judgment — there is no controlled vocabulary to automate this (the same documented limitation as `ywc-impl-review`'s within-run occurrence counting). For each class, count **distinct PRs** exhibiting it — two comments in the same PR count once toward recurrence, never twice.

### Step 5 — Recurrence-gated promotion (FR-5)

For each defect class with distinct-PR count `>= --min-recurrence`:

- Offer it to `ywc-review-learnings --mode update --source pr` as a promotion candidate, with the aggregated evidence (contributing PR numbers, one representative comment body per PR) as context.
- `ywc-review-learnings` applies its own confirmation-gated CHANGESET before writing anything to `docs/review-learnings.md` — this skill never bypasses that gate and never writes the file itself.

Classes below the threshold are listed in this skill's own report (Step 6) only — never silently dropped, never auto-promoted.

### Step 6 — Report surface (FR-6)

Always emit, regardless of what was found (auditability parity with `ywc-impl-review`'s "Learning candidates" block — a `(none)` section is stated, never omitted):

- PRs scanned (count + date range covered)
- Comments fetched
- Comments classified `DO` / `FALSE-POSITIVE` / skipped
- Defect classes found
- Which classes met vs missed the `--min-recurrence` threshold

## Edge Cases

- **Zero merged PRs in the selected window** — report `PRs scanned: 0`, no classes, no promotion candidates. Not an error; the fetch script exits `0`.
- **A PR has bot comments but no human reply/resolution on any of them** — all its comments classify as "skip"; the PR still counts toward `PRs scanned` but contributes no classified evidence.
- **A defect class recurs across exactly `--min-recurrence` PRs (boundary)** — promoted (`count >= threshold`, inclusive).
- **The same defect class is already an active learning in `docs/review-learnings.md`** — `ywc-review-learnings`'s own existing dedupe/skip behavior for already-captured learnings applies unchanged; this skill does not re-implement that check.
- **`gh` is unauthenticated or rate-limited mid-sweep** — the fetch script propagates the `gh api` failure rather than silently returning partial/empty results as if the window were genuinely empty.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | The batch fetch must respect a caller-supplied bound (`--limit` or `--since`) — no default unbounded scan (FR-1). |
| Security | The bot-login allowlist regex is anchored (`^(coderabbitai\|coderabbit\|codex\|claude\|anthropic\|github-actions)\[bot\]$`-equivalent), not a bare substring match. |
| Reliability | `gh api` failures propagate (non-zero exit) — never swallowed with `\|\| true`. |
| Auditability | The report surface (Step 6 / FR-6) is never omitted, even when a section is empty. |

## Out of Scope

- Cross-project `recurring-defects.md` append infrastructure (a `source: mining` provenance line, an append-only-sink schema) — `references/recurring-defects.md` stays read-only in this repository.
- Porting to `codex/skills/`.
- Any change to `claude-code/agents/`.
- A new `--source mining` value on `ywc-review-learnings` — the existing `--source pr` classification rule is reused verbatim.
