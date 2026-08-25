# 000076-040-domain-parallel-transition-safety

## Purpose
Make parallel executor transitions non-interactive, checkpoint-first, and isolated to one root aggregate handoff.

## Scope
Implement aggregate handoff location/writing, worker isolation, resume/timeout/conflict closure, and fallback reconstruction.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-4-non-interactive-public-interface-and-preflight`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-5-context-handoff-wire-contract`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#d-context-handoff-schema-location-and-privacy-boundary`
### Summary
Parallel execution writes exactly one aggregate handoff beside root run state and never writes worker handoff files. Worker transitions must close prompt branches with bounded statuses and reconstruct from authoritative checkpoint/task state when the aggregate cache is invalid.
### Out of Scope (from spec)
- Sequential executor behavior — handled by `000076-030-domain-sequential-transition-safety`.
- Handoff schema definition — handled by `000075-010-domain-context-handoff-contract`.

## Criticality
critical

## Dependencies
### Depends On
- `000075-010-domain-context-handoff-contract` — provides aggregate handoff rules.
- `000075-020-domain-subagent-claim-contract` — provides worker evidence boundaries.
### Depended By
- `000077-010-test-context-safety-evaluation-matrix` — verifies parallel behavior.

## Key Files
- `codex/skills/ywc-parallel-executor/SKILL.md`, `README*.md`, `agents/openai.yaml`, `evals/evals.json`
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`
- `codex/skills/ywc-parallel-executor/scripts/*.py`

## Notes
Worker-local handoff authority is prohibited. Aggregate status must not contain peer conclusions or raw output.

## Hardening Evidence
### Test Feedback Path
- RED-first target: aggregate-location, worker-isolation, and prompt-closure fixtures.
### Interface Contract
- Contract: parallel aggregate handoff and terminal transition status.
- Inputs: root checkpoint/wave state and worker status evidence.
- Outputs: one aggregate handoff or bounded terminal status.
- Error model: discard/reconstruct malformed or mismatched handoff; no prompt in non-interactive mode.
- Impacted tests: parallel executor fixtures.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: shared mutable state / atomic state replacement.
- Atomic / locking strategy: aggregate temporary sibling + fsync + rename.
- Transaction boundary: aggregate handoff only; worker/run checkpoint remains authoritative.
- Idempotency guard: exactly one root aggregate destination and prior-valid preservation.
- Required tests: concurrent worker, malformed/stale handoff, write failure.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-parallel-executor/**`
### Shared Surfaces
- Root checkpoint/wave state and shared handoff contract.
### Conflicts With
- `000076-030-domain-sequential-transition-safety` — both alter executor transition semantics.
### Parallelizable After
- `000075-010-domain-context-handoff-contract`, `000075-020-domain-subagent-claim-contract`
### Task Verify
- `python3 codex/skills/ywc-parallel-executor/scripts/resume-state.py --help`
- `bash scripts/validate.sh`

## Out of Scope
- Sequential executor implementation.
- Worker task lifecycle or cleanup authority changes.
