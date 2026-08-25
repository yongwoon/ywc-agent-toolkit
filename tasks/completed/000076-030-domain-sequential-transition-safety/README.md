# 000076-030-domain-sequential-transition-safety

## Purpose
Close sequential executor prompt branches and add checkpoint-first, atomic context handoff transitions.

## Scope
Implement non-interactive resume disposition, branch/worktree and CI wait/timeout terminal statuses, external URL profile validation, and sequential handoff recovery/writing.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-4-non-interactive-public-interface-and-preflight`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-5-context-handoff-wire-contract`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#c-non-interactive-inputs-and-handoff-validity`
### Summary
Sequential execution must never leave task transitions waiting for user progress or approval in non-interactive mode. Resume disposition and URL policy are validated before execution, while handoff is a lower-priority reconstruction cache written atomically after checkpoint/task state is authoritative.
### Out of Scope (from spec)
- Parallel worker aggregation — handled by `000076-040-domain-parallel-transition-safety`.
- Shared handoff schema definition — handled by `000075-010-domain-context-handoff-contract`.

## Criticality
critical

## Dependencies
### Depends On
- `000075-010-domain-context-handoff-contract` — provides handoff wire rules.
- `000075-020-domain-subagent-claim-contract` — provides status routing rules.
### Depended By
- `000077-010-test-context-safety-evaluation-matrix` — verifies sequential behavior.

## Key Files
- `codex/skills/ywc-sequential-executor/SKILL.md`, `README*.md`, `agents/openai.yaml`, `evals/evals.json`
- `codex/skills/ywc-sequential-executor/references/checkpoint-resume.md`
- `codex/skills/ywc-sequential-executor/references/external-url-policy.md`
- `codex/skills/ywc-sequential-executor/scripts/*.py`, `verify-transition.sh`

## Notes
Missing external URL profile is `NEEDS_CONTEXT`; do not create a new setting or prompt. Handoff never changes completion, cleanup, or worktree deletion.

## Hardening Evidence
### Test Feedback Path
- RED-first target: sequential prompt-closure and handoff recovery fixtures.
### Interface Contract
- Contract: sequential non-interactive transition and resume disposition.
- Inputs: authoritative checkpoint, current task source, optional handoff, validated URL profile.
- Outputs: bounded status and atomic handoff update.
- Error model: `NEEDS_CONTEXT` for missing/invalid disposition or URL profile; no prompt.
- Impacted tests: sequential executor fixtures.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: retryable command/API and atomic state replacement.
- Atomic / locking strategy: handoff temporary sibling + fsync + rename.
- Transaction boundary: checkpoint transition remains authoritative; handoff is cache-only.
- Idempotency guard: preserve checkpoint and prior valid handoff on failed write.
- Required tests: resume mismatch, failure injection, duplicate transition.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-sequential-executor/**`
### Shared Surfaces
- Checkpoint resume, status routing, shared handoff contract.
### Conflicts With
- `000076-040-domain-parallel-transition-safety` — both change executor transition semantics.
### Parallelizable After
- `000075-010-domain-context-handoff-contract`, `000075-020-domain-subagent-claim-contract`
### Task Verify
- `bash codex/skills/ywc-sequential-executor/scripts/verify-transition.sh`
- `bash scripts/validate.sh`

## Out of Scope
- Parallel executor implementation.
- Changes to checkpoint data model or task lifecycle ownership.
