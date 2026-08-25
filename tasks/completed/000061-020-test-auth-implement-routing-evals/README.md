# 000061-020-test-auth-implement-routing-evals

## Purpose

`ywc-auth-implement`의 routing과 safety rejection을 deterministic eval fixture로 고정한다.

## Scope

- five required scenarios와 `expected_behavior`/`anti_behavior` arrays를 포함한 eval JSON을 작성한다.
- existing-auth, unknown-stack, direct-crypto, audit failure 경로가 skill contract와 일치하는지 검증한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex_auth_implement_skill.md#acceptance-criteria` — AC9 evidence fields
- `docs/ywc-plans/codex_auth_implement_skill.md#fr-2-rationalization-defense` — rejection evidence requirement
- `docs/ywc-plans/codex_auth_implement_skill.md#fr-7-security-e2e-and-pr-gates` — Critical/High stop transitions

### Summary

Fixture는 application code를 실행하지 않고 instruction-level routing regression을 잡는다. final `SKILL.md`의 terms를 기준으로 happy path와 네 가지 safety behavior를 명시한다. `rationalization-evidence.md`는 이 task에서 수정하지 않는다.

### Out of Scope (from spec)

- skill/reference authoring — `000061-010-domain-auth-implement-skill`
- plugin sync와 full repository validation — `000062-010-infra-auth-implement-distribution-validation`

## Dependencies

### Depends On

- `000061-010-domain-auth-implement-skill` — final command, status, safety language

### Depended By

- `000062-010-infra-auth-implement-distribution-validation` — valid eval JSON and contract-runner evidence

## Key Files

- `codex/skills/ywc-auth-implement/evals/evals.json` — routing regression fixtures

## Notes

- fixture, prompt, expected behavior 어디에도 real secret, access token, credential를 넣지 않는다.
- `references/rationalization-evidence.md`는 read-only input이며 `000061-010`의 ownership이다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `codex/skills/ywc-auth-implement/evals/evals.json`
- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh`

### Interface Contract

- Contract: eval JSON schema
- Inputs: numeric `id`, non-empty `prompt`, behavior arrays
- Outputs: runner-validated fixture set
- Error model: JSON/schema failure exits nonzero
- Impacted tests: `scripts/run-codex-skill-contract-evals.sh`

### Critical Surface Review

- Review requirement: manual full implementation review — fixtures enforce auth safety routing

### Data Integrity Hardening

- Trigger surface: N/A — static test fixture
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

`codex/skills/ywc-auth-implement/evals/**` only.

### Shared Surfaces

`SKILL.md` routing/status vocabulary and repository-wide contract-eval JSON schema.

### Conflicts With

`000061-010-domain-auth-implement-skill` before its merge; otherwise `(None identified)`.

### Parallelizable After

`000061-010-domain-auth-implement-skill` merged.

### Task Verify

- `python3 -m json.tool codex/skills/ywc-auth-implement/evals/evals.json >/dev/null`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

Changing the skill body, metadata, references, catalogs, or generated plugin package.
