# Checkpoint and Resume — `ywc-sequential-executor`

> Reference for the `.ywc-run-state.json` checkpoint format and the Resume Detection procedure used by `ywc-sequential-executor`. Linked from the skill's "Checkpoint and Resume" section.

## 1. Why This Exists

A range execution may run for hours and traverse dozens of tasks, branches, and CI cycles. If the session is interrupted (network drop, accidental cancel, machine restart), the executor must be able to resume without redoing completed tasks or starting the in-progress task from scratch. The checkpoint is a small JSON file written after each major step; the Resume procedure validates the file against current git state before deciding whether to honor it.

The file lives at `.ywc-run-state.json` in the project root and is `.gitignore`d — it is per-machine, per-run state, not source.

## 2. Resume Detection (run before Pre-flight)

Before the standard Pre-flight checks, look for a checkpoint:

```bash
test -f .ywc-run-state.json && cat .ywc-run-state.json || echo "no-state"
```

If the file exists, apply these checks in order:

1. **Executor check** — `executor` must be `"sequential"`. If `"parallel"`, warn:
   *"State belongs to parallel-executor. Cannot resume as sequential."*
   Stop until the user deletes the file.

2. **Age check** — if `last_checkpoint` is older than 48 hours, treat as stale. Ask:
   *"Stale checkpoint found (\<date\>). Delete and start fresh? [Y/n]"*

3. **Git validation**:
   - Compare `completed` list against `tasks/completed/` entries — report any mismatch as a warning.
   - If `current_step >= 2` and `branch` is set: run `git branch --list <branch>`. If the branch is gone, set `branch` to `null` and regress `current_step` to `1`.

4. **Intent-match guard (run before offering resume)** — compare the current invocation's explicit task specifier/range against the saved run's tasks (`range`; `args` is the fallback):
   - **No explicit specifier** (auto-detect mode) → skip this guard; proceed to step 5 (resuming the prior run is the sensible default).
   - **Specifier matches** the saved `range` (same range, or a subset) → proceed to step 5.
   - **Specifier does NOT match** the saved `range` → the user intends a **new** run. **Do not auto-resume**, and do not default to either option — surface the divergence and wait for an explicit choice:
     ```
     ⚠️ Stale run-state for a different scope found:
        Saved run : <saved range / args>  (last checkpoint <date>, mode <mode>)
        Requested : <current specifier>
     These do not match. Choose:
       [1] Resume the saved run — your requested <specifier> is ignored
       [2] Discard the saved run and start <specifier> — delete
           .ywc-run-state.json, then run Pre-flight fresh
     ```
     This guard exists because the most damaging silent failure is a freshly requested range being **hijacked** by an interrupted prior run's state.

5. **Offer resume** (only when the guard passed — auto-detect, or a matching specifier):
   ```
   Resumable run found:
     Last checkpoint : <last_checkpoint>
     In progress     : <current_task> at Step <current_step>
     Completed       : <N> / <total>
   Resume? [Y/n]
   ```

6. If **Y** — skip Pre-flight and jump to `current_task` at `current_step`.
7. If **N**, or the guard's option **[2]** — delete `.ywc-run-state.json` and proceed with a fresh run.

## 3. State File Format

Location: `.ywc-run-state.json` in the project root. Always `.gitignore`d.

```json
{
  "executor": "sequential",
  "args": "<original arguments>",
  "mode": "local-merge|draft|skip-ci-wait|normal|aggregate-pr",
  "tasks_dir": "tasks/",
  "range": ["<task-1>", "<task-2>"],
  "completed": [],
  "current_task": null,
  "current_step": 0,
  "branch": null,
  "started_at": "<ISO 8601 UTC>",
  "last_checkpoint": "<ISO 8601 UTC>"
}
```

Initialize after Pre-flight passes. Always update `last_checkpoint` to the current UTC time when writing.

## 4. Checkpoint Events

Update the file at the following events. The skill's per-step Checkpoint markers reference this table.

| Event | Fields to update |
|---|---|
| Pre-flight passes | Initialize file; `started_at`, `range`, `mode`, `tasks_dir` |
| Step 2 complete | `current_task`, `current_step: 2`, `branch: "feature/<name>"` |
| Step 4 complete | `current_step: 4` |
| Step 5 complete (finish-branch returned DONE) | `current_step: 8` (legacy value, preserved for resume compat); `branch: null` for `normal-pr`/`local-merge`/`aggregate-pr` (the feature branch is deleted; in `aggregate-pr` the working tree returns to `work/<name>`, not the base branch); push task to `completed` |
| Step 6 transition (next task starts) | `current_task: <next-task>`, `current_step: 0` |
| All tasks done | `rm -f .ywc-run-state.json` |

## 5. Manual Inspection

```bash
python <path-to-skill>/scripts/inspect-state.py        # state summary
python <path-to-skill>/scripts/resume-state.py         # validate + resume point
python <path-to-skill>/scripts/resume-state.py --json  # machine-readable output
rm .ywc-run-state.json                                  # reset (force fresh run)
```

The `inspect-state.py` and `resume-state.py` helpers live under `scripts/` next to this reference.

## 6. .gitignore Wiring

The state file must never be committed. The skill ensures this on its first run:

```bash
grep -qxF '.ywc-run-state.json' .gitignore 2>/dev/null || echo '.ywc-run-state.json' >> .gitignore
```

If the user has a stricter ignore policy, point it there instead — but the rule stands: this file is per-machine state.
