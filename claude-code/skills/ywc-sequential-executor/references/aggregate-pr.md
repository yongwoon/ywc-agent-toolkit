# Aggregate PR Delivery (`--aggregate-pr`)

`--aggregate-pr` delivers a whole range as **one work branch and one PR**, executed
**sequentially**. Each task is merged onto a dedicated work (integration) branch in order;
after the last task, a single PR delivers the entire group to the real base branch. The
real base branch is **never checked out, reset, or mutated** during the task loop — only the
final PR merge lands the group onto it.

This is the sequential twin of `ywc-parallel-executor --aggregate-pr`. The difference: this
skill runs tasks one at a time (no worktrees, no waves), so it accumulates directly on the
work branch and avoids the parallel variant's shared-local-base hazard entirely.

## Mode comparison

| Mode | Per-task delivery | End-of-run | PRs opened | Use when |
|---|---|---|---|---|
| (default) `normal-pr` | one PR per task, merged | — | N (one per task) | Each task reviewed/merged on its own |
| `--local-merge` | merge each task into base, push | — | 0 | Personal repo, no PR wanted |
| `--aggregate-pr` | merge each task into **work branch** | one PR `work → base`, merged | 1 (for the whole range) | Group the range into a single reviewable PR |

## A. Create the work branch (once, before the task loop)

Derive the name from `--group-name` when given (preferred — distinguishes groups),
otherwise fall back to a timestamp:

```bash
# With --group-name <name>:
WORK_BRANCH="work/<group-name>"
# Without --group-name:
WORK_BRANCH="work/<base-branch>-$(date +%Y%m%d-%H%M%S)"

git checkout <base-branch>
git pull origin <base-branch>
git checkout -b "$WORK_BRANCH"
git push -u origin "$WORK_BRANCH"
```

`<base-branch>` (the real base, e.g. `main`) is the eventual PR target. It is not modified
until the final PR merges in Section C.

## B. Per-task delivery onto the work branch

For every task in the range, run the normal Execution Cycle (Step 1 → Step 4) with exactly
two substitutions — the **work branch replaces the base branch** as the per-task delivery
target:

- **Step 2 (Branch Creation)** branches from the work branch, so each task sees every prior
  task's merged code:
  ```bash
  git checkout "$WORK_BRANCH"
  git checkout -b feature/<task-name>
  ```
- **Step 5 (Delivery)** delegates to `ywc-finish-branch` in `local-merge` mode, targeting the
  **work branch** as its base:
  ```bash
  /ywc-finish-branch \
    --mode local-merge \
    --branch feature/<task-name> \
    --base-branch "$WORK_BRANCH" \
    --task-name <task-name> \
    --tasks-dir <tasks-dir> \
    --pr-lang <pr-lang>
  ```

Each task merges into the work branch, commits its `chore: mark <task-name> as completed`
marker on the work branch, and pushes the work branch. `ywc-finish-branch` leaves the
working tree on the work branch, so the next task's Step 2 `git checkout "$WORK_BRANCH"`
runs cleanly. This is the same code-availability guarantee `--local-merge` provides, but
accumulating on the work branch instead of the real base.

Before transitioning to the next task, run the same pre-transition gate the other modes use
(Step 6.2), passing the **work branch** as the integration argument:

```bash
bash claude-code/skills/ywc-sequential-executor/scripts/verify-transition.sh \
  "$WORK_BRANCH" <completed-task-name> <tasks-dir>
```

Condition 1 then asserts the working tree is back on `$WORK_BRANCH`, condition 2 that the
feature branch was deleted, and condition 4 that the task moved to `completed/`. Do not start
the next task without exit 0 — this is the aggregate-pr equivalent of the base-branch gate.

A `BLOCKED` task halts the range exactly as in other modes (four-step triage, then surface).
The work branch retains the tasks merged so far; resume picks up at the failed task.

## C. Final delivery — one PR `work → base` (after the last task)

After the last task's local-merge into the work branch (the working tree is already on the
work branch):

1. **Create the PR** via `ywc-create-pr`, passing `--skip-post-ci-check` because this
   procedure runs its own CI/bot/merge gate below, and an explicit `--title` (the caller
   owns the group title):
   ```bash
   /ywc-create-pr \
     --title "<group title — e.g. [000024-010..000025-030] project health>" \
     --lang <pr-lang> \
     --base-branch <base-branch> \
     --skip-post-ci-check
   ```
   `ywc-create-pr` opens the PR as a draft from the current branch (`$WORK_BRANCH`) to
   `<base-branch>`.

2. **Mark ready**, then run CI, bot review, and the merge-readiness gate, then merge and
   sync. These reuse the canonical references — do not inline their parameters:
   - `gh pr ready <pr-number>`
   - `gh pr checks <pr-number> --watch` — on failure, fix on `$WORK_BRANCH`, push, re-poll;
     after **2** failed cycles stop `BLOCKED` (never merge a red PR).
   - Bot review: run the loop in [pr-bot-polling.md](../../references/pr-bot-polling.md). If
     `BOT_COUNT > 0`, invoke `ywc-handle-pr-reviews`, then **re-verify CI** (bot fixes push
     new commits).
   - Merge-readiness gate per [pr-conflict-resolution.md](../../references/pr-conflict-resolution.md):
     ```bash
     gh pr view <pr-number> --json mergeable,mergeStateStatus
     ```
     `BEHIND` → merge base **into** the work branch (never rebase), push, re-verify CI:
     ```bash
     git fetch origin <base-branch>
     git checkout "$WORK_BRANCH"
     git merge --no-ff origin/<base-branch> -m "Merge origin/<base-branch> into $WORK_BRANCH"
     git push origin "$WORK_BRANCH"
     ```
     A real textual `CONFLICTING` state is a **1-attempt, surface-to-user `BLOCKED`** — never
     auto-resolve, never force-push.
   - Merge and sync:
     ```bash
     gh pr merge <pr-number> --merge --delete-branch
     git checkout <base-branch>
     git pull origin <base-branch>
     ```

The `chore: mark … as completed` commits made during the loop ride into the base branch
through this single PR merge. **Do not re-Mark-Complete** — the directories are already under
`<tasks-dir>/completed/` and committed on the work branch.

## D. Post-merge verification (hard gate)

```bash
# Every task in the range must now be under completed/.
for task in <all-range-tasks>; do
  test -d <tasks-dir>/completed/$task || { echo "LEAKED: $task missing from completed/"; exit 1; }
done
git log -1 origin/<base-branch> --format="%H"   # must include the PR merge commit
```

If verification fails, the merge or a marker commit did not land — investigate before
reporting `DONE`. Capture the merged PR URL for the Completion Report.

## E. Definition of done (group level)

The **group** is done only when: every task satisfied the normal per-task Definition of Done
against the work branch (verified, local-merged, marked complete, pushed), **and** the single
`work → base` PR was marked ready, passed CI, cleared bot review, passed the merge-readiness
gate, and was **merged** with local base synced. A run whose work PR is created but unmerged
is `DONE_WITH_CONCERNS` at best, never `DONE`.

## F. Why this is safe

Because the sequential executor accumulates on a dedicated work branch and **never checks out
or resets the local base branch**, it has none of the shared-local-base hazards that make the
parallel `--aggregate-pr` unsafe to run concurrently in one clone. Tasks run strictly one at a
time, so there is no worktree namespace, no `.ywc-run-state.json` contention beyond the single
active run, and no ref-layer collision. The only shared mutable state is the work branch
itself, which exactly one run owns.
