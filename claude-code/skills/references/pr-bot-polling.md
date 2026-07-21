# PR Bot Review Polling — Shared Reference

Used by `ywc-sequential-executor` and `ywc-parallel-executor` to detect automated review bot comments (CodeRabbit, Codex Review, Claude Review, etc.) before merging a PR. The polling shape, jq query, and detection patterns are identical across executors. Only the **post-bot action** differs: sequential re-runs CI then re-polls, while parallel re-polls and proceeds to wave-local merge.

## When This Applies

This is a **conditional** sub-step. Not all repositories use automated review bots. If no bot comments arrive after the full polling window, skip the sub-step and proceed to merge.

## Why Polling Is Required

Automated review bots (CodeRabbit, Codex Review, Claude Review) need time to analyze a PR after CI passes. They typically begin analysis when CI completes and post their reviews 1–5 minutes later. Polling immediately after CI often returns 0 — not because the project has no bots, but because the bots have not posted yet. The 60-second initial wait and the up-to-300-second polling window absorb this delay. Skipping either makes premature merges likely.

## Polling Loop

**Preferred execution — use the bundled script:**

```bash
bash claude-code/skills/scripts/poll-pr-reviews.sh <pr-number>
# stdout (last line): BOT_COUNT=<n> WINDOW=complete|degraded
# exit 0 → BOT_COUNT > 0 (bots posted)
# exit 1 → BOT_COUNT == 0 after the FULL window (no bots) → merge allowed
# exit 3 → WINDOW=degraded: every gh query failed → NOT evidence of zero bots
```

> **Mandatory Bash-call parameter**: invoke this with `timeout: 600000`. The window is up to 360 s; Claude Code's **default Bash timeout is 120 s**, which kills the poll mid-window. A bot that posts around the 2-minute mark is exactly the case that gets missed.

**Completion gate — the merge condition is not a number, it is the marker.** Only `BOT_COUNT=0 WINDOW=complete` (exit 1) permits merging:

| Observed | Meaning | Required action |
|---|---|---|
| `BOT_COUNT=<n>` with n > 0, `WINDOW=complete`, exit 0 | Bots posted | Invoke `ywc-handle-pr-reviews` |
| `BOT_COUNT=0 WINDOW=complete`, exit 1 | Full window, no bots | Proceed to merge |
| `WINDOW=degraded`, exit 3 | All `gh` queries failed | Re-run the poll; do **not** merge |
| No `WINDOW=` line at all (Bash timeout, kill, hang) | Poll never finished | Re-run with `timeout: 600000`; do **not** merge |

A Bash timeout, a `fetch failed`, or truncated output is **never** evidence of `BOT_COUNT == 0`. Merging on a missing marker line is the exact failure that shipped an unaddressed P1 bot finding in a downstream project.

Use the exit code plus the marker line to choose the action in [Action When Bot Comments Exist](#action-when-bot-comments-exist-bot_count--0) or [Action When No Bot Comments](#action-when-no-bot-comments) below. The script handles the 60-second initial wait, up to 10 × 30-second polls, and the jq query — no need to inline the loop.

Do not copy or customize the polling loop inline. The bundled script owns the
`WINDOW=complete` contract; invoke it as one Bash call with `timeout: 600000`.

## Why Two Sources Are Required

GitHub exposes PR feedback in three places, and **no single `gh` call returns all three**. Line-level code annotations — the most common output from CodeRabbit and similar bots — are not available to `gh pr view` at all.

| Feedback | Where it lives | How to fetch |
|---|---|---|
| Top-level review submissions (Approve / Request Changes) | `reviews` | `gh pr view --json reviews` |
| General PR comments (issue-style, not attached to code lines) | `comments` | `gh pr view --json comments` |
| Line-level review comments (code annotations) | review threads | `gh api repos/{owner}/{repo}/pulls/<n>/comments` |

> **`gh pr view --json reviewThreads` does not exist.** It is not an accepted field name, and `gh` rejects the *entire* call with `Unknown JSON field: "reviewThreads"` — so a query listing it returns nothing at all, not merely a partial result. Combined with a `|| echo "0"` fallback this yields a permanent `BOT_COUNT=0`: polling appears to run, always reports no bots, and never blocks a merge. Fetch line-level comments from the REST endpoint instead, and sum the two counts.

## Known Automated Reviewer Patterns

Match case-insensitively against `author.login`:

- `coderabbitai`, `coderabbit[bot]` — CodeRabbit
- `github-actions[bot]` posting Codex Review or Claude Review output
- `claude[bot]`, `anthropic[bot]`, `anthropic-review[bot]` — Anthropic-based reviewers
- Any other bot account identifiable from the repository's recent PR history

Update the regex in the polling loop if the project uses a bot not listed above.

## Action When Bot Comments Exist (`BOT_COUNT > 0`)

1. Invoke the `ywc-handle-pr-reviews` skill to process and address all comments on the current PR.
2. After the skill completes (all comments addressed and pushed), the executor's **post-bot action** kicks in. This is executor-specific:
   - **Sequential**: re-run CI verification (the push triggered a new CI run; wait for it to pass), then re-run this polling loop because the new push may have triggered new bot comments. Repeat until no new comments appear within the polling window.
   - **Parallel**: re-run this polling loop (the wave does not gate on CI between bot fixes). Repeat until no new comments appear within the polling window.

## Action When No Bot Comments

If `BOT_COUNT == 0` **and the run printed `WINDOW=complete`** (full 300-second window plus the 60-second initial wait), skip this sub-step entirely and proceed to merge. Without that marker the window did not close — re-run the poll instead of merging.

## Non-Stop Principle

The 60-second initial wait and the up-to-300-second polling window are a **required wait gate, not a pause**. "Non-stop" means the executor does not stop for user confirmation between tasks — it does not mean polling windows are optional or skippable. Never shorten or skip the polling loop in range mode. `BOT_COUNT == 0` immediately after CI is not evidence that no bots are active; it means they have not posted yet.

When `BOT_COUNT > 0`, `ywc-handle-pr-reviews` handles the comments autonomously. That skill escalates only controversial or ambiguous comments to the user — routine automated feedback does not interrupt range execution. The escalation point is inside `ywc-handle-pr-reviews`, not here.
