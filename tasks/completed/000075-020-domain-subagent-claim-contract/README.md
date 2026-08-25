# 000075-020-domain-subagent-claim-contract

## Purpose
Define bounded Claim/Evidence payloads and role-isolation rules for team orchestration.

## Scope
Extend the canonical subagent status action reference with optional Claims, evidence requirements, and independent/dependent role visibility.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-6-team-claimevidence-contract`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#e-executable-evaluation-matrix-and-release-scope`
### Summary
Claims are optional, capped at three, and each claim must cite a project-relative artifact or `file:line` evidence. Independent reviewers receive scope and artifacts without peer conclusions; dependent roles receive only claims and cited artifacts.
### Out of Scope (from spec)
- Team prompt-template implementation — handled by `000076-050-domain-team-claim-isolation`.
- Executor transition behavior — handled by `000076-030` and `000076-040`.

## Criticality
critical

## Dependencies
### Depends On
- (None — root task)
### Depended By
- `000076-030-domain-sequential-transition-safety` — shares canonical status routing semantics.
- `000076-040-domain-parallel-transition-safety` — shares worker evidence boundaries.
- `000076-050-domain-team-claim-isolation` — consumes the Claim/Evidence contract.

## Key Files
- `codex/skills/ywc-sequential-executor/references/subagent-status-actions.md` — canonical Claim/Evidence contract.

## Notes
Do not transmit transcript, chain-of-thought, peer conclusion, recommendation, or raw tool output as evidence.

## Hardening Evidence
### Test Feedback Path
- RED-first target: Claim-cap, missing-evidence, independent-isolation, and forbidden-field fixtures.
### Interface Contract
- Contract: optional `Claims` payload.
- Inputs: up to three claim objects with statement and cited evidence.
- Outputs: role-filtered status payload.
- Error model: bounded rejection for cap/evidence/privacy violations.
- Impacted tests: team/privacy evaluation fixtures.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: N/A — payload contract only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: privacy and role-isolation fixtures.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-sequential-executor/references/subagent-status-actions.md`
### Shared Surfaces
- Team prompt payloads and executor status routing.
### Conflicts With
- `000076-050-domain-team-claim-isolation` — consumes this contract and must not edit the canonical reference.
### Parallelizable After
- (Root task — no predecessor required)
### Task Verify
- `rg -n "Claims|claim|evidence|independent|dependent" codex/skills/ywc-sequential-executor/references/subagent-status-actions.md`
- `bash scripts/validate.sh`

## Out of Scope
- Prompt construction and role dispatch implementation.
