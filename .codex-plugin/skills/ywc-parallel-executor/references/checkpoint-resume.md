# Checkpoint and Resume

Use this reference when `.ywc-run-state.json` exists before `ywc-parallel-executor` Pre-flight, or when inspecting/resuming a multi-wave parallel run.

## Resume Detection

Run before Pre-flight checks:

```bash
test -f .ywc-run-state.json && cat .ywc-run-state.json || echo "no-state"
```

If the file exists:

1. **Executor check** — `executor` must be `"parallel"`. If `"sequential"`, warn: *"State belongs to sequential-executor. Cannot resume as parallel."* Stop until user deletes the file.
2. **Age check** — if `last_checkpoint` is older than 48 hours, treat as stale. Ask: *"Stale checkpoint found (<date>). Delete and start fresh? [Y/n]"*
3. **Worktree validation** — for each task in the in-progress wave's `pending` list, validate the resolved path using the same precedence as resume-state validation: recorded state root, then project `.worktrees/`, then `CLAUDE.md worktree_root`, then legacy fallback. If a worktree is missing, add a warning: the agent must recreate it in Step 4a before implementation can continue.
4. **Offer resume**:

```text
Resumable run found:
  Last checkpoint : <last_checkpoint>
  Resume at       : Wave <resume_wave>
  Already merged  : <merged_in_wave> (this wave)
  Pending         : <pending>
Resume? [Y/n]
```

5. If **Y** — skip Pre-flight and jump to Wave `resume_wave`, skipping already-merged tasks.
6. If **N** — delete `.ywc-run-state.json` and proceed with a fresh run.

## State File Format

Location: `.ywc-run-state.json` in the project root (`.gitignore`d).

```json
{
  "executor": "parallel",
  "args": "<original arguments>",
  "mode": "local-merge|draft|per-task-pr",
  "tasks_dir": "tasks/",
  "worktree_root": "<absolute resolved root from ywc-worktrees>",
  "root_kind": "standard|legacy",
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

## Checkpoint Summary

| Event | Fields to update |
|---|---|
| Pre-flight passes | Initialize file; `started_at`, `mode`, `tasks_dir`, all waves as `planned` |
| Step 4a complete (wave start) | Set wave `status` to `in_progress`; populate `pending` with all wave tasks |
| Step 4e per-task delivery complete (`ywc-finish-branch` returned `DONE`) | Move task from `pending` to `merged` in the wave entry |
| Step 4e wave loop complete (all tasks delivered or `BLOCKED`) | Set wave `status` to `completed`; `current_wave` to next wave number |
| All waves done | `rm -f .ywc-run-state.json` |

## Manual Inspection

```bash
python <path-to-skill>/scripts/save-state.py           # state summary
python <path-to-skill>/scripts/resume-state.py         # validate + resume point
python <path-to-skill>/scripts/resume-state.py --json  # machine-readable output
rm .ywc-run-state.json                                  # reset (force fresh run)
```
