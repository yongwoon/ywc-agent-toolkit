# Aggregate Delivery Procedures (`--draft` and `--aggregate-pr`)

Both `--draft` and `--aggregate-pr` collapse an entire invocation (a task range or
`--all`) into **one branch and one PR** instead of delivering per task. They share the
same wave-accumulation mechanism and differ only at the final step:

| Flag | Per-wave delivery | End-of-run PR | Merged? | Use when |
|---|---|---|---|---|
| `--draft` | `ywc-finish-branch --mode local-merge --keep-branch --defer-push` | created as **draft**, bot-reviewed, left open | **no** (human merges later) | The group needs human review before landing |
| `--aggregate-pr` | identical to `--draft` | created, marked **ready**, CI-verified, bot-reviewed, **merged** | **yes** (`gh pr merge --delete-branch`) | The group should land as one PR, unattended -- the full-lifecycle twin of `--draft` |

The shared invariant: during the wave loop, every task's `git merge --no-ff` and its
`chore: mark <task-name> as completed` marker commit accumulate **locally** on the base
branch with `--defer-push` (no per-task push, no per-task PR). The end-of-run step lifts
that accumulated state onto a single branch and opens a single PR. Because the completion
markers are already committed during the waves, the aggregate PR carries **both the
implementation code and the `tasks/completed/` moves** -- there is no separate Mark Complete
at the end.

---

## Section A -- `--draft`: Aggregate Draft PR

Execute this before the Completion Report when `--draft` is specified. All task changes
have accumulated locally on base-branch via wave merges with `--defer-push`. After all
waves pass the Wave Audit:

1. Create an aggregate branch from the current local base-branch state:
   ```bash
   DRAFT_BRANCH="draft/<base-branch>-$(date +%Y%m%d-%H%M%S)"
   git checkout -b "$DRAFT_BRANCH"
   git push origin "$DRAFT_BRANCH"
   ```
2. Reset the local base-branch to match the remote (the aggregate branch now holds all
   the changes):
   ```bash
   git checkout <base-branch>
   git reset --hard origin/<base-branch>
   ```
3. Create the draft PR targeting base-branch:
   ```bash
   gh pr create --draft \
     --base <base-branch> \
     --head "$DRAFT_BRANCH" \
     --title "<title summarising all completed tasks>" \
     --body "<bullet list of completed tasks with their one-line descriptions>"
   ```
4. Poll for bot reviews using [pr-bot-polling.md](../../references/pr-bot-polling.md). If
   `BOT_COUNT > 0`, invoke `$ywc-handle-pr-reviews` for this PR. After review fixes are
   pushed, re-verify CI:
   ```bash
   gh pr checks "$DRAFT_BRANCH_PR_NUMBER"
   ```
   If any check fails, diagnose and fix (lint/format auto-fix first, then type/test/build
   manual fix), commit, push, and re-verify. Up to **2 fix attempts**. The PR stays as
   draft after all fixes -- do not un-draft or merge.
5. Capture the PR URL; include it in the Completion Report.

---

## Section B -- `--aggregate-pr`: Single Ready PR, Full Lifecycle

`--aggregate-pr` is `--draft` plus the merge tail. Run Section A's accumulation exactly,
then instead of stopping at a draft, take the branch through `ready -> CI -> bot -> merge ->
base sync`. Steps:

### B1. Create the aggregate branch

Derive the branch name from `--group-name` when provided (preferred because it makes
concurrent groups distinguishable), otherwise fall back to a timestamp:

```bash
# With --group-name <name>:
AGG_BRANCH="aggregate/<group-name>"
# Without --group-name:
AGG_BRANCH="aggregate/<base-branch>-$(date +%Y%m%d-%H%M%S)"

git checkout -b "$AGG_BRANCH"
git push origin "$AGG_BRANCH"
```

Then reset the local base-branch to the remote, identical to Section A step 2:

```bash
git checkout <base-branch>
git reset --hard origin/<base-branch>
```

### B2. Create the PR and mark it ready

Delegate creation to `$ywc-create-pr` so the secret scan, CI pre-push validation, and body
generation run once. Pass `--title` explicitly (the caller owns the group title) and
`--skip-post-ci-check` because this procedure runs its own CI gate in B3:

```bash
$ywc-create-pr \
  --title "<group title, e.g. [000026-010..030] payments module>" \
  --lang <pr-lang> \
  --base-branch <base-branch> \
  --skip-post-ci-check
```

`$ywc-create-pr` opens the PR as a draft. Mark it ready so CI and human reviewers engage:

```bash
gh pr ready <pr-number>
```

### B3. CI verification (up to 2 fix cycles)

```bash
gh pr checks <pr-number> --watch
```

On failure, categorize (lint/format -> run the project auto-fix first; then type / test /
build), fix on `$AGG_BRANCH`, commit, `git push origin "$AGG_BRANCH"`, and re-poll. After
**2** failed fix cycles, stop with `BLOCKED`, leave the PR open, and surface to the user --
do not merge a red PR.

### B4. Bot review

Run the polling loop in [pr-bot-polling.md](../../references/pr-bot-polling.md). If
`BOT_COUNT > 0`, invoke `$ywc-handle-pr-reviews` for this PR, then **re-run B3** (bot fixes
push new commits that trigger a fresh CI run). Repeat until CI is green and no new comments
arrive within the polling window.

### B5. Merge-readiness gate

CI status and merge-readiness are independent gates: a green PR can still be `CONFLICTING`
or `BEHIND` if the base advanced (for example, a sibling group merged first). Read
[pr-conflict-resolution.md](../../references/pr-conflict-resolution.md) and apply it:

```bash
gh pr view <pr-number> --json mergeable,mergeStateStatus
```

- `BEHIND` / merely out-of-date -> update the branch by **merging base into the branch**
  (never rebase), push, and return to B3 to re-verify CI:
  ```bash
  git fetch origin <base-branch>
  git checkout "$AGG_BRANCH"
  git merge --no-ff origin/<base-branch> -m "Merge origin/<base-branch> into $AGG_BRANCH"
  git push origin "$AGG_BRANCH"
  git checkout <base-branch>
  ```
- A real textual `CONFLICTING` state is a **1-attempt, surface-to-user `BLOCKED`**
  situation. Never auto-resolve, never force-push, and never `git merge --abort` into a
  discard.

### B6. Merge and sync

Once CI is green, bots are quiet, and the branch is current:

```bash
gh pr merge <pr-number> --merge --delete-branch
git checkout <base-branch>
git pull origin <base-branch>
```

`--delete-branch` removes the remote `$AGG_BRANCH`. The completion-marker commits and all
implementation merges land on the base branch through this single PR merge. No separate
Mark Complete and no deferred-marker push are required -- they were committed onto the
aggregate branch during the waves and merged here.

### B7. Post-merge verification (hard gate)

```bash
# Every task in the invocation must now be under completed/.
for task in <all-invocation-success-tasks>; do
  test -d <tasks-dir>/completed/$task || { echo "LEAKED: $task missing from completed/"; exit 1; }
done
git log -1 origin/<base-branch> --format="%H"   # must include the merge commit
```

If verification fails, the merge or an earlier marker commit did not land. Investigate
before reporting `DONE`. Capture the merged PR URL for the Completion Report.

---

## Section C -- Running Multiple Groups in Parallel (concurrency safety)

`--aggregate-pr` makes **one invocation = one group = one PR**. To run several groups
**at the same time**, isolate each group's **local base branch**, because the
`--draft`-style accumulation mutates it directly: every group runs `git checkout <base>`,
`git reset --hard origin/<base>`, and a per-task `git merge --no-ff` onto the local
`<base>` ref. Two groups doing that against the same `<base>` overwrite each other's
accumulation.

### Why git worktrees are not enough

Splitting groups into git worktrees of one clone is **not** sufficient. Worktrees isolate
only the working tree, not the git database:

| State | Per git worktree? | Consequence for concurrent groups |
|---|---|---|
| Working-tree files, including the untracked `.ywc-run-state.json` | **separate** | The checkpoint file does **not** collide; each worktree gets its own |
| `HEAD` / index / current checked-out branch | separate | -- |
| `.git` refs and branches (including the local `<base>` branch) | **shared** | `git reset --hard origin/<base>` + per-task merges mutate the **shared** local `<base>` ref, so groups corrupt each other |
| Branch checkout exclusivity | shared | `<base>` can be checked out in only one worktree (`fatal: '<base>' is already checked out`), so the second group cannot even start its accumulation |

So worktrees move the collision off the `.ywc-run-state.json` file (which they do separate)
and onto the **ref layer**, which they cannot isolate. The local `<base>` branch is the
shared mutable state, and worktrees share it.

> Forward note: a future redesign in which each group accumulates only on its own
> `aggregate/<group>` branch, never checking out or `reset`-ing local `<base>`, would be
> worktree-safe because distinct branches can live in distinct worktrees. The current mode
> reuses the `--draft` base accumulation, so that isolation is not yet available; use
> separate clones.

Therefore the safe concurrency unit is **one clone (independent `.git`) per group**:

```bash
# One clone per group. Each runs its own --aggregate-pr concurrently and safely.
git clone <repo-url> ../grp-payments && \
  ( cd ../grp-payments && $ywc-parallel-executor 000026-010..000026-030 \
      --aggregate-pr --group-name payments --review --pr-lang ko ) &

git clone <repo-url> ../grp-search && \
  ( cd ../grp-search && $ywc-parallel-executor 000027-010..000027-040 \
      --aggregate-pr --group-name search --review --pr-lang ko ) &

wait
```

Each clone has its own base checkout and its own `.ywc-run-state.json`, so the groups never
collide. They produce two independent PRs (`aggregate/payments`, `aggregate/search`).

**Cross-group conflict caveat**: if two groups touch overlapping files, their PRs will
conflict at merge time against the shared base. The merge-readiness gate (B5) handles the
second-to-merge PR by merging base in and re-verifying CI. Partition groups by
non-overlapping surfaces (the same `Shared Surfaces` discipline used for wave planning) to
avoid serialized re-verification.

**Single-repo alternative (no extra clones)**: run the groups **back to back** in one repo.
Each group is still internally parallel (waves), and the groups simply do not overlap in
time. This is the simplest correct option when extra clones are undesirable:

```bash
$ywc-parallel-executor 000026-010..000026-030 --aggregate-pr --group-name payments --pr-lang ko
$ywc-parallel-executor 000027-010..000027-040 --aggregate-pr --group-name search   --pr-lang ko
```

---

## Section D -- The "group base branch -> one PR" recipe

This is the flow most users mean by "group the tasks and deliver them together". With
`--aggregate-pr` it collapses into a single command per group instead of a hand-assembled
sequence:

| Manual sketch | `--aggregate-pr` equivalent |
|---|---|
| 1. Create a worktree / workspace | Handled per task in Step 4a (one isolated worktree per task) |
| 2. Create a group base branch for the scope | B1 creates `aggregate/<group-name>` automatically |
| 3. Run all tasks in the scope | The wave loop runs them **in parallel**, not sequentially |
| 4. Open one PR for the group base branch | B2-B6 create, verify, and merge one PR |
| 5. Report when finished | The Completion Report prints the merged PR URL |

Preview the plan first with `--dry-run` (task order, waves, mode) before committing to the
run. Combine with `--review` to gate each task's worktree branch through `$ywc-impl-review`
before it joins the aggregate, and `--pr-lang` to fix the PR language.
