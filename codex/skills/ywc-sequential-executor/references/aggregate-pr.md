# Aggregate PR Delivery (`--aggregate-pr`)

`--aggregate-pr` delivers a sequential task range as **one work branch and one PR**. Each task still gets its own `feature/<task-name>` branch, but Step 5 local-merges that task into a dedicated `work/<name>` integration branch instead of the real base branch. After the last task, a single work -> base PR delivers the whole group.

This is intentionally different from `ywc-parallel-executor --aggregate-pr`: sequential execution runs one task at a time and owns one work branch, so it does not need the parallel executor's local-base accumulation or clone-per-group isolation model.

## Mode Comparison

| Mode | Per-task delivery | End-of-run | PRs opened |
|---|---|---|---|
| Default `normal-pr` | One PR per task, merged | None | N |
| `--local-merge` | Merge each task into base, push | None | 0 |
| `--draft` | Create one draft PR per task | Human follow-up | N |
| `--skip-ci-wait` | Create one PR per task without CI wait | Human follow-up | N |
| `--aggregate-pr` | Merge each task into `work/<name>` | One work -> base PR, merged | 1 |

## A. Create The Work Branch Once

Derive the branch name before the task loop:

```bash
# With --group-name <name>:
WORK_BRANCH="work/<group-name>"

# Without --group-name:
WORK_BRANCH="work/<base-branch>-$(date +%Y%m%d-%H%M%S)"
```

Create and push the work branch from the real base branch:

```bash
git checkout <base-branch>
git pull origin <base-branch>
git checkout -b "$WORK_BRANCH"
git push -u origin "$WORK_BRANCH"
```

`<base-branch>` remains the eventual PR target. It is not mutated during the task loop.

If `$WORK_BRANCH` already exists, do not overwrite it. First route through the resume intent-match guard in `checkpoint-resume.md`; only reuse the branch when it belongs to the saved run being resumed.

## B. Per-Task Delivery Onto The Work Branch

For every task in the range, run the normal execution cycle with these substitutions:

1. Step 2 branches from the current work branch:

   ```bash
   git checkout "$WORK_BRANCH"
   git pull origin "$WORK_BRANCH"
   git checkout -b feature/<task-name>
   ```

2. Step 5 delegates to `$ywc-finish-branch` in `local-merge` mode, using the work branch as the base branch:

   ```bash
   $ywc-finish-branch \
     --mode local-merge \
     --branch feature/<task-name> \
     --base-branch "$WORK_BRANCH" \
     --task-name <task-name> \
     --tasks-dir <tasks-dir> \
     --pr-lang <pr-lang> \
     --bot-action sequential
   ```

Each task must pass verification, local-merge into `$WORK_BRANCH`, move its task directory to `<tasks-dir>/completed/<task-name>`, commit `chore: mark <task-name> as completed`, push `$WORK_BRANCH`, and delete its feature branch before the next task starts.

Before transitioning to the next task, run the same pre-transition gate the other modes use, passing the **work branch** as the integration argument:

```bash
bash <path-to-skill>/scripts/verify-transition.sh \
  "$WORK_BRANCH" <completed-task-name> <tasks-dir>
```

Condition 1 then asserts the working tree is back on `$WORK_BRANCH`, condition 2 that the feature branch was deleted, and condition 4 that the task moved to `completed/`. Do not start the next task without exit 0.

A `BLOCKED` task halts the range as in other sequential modes. Preserve the feature branch and work branch for recovery; do not skip ahead.

## C. Final Delivery: One Work -> Base PR

After the last task has been delivered into `$WORK_BRANCH`, the working tree should be on the work branch. Create the final PR and run the full merge lifecycle:

1. Create the PR as draft with `$ywc-create-pr`, passing `--skip-post-ci-check` because this procedure owns the CI, bot, and merge-readiness gates:

   ```bash
   $ywc-create-pr \
     --title "<group title, e.g. [000024-010..000025-030] project health>" \
     --lang <pr-lang> \
     --base-branch <base-branch> \
     --skip-post-ci-check
   ```

2. Mark the PR ready:

   ```bash
   gh pr ready <pr-number>
   ```

3. Watch CI. If checks fail, fix on `$WORK_BRANCH`, push, and re-run the watch. After 2 failed fix cycles, stop with `BLOCKED`.

   ```bash
   gh pr checks <pr-number> --watch
   ```

4. Poll automated reviews using [../../references/pr-bot-polling.md](../../references/pr-bot-polling.md). If `BOT_COUNT > 0`, invoke `ywc-handle-pr-reviews`, push fixes, and re-verify CI before polling again.

5. Apply the merge-readiness gate from [../../references/pr-conflict-resolution.md](../../references/pr-conflict-resolution.md):

   ```bash
   gh pr view <pr-number> --json mergeable,mergeStateStatus
   ```

   `BEHIND` means merge the real base into the work branch, never rebase:

   ```bash
   git fetch origin <base-branch>
   git checkout "$WORK_BRANCH"
   git merge --no-ff origin/<base-branch> -m "Merge origin/<base-branch> into $WORK_BRANCH"
   git push origin "$WORK_BRANCH"
   ```

   Re-run CI after this push. A textual `CONFLICTING` result is `BLOCKED`; surface the conflict and do not force-push.

6. Merge and sync local base:

   ```bash
   gh pr merge <pr-number> --merge --delete-branch
   git checkout <base-branch>
   git pull origin <base-branch>
   ```

The completion-marker commits made during the loop ride into base through this single PR merge. Do **not** re-Mark-Complete after the PR merges.

## D. Post-Merge Verification

Verify that every task in the group is now completed on the base branch:

```bash
for task in <all-range-tasks>; do
  test -d <tasks-dir>/completed/$task || { echo "LEAKED: $task missing from completed/"; exit 1; }
done
git log -1 origin/<base-branch> --format="%H"
```

If this fails, the PR merge or marker commits did not land correctly. Investigate before reporting `DONE`.

## E. Group-Level Definition Of Done

The group is done only when every task satisfied the normal per-task Definition of Done against `$WORK_BRANCH`, and the single work -> base PR was marked ready, passed CI, cleared bot review, passed merge-readiness, merged, and local base was synced.

A run whose work PR is created but unmerged is `DONE_WITH_CONCERNS` at best, never `DONE`.

## F. Safety Rationale

The task loop never checks out, resets, or pushes the real base branch. All task code and completion-marker commits accumulate on `work/<name>`, then one PR delivers the group. This keeps the real base branch unchanged until the final reviewed merge while still giving later tasks in the range access to earlier task changes.

This mode does not require installer file-name hardcoding. It references shared lifecycle documents generically under the installed shared references directory, so the installer can copy shared references as a directory.
