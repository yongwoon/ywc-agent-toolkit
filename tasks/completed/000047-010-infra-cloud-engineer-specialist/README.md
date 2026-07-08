# 000047-010-infra-cloud-engineer-specialist

## Purpose

Codex 전용 read-only specialist agent `ywc-cloud-engineer`를 추가합니다. 이 task는 Terraform feasibility, provider-specific advisory, blast-radius sanity check, reliability review를 담당하는 bounded agent surface를 먼저 고정해 이후 skill dispatch가 안정된 이름과 계약을 참조하게 만듭니다.

## Scope

- `codex/agents/ywc-cloud-engineer.toml` 신규 작성
- Codex agent output contract와 `sandbox_mode = "read-only"` 준수
- Terraform-only / Codex-only / advisory-only 경계 명시

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#iteration-1-amendments` — write-enabled worker 대신 read-only specialist agent로 범위를 수정한 기준
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-3-ywc-cloud-engineer-custom-agent를-codex-worker로-추가한다` — 신규 cloud engineer 역할 범위
- `AGENTS.md` — Codex custom agent 위치와 bundle 규약
- `CLAUDE.md` — Codex custom agent output contract와 read-only 원칙

### Summary

이번 포트의 cloud engineer는 v1에서 파일을 직접 수정하는 worker가 아니라 read-only specialist입니다. agent는 Terraform feasibility, provider advisory, reliability review, blast-radius sanity check를 담당하고, 실제 파일 작성은 상위 Codex 세션의 skill execution이 수행합니다. 이후 `ywc-iac-author`, `ywc-infra-review`, `ywc-infra-optimize`는 이 이름과 역할 경계를 그대로 참조합니다.

### Out of Scope (from spec)

- 실제 Terraform/IaC 파일 작성
- `claude-code/**` parity 작업
- security/performance specialist 확장 작업 — `000047-020-infra-agent-lens-extensions`

## Criticality

normal

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000049-010-docs-iac-author-skill` — Terraform advisory / feasibility fan-out target를 사용
- `000049-030-docs-infra-review-skill` — reliability lens와 provider advisory dispatch를 사용
- `000049-040-docs-infra-optimize-skill` — optimization planning 시 conservative advisory target를 사용

## Key Files

- `codex/agents/ywc-cloud-engineer.toml` — 신규 specialist agent 정의

## Notes

- 기존 Codex agent와 동일하게 `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` 형식을 사용합니다.
- `Next action:` 라인을 포함해 상위 skill이 후속 행동을 결정할 수 있게 합니다.
- Terraform-only 전략이므로 Pulumi, Bicep, CDK, CloudFormation authoring을 포괄하는 표현을 피합니다.

## Hardening Evidence

### Test Feedback Path

- Existing coverage: `bash scripts/validate.sh`
- Targeted evidence: agent definition grep and file-existence checks

### Interface Contract

- Contract: `ywc-cloud-engineer`는 read-only Codex specialist agent다.
- Inputs: bounded spec/code/context packet from infra skills
- Outputs: status line, concise findings or advisory summary, `Next action:`
- Error model: scope mismatch, missing provider context, or write-required requests는 `NEEDS_CONTEXT` 또는 boundary reminder로 반환
- Impacted tests: repository validator for Codex agent TOML shape

### Critical Surface Review

- Review requirement: read-only custom agent이므로 `sandbox_mode`와 mission boundary를 reviewer가 확인해야 함

## Parallel Execution Metadata

### Ownership

- `codex/agents/ywc-cloud-engineer.toml`

### Shared Surfaces

- Codex custom agent catalog
- Infra skill dispatch names

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `test -f codex/agents/ywc-cloud-engineer.toml`
- `rg -n 'sandbox_mode = "read-only"|Next action:|Terraform|blast-radius|reliability' codex/agents/ywc-cloud-engineer.toml`
- `bash scripts/validate.sh`

## Out of Scope

- Skill directories under `codex/skills/**`
- Generated plugin mirror
