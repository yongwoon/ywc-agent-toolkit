# 000048-020-docs-infra-provider-packs

## Purpose

공용 infra reference의 provider pack을 추가합니다. AWS, GCP, Azure, Kubernetes provider 문서를 만들어 개별 skill이 provider 확정 후 한 문서만 읽는 Progressive Disclosure를 유지합니다.

## Scope

- `codex/skills/references/infra/providers/aws.md`
- `codex/skills/references/infra/providers/gcp.md`
- `codex/skills/references/infra/providers/azure.md`
- `codex/skills/references/infra/providers/k8s.md`
- `000048-010`에서 만든 core reference와 링크 관계 정렬

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-2-claude-전용-reference-구조를-codex-공용-reference-구조로-재배치한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#scope`
- `AGENTS.md` — shared Codex material 위치 규약

### Summary

provider pack은 각 skill이 모든 클라우드 문서를 한 번에 읽지 않도록 분리된 reference 세트입니다. core reference가 Terraform-only 전략과 lens taxonomy를 정의한 뒤, 이 task가 provider별 prior-art와 pitfalls를 정리합니다. 완료 후 skill task들은 provider 확정 후 정확히 한 provider 문서만 링크하면 됩니다.

### Out of Scope (from spec)

- lens / Terraform core 문서 — `000048-010-docs-infra-reference-core`
- skill-local provider notes 복제

## Criticality

normal

## Dependencies

### Depends On

- `000048-010-docs-infra-reference-core` — Terraform-only vocabulary와 lens terminology를 제공

### Depended By

- `000049-010-docs-iac-author-skill`
- `000049-020-docs-infra-design-skill`
- `000049-030-docs-infra-review-skill`
- `000049-040-docs-infra-optimize-skill`

## Key Files

- `codex/skills/references/infra/providers/aws.md`
- `codex/skills/references/infra/providers/gcp.md`
- `codex/skills/references/infra/providers/azure.md`
- `codex/skills/references/infra/providers/k8s.md`

## Notes

- 각 문서는 provider-specific concerns만 담고, 공통 lens taxonomy는 core docs를 링크합니다.
- Kubernetes는 Terraform provider 관점으로 서술하고 Helm general guide로 확장하지 않습니다.
- 이 task는 mid-plan validation spot-check를 포함해 늦은 rework를 줄입니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only shared reference authoring
- Targeted evidence: provider file-existence checks, vocabulary grep, mid-plan validator spot-check

### Interface Contract

- Contract: provider-specific references exist at stable paths and align with Terraform-only core docs.
- Inputs: core infra references from `000048-010`
- Outputs: four provider reference documents
- Error model: stale or mismatched paths break downstream relative links and skill body references
- Impacted tests: `bash scripts/validate.sh`

### Critical Surface Review

- Review requirement: provider scope drift나 non-Terraform tool mixing이 없는지 reviewer 확인

## Parallel Execution Metadata

### Ownership

- `codex/skills/references/infra/providers/aws.md`
- `codex/skills/references/infra/providers/gcp.md`
- `codex/skills/references/infra/providers/azure.md`
- `codex/skills/references/infra/providers/k8s.md`

### Shared Surfaces

- Shared infra terminology
- Shared reference path contract

### Conflicts With

- `000048-010-docs-infra-reference-core` — 같은 `codex/skills/references/infra/**` subtree와 shared terminology를 사용

### Parallelizable After

- `000048-010-docs-infra-reference-core`

### Task Verify

- `for f in codex/skills/references/infra/providers/aws.md codex/skills/references/infra/providers/gcp.md codex/skills/references/infra/providers/azure.md codex/skills/references/infra/providers/k8s.md; do test -f "$f"; done`
- `rg -n 'Terraform|provider|IAM|network|state|module|cluster|RBAC' codex/skills/references/infra/providers`
- `bash scripts/validate.sh`

## Out of Scope

- Core reference rewrites beyond link normalization
- Skill directories
