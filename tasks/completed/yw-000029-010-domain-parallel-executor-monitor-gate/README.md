# yw-000029-010-domain-parallel-executor-monitor-gate

## Purpose
Wire `ywc-parallel-executor`'s Step 4b wave dispatch to the shared async-monitoring contract so a wave is never treated as complete without full-roster reconciliation, and route a missing-notification timeout the same way an existing `BLOCKED` return is routed.

## Scope
Add a new `**4b-monitor**` mechanical-gate subsection between the existing Step 4b paragraph and the "Handling each subagent's status return" paragraph, and add one new row to the inline `## Status Routing` table.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#functional-requirements` — FR2, FR3
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#acceptance-criteria` — AC1, AC2
- `claude-code/skills/ywc-parallel-executor/SKILL.md:198-201` — the existing `4a-verify` gate is the style template (imperative, includes a runnable check, "never reach X without Y" phrasing)
- `claude-code/skills/ywc-parallel-executor/SKILL.md:238-249` — the exact `## Status Routing` table the new row is appended to (5 existing rows; there is no separate `references/status-routing.md` file in this repo)
- `claude-code/skills/references/subagent-async-monitoring.md` (produced by `yw-000028-010`) — the contract this gate cites

### Summary
Step 4b spawns one subagent per task in a wave via the `Agent` tool — the exact concurrent-dispatch pattern that caused the source incident (two completions mixed up, a finished task mistaken for pending ~40 minutes). The new `4b-monitor` subsection names each dispatched agent uniquely by task name and requires full-roster reconciliation before the wave is treated as complete, citing `../references/subagent-async-monitoring.md`. The Status Routing table gains one row for "no completion notification within the escalation threshold," routed to the same consequence as the existing `BLOCKED` row (four-step triage, preserve branch/worktree, record for Completion Report).

### Out of Scope (from spec)
- The shared reference file's content — handled by `yw-000028-010-docs-subagent-async-monitoring-contract` (dependency)
- `ywc-sequential-executor` and `ywc-impl-review` edits — handled by `yw-000029-020` and `yw-000029-030` respectively
- The existing Linear-chain guard for a wave of exactly 1 task (`SKILL.md:168`) already routes single-task waves to `ywc-sequential-executor` before Step 4 — no additional guard needed in Step 4b itself per the spec's Edge Cases

## Criticality
normal — orchestration/documentation prose only; no auth, payment, crypto, PII, or external-input-handling code path.

## Dependencies

### Depends On
- `yw-000028-010-docs-subagent-async-monitoring-contract` — provides `claude-code/skills/references/subagent-async-monitoring.md` and its four section names, which this task cites

### Depended By
- `yw-000030-010-infra-async-monitoring-validation` — validates this edit alongside the other two consumer edits

## Key Files
- `claude-code/skills/ywc-parallel-executor/SKILL.md` — new `**4b-monitor**` subsection + one new `## Status Routing` table row

## Notes
- The new subsection must sit strictly between the last "append verbatim" directive bullet (Test-first-where-feasible, currently ending the 4b paragraph block) and the "Handling each subagent's status return" paragraph — do not insert it before the directive bullets or after the Status Routing table.
- Match the `4a-verify` style exactly: a short imperative paragraph plus an optional one-line shell-style check — not a multi-paragraph essay.
- The new Status Routing row's Caller action text must be word-for-word equivalent to the existing `BLOCKED` row's action (four-step triage, preserve branch/worktree — skip 4g, record for Completion Report), not a new consequence.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-parallel-executor/SKILL.md`

### Owned Interface
- (None — this task only adds a subsection and a table row to an existing skill body; no new public interface)

### Shared Surfaces
- (None identified) — `yw-000029-020` and `yw-000029-030` edit different SKILL.md files with no overlap.

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000028-010-docs-subagent-async-monitoring-contract`

### Task Verify
- `rg -n "4b-monitor" claude-code/skills/ywc-parallel-executor/SKILL.md`
- `rg -n "subagent-async-monitoring.md" claude-code/skills/ywc-parallel-executor/SKILL.md`
- `rg -n "No completion notification" claude-code/skills/ywc-parallel-executor/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-parallel-executor --format json`

## Out of Scope
- Any edit to `claude-code/skills/ywc-sequential-executor/SKILL.md`, `claude-code/skills/ywc-impl-review/SKILL.md`, or `claude-code/skills/references/subagent-async-monitoring.md`.
- Any change to the existing 5 Status Routing rows, the `4a-verify` gate, or the Return Payload Contract text.
