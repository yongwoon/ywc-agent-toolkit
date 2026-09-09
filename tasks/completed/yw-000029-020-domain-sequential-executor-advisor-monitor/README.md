# yw-000029-020-domain-sequential-executor-advisor-monitor

## Purpose
Wire `ywc-sequential-executor`'s ad-hoc background-fork risk and bounded Opus advisor dispatch to the shared async-monitoring contract, without growing the file past its current 502-line total.

## Scope
Add one new Rationalization Defense row, append one inline cross-reference sentence to the Advisor Escalation Policy paragraph, and remove one blank line elsewhere in the same file so the net line count stays at 502.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#functional-requirements` — FR4, FR5, FR6
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#acceptance-criteria` — AC3
- `claude-code/skills/ywc-sequential-executor/SKILL.md:19-39` — the 21-row Rationalization Defense table the new row is appended to
- `claude-code/skills/ywc-sequential-executor/SKILL.md:213` — the Advisor Escalation Policy paragraph the citation is appended to inline (no new line break)
- `claude-code/skills/ywc-sequential-executor/SKILL.md:483-485` — the exact blank-line trim location (immediately after the closing code-fence of the state-cleanup verification block, before "If the verification line prints `WARNING`...")

### Summary
`ywc-sequential-executor/SKILL.md` is confirmed at exactly 502 total lines / `body_lines = 499` against the `A8_body_cap` threshold (`body_lines <= 500`) — 1 line of headroom. FR4 adds a Rationalization Defense row blocking ad-hoc, unplanned background-agent forking mid-task/mid-range (+1 line). FR5 appends a cross-reference sentence to the existing Advisor Escalation Policy paragraph **inline, with no new line break** (+0 lines) — this is load-bearing: a new line here would push the file to 503 and breach AC3. FR6 removes the single blank line at lines 483-485 (−1 line). Net: +1 +0 −1 = 0; final total stays 502.

### Out of Scope (from spec)
- The shared reference file's content — handled by `yw-000028-010-docs-subagent-async-monitoring-contract` (dependency)
- `ywc-parallel-executor` and `ywc-impl-review` edits — handled by `yw-000029-010` and `yw-000029-030` respectively
- Any change to the Rationalization Defense table's existing 21 rows — each is a distinct, incident-specific guardrail; none may be merged or trimmed as the line-count offset (the spec explicitly forbids this)
- Single-task (non-range) invocations with no `--review` fan-out never trigger the fallback-wakeup machinery — the new row and citation apply only when a concurrent dispatch is actually considered (per the spec's Edge Cases)

## Criticality
normal — orchestration/documentation prose only; no auth, payment, crypto, PII, or external-input-handling code path.

## Dependencies

### Depends On
- `yw-000028-010-docs-subagent-async-monitoring-contract` — provides `claude-code/skills/references/subagent-async-monitoring.md`, which this task cites from both the new Rationalization Defense row and the Advisor Escalation Policy paragraph

### Depended By
- `yw-000030-010-infra-async-monitoring-validation` — validates this edit's exact 502-line total alongside the other two consumer edits

## Key Files
- `claude-code/skills/ywc-sequential-executor/SKILL.md` — one new Rationalization Defense row, one inline-appended sentence, one blank-line removal

## Notes
- The FR5 append **must** extend the existing sentence at line 213 with no line break — appending it as a new line adds +1 on top of FR4's +1, which FR6's single-line trim cannot fully offset, breaching the ≤502-line cap even though `score.py`'s `body_lines <= 500` gate would still pass at the boundary.
- The FR6 trim is a pure whitespace removal with zero content loss — do not touch the sentence itself, only the blank line preceding it.
- Verify the final line count with `wc -l` after all three edits — it must read exactly 502, not merely "under some threshold."

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-sequential-executor/SKILL.md`

### Owned Interface
- (None — this task only adds a table row, an inline sentence, and removes a blank line in an existing skill body; no new public interface)

### Shared Surfaces
- (None identified) — `yw-000029-010` and `yw-000029-030` edit different SKILL.md files with no overlap.

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000028-010-docs-subagent-async-monitoring-contract`

### Task Verify
- `wc -l claude-code/skills/ywc-sequential-executor/SKILL.md` — expect exactly 502
- `rg -n "subagent-async-monitoring.md" claude-code/skills/ywc-sequential-executor/SKILL.md`
- `rg -n "fork a background agent" claude-code/skills/ywc-sequential-executor/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-sequential-executor --format json`

## Out of Scope
- Any edit to `claude-code/skills/ywc-parallel-executor/SKILL.md`, `claude-code/skills/ywc-impl-review/SKILL.md`, or `claude-code/skills/references/subagent-async-monitoring.md`.
- Any change to the existing 21 Rationalization Defense rows beyond appending the one new row.
