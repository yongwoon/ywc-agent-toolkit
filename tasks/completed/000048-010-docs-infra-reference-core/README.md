# 000048-010-docs-infra-reference-core

## Purpose

Codex 공용 infra reference의 핵심 뼈대를 먼저 만듭니다. Terraform-only 전략과 review lens 핵심 문서를 먼저 고정해 이후 skill들이 같은 용어와 링크 경로를 공유하도록 만듭니다.

## Scope

- `codex/skills/references/infra/iac/terraform.md`
- `codex/skills/references/infra/lenses/security.md`
- `codex/skills/references/infra/lenses/cost.md`
- `codex/skills/references/infra/lenses/reliability.md`

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-2-claude-전용-reference-구조를-codex-공용-reference-구조로-재배치한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#iteration-1-amendments` — v1 범위 고정
- `AGENTS.md` — shared Codex material 위치 규약

### Summary

공용 reference는 skill별 복제를 막기 위한 중앙 자산입니다. 이 task는 Terraform-only 전략과 security/cost/reliability lens의 공통 판단 프레임을 먼저 기록합니다. provider-specific 문서는 다음 task에서 추가하고, 본 task의 결과를 기준 vocabulary로 사용합니다.

### Out of Scope (from spec)

- provider별 상세 문서 — `000048-020-docs-infra-provider-packs`
- 개별 skill 본문 작성 — `000049-*`

## Criticality

normal

## Dependencies

### Depends On

- `000047-010-infra-cloud-engineer-specialist` — reliability / provider advisory role wording과 정렬
- `000047-020-infra-agent-lens-extensions` — security/cost lens wording과 정렬

### Depended By

- `000048-020-docs-infra-provider-packs` — provider pack 용어를 본 task의 core reference에 맞춤
- `000049-010-docs-iac-author-skill` — Terraform-only 공통 링크 사용
- `000049-020-docs-infra-design-skill` — lens link와 terminology 사용
- `000049-030-docs-infra-review-skill` — security/cost/reliability lens link와 routing 사용
- `000049-040-docs-infra-optimize-skill` — lens link와 Terraform-only wording 사용

## Key Files

- `codex/skills/references/infra/iac/terraform.md`
- `codex/skills/references/infra/lenses/security.md`
- `codex/skills/references/infra/lenses/cost.md`
- `codex/skills/references/infra/lenses/reliability.md`

## Notes

- provider specifics를 섞지 말고 각 문서의 역할을 분리합니다.
- `terraform validate`와 `terraform plan`은 author/review/optimize skill들이 공통으로 참조할 수 있는 baseline command로 정리합니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only shared reference authoring
- Targeted evidence: file-existence checks, terminology grep, repository validation spot-check

### Interface Contract

- Contract: shared infra references exist at stable project-relative paths and Codex skills can link them directly.
- Inputs: port spec, existing agent wording
- Outputs: four core reference documents
- Error model: missing files or stale link paths break downstream skill references and validator checks
- Impacted tests: `bash scripts/validate.sh` reference-path validation

### Critical Surface Review

- Review requirement: Terraform-only wording과 lens boundaries가 spec과 어긋나지 않는지 reviewer 확인

## Parallel Execution Metadata

### Ownership

- `codex/skills/references/infra/iac/terraform.md`
- `codex/skills/references/infra/lenses/security.md`
- `codex/skills/references/infra/lenses/cost.md`
- `codex/skills/references/infra/lenses/reliability.md`

### Shared Surfaces

- Shared infra terminology
- Shared reference path contract

### Conflicts With

- `000048-020-docs-infra-provider-packs` — 같은 `codex/skills/references/infra/**` subtree와 terminology를 공유

### Parallelizable After

- `000047-010-infra-cloud-engineer-specialist`
- `000047-020-infra-agent-lens-extensions`

### Task Verify

- `for f in codex/skills/references/infra/iac/terraform.md codex/skills/references/infra/lenses/security.md codex/skills/references/infra/lenses/cost.md codex/skills/references/infra/lenses/reliability.md; do test -f \"$f\"; done`
- `rg -n 'Terraform|terraform validate|terraform plan|security|cost|reliability' codex/skills/references/infra`
- `bash scripts/validate.sh`

## Out of Scope

- Provider-specific docs
- Skill-local copies of these references
