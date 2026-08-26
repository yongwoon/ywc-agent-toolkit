# 000076-050-domain-team-claim-isolation

## Purpose
Apply the Claim/Evidence contract to team assembly prompts and enforce independent/dependent role isolation.

## Scope
Update team prompt templates, role payload construction, claim caps, cited-artifact filtering, and privacy behavior.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-6-team-claimevidence-contract`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#e-executable-evaluation-matrix-and-release-scope`
### Summary
Team assembly must pass included scope, excluded scope, artifact list, and bounded Claims only. Independent reviewers cannot receive peer claims, conclusions, or recommendations; dependent roles may receive Claims and cited artifacts but no transcript or raw output.
### Out of Scope (from spec)
- Canonical Claim contract — handled by `000075-020-domain-subagent-claim-contract`.
- Executor status routing — handled by `000076-030` and `000076-040`.

## Criticality
critical

## Dependencies
### Depends On
- `000075-020-domain-subagent-claim-contract` — provides canonical Claim/Evidence rules.
### Depended By
- `000077-010-test-context-safety-evaluation-matrix` — verifies team/privacy behavior.

## Key Files
- `codex/skills/ywc-team-assemble/SKILL.md`, `README*.md`, `agents/openai.yaml`, `evals/evals.json`
- `codex/skills/ywc-team-assemble/references/prompt-templates.md`

## Notes
The canonical reference remains owned by `000075-020`; this task only consumes it.

## Hardening Evidence
### Test Feedback Path
- RED-first target: independent/dependent payload isolation and three-Claim-cap fixtures.
### Interface Contract
- Contract: role-specific team prompt payload.
- Inputs: scope, exclusions, artifact paths, validated claims.
- Outputs: filtered reviewer/dependent prompt context.
- Error model: reject over-cap or uncited/private fields.
- Impacted tests: team/privacy evaluation fixtures.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: N/A — payload filtering only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: role-isolation and forbidden-field rejection.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-team-assemble/**`
### Shared Surfaces
- Canonical Claim/Evidence contract and reviewer prompt context.
### Conflicts With
- `000075-020-domain-subagent-claim-contract` — reads the contract; must not edit its file.
### Parallelizable After
- `000075-020-domain-subagent-claim-contract`
### Task Verify
- `rg -n "Claims|included scope|excluded scope|independent|dependent|recommendation" codex/skills/ywc-team-assemble`
- `bash scripts/validate.sh`

## Out of Scope
- Changes to executor status-action reference.
- Changes to checkpoint or handoff schemas.
