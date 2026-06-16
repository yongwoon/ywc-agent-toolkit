# Checkpoint and Resume - `ywc-sequential-executor`

Reference for `.ywc-run-state.json` and resume detection. Root state is the
default; `--worktree` runs store state at `$WT/.ywc-run-state.json`.

## Resume Detection

Run before Pre-flight. Check root state first:

```bash
test -f .ywc-run-state.json && cat .ywc-run-state.json || echo "no-state"
```

If root state is absent, enumerate preserved run worktrees:

```bash
git worktree list --porcelain
test -f <worktree>/.ywc-run-state.json && cat <worktree>/.ywc-run-state.json
```

If multiple worktree state candidates exist, return `NEEDS_CONTEXT` with the
candidate paths. Do not guess which run to resume.

If the file exists, apply these checks in order:

1. `executor` must be `"sequential"`; if it is `"parallel"`, stop until the user deletes it or chooses the parallel executor.
2. If `last_checkpoint` is older than 48 hours, treat it as stale and ask whether to delete it and start fresh.
3. Compare `completed` against `<tasks-dir>/completed/`; warn on mismatch. If `current_step >= 2` and `branch` is set but missing locally, set `branch` to `null` and regress to Step 1.
4. **Intent-match guard (run before offering resume)** — compare the current invocation's explicit task specifier/range against the saved run's scope. Prefer saved `range`; if it is absent or incomplete, fall back to parsing saved `args`.
   - **No explicit specifier** (auto-detect mode) → skip this guard and continue to step 5. Auto-detect reasonably means "continue the interrupted run."
   - **Matching specifier** → continue to step 5. A match means the requested single task or range is the same as the saved `range`, or is a subset of the saved task set.
   - **Mismatching specifier** → treat the checkpoint as stale for the current intent. Do **not** auto-resume, and do not silently discard the state. Surface the divergence and require an explicit choice:

     ```text
     Stale run-state for a different scope found:
       Saved run : <saved range / args> (last checkpoint <date>, mode <mode>)
       Requested : <current specifier>

     These do not match. Choose:
       [1] Resume the saved run — the requested specifier is ignored
       [2] Discard the saved run and start the requested specifier — delete
           .ywc-run-state.json, then run Pre-flight fresh
     ```

     This guard prevents a stale run-state from hijacking a freshly requested range.
5. Offer resume only after the guard passes:

   ```text
   Resumable run found:
     Last checkpoint : <last_checkpoint>
     In progress     : <current_task> at Step <current_step>
     Completed       : <N> / <total>
   Resume? [Y/n]
   ```
6. If the user resumes, skip Pre-flight and jump to the saved task and step.
7. If the user declines, or chooses option [2] from the mismatch branch, delete `.ywc-run-state.json` and run normal Pre-flight.

## State File Format

```json
{
  "executor": "sequential",
  "args": "<original arguments>",
  "mode": "local-merge|draft|skip-ci-wait|aggregate-pr|normal",
  "tasks_dir": "tasks/",
  "range": ["<task-1>", "<task-2>"],
  "completed": [],
  "current_task": null,
  "current_step": 0,
  "branch": null,
  "worktree_mode": false,
  "worktree_path": null,
  "integration_branch": null,
  "start_point": null,
  "run_task_name": null,
  "started_at": "<ISO 8601 UTC>",
  "last_checkpoint": "<ISO 8601 UTC>"
}
```

For `--worktree`, set `worktree_mode: true`, write this file under
`$WT/.ywc-run-state.json`, and populate `worktree_path`, `integration_branch`,
`start_point`, and `run_task_name`.

## Checkpoint Events

| Event | Fields to update |
|---|---|
| Pre-flight passes | `started_at`, `range`, `mode`, `tasks_dir`; for `--worktree`, also `worktree_mode`, `worktree_path`, `integration_branch`, `start_point`, `run_task_name` |
| Step 2 complete | `current_task`, `current_step: 2`, `branch: "feature/<name>"` |
| Step 4 complete | `current_step: 4` |
| Step 5 complete (`ywc-finish-branch` returned `DONE`) | `current_step: 8` for resume compatibility; `branch: null` for `normal-pr`/`local-merge`/`aggregate-pr` (feature branch deleted; in `aggregate-pr`, working tree returns to `work/<name>`); append completed task when finalized |
| Step 6 transition to next task | `current_task: <next-task>`, `current_step: 0` |
| All tasks done | remove root `.ywc-run-state.json`, or `$WT/.ywc-run-state.json` for `--worktree`; then apply worktree cleanup rules from `worktree-run.md` |

## Manual Inspection

```bash
python <path-to-skill>/scripts/inspect-state.py
python <path-to-skill>/scripts/inspect-state.py --json
python <path-to-skill>/scripts/resume-state.py
python <path-to-skill>/scripts/resume-state.py --json
python <path-to-skill>/scripts/inspect-state.py --state-file <worktree>/.ywc-run-state.json --json
```

The file must be added to `.gitignore`.
