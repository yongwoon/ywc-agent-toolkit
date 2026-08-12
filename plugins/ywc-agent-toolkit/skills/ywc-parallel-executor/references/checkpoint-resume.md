# Checkpoint and Resume

Use this reference when `.ywc-run-state.json` exists before `ywc-parallel-executor` Pre-flight, or when inspecting/resuming a multi-wave parallel run.

## Resume Detection

Run before Pre-flight checks:

```bash
test -f .ywc-run-state.json && cat .ywc-run-state.json || echo "no-state"
```

If the file exists, this is an authoritative checkpoint: `--resume-disposition resume|stop` is required (see the parallel executor's Arguments table). No step below opens an interactive prompt — every branch produces a bounded status.

1. **Executor check** — `executor` must be `"parallel"`. If `"sequential"`, return `BLOCKED`: "State belongs to sequential-executor. Cannot resume as parallel." Do not delete the file; the user removes it manually if that is the intended recovery.
2. **Age check** — if `last_checkpoint` is older than 48 hours, note `stale_checkpoint: true` in the bounded report. This is informational only — it does not change the outcome; the disposition below still decides whether the run resumes or stops.
3. **Worktree validation** — for each task in the in-progress wave's `pending` list, validate the resolved path using the same precedence as resume-state validation: recorded state root, then project `.worktrees/`, then `CLAUDE.md worktree_root`, then legacy fallback. If a worktree is missing, add a warning: the agent must recreate it in Step 4a before implementation can continue.
4. **Intent-match guard** — compare the current invocation's explicit task specifier/range against the saved run's task set. Prefer the union of `waves[].tasks`; if `waves` is absent or incomplete, fall back to parsing saved `args`.
   - **No explicit specifier** (auto-detect mode or `--all`) → no mismatch; continue to step 5.
   - **Matching specifier** → no mismatch; continue to step 5. A match means the requested single task or range is the same as the saved task set, or is a subset of it.
   - **Mismatching specifier** → do not auto-resume the saved run under a silently different scope. Include the divergence in the bounded report (`saved: <saved waves' tasks / args> (last checkpoint <date>, mode <mode>)`, `requested: <current specifier>`) and continue to step 5 — disposition still governs the outcome, and `resume` means resuming the saved run with the requested specifier ignored.
5. **Resolve disposition** — read `--resume-disposition`:
   - Missing, or not exactly `resume` / `stop` → `NEEDS_CONTEXT: --resume-disposition`. Never guess and never fall back to an implicit default.
   - `resume` → skip Pre-flight and jump to Wave `resume_wave`, skipping already-merged tasks. On a scope mismatch (step 4), the requested specifier is ignored in favor of the saved run.
   - `stop` → leave `.ywc-run-state.json` and every worktree/branch it references unchanged; return `DONE_WITH_CONCERNS` (`resume_stopped`). Discarding the saved run and starting the requested specifier fresh is a separate, explicit follow-up: clean it up via the `ywc-worktrees` audit/prune flow — do not remove unknown worktrees or branches owned by another active operator — then re-invoke with a fresh `--resume-disposition` once no checkpoint remains.

## State File Format

Location: `.ywc-run-state.json` in the project root (`.gitignore`d).

```json
{
  "executor": "parallel",
  "args": "<original arguments>",
  "mode": "local-merge|draft|per-task-pr|aggregate-pr",
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
| Step 4e per-task delivery complete (`ywc-finish-branch` returned `DONE` for `--local-merge` / `--draft` / `--aggregate-pr`, or the inline `--per-task-pr` PR merge + Mark Complete path succeeded) | Move task from `pending` to `merged` in the wave entry |
| Step 4e wave loop complete (all tasks delivered or `BLOCKED`) | Set wave `status` to `completed`; `current_wave` to next wave number |
| All waves done | `rm -f .ywc-run-state.json` |

## Parallel aggregate transition cache

Parallel resume keeps `.ywc-run-state.json` as the only lifecycle authority. After a wave transition, the executor may write exactly one `.ywc-context-handoff.json` beside that root state through `scripts/transition_safety.py`. The file is a bounded, non-authoritative aggregate cache: worker worktrees never write handoffs, and worker-local output or peer conclusions are not copied into it.

The writer uses a same-directory temporary sibling, fsync, rename, and parent-directory fsync where supported. If replacement fails, the previous valid cache remains and checkpoint, completion, cleanup, and worktree deletion are unchanged. Readers discard missing, malformed, stale, mismatched, private, or worker-local values and reconstruct in this order: authoritative checkpoint, current `README.md`, then `task.md`.

With `--non-interactive`, resume, branch/worktree conflict, CI wait/timeout, and policy decisions are terminal statuses rather than prompts: missing `--resume-disposition` is `NEEDS_CONTEXT`, branch/worktree conflict is `BLOCKED`, and CI timeout is `DONE_WITH_CONCERNS` with `ci_timeout`.

## Manual Inspection

```bash
python <path-to-skill>/scripts/save-state.py           # state summary
python <path-to-skill>/scripts/resume-state.py         # validate + resume point
python <path-to-skill>/scripts/resume-state.py --json  # machine-readable output
rm .ywc-run-state.json                                  # reset (force fresh run)
```
