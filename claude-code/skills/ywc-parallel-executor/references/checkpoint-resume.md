# Checkpoint and Resume — ywc-parallel-executor

> Tier-3 reference extracted from `SKILL.md` (ywc-skill-author A8/A14). The executor links this file from its `## Checkpoint and Resume` pointer.

The executor writes `.ywc-run-state.json` in the project root after each major wave event. If a multi-wave run is interrupted, you can resume from the last checkpoint — completed waves are skipped and the in-progress wave restarts with only its remaining pending tasks.

### Resume Detection

Run before Pre-flight checks:
```bash
test -f .ywc-run-state.json && cat .ywc-run-state.json || echo "no-state"
```

If the file exists:
1. **Executor check** — `executor` must be `"parallel"`. If `"sequential"`, warn: *"State belongs to sequential-executor. Cannot resume as parallel."* Stop until user deletes the file.
2. **Age check** — if `last_checkpoint` is older than 48 hours, treat as stale. Ask: *"Stale checkpoint found (<date>). Delete and start fresh? [Y/n]"*
3. **Worktree validation** — for each task in the in-progress wave's `pending` list, check whether `../worktree-<task-name>` exists. If a worktree is missing, add a warning: the agent must recreate it in Step 4a before implementation can continue.
4. **Intent-match guard (run before offering resume)** — compare the current invocation's explicit task specifier/range against the saved run's tasks (`waves[].tasks`; `args` is the fallback):
   - **No explicit specifier** (auto-detect mode) → skip this guard; proceed to step 5 (resuming the prior run is the sensible default).
   - **Specifier matches** the saved tasks (same range, or a subset of the saved set) → proceed to step 5.
   - **Specifier does NOT match** the saved tasks → the user intends a **new** run. **Do not auto-resume**, and do not default to either option — surface the divergence and wait for an explicit choice:
     ```
     ⚠️ Stale run-state for a different scope found:
        Saved run : <saved waves' tasks / args>  (last checkpoint <date>, mode <mode>)
        Requested : <current specifier>
     These do not match. Choose:
       [1] Resume the saved run — your requested <specifier> is ignored
       [2] Discard the saved run and start <specifier> — first delete
           .ywc-run-state.json and remove the saved run's leftover worktrees and
           branches (`ywc-worktrees --mode prune`, then `git branch -D
           feature/<saved-task>` for each), then run Pre-flight fresh
     ```
     This guard exists because the most damaging silent failure is a freshly requested range being **hijacked** by an interrupted prior run's state — exactly the case where an interrupted `--aggregate-pr` run silently resumes when a later, different range is requested.
5. **Offer resume** (only when the guard passed — auto-detect, or a matching specifier):
   ```
   Resumable run found:
     Last checkpoint : <last_checkpoint>
     Resume at       : Wave <resume_wave>
     Already merged  : <merged_in_wave> (this wave)
     Pending         : <pending>
   Resume? [Y/n]
   ```
6. If **Y** — skip Pre-flight and jump to Wave `resume_wave`, skipping already-merged tasks.
7. If **N**, or the guard's option **[2]** — delete `.ywc-run-state.json` (and for [2], also remove the saved run's worktrees/branches) and proceed with a fresh run.

### State File Format

Location: `.ywc-run-state.json` in the project root (`.gitignore`d).

```json
{
  "executor": "parallel",
  "args": "<original arguments>",
  "mode": "local-merge|draft|per-task-pr|aggregate-pr",
  "tasks_dir": "tasks/",
  "current_wave": 0,
  "waves": [
    {
      "wave": 0,
      "tasks": ["<task-1>", "<task-2>"],
      "status": "completed|in_progress|planned|failed",
      "merged": [],
      "pending": []
    }
  ],
  "started_at": "<ISO 8601 UTC>",
  "last_checkpoint": "<ISO 8601 UTC>"
}
```

Initialize after Pre-flight passes. Always update `last_checkpoint` to the current UTC time when writing.

### Checkpoint Summary

| Event | Fields to update |
|---|---|
| Pre-flight passes | Initialize file; `started_at`, `mode`, `tasks_dir`, all waves as `planned` |
| Step 4a complete (wave start) | Set wave `status` to `in_progress`; populate `pending` with all wave tasks |
| Step 4e per-task delivery complete (DONE — finish-branch for `--local-merge`/`--draft`, inline `gh pr merge` + Mark Complete for `--per-task-pr`) | Move task from `pending` to `merged` in the wave entry |
| Step 4e.5 Hardener dispatch exit (contract-bearing wave, `--local-merge`/`--draft`/`--aggregate-pr` only) | `hardener-verdict <N> <absent\|PASS\|BLOCKED>` — written **before** promotion is attempted |
| Step 4e.6 promotion succeeds | Set wave `status` to `completed`; `current_wave` to next wave number — **this replaces the old "wave loop complete" trigger below for a wave that created `wave-int/<N>`** |
| Step 4e wave loop complete, wave never created `wave-int/<N>` (contract-less, or `--per-task-pr`) | Set wave `status` to `completed`; `current_wave` to next wave number — unchanged from today |
| Step 4e.6 promotion-conflict base-merge retried | `promotion-retry <N>` — capped at 2; exceeding marks the wave `BLOCKED` with reason `promotion-churn` |
| All waves done | `rm -f .ywc-run-state.json` |

### Resume with `wave-int/<N>`

For a wave that created `wave-int/<N>` (`integration_branch` non-`None`), the checkpoint table above changes what "`wave-complete` not yet stamped" means on resume. Three distinct cases, in resume-check order:

1. **Partial-merge** (`pending` non-empty, `wave-int/<N>` already exists) — resume by reusing the existing branch and merging the remaining `pending` tasks onto it, per the idempotent-creation rule in [wave-integration-branch.md](wave-integration-branch.md). Only once `pending` is empty does the wave enter case 2 or 3 below.
2. **Fully-merged-not-promoted, `hardener_verdict` absent or `PASS`** (`pending` empty, `status != completed`) — the common transient case: interrupted before Hardener ran, or Hardener passed but the run died before promotion. Resume **auto-retries** Hardener + promotion with no prompt; Hardener is a measurement gate, so re-running against unchanged input is a safe no-op.
3. **Fully-merged-not-promoted, `hardener_verdict == BLOCKED`** (`pending` empty, `status != completed`) — a deliberate, unresolved gate failure. Resume **stops and prints the recorded blocking findings**, then requires explicit user confirmation before re-running Hardener — matching the human-in-the-loop convention used for every other `BLOCKED` condition in this skill (merge conflict, circular dependency, base-refresh conflict). Idempotency makes the re-run *safe*, not *informative*; silently re-deriving an unresolved `BLOCKED` days later would train the user to ignore the gate.

A fully contract-less wave (`integration_branch` was `None` from init) never entered this branch of the resume logic — it keeps today's resume behavior unchanged.

### Manual Inspection

```bash
python <path-to-skill>/scripts/save-state.py           # state summary
python <path-to-skill>/scripts/resume-state.py         # validate + resume point
python <path-to-skill>/scripts/resume-state.py --json  # machine-readable output
rm .ywc-run-state.json                                  # reset (force fresh run)
```
