# 000076-020-domain-agentic-authority-preflight

## Purpose
Make `ywc-agentic` route only verified producer artifacts and close every required non-interactive input branch.

## Scope
Implement paired Result consumption, Small versus Medium/Large routing, deterministic preflight, status propagation, and no-guessed-path behavior.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-3-one-authority-orchestration-flow`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-4-non-interactive-public-interface-and-preflight`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#c-non-interactive-inputs-and-handoff-validity`
### Summary
Small routes the verified planner artifact directly to code generation. Medium/Large route only a DONE spec-ready artifact to task generation, re-plan, and evaluation. Agentic validates every required input immediately before each callee and returns `NEEDS_CONTEXT` or `BLOCKED` without prompting or invoking downstream work when evidence is missing or invalid.
### Out of Scope (from spec)
- Producer implementation — handled by `000076-010-domain-producer-result-artifact-profile`.
- Executor internals — handled by `000076-030` and `000076-040`.

## Criticality
critical

## Dependencies
### Depends On
- `000076-010-domain-producer-result-artifact-profile` — defines producer Result schemas and artifact roots.
### Depended By
- `000077-010-test-context-safety-evaluation-matrix` — verifies orchestration and preflight.

## Key Files
- `codex/skills/ywc-agentic/SKILL.md`, `README*.md`, `agents/openai.yaml`, `evals/evals.json`

## Notes
Invocation packets must carry resolved artifact values. Logs are not an authority and must not store producer responses or raw tool output.

## Hardening Evidence
### Test Feedback Path
- RED-first target: paired Result routing and missing-input preflight fixtures.
### Interface Contract
- Contract: `ywc-agentic --non-interactive` forwarding arguments and terminal statuses.
- Inputs: verified Scale/Artifact, mode/lang/suggestions/resume dispositions as applicable.
- Outputs: downstream invocation packet or bounded terminal status.
- Error model: `BLOCKED` for invalid producer results; `NEEDS_CONTEXT` for missing deterministic inputs.
- Impacted tests: agentic routing/preflight fixtures.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: duplicate-sensitive orchestration dispatch.
- Atomic / locking strategy: N/A — validate-before-dispatch.
- Transaction boundary: one callee dispatch decision.
- Idempotency guard: no downstream call on failed preflight.
- Required tests: downstream-call count assertions.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-agentic/**`
### Shared Surfaces
- Producer Result contract; task-generator and executor invocation packets.
### Conflicts With
- `000076-010-domain-producer-result-artifact-profile` — reads its contract; do not modify its files.
### Parallelizable After
- `000076-010-domain-producer-result-artifact-profile`
### Task Verify
- `rg -n "artifact-profile agentic|NEEDS_CONTEXT|BLOCKED|Scale|Artifact|suggestions|resume-disposition" codex/skills/ywc-agentic`
- `bash scripts/validate.sh`

## Out of Scope
- Changes to producer Result emission.
- Changes to executor checkpoint storage.
