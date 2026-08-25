# 000076-010-domain-producer-result-artifact-profile

## Purpose
Make `ywc-plan` and `ywc-spec-ready` emit strict, producer-specific Result blocks and enforce agentic-owned artifact paths.

## Scope
Implement the agentic artifact profile, mutually exclusive output behavior, exact Result schemas, path validation, and producer handoff documentation/evals.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-1-parseable-producer-result-block`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-2-agentic-owned-artifact-profile`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#b-result-block-schemas-and-consumer-routing`
### Summary
`ywc-plan` emits Scale plus Artifact; `ywc-spec-ready` emits Status plus Artifact. Only one exact success block is authoritative, and artifacts must be existing repository-relative Markdown files inside the declared root. Small artifacts use a date-prefixed `small_<slug>` name; Medium/Large candidates are finalized by spec-ready.
### Out of Scope (from spec)
- Agentic consumer routing — handled by `000076-020-domain-agentic-authority-preflight`.
- Focused evaluation matrix — handled by `000077-010-test-context-safety-evaluation-matrix`.

## Criticality
critical

## Dependencies
### Depends On
- `000075-010-domain-context-handoff-contract` — provides shared path/privacy validation conventions.
### Depended By
- `000076-020-domain-agentic-authority-preflight` — parses these producer results.
- `000077-010-test-context-safety-evaluation-matrix` — verifies producer behavior.

## Key Files
- `codex/skills/ywc-plan/SKILL.md`, `README*.md`, `agents/openai.yaml`, `evals/evals.json`
- `codex/skills/ywc-spec-ready/SKILL.md`, `README*.md`, `agents/openai.yaml`, `evals/evals.json`

## Notes
Direct calls without `--artifact-profile agentic` retain existing behavior. Terminal non-DONE statuses are not Result authorities.

## Hardening Evidence
### Test Feedback Path
- RED-first target: producer Result parser and artifact-root fixtures.
### Interface Contract
- Contract: producer-specific `## Result` blocks defined in the spec.
- Inputs: producer invocation and generated artifact.
- Outputs: exact labelled status/scale/artifact fields.
- Error model: parse/path failure becomes bounded `BLOCKED`; no fallback path.
- Impacted tests: plan/spec-ready focused eval fixtures.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: N/A — artifact contract and documentation behavior.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: duplicate/missing/out-of-root/non-Markdown cases.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-plan/**`
- `codex/skills/ywc-spec-ready/**`
### Shared Surfaces
- Result block schema and artifact roots.
### Conflicts With
- `000076-020-domain-agentic-authority-preflight` — consumer must follow this producer contract.
### Parallelizable After
- `000075-010-domain-context-handoff-contract`
### Task Verify
- `rg -n "artifact-profile|## Result|Scale:|Artifact:|repository-relative|small_" codex/skills/ywc-plan codex/skills/ywc-spec-ready`
- `bash scripts/validate.sh`

## Out of Scope
- Changes to Small code generation behavior.
- Executor and team prompt changes.
