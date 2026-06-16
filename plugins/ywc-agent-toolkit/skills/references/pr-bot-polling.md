# PR Bot Review Polling — Shared Reference

Used by `ywc-sequential-executor`, `ywc-parallel-executor`, and `ywc-finish-branch` to detect automated review bot comments (CodeRabbit, Codex Review, Claude Review, etc.) before merging a PR. The polling shape, jq query, and detection patterns are identical across executors. Only the **post-bot action** differs: sequential re-runs CI then re-polls, while parallel re-polls and proceeds to wave-local merge.

## When This Applies

This is a **conditional** sub-step. Not all repositories use automated review bots. If no bot comments arrive after the full polling window, skip the sub-step and proceed to merge.

## Why Polling Is Required

Automated review bots (CodeRabbit, Codex Review, Claude Review) need time to analyze a PR after CI passes. They typically begin analysis when CI completes and post their reviews 1-5 minutes later. Polling immediately after CI often returns 0 — not because the project has no bots, but because the bots have not posted yet. The 60-second initial wait and the up-to-300-second polling window absorb this delay. Skipping either makes premature merges likely.

## Polling Loop

**Preferred execution — use the bundled script:**

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/poll-pr-reviews.sh" <pr-number>
# stdout: BOT_COUNT integer
# exit 0 -> BOT_COUNT > 0 (bots posted); exit 1 -> BOT_COUNT == 0 (no bots after full window)
```

Use the exit code to choose the action in [Action When Bot Comments Exist](#action-when-bot-comments-exist-bot_count--0) or [Action When No Bot Comments](#action-when-no-bot-comments) below. The script handles the 60-second initial wait, up to 10 x 30-second polls, and the jq query — no need to inline the loop.

**Reference implementation (if customization is needed):**

> **Critical execution rule**: Submit the ENTIRE block below as a **single shell call**. Never split it into per-iteration calls. If you run `gh pr view` once, see `BOT_COUNT=0`, and then issue a separate `sleep 30 && gh pr view` call, command hooks may block the `sleep &&` chain and the polling loop stalls entirely.
>
> The approved wait-for-condition pattern is `until <check>; do sleep N; done` — sleep inside the loop body is permitted; `sleep N && command` as a standalone call is blocked in some agent runtimes.

```bash
# Run this ENTIRE block as a SINGLE shell call — never split per iteration.
# Initial wait (60s) is inside the loop to avoid a standalone `sleep 60`
# that some command hooks block as a "long leading sleep" command.
POLL_COUNT=0
BOT_COUNT=0
until [ "$BOT_COUNT" -gt 0 ] || [ "$POLL_COUNT" -ge 11 ]; do
  if [ "$POLL_COUNT" -eq 0 ]; then
    sleep 60  # initial wait: bots begin analysis only after CI completes
  else
    sleep 30  # 30s between subsequent polls
  fi
  BOT_COUNT=$(gh pr view <pr-number> --json reviews,comments,reviewThreads \
    --jq '
      [ .reviews[],
        .comments[],
        (.reviewThreads[]?.comments[]?)
      ]
      | map(select(.author.login
          | test("coderabbitai|coderabbit|codex|claude|anthropic|github-actions"; "i")))
      | length
    ')
  POLL_COUNT=$((POLL_COUNT + 1))
done
# Total window: 60s (initial) + up to 10 x 30s = 360s max
# BOT_COUNT > 0 -> bots posted -> invoke ywc-handle-pr-reviews
# BOT_COUNT == 0 -> no bots after full window -> proceed to merge
```

## Why `reviewThreads` Is Included

GitHub stores PR data in three distinct fields. Line-level code annotations — the most common output from CodeRabbit and similar bots — live in `reviewThreads`, not in `reviews` or `comments`. Without `reviewThreads` the query misses most bot feedback.

| GitHub PR Data Field | What It Contains |
|---|---|
| `reviews` | Top-level review submissions (Approve / Request Changes) |
| `comments` | General PR comments (issue-style, not attached to code lines) |
| `reviewThreads` | Line-level review comments (code annotations) |

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

If `BOT_COUNT == 0` after the full 300-second polling window (plus the 60-second initial wait), skip this sub-step entirely and proceed to merge.

## Non-Stop Principle

The 60-second initial wait and the up-to-300-second polling window are a **required wait gate, not a pause**. "Non-stop" means the executor does not stop for user confirmation between tasks — it does not mean polling windows are optional or skippable. Never shorten or skip the polling loop in range mode. `BOT_COUNT == 0` immediately after CI is not evidence that no bots are active; it means they have not posted yet.

When `BOT_COUNT > 0`, `ywc-handle-pr-reviews` handles the comments autonomously. That skill escalates only controversial or ambiguous comments to the user — routine automated feedback does not interrupt range execution. The escalation point is inside `ywc-handle-pr-reviews`, not here.
