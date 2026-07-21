# PR Bot Review Polling — Shared Reference

Used by `ywc-create-pr`, `ywc-sequential-executor`, `ywc-parallel-executor`, and `ywc-finish-branch` to wait for automated review bot comments (CodeRabbit, Codex Review, Claude Review, etc.) before the mandatory PR health sweep. The polling shape, jq query, and detection patterns are identical across executors.

## When This Applies

This is a **required wait gate** for PR lifecycle flows that may merge, hand off, or claim a PR is ready. Not all repositories use automated review bots, so `BOT_COUNT == 0` is a valid polling result. It is not permission to skip the PR health sweep. After the polling window closes, always invoke `ywc-handle-pr-reviews`; the handler checks review artifacts, CI status, and merge-readiness even when no bot comments were detected.

## Why Polling Is Required

Automated review bots (CodeRabbit, Codex Review, Claude Review) need time to analyze a PR after CI passes. They typically begin analysis when CI completes and post their reviews 1-5 minutes later. Polling immediately after CI often returns 0 — not because the project has no bots, but because the bots have not posted yet. The 60-second initial wait and the up-to-300-second polling window absorb this delay. Skipping either makes premature merges likely.

## Polling Loop

**Preferred execution — use the bundled script:**

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/poll-pr-reviews.sh" <pr-number>
# stdout: BOT_COUNT integer
# exit 0 -> BOT_COUNT > 0 (bots posted); exit 1 -> BOT_COUNT == 0 (no bots after full window)
# exit 3 -> GitHub reads repeatedly failed; exit 4 -> no valid completed-poll artifact
```

Allow this shell call at least **600 seconds** to finish. A tool timeout, interruption, or failed GitHub read is **not** a zero-result poll. The script handles the 60-second initial wait, up to 10 x 30-second polls, transient GitHub-read retries, and the jq query — no need to inline the loop.

When the script exits 0 or 1, it atomically writes a completion artifact under the repository's Git directory. Before any merge or PR-ready claim, verify that the current PR has that artifact:

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/poll-pr-reviews.sh" --verify <pr-number>
```

This is a **mechanical merge gate**: do not run `gh pr merge` and do not claim the PR is ready if either the poll or `--verify` fails. The artifact is removed before every new poll and written only after the complete window finishes. `--verify` also checks the recorded PR head SHA against GitHub, so a stale result, a new push, or a process killed by a tool timeout cannot be mistaken for `BOT_COUNT == 0`.

Use the exit code as telemetry only after the completion artifact verifies. `BOT_COUNT > 0` tells you review bots posted during the window; `BOT_COUNT == 0` tells you none were detected after the full wait. In both cases, continue to [Action After Polling](#action-after-polling).

Do not copy or customize the polling loop inline. The bundled script owns the
completion artifact and `--verify` contract; invoke it as one shell call with a
600-second timeout instead.

## Why Two Sources Are Required

GitHub exposes PR feedback in three places, and **no single `gh` call returns all three**. Line-level code annotations — the most common output from CodeRabbit and similar bots — are not available to `gh pr view` at all.

| Feedback | Where it lives | How to fetch |
|---|---|---|
| Top-level review submissions (Approve / Request Changes) | `reviews` | `gh pr view --json reviews` |
| General PR comments (issue-style, not attached to code lines) | `comments` | `gh pr view --json comments` |
| Line-level review comments (code annotations) | review threads | `gh api repos/{owner}/{repo}/pulls/<n>/comments` |

> **`gh pr view --json reviewThreads` does not exist.** It is not an accepted field name, and `gh` rejects the *entire* call with `Unknown JSON field: "reviewThreads"` — so a query listing it returns nothing at all, not merely a partial result. A poll built on it can never observe a bot comment. Fetch line-level comments from the REST endpoint instead, and sum the two counts.

## Known Automated Reviewer Patterns

Match case-insensitively against `author.login`:

- `coderabbitai`, `coderabbit[bot]` — CodeRabbit
- `github-actions[bot]` posting Codex Review or Claude Review output
- `claude[bot]`, `anthropic[bot]`, `anthropic-review[bot]` — Anthropic-based reviewers
- Any other bot account identifiable from the repository's recent PR history

Update the regex in the polling loop if the project uses a bot not listed above.

## Action After Polling

Always invoke the `ywc-handle-pr-reviews` skill as a PR health sweep for the current PR, regardless of whether `BOT_COUNT` is greater than zero. A zero bot-comment count is not terminal success; it only means the polling window did not observe a known automated reviewer. After the handler runs, re-poll and re-verify whenever it pushes changes.

The handler owns the three gates:

- **Review artifacts**: line threads, PR comments, top-level review submissions, and review-like failed checks.
- **CI status**: failed or pending status checks that block readiness.
- **Merge-readiness**: conflicts, behind branches, blocked merge states, and hook-required states.

If `ywc-handle-pr-reviews` applies fixes, re-verify CI because the push triggered a fresh run, then re-run this polling loop because the new push may trigger new bot comments. Repeat until CI is green, merge-readiness is clean, and no new review artifacts arrive within the polling window.

## Non-Stop Principle

The 60-second initial wait and the up-to-300-second polling window are a **required wait gate, not a pause**. "Non-stop" means the executor does not stop for user confirmation between tasks — it does not mean polling windows are optional or skippable. Never shorten or skip the polling loop in range mode. `BOT_COUNT == 0` immediately after CI is not evidence that no bots are active; it means they have not posted yet.

`ywc-handle-pr-reviews` handles routine artifacts autonomously. That skill escalates only controversial or ambiguous comments to the user — routine automated feedback does not interrupt range execution. The escalation point is inside `ywc-handle-pr-reviews`, not here.
