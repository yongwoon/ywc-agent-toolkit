# Non-Stop Execution Principle — Shared Reference

Used by `ywc-sequential-executor` and `ywc-parallel-executor`. Both executors must execute their full range (sequential tasks, or parallel waves) without interruption. The principle is the **same**; only the unit (task vs. wave) and the per-step indices differ.

When citing this from a skill, replace `<unit>` with the executor's unit (`task` for sequential, `wave` for parallel) and use the executor's own step indices for the "Zero output" paragraph.

## Allowed Stop Reasons (Exhaustive)

A stop is permissible **only** for the conditions below. Anything not on this list is not a valid stop reason.

**Common to both executors:**
- Pre-flight failure
- `git push` rejected by remote
- Merge conflict
- Flag conflict detected in arguments

**Sequential-specific (per task):**
- Dependency not satisfied and no exception applies (Step 1)
- A `task.md` Stop Condition is triggered (Step 3)
- Verification fails after 2 fix attempts (Step 4)
- CI fails after 2 fix attempts (Step 6, normal mode)

**Parallel-specific (per wave):**
- Circular dependency detected
- All tasks in a wave failed

## Never Stop For These Reasons

- "Let me check if you want to continue" — the user already specified the range; that **is** the instruction.
- Reporting success of the current `<unit>` before starting the next — defer all reporting to the Completion Report.
- Asking whether the implementation looks correct — trust the verification step.
- Summarizing what was done so far — this breaks flow and adds no value mid-range.
- Any form of "shall I proceed?" or "ready for the next `<unit>`?" — yes, always; that is what range mode means.
- A minor warning (not an error) from lint, build, or a single verify step — log it internally and continue.
- Context window getting long — continue without summarizing; do not generate a "progress checkpoint" message.
- Uncertainty about whether to continue — if the situation is not on the Allowed list above, the answer is always **continue**.

## Force Continue Rule

The Allowed stop list is exhaustive. If a situation is not on that list, proceed **immediately** — do not pause to evaluate whether it should be a stop reason. The impulse to pause is itself the failure mode. When in doubt, continue.

## Tool Error Recovery

Tool call failures are **not** stop conditions that require extended reasoning. They are implementation obstacles with deterministic recovery actions. Execute the recovery immediately — do not enter extended thinking.

### Edit / Update — "Error editing file"

The most common cause: `old_string` no longer matches the file because a preceding tool call modified it since the last read.

Recovery sequence (execute immediately, no thinking required):
1. **Re-read the file** with the `Read` tool (full content).
2. **Retry the edit** with `old_string` extracted from the freshly read content.

**Attempt cap**: 2 retries. If still failing after 2 retries: stop and report — include the file path, the section you were attempting to replace, and the exact error text.

### Bash — non-zero exit or unexpected output

For transient failures (network timeout, race condition): retry once. For all others: inspect the error output, fix the root cause (wrong flag, missing path, missing binary, wrong working directory), re-run. Maximum 2 fix attempts before stopping.

### General Rule

> A tool error always has a mechanical fix. Identify and apply it immediately. Only failure after 2 fix attempts escalates to a stop condition. Extended thinking is never the right response to a tool error.

## Zero Output Between `<unit>` Transitions

After completing the final step of one `<unit>` and before beginning the first step of the next, emit **no text output**. No "`<Unit>` N complete", no "Moving to `<unit>` N+1", no blank line, no status summary. The transition is silent. All reporting is deferred to the Completion Report at the end of the range. Every character of intermediate output is a potential interruption vector.

## Tool Permission Prompts Are Not a Stop Condition

If Claude Code prompts for user confirmation on a `git`, `gh`, or `mv` command during range execution, the relevant Bash patterns were not pre-authorized before the run. Pre-authorize all required tools before starting (see [`local-merge-permissions.md`](./local-merge-permissions.md)). A permission prompt is an infrastructure problem to fix before the next run, **not** a stop signal for the current run.

## Why This Matters Most in `--local-merge` Mode

`--local-merge` removes the two natural pause points (CI wait, PR review). The entire value proposition of `--local-merge` is fast, uninterrupted execution against the local clone. There is no external process to wait for, so there is no reason to pause.

## "Non-Stop" Means Non-Stop Transitions, Not Non-Stop Coding on One Branch

The branch lifecycle between `<unit>`s — merge into base branch, delete feature branch, create a new feature branch — is **not** an interruption. It IS the execution. These git operations take seconds and are what make per-`<unit>` isolation work. Skipping them to "keep coding" is the single most common range-mode failure: it results in multiple tasks landing on one branch, orphaned branches, and cherry-picked commits with broken SHA lineage. If you feel tempted to "optimize" by staying on the same branch for the next `<unit>`, stop — that optimization breaks everything downstream.
