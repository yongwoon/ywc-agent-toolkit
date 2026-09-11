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
  "run_id": "<8 hex chars, immutable for the run's life>",
  "current_wave": 0,
  "waves": [
    {
      "wave": 0,
      "tasks": ["<task-1>", "<task-2>"],
      "status": "completed|in_progress|planned|failed|BLOCKED",
      "merged": [],
      "pending": [],
      "integration_branch": "wave-int/0",
      "integration_branch_owner": "<run_id of the run that created/last advanced this branch — absent until first write>",
      "integration_branch_tip_sha": "<40-char sha, last-known-good checkpoint — absent until first write>",
      "hardener_verdict": "<absent|PASS|BLOCKED|NEEDS_CONTEXT — present only for a contract-bearing wave once Step 4e.5 has run>",
      "hardener_detail": "<Hardener's own diagnostic text for the current hardener_verdict — absent when hardener-verdict ran without --detail>",
      "reason": "<blocking reason — present only when status is BLOCKED>",
      "blocked_detail": "<expected/actual diagnostic text — absent when wave-int-blocked ran without --detail>"
    }
  ],
  "started_at": "<ISO 8601 UTC>",
  "last_checkpoint": "<ISO 8601 UTC>"
}
```

`run_id` is generated once by `init-parallel` and never modified afterward, including across a resume (the resumed run reads the same file, so the same `run_id`). `integration_branch_owner` / `integration_branch_tip_sha` are absent — key omitted entirely, never `null` — for a wave whose `integration_branch` is `None`, and remain absent for a contract-bearing wave until its first `wave-int-owner` call. `reason` is written whenever a wave's `status` becomes `BLOCKED` — by `wave-int-blocked` (reuse-verification failure) or by `promotion-retry` hitting its cap (`promotion-churn`) — and persists even after `promotion_retry_count` exceeds the cap. `blocked_detail` is written only alongside `wave-int-blocked --detail` and is removed (key omitted, never `null`) on a subsequent `wave-int-blocked` call made without `--detail`. `hardener_detail` is a distinct field owned by `hardener-verdict --detail` — never conflate it with `blocked_detail`, which is exclusively the reuse-verification path's field; it is removed (key omitted, never `null`) on a subsequent `hardener-verdict` call made without `--detail`.

Initialize after Pre-flight passes. Always update `last_checkpoint` to the current UTC time when writing.

## Checkpoint Summary

| Event | Fields to update |
|---|---|
| Pre-flight passes | Initialize file; `started_at`, `mode`, `tasks_dir`, `run_id`, all waves as `planned` |
| Step 4a complete (wave start) | Set wave `status` to `in_progress`; populate `pending` with all wave tasks |
| `wave-int/<N>` created or its base-merge pushed (contract-bearing wave only) | `wave-int-owner <N> --tip-sha <sha>` — records checkpoint ownership + last-known-good tip; verified before any reuse per [wave-integration-branch.md](wave-integration-branch.md) |
| Reuse verification blocks (branch missing / ownership mismatch / tip divergence / materialize failure) | `wave-int-blocked <N> --reason <reason> --detail <text>` — wave `status` → `BLOCKED`, never a bare prose instruction or hand-edit |
| Step 4e per-task delivery complete (`ywc-finish-branch` returned `DONE` for `--local-merge` / `--draft` / `--aggregate-pr`, or the inline `--per-task-pr` PR merge + Mark Complete path succeeded) | Move task from `pending` to `merged` in the wave entry |
| Step 4e.5 Hardener/aggregate exit (contract-bearing wave, `--local-merge`/`--draft`/`--aggregate-pr` only) | `hardener-verdict <N> <absent\|PASS\|BLOCKED\|NEEDS_CONTEXT> [--detail <text>]` — written **before** promotion is attempted; pass `--detail` with Hardener's own diagnostic text whenever the verdict is `NEEDS_CONTEXT` |
| Step 4e.6 promotion succeeds | Set wave `status` to `completed`; `current_wave` to next wave number — **this replaces the row below for a wave that created `wave-int/<N>`** |
| Step 4e wave loop complete, wave never created `wave-int/<N>` (contract-less, or `--per-task-pr`) | Set wave `status` to `completed`; `current_wave` to next wave number — unchanged from today |
| Step 4e.6 promotion-conflict base-merge retried | `promotion-retry <N>` — capped at 2; exceeding marks the wave `BLOCKED` with reason `promotion-churn` |
| All waves done | `rm -f .ywc-run-state.json` |

### Resume with `wave-int/<N>`

For a wave that created `wave-int/<N>` (`integration_branch` non-`None`), "`wave-complete` not yet stamped" on resume means one of:

1. **Partial-merge** (`pending` non-empty, `wave-int/<N>` already exists) — resume by first running the reuse-verification procedure in [wave-integration-branch.md](wave-integration-branch.md): a same-run resume passes trivially since `run_id` and the prior `integration_branch_tip_sha` are already in this run's own state file (the ancestor-check tolerates the branch having advanced past the last checkpoint). Only after ownership verifies does resume merge the remaining `pending` tasks onto the branch.
2. **Fully-merged-not-promoted, `hardener_verdict` absent or `PASS`** (`pending` empty, `status != completed`) — resume auto-retries the wave-boundary aggregate + promotion with no prompt.
3. **Fully-merged-not-promoted, `hardener_verdict == BLOCKED`** (`pending` empty, `status != completed`) — resume stops and prints the recorded blocking findings, then requires explicit user confirmation before re-running the gate.
4. **Fully-merged-not-promoted, `hardener_verdict == NEEDS_CONTEXT`** (`pending` empty, `status != completed`) — resume stops and prints the recorded `hardener_detail` (Hardener's own missing-context diagnostic, distinct from `blocked_detail`), then requires the missing context to be supplied — not a bare confirmation — before re-running the gate.

A fully contract-less wave (`integration_branch` was `None` from init) keeps today's resume behavior unchanged.

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
