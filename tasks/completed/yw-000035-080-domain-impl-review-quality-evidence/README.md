# yw-000035-080-domain-impl-review-quality-evidence

## Purpose
Teach the claude-code `ywc-impl-review` QA subagent and Confidence Gate to consume Quality Gate Contract evidence correctly: a surviving mutant as required evidence for a P1 Testing finding, and a bounded Evidence-quality score cap only when a gate genuinely failed to run against an existing contract.

## Scope
Append two clauses to `claude-code/skills/ywc-impl-review/SKILL.md` only: one to the QA subagent's description, one to the Confidence Gate's Evidence-quality dimension bullet.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-5-ywc-impl-review--qa-subagent-and-confidence-gate-evidence-requirements` — FR-5 (claude-code half only; codex half already delivered by `yw-000033-030-domain-review-quality-evidence`)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#acceptance-criteria` — AC10, AC11
- `claude-code/skills/references/quality-gates.md` (created by `yw-000035-010`) — canonical `gate_state` vocabulary this task's clauses reference

### Summary
QA subagent clause: when the task's Quality Gate Contract ran a Mutation gate, a surviving mutant is required evidence for a P1 Testing finding; absence of a contract or a 0-survivor result must not itself license unsupported subjective Testing criticism, but must also not force additional criticism where none is warranted. Confidence Gate clause: the Evidence-quality score cap applies only when a contract exists **and** `gate_state` shows the gate did not run (`"not run — tool unavailable"` / `"not run — dispatch failed"`) — never when the contract itself is absent, so a gate-less project is never permanently held below the REVIEW band. Both clauses must preserve the `N/A — no quality gate contract` fallback per AC11.

### Out of Scope (from spec)
- The codex `ywc-impl-review` / `qa-agent.md` equivalent — already delivered by `yw-000033-030-domain-review-quality-evidence`.
- `ywc-sequential-executor` and `ywc-parallel-executor` insertions — `yw-000035-060` and `yw-000035-070`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000035-010-docs-quality-gate-contract-claude` — provides `claude-code/skills/references/quality-gates.md`, which the `gate_state` vocabulary referenced by the Confidence Gate clause is defined in.

### Depended By
- (None identified)

## Key Files
- `claude-code/skills/ywc-impl-review/SKILL.md` — append two clauses (QA subagent description paragraph; Confidence Gate Evidence-quality bullet).

## Notes
Both clauses are additive appends to existing prose — do not restructure the QA subagent description or the Confidence Gate's dimension list beyond the two required additions.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-impl-review/SKILL.md`

### Owned Interface
(None — no public interface owned.)

### Shared Surfaces
- `claude-code/skills/references/quality-gates.md` — read-only reference; not modified by this task.

### Conflicts With
- (None identified — `yw-000035-060` and `yw-000035-070` edit different skill directories)

### Parallelizable After
- `yw-000035-010-docs-quality-gate-contract-claude`

### Task Verify
- `grep -n "surviving mutant" claude-code/skills/ywc-impl-review/SKILL.md`
- `grep -n "gate_state" claude-code/skills/ywc-impl-review/SKILL.md`
- `grep -q "N/A — no quality gate contract" claude-code/skills/ywc-impl-review/SKILL.md`
- `bash scripts/validate.sh`

## Out of Scope
- Any codex-side `ywc-impl-review` change.
- Any change to the Confidence Gate's other required dimension (`Root cause identified`).
