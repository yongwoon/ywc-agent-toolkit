# Completion Report Format — `ywc-parallel-executor`

> Reference for the report body displayed after all waves finish (Step 5). Linked from the skill's "Step 5: Completion Report" section. The `Completion Status` table and the Operational Self-Improvement / State cleanup rules stay in `SKILL.md`.

## 1. Report Content

Display the following after all waves are complete:

- Total tasks executed, total waves
- Each task: name, status (success/failed/skipped), merge commit SHA in `--local-merge` mode, or the merged PR URL in `--per-task-pr` mode, and its dispatch model as `<model> (<source>)` (source `hint` / `frontmatter` / `env` / `default`), plus an `Invalid Model Hint` note for any ignored hint (see [../../references/model-routing.md](../../references/model-routing.md))
- Failed/skipped tasks with reasons
- Per-wave changed public contracts (interfaces/DTOs altered) and any critical-path tasks that triggered `/ywc-security-audit`
- In `--local-merge` mode: remind that no PR was created, no remote CI ran, only local verification was performed
- In `--per-task-pr` mode: each task's PR was created, CI-verified, bot-reviewed, and **merged** (`gh pr merge`); list each PR URL with its merged status
- **Worktree cleanup status** — one line per task, in one of these categories (omitted when `--terse` is set):
  - `clean` — worktree removed and branch deleted via Step 4g (the expected outcome for every successful task)
  - `force-cleaned` — `git worktree remove --force` was required; note the reason (lock, disposable artifacts, etc.)
  - `preserved (failure)` — intentionally retained for recovery; include the worktree path and branch name so the user can resume work
  - `LEAKED` — Step 4g did not produce a clean result and the cause is not a recorded failure; this is a bug, surface it explicitly with the path and branch so the user can clean up manually

  Run a final audit before printing the report:

  ```bash
  git worktree list --porcelain | awk '/^worktree /{print $2}' | grep -E '/worktree-' || echo "OK: no parallel-executor worktrees remain"
  git branch --list 'feature/*' | sed 's/^[* ] //' || true
  ```

  Any `worktree-*` path or `feature/*` branch that does not map to a `preserved (failure)` task in the report is a leak and must be reported as `LEAKED`, not silently omitted.

**When `--terse` is set**, omit all prose reminders, worktree audit lines, and mode-specific explanations. Emit only:
1. The task table (name | status | merge SHA or PR URL)
2. The `Completion Status` line

This is the preferred format for CI scripts or automation that parse the report output.

**Reporting Symbols**: Use the shared vocabulary in [symbols.md](../../references/symbols.md) for the per-task status column, the worktree cleanup status column, and the wave-level summary line. **Parallel-specific addition**: `🚨` for `LEAKED` worktree or branch detected by the final audit (Step 5) — surface explicitly, never reduce to `❌`. Leaks are a distinct severity category the user must act on regardless of overall run status. For multi-step worktree lifecycle traces, use the flow operator `»` (e.g. `worktree ✅ » impl ✅ » verify ✅ » merge ✅ » cleanup ✅`).

## 2. Placement

The report is displayed once, after the Aggregate PR step (when applicable). The `Completion Status` line from `SKILL.md` is always the last line of the report; nothing in this reference follows it.
