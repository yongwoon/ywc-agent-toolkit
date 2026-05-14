# Per-Task Branch Lifecycle (Range Mode)

> Referenced from: SKILL.md → Execution Cycle overview
> Read this when: about to execute a range of tasks, or diagnosing the most common range-mode failure (multiple tasks landing on a single branch).

Understanding the branch lifecycle per mode prevents the most common range-execution mistake: accidentally running multiple tasks on a single branch. Each mode has a different lifecycle because each mode treats merging differently.

## Normal mode (PR flow)

```
for each task in range:
  git checkout <base-branch> && git pull origin <base-branch>
  git checkout -b feature/<task-name>
  → implement → verify → create PR → CI
  → [automated review comments?]
      yes → ywc-handle-pr-reviews → re-run CI (loop until clean)
      no  → (skip)
  → merge PR
  → git checkout <base-branch> && git pull
  → mark complete
```

Each task starts from a **fresh, up-to-date base branch**. The PR merge updates the base branch on the remote, and `git pull` after merge brings those updates into local before the next task starts.

The automated review step is **conditional** — it only runs when a repository has configured review bots such as CodeRabbit, Codex Review, or Claude Review. Repositories without these tools skip the step entirely. When automated review comments exist, `ywc-handle-pr-reviews` processes them and pushes any fixes; CI is then re-verified before the merge proceeds.

## `--local-merge` mode

```
for each task in range:
  git checkout <base-branch> && git pull origin <base-branch>
  git checkout -b feature/<task-name>
  → implement → verify
  → git checkout <base-branch> && git merge --no-ff feature/<task-name>
  → git push origin <base-branch>
  → delete feature branch → mark complete
```

Same starting point as normal mode — each task gets a fresh base branch — but the merge happens locally with `git merge --no-ff` instead of via `gh pr merge`. The `--no-ff` flag preserves the original commit SHAs from the feature branch and creates a merge commit that marks the task boundary in `git log --graph`.

## `--draft` / `--skip-ci-wait` mode (chain branching)

```
for each task in range:
  git checkout feature/<previous-task-name>   # (or base-branch for first task)
  git checkout -b feature/<task-name>
  → implement → verify → create PR (draft)
  # no merge occurs — chain from this branch to next
```

Chain branching is necessary in this mode because earlier tasks are **not merged** into the base branch. Subsequent tasks must inherit code changes from the previous task's feature branch, otherwise dependent code would be missing at compile or test time.

The pre-transition state check in Step 9 is **skipped** for this mode because the feature branch intentionally remains.

## "Non-stop" means non-stop transitions, not non-stop coding

The branch lifecycle between tasks — merge into base branch, delete feature branch, create a new feature branch — is **not an interruption**. It IS the execution. These git operations take seconds and are what make per-task isolation work.

Skipping them to "keep coding" is the single most common range-mode failure. Symptoms include:

- Multiple tasks landing on one branch (cannot be reviewed, merged, or rolled back independently)
- Orphaned branches in `git branch --list "feature/*"`
- Cherry-picked commits with broken SHA lineage (the feature branch appears unmerged even though its code is on main)
- Dependency resolution failures because `tasks/completed/` does not match what is actually merged

If you feel tempted to "optimize" by staying on the same branch for the next task, **stop**. That optimization breaks everything downstream. The Step 9 pre-transition state check exists precisely to catch this failure mode before it propagates to the next task.

## Decision table

| Mode | Branch start point | Merge happens? | Per-task fresh branch? | Chain branching? |
|---|---|---|---|---|
| Normal (PR) | base branch | yes (via PR) | yes | no |
| `--local-merge` | base branch | yes (local `--no-ff`) | yes | no |
| `--draft` | previous feature branch (or base for first) | no | yes (per task) | yes |
| `--skip-ci-wait` | previous feature branch (or base for first) | no | yes (per task) | yes |

The "per-task fresh branch" column is **always yes**. Even in chain-branching modes, every task gets its own feature branch — it just happens to start from the previous feature branch instead of the base branch.
