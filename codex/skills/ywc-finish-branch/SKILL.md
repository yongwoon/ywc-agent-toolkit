---
name: ywc-finish-branch
description: >-
  (ywc) Use when delivering a single completed feature branch to the base branch — covers mark-PR-ready, CI wait + bot review polling, merge (PR or local), post-merge verification, Mark Task Complete bookkeeping, and local branch cleanup. Triggers: "finish branch", "deliver branch", "finish-branch", "ywc-finish-branch", "merge feature branch", "branch 마무리", "branch 마감", "ブランチ完了", "deliver task", "task 마감". Do not use for branch creation (handled by upstream executor), worktree management (caller of `ywc-parallel-executor` handles), draft PR creation alone (use `ywc-create-pr`), or PR review comment handling (use `ywc-handle-pr-reviews`).
---

# ywc-finish-branch

**Announce at start:** "I'm using the ywc-finish-branch skill to deliver this feature branch."

Encapsulates the post-implementation delivery flow that `ywc-sequential-executor` and `ywc-parallel-executor` previously inlined separately. One feature branch, one task — given a verified branch with passing local tests, this skill takes it the rest of the way to "done": optionally creates the PR, marks it ready, waits for CI, handles automated bot reviews, merges (PR or local), runs the post-merge hard gate, moves the task directory to `completed/`, and deletes the local feature branch. Worktree-specific cleanup is intentionally **not** in scope — that stays with `ywc-parallel-executor` because the lifecycle differs.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Step 4 (Merge) succeeded, that means we are done" | The Definition of Done has 5 conditions. Merge is condition 2 of 5. Mark Task Complete (Step 7) and branch deletion (Step 8) are equally required — skipping them silently breaks dependency resolution for downstream tasks. |
| "Post-merge verification is just running `git log` — skip it for speed" | The hard gate exists because `git merge` can silently no-op (already merged, nothing to do, fast-forward elided) and the caller cannot tell from exit code alone. Always verify. |
| "Bot review polling found 0 comments, skip the wait window" | Polling the full window is the contract. Bots can post asynchronously after CI completes; cutting short the window misses real findings. |
| "Branch was already deleted by `gh pr merge --delete-branch`, skip the local cleanup" | `--delete-branch` only removes the **remote** branch. The local copy persists and the next task's branch creation will conflict. Always run `git branch -d`. |
| "Mode flag conflict was already validated upstream, skip the check here" | This skill is a callable unit and may be invoked outside the executors. Validate flag conflicts at every entry point, not just the upstream caller. |
| "Mark Task Complete is bookkeeping — defer it for after all wave tasks merge" | `tasks/completed/` is the contract that downstream tasks read for dependency resolution. Move-then-merge ordering is forbidden by the Definition of Done; merge-then-move within the same task cycle is required. |
| "If `git merge --no-ff` reports a conflict, abort and try again" | An aborted merge loses the working state needed to debug the conflict. **Never** auto-abort — surface the conflict to the user so they can inspect it. |
| "`build-pr-title.py` exited 1 — I'll use just the slug as the title" | Exit 1 means `TASK_NUMBER` was not detected. Stop and return `NEEDS_CONTEXT` — do not construct a title without `[TASK_NUMBER]`. A title without the task number cannot be traced back to the task in the audit trail. |
| "`ywc-create-pr` generates its own title from `git log`, so `--title` is optional" | `ywc-create-pr`'s internal title generation does not know the task-number format. It silently produces a title without `[TASK_NUM]`. Always pass `--title` explicitly with `[TASK_NUMBER]` already included. |
| "CI failed twice — return BLOCKED and let the user fix it" | Before returning BLOCKED, categorize the failure type. Lint/format failures are auto-fixable without judgment. Type errors and build errors usually have a clear mechanical fix visible in the log. Only return BLOCKED when the root cause requires a design decision or all fix attempts are genuinely exhausted. |
| "The UL update in Step 1.5 is optional bookkeeping — skip it to save time" | The glossary is the shared vocabulary LLMs use in every subsequent prompt on this project. A branch that introduces new domain terms without updating the glossary silently pollutes downstream code generation and spec reviews. If `docs/ubiquitous-language.md` does not exist, Step 1.5 skips automatically — there is no overhead in that case. |

**Violating the letter of these rules is violating the spirit.** Delivery is the step where the user trusts the executor most — earning that trust requires honesty about partial completion.

## Arguments

| Parameter | Format | Example | Description |
|---|---|---|---|
| `--mode` | `<mode>` | `--mode local-merge` | One of `normal-pr`, `local-merge`, `draft`, `skip-ci-wait`, `per-task-pr`. See [Modes](#modes). |
| `--branch` | `feature/<task-name>` | `--branch feature/000001-010-db-create-users` | The feature branch to deliver. Must already exist locally. |
| `--base-branch` | `<branch-name>` | `--base-branch develop` | Target branch. Default: auto-detect (`develop` > `main` > `master`). |
| `--task-name` | `<task-name>` | `--task-name 000001-010-db-create-users` | Task directory name under `<tasks-dir>/`, used for the Mark Complete commit. |
| `--tasks-dir` | `<path>` | `--tasks-dir tasks/` | Tasks directory root. Default: `tasks/`. |
| `--pr-lang` | `<lang>` | `--pr-lang ja` | PR title/description language. Default: auto-detect from CLAUDE.md / AGENTS.md / recent PRs. |
| `--bot-action` | `sequential` \| `parallel` | `--bot-action sequential` | Post-bot polling behavior. Default: `sequential` (re-run CI after bot fixes). Use `parallel` when called from a wave loop where CI does not re-gate between bot iterations. |
| `--defer-push` | flag | | Skip the push of the Mark Complete commit. Used by range-mode callers that batch pushes at the end of the range. |
| `--keep-branch` | flag | | Skip the local feature branch deletion (`git branch -d`). Used by `ywc-parallel-executor`, where the branch is checked out in a worktree at the time of merge — `git branch -d` would fail until the worktree is removed. Caller takes responsibility for the eventual `git worktree remove` + `git branch -d`. |

**Mode-flag mutual exclusivity**: `--mode` is a single value; conflicts are impossible by construction. The caller is responsible for resolving ambiguity (e.g., the upstream executor's `--draft` and `--local-merge` flags must be collapsed into one `--mode` value before invoking this skill).

## Modes

| Mode | PR? | CI wait? | Merge? | Mark Complete? | Cleanup? | Use case |
|---|---|---|---|---|---|---|
| `normal-pr` | yes (delegates to `ywc-create-pr`) | yes | yes (`gh pr merge --delete-branch`) | yes | yes (`git branch -d`) | Default upstream flow |
| `local-merge` | no | no | yes (`git merge --no-ff` + push) | yes | yes | Personal repos, fast iteration |
| `draft` | yes | no | no | **no** (task stays open until manually merged) | no | User wants PR for review without auto-merge |
| `skip-ci-wait` | yes (mark ready) | no | no | **no** | no | User merges manually after offline review |
| `per-task-pr` | yes | no (caller handles per-wave CI) | no (caller merges locally for wave progression) | no (caller marks complete in wave loop) | no | `ywc-parallel-executor` per-task PR delivery |

`per-task-pr` is the special mode used inside `ywc-parallel-executor`'s wave loop — this skill creates and pushes the PR but stops short of merging or marking complete, because wave-level orchestration handles those steps. For all other modes, this skill executes the full lifecycle.

## Definition of Done

A `--mode normal-pr` or `--mode local-merge` invocation is **done** only when all of the following have happened, in this order:

1. **Verification gate passed** (caller's responsibility — this skill does not re-run tests; the upstream executor must have completed its verification before invoking).
2. **Merge succeeded**: either the PR was merged via `gh pr merge --delete-branch` (normal-pr) or `git merge --no-ff` succeeded locally and was pushed (local-merge).
3. **Post-merge verification passed**: `git log -1 --format="%s"` on the base branch begins with `Merge branch 'feature/`.
4. **Task directory moved**: `git mv <tasks-dir>/<task-name> <tasks-dir>/completed/<task-name>` and the `chore: mark <task-name> as completed` commit was created.
5. **Local feature branch deleted**: `git branch -d feature/<task-name>` succeeded (refuses to delete an unmerged branch — that is the safety check).

For `--mode draft` and `--mode skip-ci-wait`, conditions 2–5 are intentionally not performed; the skill's responsibility ends at PR creation (and ready-marking for `skip-ci-wait`). For `--mode per-task-pr`, only the PR creation portion runs; the caller handles the rest within the wave loop.

## Execution Steps

### Step 1: Validate Inputs

- Confirm `--branch` exists locally (`git branch --list <branch>` returns the branch).
- Confirm `--base-branch` is reachable (`git rev-parse --verify <base-branch>` succeeds).
- Confirm `--task-name` matches an entry under `<tasks-dir>/` (not under `<tasks-dir>/completed/`).
- For PR-based modes: confirm `gh auth status` succeeds.

If any check fails, return `NEEDS_CONTEXT` with the specific missing input. Do not proceed with partial information.

### Step 1.5: Ubiquitous Language Update (optional)

Check whether `docs/ubiquitous-language.md` exists in the project root:

```bash
test -f docs/ubiquitous-language.md
```

- **Exists**: Invoke `ywc-ubiquitous-language --mode update`. This runs before PR creation so that any new domain terms introduced by this branch are captured in the glossary before the PR description is written.
- **Not exists**: Skip silently — the project has not yet established a ubiquitous language document.

`ywc-create-pr` is called in Step 2 with `--skip-ubiquitous-update` to prevent a second invocation of the same update.

### Step 2: PR Creation (PR-based modes only)

For `--mode` ∈ {`normal-pr`, `draft`, `skip-ci-wait`, `per-task-pr`}: construct the PR title per the format below, then invoke `ywc-create-pr` passing:
- `--title "<constructed-title>"` — the `[task-number] description` string built from `--task-name` and `--pr-lang`
- `--lang <pr-lang>` — so the description is written in the correct language
- `--base-branch <base-branch>` — the resolved target branch
- `--skip-post-ci-check` — prevents `ywc-create-pr` from running its own post-PR CI + bot check; this skill handles CI verification in Step 4
- `--skip-ubiquitous-update` — prevents `ywc-create-pr` from running the UL update a second time; Step 1.5 already ran it

`ywc-create-pr` handles security check, CI pre-push validation, push, and PR creation as a draft. Because `--title` is provided explicitly, `ywc-create-pr` will use it verbatim and skip its own title-generation step.

**PR title format**: `[<task-number>] <human-readable description in --pr-lang>`

Run the bundled script to extract the task number and English slug without regex parsing:

```bash
python codex/skills/ywc-finish-branch/scripts/build-pr-title.py <task-name>
# TASK_NUMBER=000001-010
# SLUG_EN=Db Create Users Table
```

**If the script exits 1 (`TASK_NUMBER` is empty)**: stop immediately and return `NEEDS_CONTEXT` — report the task name that failed to parse. Do not construct a title with an empty task number.

For English PRs (`--pr-lang en`), use `--format title` to get the complete title directly:

```bash
python codex/skills/ywc-finish-branch/scripts/build-pr-title.py <task-name> --format title
# [000001-010] Db Create Users Table
```

For other languages, translate only `SLUG_EN` to `--pr-lang`, then compose: `[<TASK_NUMBER>] <translated-slug>`.

The script supports both task-name formats (new `000001-010-slug` and legacy `001010-slug`). Examples of final titles: `[000001-010] Create users table` (en) · `[000001-010] ユーザーテーブル作成` (ja) · `[001010] DB 사용자 테이블 생성` (ko).

**Before calling `ywc-create-pr`**: verify the constructed title string starts with `[`. If it does not, stop — the `[TASK_NUMBER]` prefix was lost somewhere in the construction. Do not call `ywc-create-pr` without a valid title.

For `--mode local-merge`: skip this step entirely. Local-merge does not produce a PR.

### Step 3: Mark PR Ready (normal-pr only)

Invoke `gh pr ready <pr-number>` to convert the draft into an open PR. Skip for `--mode draft`, `--mode skip-ci-wait`, `--mode per-task-pr` (those modes leave the PR as draft or hand control back to the caller).

### Step 4: CI Verification + Bot Review Polling (normal-pr only)

> **Action required**: Read [`../references/pr-bot-polling.md`](../references/pr-bot-polling.md) now before proceeding. The 60-second initial wait, the 300-second polling window, the `BOT_COUNT` jq query, and the merge condition are all defined there. Do not implement your own polling logic without reading it first.

Run the CI wait + fix loop and the bot review polling per [../references/pr-bot-polling.md](../references/pr-bot-polling.md). The polling reference defines the canonical loop; this skill applies its `--bot-action` parameter to choose the post-bot behavior:

- `--bot-action sequential`: after `ywc-handle-pr-reviews` runs, re-run the CI verification step before re-polling. Bot fixes may trigger a new CI run that must pass before merging.
- `--bot-action parallel`: after `ywc-handle-pr-reviews` runs, re-poll without re-gating on CI. The wave loop in `ywc-parallel-executor` handles CI at the wave level.

**CI failure handling (up to 2 fix attempts per failure cycle):**

1. **Identify failing checks:**
   ```bash
   gh pr checks <pr-number>
   ```

2. **Get failure logs:**
   ```bash
   # Get the most recent failed run ID for the feature branch
   gh run list --branch <feature-branch> \
     --json databaseId,name,conclusion \
     --jq '.[] | select(.conclusion == "failure") | .databaseId' | head -1
   gh run view <run-id> --log-failed
   ```

3. **Categorize and fix by failure type:**

   | Failure type | Fix action |
   |---|---|
   | Lint / format | Run the project's auto-fix command (`eslint --fix`, `prettier --write`, `ruff --fix`, `biome check --apply`), commit, push |
   | Type errors | Read compiler output, fix type mismatches in affected files, commit, push |
   | Test failures | Analyze failing test output, fix the implementation (never disable or weaken tests), commit, push |
   | Build errors | Read compiler/bundler output, fix compilation or import errors, commit, push |

4. After each push, re-run the CI wait and bot review polling loop (return to the top of Step 4).

5. If CI still fails after **2 fix attempts**, return `BLOCKED` with: the failing check name(s), a log excerpt (last 30 lines), the PR URL, and the failure category so the user has enough context to resolve it manually.

Skip this step entirely for `--mode local-merge`, `--mode draft`, `--mode skip-ci-wait`, `--mode per-task-pr`.

### Step 5: Merge

For `--mode normal-pr`:
```bash
gh pr merge <pr-number> --delete-branch
```

For `--mode local-merge`:
```bash
# Caller has already verified its Step 4 (Task Verification); this skill does not re-verify.
git checkout <base-branch>
git pull origin <base-branch>
git merge --no-ff feature/<task-name> -m "Merge branch 'feature/<task-name>'"
git push origin <base-branch>          # omit when --defer-push is set
git branch -d feature/<task-name>      # omit when --keep-branch is set (parallel wave loop case)
```

For all other modes: skip — merge happens later (manual for `draft`, caller for `skip-ci-wait` and `per-task-pr`).

**Why `git merge --no-ff` specifically** (not cherry-pick, not direct commit on main): preserves original commit SHAs, marks the task boundary in `git log --graph`, and lets `git branch -d` act as a built-in safety check that refuses to delete an unmerged branch. Full rationale lives in the upstream executor's `references/branch-lifecycle.md`.

**Error handling**: `git merge` conflict → stop and ask the user to resolve manually (do not auto-abort; the user may want to inspect). `gh pr merge` failure → stop and report. Push rejected (remote moved) → stop; never force-push.

### Step 6: Post-Merge Verification (hard gate)

For `--mode normal-pr` and `--mode local-merge`:
```bash
git log -1 --format="%s"
```
The output **must** begin with `Merge branch 'feature/`. If not, the merge did not execute correctly — investigate and retry before proceeding to Step 7. Do not write a completion marker for a merge that did not happen; downstream tasks would resolve dependencies against a broken contract.

### Step 7: Mark Task Complete

For `--mode normal-pr` and `--mode local-merge`:

Use the shared marker script — it handles the `.gitignore` branch, the mandatory marker commit, and the post-move verification in one deterministic step (exits non-zero if anything failed):

```bash
MARK_SCRIPT="codex/skills/scripts/mark-complete.sh"
[ -f "$MARK_SCRIPT" ] || MARK_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/scripts/mark-complete.sh"
bash "$MARK_SCRIPT" <tasks-dir> <task-name> [--push | --defer-push]
```

Why a script, not inline git: `git mv` cannot stage a path inside a gitignored `<tasks-dir>` (the move produces no diff), so that case needs a plain `mv` plus an `--allow-empty` marker commit, while a tracked `<tasks-dir>` uses `git mv`. The script detects which applies. The `chore: mark <task-name> as completed` commit is **mandatory in both cases** — it is the `git log` audit boundary that humans, audit tooling, downstream skills, the Completion Report, and resume / replay all rely on to verify task completion at a specific commit. The script then verifies the move (destination exists, source gone, marker commit at HEAD) and exits non-zero if any check fails; **do not declare `DONE` on a non-zero exit** — investigate and retry.

**Push strategy**: pass `--push` to `mark-complete.sh` for `--mode local-merge` and for `--mode normal-pr` when `--defer-push` is **not** set. Otherwise pass `--defer-push` (the script's default) so the caller can batch completion-marker commits and push them once at the end of the range. The caller is responsible for the eventual push when deferral is requested.

For `--mode draft`, `--mode skip-ci-wait`, `--mode per-task-pr`: skip Step 7 entirely. The task is not yet merged; marking it complete would be incorrect.

### Step 8: Local Branch Cleanup

For `--mode normal-pr`:
```bash
git checkout <base-branch>
git pull origin <base-branch>
git branch -d feature/<task-name>      # omit when --keep-branch is set
```
The local branch must be deleted explicitly because `gh pr merge --delete-branch` only removes the remote. Skip the deletion when `--keep-branch` is set — the caller (typically `ywc-parallel-executor`) will release the worktree and delete the branch in its own cleanup step.

For `--mode local-merge`: already handled inside Step 5's command sequence (which honors `--keep-branch` likewise).

For all other modes: skip. The branch stays alive for the user or caller to handle.

**Worktree prune (when caller used a worktree)** — if the caller created a per-task worktree (`ywc-parallel-executor` does this), the post-cleanup prune is delegated to the [`ywc-worktrees`](../ywc-worktrees/) skill:

```bash
ywc-worktrees --mode prune --task-name <task-name>
```

`ywc-worktrees --mode prune` runs the bundled `cleanup-worktree.sh` against the resolved worktree path — `git worktree remove` + local `git branch -d` + `git worktree prune` + post-removal verification, refusing to operate on dirty worktrees without `--force`. This skill does not inline the prune logic; the worktree priority chain (`.worktrees/` > CLAUDE.md `worktree_root` > `--root` fallback) and the dirty-tree safety check live in one place. Skip this delegation when no worktree was created (the typical `--mode local-merge` / `--mode normal-pr` flow that ran inside the main checkout).

## Output Format

```text
## Finish Branch Result: <task-name>

### Mode
<mode>

### Outcome
- PR: <pr-url-or-"none-local-merge">
- Merge: <commit-sha-or-"deferred">
- Mark Complete commit: <commit-sha-or-"skipped">
- Local branch: <"deleted"|"preserved">

### Verification
- Post-merge gate: <passed|skipped|failed>
- Post-move gate: <passed|skipped|failed>

### Completion Status
<DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
```

**Completion Status rules:**

| Status | When to use |
|---|---|
| `DONE` | All applicable steps for the chosen mode succeeded; verification gates passed |
| `DONE_WITH_CONCERNS` | Delivery succeeded but with caveats (e.g., advisor budget exceeded for the bot-polling loop, or `--defer-push` was set and the caller now owns the push) |
| `BLOCKED` | Cannot proceed — merge conflict, CI failure unfixable in 2 attempts, push rejected, or post-merge verification failed |
| `NEEDS_CONTEXT` | One of `--branch`, `--base-branch`, `--task-name`, `--tasks-dir`, or `--mode` was missing or invalid; no work was performed |

## Banned Output Patterns

This skill produces operational side effects (commits, pushes, merges), not source code. The "Banned Output Patterns" idea applied here means: **never** declare `DONE` while leaving any of the following:

- A merge commit that the post-merge verification step did not confirm
- A `chore: mark <task-name> as completed` commit that has not been verified by the post-move test
- A local feature branch that should have been deleted (modes `normal-pr` and `local-merge`, when `--keep-branch` is **not** set)
- An unpushed commit when push was required (modes `local-merge` always; `normal-pr` when `--defer-push` is not set)

Each of these is a hidden defect that breaks the next task's dependency resolution. Surface them honestly via `DONE_WITH_CONCERNS` or `BLOCKED` rather than declaring `DONE`.

## Integration

- **upstream**: `ywc-sequential-executor` (replaces its Steps 5–8), `ywc-parallel-executor` (replaces the merge + mark-complete portion of Step 4e–4f; worktree cleanup at Step 4g stays in parallel).
- **internal delegation**: `ywc-create-pr` (Step 2), `ywc-handle-pr-reviews` (Step 4 inside the bot polling loop).
- **shared references**: [../references/pr-bot-polling.md](../references/pr-bot-polling.md) (CI + bot polling), [../references/local-merge-permissions.md](../references/local-merge-permissions.md) (pre-authorized git/gh patterns the caller must set), [../references/subagent-status-actions.md](../references/subagent-status-actions.md) (how the caller responds to this skill's status return).

## Notes

This skill is a single-task delivery unit. It does not iterate over a range, manage a wave, or maintain checkpoint state — those concerns belong to the calling executor. Worktree creation and removal are intentionally out of scope, because the lifecycle differs between sequential (no worktree) and parallel (per-task worktree); placing it here would force one of the two callers to special-case its cleanup.
