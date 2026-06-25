---
name: ywc-handle-pr-reviews
description: >-
  (ywc) Use when handling an open PR's review feedback — addressing code review comments, responding to GitHub PR review threads, and leaving the PR mergeable by also clearing any CI failures and base-branch conflicts on that same PR. Triggers: "handle PR reviews", "address review comments", "respond to PR comments", "fix PR CI", "resolve PR conflict", "PR CI 고쳐줘", "PR conflict 해결", "리뷰 대응", "리뷰 코멘트 처리", "レビュー対応". Do not use for creating a new PR (use ywc-create-pr), performing a code review yourself (use ywc-impl-review), for the verify-before-agreeing discipline on reviewer feedback (use ywc-receive-review), for storing or reading durable review preferences as learnings (use ywc-review-learnings), or for changes outside an open PR context.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Agent
---

# Handle PR Review Comments

**Announce at start:** "I'm using the ywc-handle-pr-reviews skill to leave this PR mergeable — addressing review comments, then clearing CI and conflicts."

Handling a PR is not just replying to comments. It means leaving the PR **mergeable**: review comments addressed, CI green, and no conflict with the base. Review the comments, fix issues where needed, reply to each thread, then clear CI and merge-readiness — every time.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "This comment is just opinion, no fix needed" | Even disagreement requires a reply explaining why. Silent skip looks like neglect. |
| "I'll batch all replies after fixing everything" | Reply per thread as fixes land. Reviewers track which threads are resolved. |
| "Push without reply, the diff speaks for itself" | Reviewers cannot tell intent from diff alone. Always pair fix with reply. |
| "Resolving the thread without reply is fine" | Resolving without reply implies the reviewer's concern was wrong. Always state how it was addressed. |
| "Conflict in suggestions, pick one and move on" | Surface the conflict to the user. Do not silently choose between reviewer A and reviewer B. |
| "PR not found for this branch, scan recent PRs" | Stop and ask. Acting on a wrong PR overwrites unrelated reviewer threads. |
| "All review comments are addressed — CI is a separate concern" | Fixes to source code (refactors, new imports, logic changes) can break CI. Always re-verify CI after pushing review fixes. A PR with all comments addressed but failing CI is still blocked from merging. |
| "The comments only needed replies, no code changed — so CI is fine to skip" | CI can already be red for reasons unrelated to the comments (a flaky earlier push, a base-branch change, a dependency break). Handling a PR means leaving it mergeable. Always check current CI status when handling a PR, even when your replies pushed no code. |
| "CI is green and comments are addressed — the PR is mergeable" | While the review was in progress the base branch may have advanced and the PR may now be `CONFLICTING`. Handling a PR means leaving it mergeable, which requires checking `gh pr view --json mergeable,mergeStateStatus`, not just CI. A conflicting PR is blocked from merge regardless of how many comments were resolved. |
| "The PR conflicts with base — rebase the branch to clear it" | Rebasing rewrites SHAs and orphans the very review threads you are replying to. Merge the base *into* the feature branch (`git merge --no-ff origin/<base>`) instead. See `references/pr-conflict-resolution.md`. |
| "No unresolved comments — nothing to handle, the PR is done" | Zero comments clears only the first of three gates. CI may be red and the base may have advanced into a conflict regardless of whether anyone commented. The CI gate (Step 7) and merge-readiness gate (Step 8) are **mandatory on every invocation** — never report done from an empty comment array without running both. |

**Violating the letter of these rules is violating the spirit.** Code review is a conversation, not a checklist.

## Definition of Done

Handling a PR means leaving it **mergeable**, which requires clearing **three independent blockers** — not just the first one:

| # | Gate | Cleared when | Step |
|---|---|---|---|
| 1 | **Review comments** | Every unresolved thread is fixed-or-answered and replied to | Steps 2–5 |
| 2 | **CI status** | `gh pr checks` is green (or failures triaged to the user) | Step 7 |
| 3 | **Merge-readiness** | `gh pr view --json mergeable` is `MERGEABLE` / `CLEAN` (or a real conflict surfaced) | Step 8 |

These gates are **independent**. A PR with every comment answered but red CI, or green CI but `CONFLICTING` against the base, is **not handled**. Gates 2 and 3 run on **every** invocation — including when Step 2 finds zero unresolved comments, because CI can be red and the base can have advanced regardless of whether anyone commented.

**Before touching the PR, create a TodoWrite list with all three gates** so none is silently skipped. Do not report the run complete until all three are cleared, or explicitly surfaced to the user as blocked.

## Context

- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Task

Follow the steps below to handle PR review comments.

### Step 1: Identify PR Number

- If a PR number is specified in `$ARGUMENTS`, use it
- Otherwise, identify the current branch's PR with `gh pr view --json number`
- If no PR exists for the current branch, stop and notify the user rather than proceeding blindly

Resolve `{owner}/{repo}` dynamically at this stage — it's used throughout the workflow:

```bash
gh repo view --json nameWithOwner --jq .nameWithOwner
```

### Step 2: Retrieve and Filter Comments

Retrieve all PR review comments and filter out those that don't need action. This prevents duplicate work and keeps the process focused on genuinely unresolved feedback.

```bash
bash tools/claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh \
  {owner}/{repo} {pr_number}
# exit 0 → JSON array of unresolved threads on stdout (may be [])
# exit 1 → gh CLI error (not authenticated or PR not found)
```

The script fetches paginated comments, groups them into threads, and applies the skip conditions automatically: threads containing `<!-- <review_comment_addressed> -->` are dropped, and threads where your reply is newer than the latest reviewer comment are dropped. The output JSON array contains only actionable threads — each element has `id`, `body`, `path`, `line`, `user`, `created_at`, and `thread_comment_count`.

**If the array is `[]`** (no comments to fix): skip Steps 3–5, but you **must still run Step 7 (CI gate) and Step 8 (Merge-Readiness gate)** before the Final Summary. Zero comments does not mean the PR is mergeable — CI can be red and the base can have advanced into a conflict regardless of whether anyone commented. **Never jump straight to the summary on an empty comment array** — that is the exact path that leaves red CI and conflicts unhandled.

### Step 3: Group and Analyze Comments

Before fixing anything, group all remaining comments by file. Processing file-by-file is more efficient — you read each file once, apply all related fixes together, and create one coherent commit per file instead of jumping back and forth.

**Processing strategy:**

1. Collect all unresolved comments and group by target file path
2. For each file, read the file once and analyze all related comments together
3. Apply fixes for that file and commit as a unit
4. Move to the next file

### Step 4: Classify and Fix Comments

For each comment, classify it into one of four categories:

| Category                                                                                                   | Action                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Approval / Acknowledgment** (tagged `review_comment_addressed`)                                          | Skip — already resolved                                                                                                                                                                 |
| **Clear code change request** (the fix is straightforward and unambiguous)                                 | Apply the fix                                                                                                                                                                           |
| **Controversial or ambiguous change request** (disagreement, architectural concern, or trade-off involved) | Do NOT auto-fix. Present the comment to the user with context, explain the trade-off, and ask for a decision. Reviewer feedback deserves thoughtful consideration, not blind acceptance |
| **Question only** (no code change implied)                                                                 | Reply with an explanation — no fix needed                                                                                                                                               |

**Security guardrails (never auto-apply, always defer to user):**

- Removal of authentication, authorization, or security middleware
- Addition of `eval()`, `exec()`, or dynamic code execution
- Disabling RLS, bypassing tenant isolation, or weakening input validation
- Hardcoded credentials or secrets

**When applying fixes:**

- Read the target file and identify the exact problem area referenced by the comment
- Apply the minimal fix that addresses the reviewer's concern
- If the comment references outdated code (the file has changed since the review), check whether the concern still applies to the current code. If it does, fix the current version. If not, reply explaining the code has already changed

**Commit rules:**

- One commit per file (group all fixes for the same file into a single commit)
- Use commit message format: `fix: summary of the fix`
- Push to remote after all commits are ready — pushing once at the end is cleaner than pushing after each commit

### Step 5: Reply to Comments

**Attitude layer (mandatory)**: every reply must go through the discipline defined in [`ywc-receive-review`](../ywc-receive-review/SKILL.md) — verify each comment against the codebase before agreeing; replies state the fix or a technical pushback ending in a question; the forbidden vocabulary list ("You're absolutely right!", "Great point!", "Thanks!") applies to all `body` content surfaced via the reply API below.

Reply to every processed comment so the reviewer knows their feedback was addressed. Use the thread reply API to keep conversations organized:

```bash
gh api repos/{owner}/{repo}/pulls/{pull_number}/comments/{in_reply_to_id}/replies -F body=@- <<'REPLY_BODY'
...
REPLY_BODY
```

**Reply language:** Match the language of the original comment. If the reviewer wrote in Korean, reply in Korean. If in English, reply in English.

**Reply format by category:**

- **Fixed:**
  ```markdown
  Fixed: [commit-hash](https://github.com/{owner}/{repo}/pull/{pr}/commits/{full_sha})
  Description of what was changed and why
  ```
- **Deferred to user:** `This requires a decision — I've flagged it for the PR author.`
- **No fix needed:** Reply explaining the reasoning (e.g., intentional design choice, already handled elsewhere)
- **Outdated comment:** `This code has been updated since the review. The concern no longer applies because [reason].`

### Step 6: Error Handling

Things can go wrong during the process. Handle these gracefully:

| Error                                 | How to handle                                                                           |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| `gh pr view` fails (no PR for branch) | Stop and tell the user. Don't guess the PR number                                       |
| Push fails (non-fast-forward, remote feature branch advanced) | `git pull --rebase origin <feature-branch>` (rebase on the feature branch you own is safe), then re-push. Don't force-push without approval. See `references/pr-conflict-resolution.md` |
| Comment reply API returns 403/404     | Log the error, skip that reply, and report it in the final summary                      |
| Referenced file no longer exists      | Reply to the comment explaining the file was removed, and skip the fix                  |

### Step 7: CI Status Gate — run on EVERY invocation

**Always run this gate — including when Step 2 found zero comments and your replies pushed no code.** A PR review thread and CI status are two independent blockers on the same PR. Addressing every comment but leaving CI red still leaves the PR unmergeable, so handling a PR means checking both. This gate covers two cases at once: CI regressions introduced by the fixes in Step 4, **and** pre-existing CI failures that were already red before you touched the PR (a flaky earlier push, a base-branch change, a broken dependency).

```bash
PR_NUMBER=$(gh pr view --json number --jq .number)
gh pr checks $PR_NUMBER
# exit 0 = all checks passed; non-zero = one or more checks failed or are pending
```

- **All checks pass**: proceed to Step 8 (Merge-Readiness gate).
- **Checks still pending**: wait for completion with `gh pr checks $PR_NUMBER --watch`, then re-evaluate.
- **Any check fails**:
  1. Get failure logs:
     ```bash
     gh run list --branch $(git branch --show-current) \
       --json databaseId,conclusion \
       --jq '.[] | select(.conclusion == "failure") | .databaseId' | head -1
     gh run view <run-id> --log-failed
     ```
  2. Categorize and fix:
     | Failure type | Fix action |
     |---|---|
     | Lint / format | Run the project's auto-fix command, commit, push |
     | Type / test / build | Analyze output, fix implementation, commit, push |
     | Infra / flaky / clearly unrelated to this PR's scope | Do **not** blindly patch. Surface the failing check and logs to the user and ask how to proceed (e.g., re-run the job, or fix in a separate PR) |
  3. Re-check CI after each push. Up to **2 fix attempts**.
  4. If CI still fails after 2 attempts: record the failing check names in Step 9's summary and set the overall outcome to `DONE_WITH_CONCERNS` (not `DONE`).

### Step 8: Merge-Readiness / Conflict Gate — run on EVERY invocation

**Always run this gate — including when Step 2 found zero comments.** CI green and all comments addressed still does not guarantee the PR can merge — while the review was in progress the base branch may have advanced into a conflict. A PR review thread, CI status, and merge-readiness are three independent blockers on the same PR; handling a PR means leaving all three clear.

> **Action required**: Read [`claude-code/skills/references/pr-conflict-resolution.md`](../references/pr-conflict-resolution.md) before proceeding — it defines the `mergeable` / `mergeStateStatus` semantics and the merge-not-rebase update procedure.

```bash
gh pr view $PR_NUMBER --json mergeable,mergeStateStatus --jq '{mergeable, mergeStateStatus}'
```

- `MERGEABLE` / `CLEAN` → proceed to Step 9 (Final Summary).
- `BEHIND` → the branch is merely out of date (no textual conflict). Follow **Update Branch From Base** (merge the base into the feature branch — never rebase, since that orphans the review threads you just replied to), push, and re-verify CI (one additional cycle).
- `CONFLICTING` / `DIRTY` → follow **Update Branch From Base** in the reference. If it auto-resolves, push and re-verify CI (one additional cycle). If it reports real textual conflicts, surface the conflicting files + PR URL to the user, stop, and set the outcome to `BLOCKED` — do not auto-resolve or force-push.
- `BLOCKED` → a required check or review gate is missing — **not** a conflict. Do not run the base-merge procedure; surface which required check or review is outstanding and set the outcome to `BLOCKED`.
- `UNKNOWN` → poll briefly per the reference, then re-read.

### Step 9: Final Summary

Report the results so the user has a clear picture of what happened. **Report the status of all three Definition-of-Done gates**, not just comments:

- **Comments**: total processed vs skipped; applied fixes with file paths and commit hashes; any comments deferred to the user (with links)
- **CI (Step 7)**: final check status — `green`, or the failing check names + outcome (`DONE_WITH_CONCERNS`)
- **Merge-readiness (Step 8)**: `MERGEABLE`, or the conflicting files surfaced + outcome (`BLOCKED`)
- Any errors encountered during the process

## Notes

- Follow any additional instructions in `$ARGUMENTS`
- When in doubt about a reviewer's intent, ask the user rather than guessing — misinterpreting feedback wastes more time than a quick clarification

## Integration

- **upstream**: ywc-create-pr (a PR must exist before review comments can be handled); ywc-sequential-executor / ywc-parallel-executor (executors that generate the PRs being reviewed)
- **downstream**: None — this skill closes the PR review loop; subsequent work is driven by the reviewer's approval or further comments
