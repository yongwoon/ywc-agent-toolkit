# 000077-010-test-context-safety-evaluation-matrix

## Purpose
Add executable focused evaluation coverage for the complete context-safety contract.

## Scope
Cover producer Result parsing, artifact authority, agentic preflight, suggestion closure, executor prompt closure, handoff recovery, team isolation, Claim limits, and privacy rejection across affected skill eval suites.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#e-executable-evaluation-matrix-and-release-scope`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#ac9-regression-evidence`
### Summary
Each case must declare input, expected terminal status, expected downstream-call count, and handoff acceptance/rejection. The matrix must reject malformed, duplicate, out-of-root, stale, mismatched, guessed-path, prompt-leaking, and privacy-violating inputs.
### Out of Scope (from spec)
- Production skill behavior — completed by the Phase `000076` tasks.
- Final bundle metadata and release validation — handled by `000077-020-infra-distribution-validation`.

## Criticality
critical

## Dependencies
### Depends On
- `000076-010-domain-producer-result-artifact-profile` — producer contract.
- `000076-020-domain-agentic-authority-preflight` — agentic routing/preflight.
- `000076-030-domain-sequential-transition-safety` — sequential closure.
- `000076-040-domain-parallel-transition-safety` — parallel closure.
- `000076-050-domain-team-claim-isolation` — team privacy contract.
### Depended By
- `000077-020-infra-distribution-validation` — consumes the complete fixture/eval inventory.

## Key Files
- `codex/skills/ywc-agentic/evals/evals.json`
- `codex/skills/ywc-plan/evals/evals.json`
- `codex/skills/ywc-spec-ready/evals/evals.json`
- `codex/skills/ywc-sequential-executor/evals/evals.json`
- `codex/skills/ywc-parallel-executor/evals/evals.json`
- `codex/skills/ywc-team-assemble/evals/evals.json`
- Other affected eval files only when the case directly belongs to that skill.

## Notes
Use shared fixtures under `codex/skills/references/` only when cases cite them and no skill-specific ownership is obscured.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh` plus each affected `evals/evals.json`.
### Interface Contract
- Contract: focused eval case schema with input/status/downstream-call/handoff assertions.
- Inputs: valid and invalid producer, preflight, checkpoint, role payload, and handoff fixtures.
- Outputs: deterministic expected status and call count.
- Error model: explicit `BLOCKED`/`NEEDS_CONTEXT`/accepted handoff outcome.
- Impacted tests: all affected eval suites.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: N/A — test fixtures and eval metadata.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: failure-injection and duplicate-call assertions.

## Parallel Execution Metadata
### Ownership
- `codex/skills/*/evals/evals.json` for the affected eight skills only.
### Shared Surfaces
- Global eval schema, status names, downstream-call counts, and fixture conventions.
### Conflicts With
- `000077-020-infra-distribution-validation` — validation must consume the final eval inventory.
### Parallelizable After
- All Phase `000076` tasks.
### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/validate.sh`

## Out of Scope
- Changing production skill instructions.
- Updating generated plugin output or release metadata.
