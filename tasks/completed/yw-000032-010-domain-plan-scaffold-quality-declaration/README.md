# yw-000032-010-domain-plan-scaffold-quality-declaration

## Purpose
Make planning and project scaffolding explicitly carry an opt-in Quality Gate Contract or the exact no-contract sentinel.

## Scope
Update `ywc-plan`, its spec template/evals, and `ywc-project-scaffold` guidance/evals so declarations include state, thresholds, ownership, approved command identities/digests, and evidence requirements without inventing commands or project files.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-1-shared-contract-and-planning-declaration`
- `codex/skills/references/quality-gates.md`
### Summary
Planner output must declare a complete bounded contract or exact `N/A — no quality gate contract`. Scaffold may seed advisory metadata only when requested and must never infer executable commands. Both skills preserve the current behavior when no contract is declared.
### Out of Scope (from spec)
- Task metadata propagation — `yw-000032-020-domain-task-quality-gate-packet`.
- Executor dispatch, worker implementation, and review evidence — Phase `yw-000033`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000031-010-docs-quality-gate-contract` — provides canonical states and packet semantics.
### Depended By
- `yw-000032-020-domain-task-quality-gate-packet` — consumes producer declaration rules.
- `yw-000034-010-infra-quality-gate-distribution-validation` — validates affected skill surfaces.

## Key Files
- `codex/skills/ywc-plan/SKILL.md`
- `codex/skills/ywc-plan/references/spec-template.md`
- `codex/skills/ywc-plan/evals/evals.json`
- `codex/skills/ywc-project-scaffold/SKILL.md`
- `codex/skills/ywc-project-scaffold/evals/evals.json`

## Notes
Keep Codex frontmatter unchanged and do not add any Claude Code counterpart.

## Hardening Evidence
### Test Feedback Path
- RED-first target: affected skill contract evals in each `evals/evals.json`.
### Interface Contract
- Contract: planner/scaffold declaration → task-generator packet
- Owner task: this task
- Canonical signature: declaration or exact N/A sentinel → bounded state/threshold/identity metadata
- Consumers: `yw-000032-020-domain-task-quality-gate-packet`
- Implementation opacity: consumers do not infer missing fields.
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: `ywc-impl-review` via final validation.
### Data Integrity Hardening
- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-plan/**`
- `codex/skills/ywc-project-scaffold/**`
### Shared Surfaces
- `codex/skills/references/quality-gates.md` — read-only shared contract.
### Conflicts With
- (None identified)
### Parallelizable After
- `yw-000031-010-docs-quality-gate-contract`
### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `rg -n "Quality Gate Contract|N/A — no quality gate contract|approved.*digest|do not invent" codex/skills/ywc-plan codex/skills/ywc-project-scaffold`

## Out of Scope
Task-generator packet format, worker agents, executor gates, implementation-review behavior, and generated package sync.
