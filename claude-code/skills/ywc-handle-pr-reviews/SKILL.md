---
name: ywc-handle-pr-reviews
description: >-
  (ywc) Use when handling an open PR's review feedback — addressing comments, replying to review threads, and leaving the PR mergeable by clearing CI failures and base-branch conflicts too. Triggers: "handle PR reviews", "fix PR CI", "resolve PR conflict", "PR CI 고쳐줘", "PR conflict 해결", "리뷰 대응", "レビュー対応". Do not use for creating a new PR (use ywc-create-pr), reviewing code yourself (use ywc-impl-review), verify-before-agreeing on feedback (use ywc-receive-review), storing durable review learnings (use ywc-review-learnings), merging or delivering the branch (use ywc-finish-branch), or debugging outside an open PR (use ywc-debug-rootcause).
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Agent, Skill
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
| "Nitpick items have no thread to reply to, so I'll just fix them silently without posting anything" | Nitpick items still need a consolidated PR-level reply. Skipping it leaves no `nitpick-addressed` marker, so the fetch script's dedup never excludes them and the same items resurface on every future run. |
| "I'll add a worktree for the PR branch myself — it's one command" | An inline worktree lands outside the location convention that `ywc-worktrees` resolves and that its audit and prune tooling scan, and skips its branch-name validation. Use `ywc-worktrees --mode create --existing-branch`; if that skill is missing, `BLOCKED`. |
| "I `cd`'d into the worktree, so the file paths I already know still work" | Read, Edit and Write ignore the Bash cwd, so a path under the invoking checkout silently edits the wrong tree. Build every path from `$WT_PATH`. |

**Violating the letter of these rules is violating the spirit.** Code review is a conversation, not a checklist.

## Definition of Done

Handling a PR means leaving it **mergeable**, which requires clearing **three independent blockers** — not just the first one:

| # | Gate | Cleared when | Step |
|---|---|---|---|
| 1 | **Review comments** | Every unresolved thread and every unaddressed Nitpick item is fixed-or-answered and replied to (via the thread-reply API or the consolidated PR-level comment, respectively) | Steps 2–5 |
| 2 | **CI status** | `gh pr checks` is green (or failures triaged to the user) | Step 7 |
| 3 | **Merge-readiness** | `gh pr view --json mergeable` is `MERGEABLE` / `CLEAN` (or a real conflict surfaced) | Step 8 |

These gates are **independent**. A PR with every comment answered but red CI, or green CI but `CONFLICTING` against the base, is **not handled**. Gates 2 and 3 run on **every** invocation — including when Step 2 finds zero unresolved comments, because CI can be red and the base can have advanced regardless of whether anyone commented.

**Before touching the PR, create a TodoWrite list with all three gates** so none is silently skipped. Do not report the run complete until all three are cleared, or explicitly surfaced to the user as blocked.

## Arguments

| Parameter | Format | Example | Description |
|---|---|---|---|
| `<pr-number>` | positional, optional | `123` | The PR to handle. Without `--worktree` it defaults to the current branch's PR (Step 1). |
| `--worktree` | flag | `123 --worktree` | Handle the PR's head branch in a dedicated worktree instead of the invoking checkout (Step 1.5). If the head branch is already checked out somewhere, that worktree is reused; when it is the main checkout (`in-place`), the main checkout itself is refreshed and edited. The PR number is required. Fork PRs are not supported. |

## Context

- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

With `--worktree`, these values describe the invoking checkout, not the PR branch.

## Task

Follow the steps below to handle PR review comments.

### Step 1: Identify PR Number

- If a PR number is specified in `$ARGUMENTS`, use it
- Otherwise, identify the current branch's PR with `gh pr view --json number`
- If no PR exists for the current branch, stop and notify the user rather than proceeding blindly
- `--worktree` without a PR number → stop and ask for the number, before any worktree work

Resolve `{owner}/{repo}` dynamically at this stage — it's used throughout the workflow:

```bash
gh repo view --json nameWithOwner --jq .nameWithOwner
```

### Step 1.5: Worktree Setup (only with --worktree)

Skip this step unless `--worktree` is set. Otherwise handle the PR head branch `H` in a worktree so the invoking checkout stays untouched. The one exception is `in-place`: when `H` is already checked out in the main checkout, that checkout becomes the working location, so sub-step 5 (fetch, `merge --ff-only`, upstream setting) and every later commit act on it. Each failure below stops with `BLOCKED: <cause>`; nothing is repaired silently. Bash variables do not survive between calls, so every command below that shows `$MAIN`, `$WT_PATH` or `<H>` is a placeholder: substitute the literal value you recorded, never an unset shell variable (an empty `$MAIN` would turn `cd "$MAIN"` into `cd ""`). Double-quote the substituted value, and treat the validation in sub-steps 0–1 as the injection boundary, since double quotes alone do not stop `$(…)` or backticks.

0. **Validate `<N>`** yourself, before any Bash call that contains it: it must match `^[0-9]+$` over the whole string, because it becomes the path `pr-<N>`; otherwise `BLOCKED: PR number must be numeric`.
1. **Resolve `H`** with the bundled script. GitHub returns the head branch name, but whoever pushed the branch chose it. The script reads it into a variable and never puts it on a command line, so it is validated before any shell use:

   ```bash
   bash "${CLAUDE_SKILL_DIR}/scripts/resolve-pr-head.sh" "<N>"
   # exit 0 → stdout line 1 is the validated head branch H, line 2 the
   #          validated head commit SHA O (record both verbatim)
   # exit 1 → BLOCKED; relay the stderr line verbatim and stop
   # exit 2 → usage error
   ```

   The script re-checks `<N>` against `^[0-9]+$`, then runs `gh pr view <N> --json headRefName,headRefOid,isCrossRepository,state` and fails closed:
   - `gh` fails (no such PR, authentication) → `BLOCKED` with gh's stderr.
   - `state` is not `OPEN` → `BLOCKED: PR is <state>` (the head branch of a merged or closed PR may be gone from the remote).
   - `isCrossRepository` is anything but the JSON boolean `false` (a fork PR, or a missing value) → `BLOCKED: --worktree does not support fork PRs`. Cloning the fork is not supported.
   - `headRefName` must match `^[A-Za-z0-9._/-]+$` over the whole string, not start with `-`, not contain `..`, and only then pass `git check-ref-format "refs/heads/<H>"` (the same rules as `ywc-worktrees --existing-branch`); otherwise `BLOCKED: invalid head branch name`.
   - `headRefOid` must be a full SHA matching `^[0-9a-f]{40}$`; otherwise `BLOCKED: invalid head commit`.

   Never run `gh pr view` yourself to obtain `H`, and never paste an unvalidated `headRefName` into a command. If the script cannot be found, follow the Skill-local script path fallback and stop with `BLOCKED: unresolved skill path`.
2. **Locate an existing worktree.** Run `git worktree list --porcelain`.
   - The first `worktree <path>` line is the main checkout `MAIN`; always derive it, because the Step 9 prune guidance uses it for every state. A `bare` line in that first entry → `BLOCKED: bare repository`.
   - Check `MAIN` and any candidate `WT_PATH` for `"`, `$`, a backtick, `\` or a newline first, before using either in a command → `BLOCKED: unsafe path`.
   - Find the entry whose `branch refs/heads/<H>` line equals the whole line (not a prefix). If the entry has `prunable` or `locked`, or its directory does not exist → `BLOCKED` with a `git worktree prune` (prunable) or `git worktree unlock` (locked) hint; for a missing directory that is neither, name the path and suggest `git worktree prune`.
   - Otherwise its path is `WT_PATH`: `in-place` when it equals `MAIN`, else `reused`. Skip sub-step 3 and do not call `ywc-worktrees`.
3. **Create when no entry exists.**
   - In a separate Bash call run `cd "$MAIN" && pwd -P`; in the next call confirm `[ "$(pwd -P)" = "<that canonical path>" ]`, otherwise `BLOCKED: run from the main checkout`. A session started inside a linked worktree can have its cwd reset, and `ywc-worktrees` resolves the repository root from the current checkout, so a linked-worktree cwd yields the wrong root.
   - Invoke `/ywc-worktrees --mode create --task-name pr-<N> --branch <H> --existing-branch` with the Skill tool. If that skill cannot be found → `BLOCKED: ywc-worktrees not installed`; never fall back to creating the worktree inline with git.
   - Do not trust the path the skill prints. Repeat sub-step 2's lookup and take `WT_PATH` from the `branch refs/heads/<H>` entry, applying the same path-character check; record `created`. Then, in one Bash call, write an ownership marker into this worktree's own git directory, which git deletes together with the worktree: `GD=$(git -C "<WT_PATH>" rev-parse --absolute-git-dir) && [ -d "$GD" ] && printf 'ywc-handle-pr-reviews pr-%s refs/heads/%s\n' "<N>" "<H>" > "$GD/ywc-owner"`. The `&&` chain keeps a failed lookup from writing to `/ywc-owner`. A failure is not `BLOCKED`: report `ownership marker not written` and continue; Step 9 then falls back to asking the user.
   - If create fails, repeat the lookup once, since a concurrent run on the same PR may have created it: found → `reused`; still absent → `BLOCKED` carrying the `ywc-worktrees` message verbatim.
4. **Require a clean tree.** `git -C "$WT_PATH" status --porcelain` must be empty, otherwise `BLOCKED: worktree has uncommitted changes`, so unrelated work never lands in a review-fix commit.
5. **Refresh from the remote** (review line numbers refer to the remote head; this also applies to `in-place`):
   - `git -C "$WT_PATH" fetch origin "+refs/heads/<H>:refs/remotes/origin/<H>"`; a failure → `BLOCKED` quoting git's stderr.
   - `git -C "$WT_PATH" rev-parse "refs/remotes/origin/<H>"` must print exactly `O`; otherwise `BLOCKED: origin/<H> is not the head of PR <N>`. `gh` resolves the PR in its default repository while fetch and push use the `origin` remote, so this ties them together (and catches a head that moved after the lookup).
   - `git -C "$WT_PATH" rev-list --count "origin/<H>..HEAD"` not `0` → `BLOCKED: <H> has unpushed local commits` (`merge --ff-only` succeeds when local is merely ahead, so this check is separate).
   - Otherwise `git -C "$WT_PATH" merge --ff-only "origin/<H>"`; a failure → `BLOCKED: local <H> diverged from origin/<H>`.
   - If `git -C "$WT_PATH" rev-parse --abbrev-ref "<H>@{upstream}"` fails or prints anything other than `origin/<H>`, run `git -C "$WT_PATH" branch --set-upstream-to="origin/<H>" "<H>"`, so that status and pull reflect the PR branch. A branch checked out with `--existing-branch` keeps whatever upstream or `pushRemote` it already had, so Step 4 does not rely on either (see the explicit push target there).

**Switch the working directory.** In a separate Bash call run `cd "$WT_PATH"`, then confirm `git branch --show-current` prints `H`; otherwise `BLOCKED: worktree branch mismatch`. Record `pwd -P` as the canonical `WT_PATH`. From here on, every Read, Edit and Write path is an absolute path under `$WT_PATH`.

**Re-check the working directory.** The harness can reset the Bash cwd (for example when the worktree root lies outside the project). With `--worktree`, before the first Bash call of Step 2, Step 4 (commit and push), Step 6 (re-push after a rejection), Step 7 and Step 8, confirm `[ "$(pwd -P)" = "<canonical WT_PATH>" ]`. If it differs, run `cd "<canonical WT_PATH>" && [ "$(pwd -P)" = "<canonical WT_PATH>" ]` as one Bash call; still failing → `BLOCKED: working directory left the worktree`. Every later git command in worktree mode either uses `git -C "<canonical WT_PATH>"` or repeats that `cd` in the same Bash call.

### Step 2: Retrieve and Filter Comments

Retrieve all PR review feedback across two tiers and filter out what doesn't need action. This prevents duplicate work and keeps the process focused on genuinely unresolved feedback.

**Actionable** (thread-level review comments — each has an `id` you can reply to directly):

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/fetch-unresolved-comments.sh" \
  {owner}/{repo} {pr_number}
# exit 0 → JSON array of unresolved threads on stdout (may be [])
# exit 1 → gh CLI error (not authenticated or PR not found)
```

The script fetches paginated comments, groups them into threads, and applies the skip conditions automatically: threads containing `<!-- <review_comment_addressed> -->` are dropped, and threads where your reply is newer than the latest reviewer comment are dropped. The output JSON array contains only actionable threads — each element has `id`, `body`, `path`, `line`, `user`, `created_at`, and `thread_comment_count`.

**Nitpick** (CodeRabbit's advisory-tier items nested inside a single review body — no `id`/thread to reply to individually):

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/fetch-nitpick-comments.sh" \
  {owner}/{repo} {pr_number}
# exit 0 → JSON array of Nitpick items on stdout (may be [])
# exit 1 → gh CLI error (not authenticated or PR not found)
# exit 2 → usage error (invalid <owner>/<repo> or <pr-number>)
```

The script fetches all `coderabbitai[bot]` reviews, parses each body's `Nitpick comments (N)` section, dedups by hash across reviews (keeping the most recent), and excludes items already marked addressed via a `<!-- nitpick-addressed:<hash> -->` PR-level comment authored by the current user. Each element has `hash`, `path`, `line_start`, `line_end`, `title`, `body`, `severity: "nitpick"`, and `parse_status` (`"ok"` or `"raw_fallback"` for a segment the parser could not confidently attribute).

**If both arrays are `[]`** (no Actionable comments and no Nitpick items): skip Steps 3–5, but you **must still run Step 7 (CI gate) and Step 8 (Merge-Readiness gate)** before the Final Summary. A PR with 0 Actionable but nonzero Nitpick items (or vice versa) must still proceed to Step 3 — only skip when **both** arrays are empty. Zero comments does not mean the PR is mergeable — CI can be red and the base can have advanced into a conflict regardless of whether anyone commented. **Never jump straight to the summary on two empty arrays** — that is the exact path that leaves red CI and conflicts unhandled.

### Step 3: Group and Analyze Comments

Before fixing anything, group all remaining comments, from both labeled lists, by target file path. Processing file-by-file is more efficient — you read each file once, apply all related fixes together, and create one coherent commit per file instead of jumping back and forth.

**Processing strategy:**

1. Collect all unresolved comments from both the Actionable and Nitpick lists, and group by target file path
2. For each file, read the file once and analyze all related comments together
3. Apply fixes for that file and commit as a unit
4. Move to the next file

### Step 4: Classify and Fix Comments

Nitpick items go through this same four-category classification as Actionable comments. "Question only" and "Approval" rarely apply, since Nitpicks are advisory by definition — but no separate classification logic is introduced for them.

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
- With `--worktree`, push with the explicit target `git push origin "HEAD:<H>"` (the re-push in Step 6 and the base-merge push in Step 8 as well) instead of a plain `git push`, so a different upstream or a configured `pushRemote` cannot redirect it.
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

**Nitpick items — consolidated PR-level reply (not a thread reply):**

Nitpick items have no `in_reply_to_id`, so they cannot use the thread-reply API above. Instead, after processing all Nitpick items in this run, post **one** PR-level comment listing every processed item:

```bash
gh pr comment {pr_number} --body-file - <<'NITPICK_REPLY'
...
NITPICK_REPLY
```

For every processed **non-`raw_fallback`** item, include a `<!-- nitpick-addressed:<hash> --> ` marker line so `fetch-nitpick-comments.sh`'s dedup-exclusion step (FR-2 stage 5) can find it on the next run. `raw_fallback` items (`hash: ""`) are still described in the reply body for visibility, but **never** get a marker line — they will always resurface on the next run by design (Amendment B), since the parser could not confidently attribute them to a stable identity. Both reply paths coexist: the thread-reply API above for Actionable comments, this one consolidated comment for Nitpick items.

### Step 6: Error Handling

Things can go wrong during the process. Handle these gracefully:

| Error                                 | How to handle                                                                           |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| `gh pr view` fails (no PR for branch) | Stop and tell the user. Don't guess the PR number                                       |
| Push fails (non-fast-forward, remote feature branch advanced) | `git pull --rebase origin <feature-branch>` (rebase on the feature branch you own is safe), then re-push. Don't force-push without approval. See `references/pr-conflict-resolution.md` |
| Comment reply API returns 403/404     | Log the error, skip that reply, and report it in the final summary                      |
| Referenced file no longer exists      | Reply to the comment explaining the file was removed, and skip the fix                  |
| `gh pr comment` (Nitpick consolidated reply) returns non-zero/403/404 | Log the error with the PR number and affected item count. Do **not** write any `nitpick-addressed` marker for that batch, so the excluded-by-marker filter in `fetch-nitpick-comments.sh` correctly re-surfaces them next run. Report the failure and affected item count in Step 9's Final Summary. |

### Step 7: CI Status Gate — run on EVERY invocation

**Always run this gate — including when Step 2 found zero comments and your replies pushed no code.** A PR review thread and CI status are two independent blockers on the same PR. Addressing every comment but leaving CI red still leaves the PR unmergeable, so handling a PR means checking both. This gate covers two cases at once: CI regressions introduced by the fixes in Step 4, **and** pre-existing CI failures that were already red before you touched the PR (a flaky earlier push, a base-branch change, a broken dependency).

With `--worktree`, skip the lookup below and write the literal `<N>` validated in Step 1.5 wherever a Step 7 or Step 8 `gh` command shows `$PR_NUMBER` (including `--watch` and the Step 8 `gh pr view`): a shell variable does not survive into a later Bash call, and an empty one falls back to the current branch's PR. That lookup follows the current branch of the working directory, so it can resolve a different PR if the cwd drifted or several PRs share the head branch.

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
- **Nitpick**: total Nitpick items processed (Fixed/Deferred/No fix needed) vs any that failed to post (the `gh pr comment` error case from Step 6)
- **CI (Step 7)**: final check status — `green`, or the failing check names + outcome (`DONE_WITH_CONCERNS`)
- **Merge-readiness (Step 8)**: `MERGEABLE`, or the conflicting files surfaced + outcome (`BLOCKED`)
- Any errors encountered during the process
- **Worktree** (only with `--worktree`): `Worktree: <WT_PATH> (created | reused | in-place)`. This skill never runs a cleanup command; report guidance by state:
  - `created`, or `reused` where the basename of `WT_PATH` is `pr-<N>`, or `worktree-pr-<N>` under the legacy `../worktree-<task-name>` root (made by an earlier run of this skill): first read the ownership marker written in Step 1.5 (`GD=$(git -C "<WT_PATH>" rev-parse --absolute-git-dir) && cat "$GD/ywc-owner"`). When it prints exactly `ywc-handle-pr-reviews pr-<N> refs/heads/<H>`, say the worktree was created by this skill. Otherwise (no marker, a failed read, any other content, or a worktree from before markers existed), the basename and head branch make this likely but do not prove who created it, so word the guidance that way and ask the user to confirm the worktree is theirs before removing it. Next, check that prune would remove this exact path. Prune removes `<root>/pr-<N>`, where `<root>` is what `/ywc-worktrees --mode resolve` prints from `<MAIN>`, or `<root>/worktree-pr-<N>` when that root is the legacy `..` fallback. If that path is not `WT_PATH` (for example a legacy `../worktree-pr-<N>` reused after `.worktrees/` was added), do not suggest prune, because it would act on a different path. Report `git -C "<MAIN>" worktree remove "<WT_PATH>"` instead (no `--force`, so it refuses a dirty tree; the branch is kept) and tell the user to confirm with `git worktree list` that the path is gone. Before either removal, tell the user to run `git -C "<WT_PATH>" status --ignored --short` and copy out anything worth keeping: `git worktree remove` deletes ignored files such as `.env` even without `--force`. Otherwise, from the main checkout `<MAIN>` run `/ywc-worktrees --mode prune --task-name pr-<N> --branch <H> --keep-branch`. Run it there because `cleanup-worktree.sh` resolves the root from `git rev-parse --show-toplevel` and inside a linked worktree would not find `.worktrees/`. `--keep-branch` is mandatory: without it prune deletes the local PR head branch while the PR is still open. Add that while this worktree exists, the `ywc-parallel-executor` pre-flight audit reports it under `DRIFT: unexpected worktrees found` and stops that run; this includes a legacy `../worktree-pr-<N>` after `.worktrees/` was added.
  - any other `reused`: report "not created by this skill, so not cleaned up" (another executor may own it).
  - `in-place`: no cleanup guidance.
  - If local verification (tests, lint) could not run in the worktree (a Docker bind-mount pointing at the main checkout, gitignored `.env` or `node_modules` missing), report `local verification not performed in the worktree: <reason>` and state that only CI results were used.

## Notes

- Follow any additional instructions in `$ARGUMENTS`
- When in doubt about a reviewer's intent, ask the user rather than guessing — misinterpreting feedback wastes more time than a quick clarification

## Integration

- **upstream**: ywc-create-pr (a PR must exist before review comments can be handled); ywc-sequential-executor / ywc-parallel-executor (executors that generate the PRs being reviewed)
- **downstream**: `ywc-worktrees` (`--mode create --existing-branch`, only with `--worktree`); otherwise none — this skill closes the PR review loop and subsequent work is driven by the reviewer's approval or further comments
