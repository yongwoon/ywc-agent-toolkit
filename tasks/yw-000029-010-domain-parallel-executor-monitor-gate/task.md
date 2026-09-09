# yw-000029-010-domain-parallel-executor-monitor-gate — Implementation Checklist

## Prerequisites
- [ ] `yw-000028-010-docs-subagent-async-monitoring-contract` is completed (merged) — `claude-code/skills/references/subagent-async-monitoring.md` exists with its four named sections

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`: `claude-code/skills/ywc-parallel-executor/SKILL.md` only
- [ ] If the task requires edits outside this file, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `claude-code/skills/references/subagent-async-monitoring.md` does not exist or is missing one of its four named sections
- [ ] Stop if the existing `## Status Routing` table no longer has exactly 5 rows at the location the spec describes (re-verify with `rg -n "^\| \`" claude-code/skills/ywc-parallel-executor/SKILL.md` before editing)
- [ ] Stop if inserting the `4b-monitor` subsection would require reflowing or renumbering any of the existing `4a`/`4b`/`4c` step labels

## Implementation Steps
- [ ] Insert a new `**4b-monitor** (mechanical gate — do not skip)` subsection immediately after the last "append verbatim" directive bullet (Test-first-where-feasible) and immediately before the "Handling each subagent's status return" paragraph:
  - [ ] Imperative opening sentence: before treating the wave as complete, the orchestrator must reconcile the full expected roster (every task name dispatched in this wave) against the set of task names it has received a terminal status for.
  - [ ] Cite `../references/subagent-async-monitoring.md` for the Unique Dispatch Labeling and Full-Roster Reconciliation rules — do not restate their content inline.
  - [ ] Phrase it "never treat the wave complete without one terminal status per dispatched task name" (mirroring `4a-verify`'s "never reach 4b without..." pattern).
  - [ ] Optionally include a one-line shell-style illustrative check analogous to `4a-verify`'s `for t in <wave-task-names>; do ...; done` pattern — a check-shaped example, not a bundled script (per the spec's Out of Scope: no new tooling is introduced).
- [ ] Add one new row to the inline `## Status Routing` table (currently 5 rows):
  - [ ] Returned status column: `No completion notification received within the escalation threshold`
  - [ ] Caller action column: identical consequence to the existing `BLOCKED` row — run the four-step triage (context → reasoning → scope → plan), preserve the task's branch and worktree (skip Step 4g for this task), record for the Completion Report
- [ ] Re-read the full diff and confirm the existing 5 Status Routing rows and the `4a-verify` gate text are unchanged.

## Task Verify
- [ ] `rg -n "4b-monitor" claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `rg -n "subagent-async-monitoring.md" claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `rg -n "No completion notification" claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-parallel-executor --format json`

## Verification
- [ ] `bash scripts/validate.sh` still passes
- [ ] `git diff --check` reports no whitespace errors

## Implementation Notes (optional)
