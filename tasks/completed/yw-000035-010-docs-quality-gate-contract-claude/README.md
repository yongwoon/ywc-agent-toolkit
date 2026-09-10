# yw-000035-010-docs-quality-gate-contract-claude

## Purpose
Create the canonical claude-code-side Quality Gate Contract shared reference so every downstream claude-code skill (`ywc-plan`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-impl-review`) can link one authoritative document instead of restating CRAP/Mutation gate rules inline.

## Scope
Author `claude-code/skills/references/quality-gates.md`, adapted from `develop-with-llm`'s canonical claude-code-side version: gate role split (Cleaner = CRAP/complexity, Hardener = Mutation/test-effectiveness), CRAP threshold 6–8 and Mutation threshold ≥90% with rationale, the diff-only principle (never full-codebase retroactive), the 3-round Mutation loop cap, the equivalent-mutant policy (forwarded to review, never adjudicated by executor/agent), the contract-absent fallback (`N/A — no quality gate contract`), the `Baseline` artifact convention (a per-adopting-project file, never written by this toolkit), and the `gate_state` sentinel vocabulary (`"not run — tool unavailable"`, `"not run — dispatch failed"`, etc.).

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-1-shared-quality-gatesmd-reference--both-roots-deliberately-divergent-content` — FR-1 (claude-code half only; the codex half is out of this task's scope, already delivered by the separate `yw-000031-010-docs-quality-gate-contract` codex-side task)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#acceptance-criteria` — AC1

### Summary
This is the foundational document for the claude-code-side port. Per the spec's Edge Cases "Partial-port interruption" note, this task must land before `yw-000035-060`, `yw-000035-070`, and `yw-000035-080`, each of which inserts an `> **Action required**: Read [../../references/quality-gates.md]` pointer to this file. Content is adapted from `develop-with-llm`'s canonical English-language version, not translated from the already-existing codex `quality-gates.md` (the two contracts are structurally different — see the port spec's FR-1).

### Out of Scope (from spec)
- Codex-side `quality-gates.md` — already delivered by `yw-000031-010-docs-quality-gate-contract` (a prior, separately-scoped codex-only batch).
- Inserting the pointer into any consuming SKILL.md — handled by `yw-000035-020`, `yw-000035-060`, `yw-000035-070`, `yw-000035-080`.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000035-060-domain-sequential-executor-quality-gate` — links this file from the new `quality-gate-steps.md` reference.
- `yw-000035-070-domain-parallel-executor-quality-gate` — links this file from the new parallel-executor gate procedure.
- `yw-000035-080-domain-impl-review-quality-evidence` — links this file for the QA subagent / Confidence Gate clauses' contract-presence check.

## Key Files
- `claude-code/skills/references/quality-gates.md` — new shared reference (create).

## Notes
Do not restate this file's thresholds inline in any consuming SKILL.md — every consumer links it via an `> **Action required**: Read [...]` pointer, matching the existing convention used by `pr-bot-polling.md` and `subagent-async-monitoring.md` in `claude-code/skills/CLAUDE.md`. This task creates zero new skill directories, so no new README locale set is required (per the port spec's Global Constraints).

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/references/quality-gates.md`

### Owned Interface
(None — no public interface owned; this is a documentation-only reference file, not a code module with a signature other tasks call.)

### Shared Surfaces
- (None identified — this file does not exist yet, so no other in-flight task reads or writes it until this task creates it.)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `test -f claude-code/skills/references/quality-gates.md`
- `grep -q "CRAP" claude-code/skills/references/quality-gates.md && grep -q "Mutation" claude-code/skills/references/quality-gates.md`
- `grep -q "gate_state" claude-code/skills/references/quality-gates.md`
- `bash scripts/validate.sh`

## Out of Scope
- Any change to `codex/skills/references/quality-gates.md` (already exists via the prior codex batch).
- Any SKILL.md insertion — this task produces only the reference document.
