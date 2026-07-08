# 000047-020-infra-agent-lens-extensions

## Purpose

기존 Codex specialist agent 두 개를 infra-review 흐름에 맞게 확장합니다. `ywc-security-engineer`는 IaC misconfiguration / IAM-RBAC over-privilege / public exposure / secrets-in-state 문맥을, `ywc-performance-engineer`는 cost / right-sizing / idle resource / transfer cost 문맥을 수용하도록 description과 developer instructions를 보강합니다.

## Scope

- `codex/agents/ywc-security-engineer.toml`
- `codex/agents/ywc-performance-engineer.toml`
- infra-review routing에서 필요한 bounded wording 추가

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-4-기존-specialist-agent를-infra-review-흐름에-맞게-확장한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#scope`
- `CLAUDE.md` — Codex custom agent output contract와 read-only 원칙

### Summary

infra-review는 security, cost, reliability 세 렌즈를 fan-out해야 하므로 기존 두 specialist가 infra use case를 인식할 수 있어야 합니다. 이 task는 새 agent를 만들지 않고 기존 security/performance specialists의 description과 bounded instructions만 넓혀서 routeable surface를 만듭니다. reliability는 `ywc-cloud-engineer`가 담당하므로 여기서는 그 경계를 침범하지 않습니다.

### Out of Scope (from spec)

- 신규 security/performance agent 생성
- `ywc-infra-review` skill 본문 작성 — `000049-030-docs-infra-review-skill`
- reliability lens 정의 — `000047-010-infra-cloud-engineer-specialist`

## Criticality

critical — 보안 및 비용 판단 경계를 바꾸는 agent contract이므로 wording drift를 엄격히 검토해야 함

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000049-030-docs-infra-review-skill` — security / cost dispatch target를 사용

## Key Files

- `codex/agents/ywc-security-engineer.toml`
- `codex/agents/ywc-performance-engineer.toml`

## Notes

- 기존 app-security / app-performance 용도를 약화시키지 않도록 append-only 성격으로 보강합니다.
- severity 기준, output shape, read-only property는 유지합니다.

## Hardening Evidence

### Test Feedback Path

- Existing coverage: `bash scripts/validate.sh`
- Targeted evidence: infra lens wording grep

### Interface Contract

- Contract: 기존 specialist가 infra review 요청을 scope-correct하게 받을 수 있다.
- Inputs: bounded diff, file set, spec excerpt, IaC snippet
- Outputs: 기존 status/summary/findings 형식 유지
- Error model: runtime metric 또는 trust-boundary evidence 부족 시 기존 `NEEDS_CONTEXT`/`BLOCKED` semantics 유지
- Impacted tests: repository validator for Codex agent TOML shape

### Critical Surface Review

- Review requirement: security/performance scope 확장 wording이 기존 routing을 훼손하지 않는지 reviewer 확인 필요

## Parallel Execution Metadata

### Ownership

- `codex/agents/ywc-security-engineer.toml`
- `codex/agents/ywc-performance-engineer.toml`

### Shared Surfaces

- Codex specialist agent routing vocabulary
- Infra review dispatch names

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `rg -n 'IaC|IAM|RBAC|public exposure|secrets-in-state' codex/agents/ywc-security-engineer.toml`
- `rg -n 'cost|right-sizing|idle resource|transfer cost|FinOps' codex/agents/ywc-performance-engineer.toml`
- `bash scripts/validate.sh`

## Out of Scope

- New agent files
- Skill directories
- Generated plugin mirror
