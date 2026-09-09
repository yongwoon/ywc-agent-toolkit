# yw-000029-030-domain-impl-review-monitor-citation

## Purpose
Wire `ywc-impl-review`'s two highest-concurrency fan-outs (Phase 1's 5-way subagent dispatch and Step 4.5's up-to-20-way verifier dispatch) to the shared async-monitoring contract for roster reconciliation.

## Scope
Append one citation sentence to the Phase 1 dispatch paragraph and one citation sentence to the Step 4.5 dispatch paragraph. No change to the Return Payload Contract text.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#functional-requirements` — FR7
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#acceptance-criteria` — AC4
- `claude-code/skills/ywc-impl-review/SKILL.md:73` — Phase 1 dispatch paragraph ("Use the Task tool to spawn five subagents in parallel...")
- `claude-code/skills/ywc-impl-review/SKILL.md:108` — Step 4.5 dispatch paragraph ("Independent Verification Pass...")
- `claude-code/skills/ywc-impl-review/SKILL.md:112` — Step 4.5's 20-finding verifier dispatch cap, the concrete evidence this is the highest-concurrency fan-out in the toolkit
- `claude-code/skills/ywc-impl-review/SKILL.md:84-94` — the existing Return Payload Contract text; unaffected by this task

### Summary
Phase 1 dispatches 5 concurrent subagents (Architecture/Design/Devex/Security/QA); Step 4.5 can dispatch up to 20 concurrent Sonnet verifier subagents — the highest-concurrency fan-out in this toolkit and the most exposed to the source incident's failure mode. Each of the two dispatch paragraphs gets one appended sentence citing `../references/subagent-async-monitoring.md` for roster reconciliation across the concurrent dispatch. This applies regardless of `--no-advisor` (that flag only skips Phase 2; both fan-outs still run).

### Out of Scope (from spec)
- The shared reference file's content — handled by `yw-000028-010-docs-subagent-async-monitoring-contract` (dependency)
- `ywc-parallel-executor` and `ywc-sequential-executor` edits — handled by `yw-000029-010` and `yw-000029-020` respectively
- Any rewrite of the Return Payload Contract text (`SKILL.md:84-94`) — this is a complementary citation, not a rewrite

## Criticality
normal — orchestration/documentation prose only; no auth, payment, crypto, PII, or external-input-handling code path.

## Dependencies

### Depends On
- `yw-000028-010-docs-subagent-async-monitoring-contract` — provides `claude-code/skills/references/subagent-async-monitoring.md`, which both citations point to

### Depended By
- `yw-000030-010-infra-async-monitoring-validation` — validates this edit alongside the other two consumer edits

## Key Files
- `claude-code/skills/ywc-impl-review/SKILL.md` — two appended citation sentences (Phase 1 paragraph, Step 4.5 paragraph)

## Notes
- The `--no-advisor` flag only skips Phase 2 — both the Phase 1 5-way fan-out and Step 4.5's verifier fan-out still run regardless, so both citations apply unconditionally (per the spec's Edge Cases).
- Do not touch the numbered list structure (`3.`, `4.`, `4.5.`, `5.`) or any other paragraph in Phase 1 or Step 4.5 beyond the single appended sentence in each.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-impl-review/SKILL.md`

### Owned Interface
- (None — this task only appends two citation sentences to an existing skill body; no new public interface)

### Shared Surfaces
- (None identified) — `yw-000029-010` and `yw-000029-020` edit different SKILL.md files with no overlap.

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000028-010-docs-subagent-async-monitoring-contract`

### Task Verify
- `rg -c "subagent-async-monitoring.md" claude-code/skills/ywc-impl-review/SKILL.md` — expect 2
- `rg -n "subagent-async-monitoring.md" claude-code/skills/ywc-impl-review/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-impl-review --format json`

## Out of Scope
- Any edit to `claude-code/skills/ywc-parallel-executor/SKILL.md`, `claude-code/skills/ywc-sequential-executor/SKILL.md`, or `claude-code/skills/references/subagent-async-monitoring.md`.
- Any change to the Return Payload Contract text (`SKILL.md:84-94`) or the Phase 2 Advisor Pass section.
