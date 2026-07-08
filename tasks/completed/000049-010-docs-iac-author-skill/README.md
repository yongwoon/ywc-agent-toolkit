# 000049-010-docs-iac-author-skill

## Purpose

Codex `ywc-iac-author` skill을 작성합니다. 설계 입력을 받아 Terraform 코드 authoring workflow, `terraform validate` / `terraform plan` 확인, blast-radius summary, `ywc-cloud-engineer` advisory fan-out를 수행하는 skill surface를 Codex bundle 규약에 맞게 추가합니다.

## Scope

- `codex/skills/ywc-iac-author/SKILL.md`
- `codex/skills/ywc-iac-author/agents/openai.yaml`
- `codex/skills/ywc-iac-author/README.md`
- `codex/skills/ywc-iac-author/README.en.md`
- `codex/skills/ywc-iac-author/README.ja.md`
- `codex/skills/ywc-iac-author/README.ko.md`

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-1-codex용-infra-taxonomy를-신규-skill-4종으로-포트한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-5-각-skill에-codex용-ui-metadata와-locale-readme를-추가한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-6-신규-skill-간-dispatch-경계와-anti-trigger를-codex-스타일로-명시한다`
- `AGENTS.md` — Codex skill file-set requirements

### Summary

`ywc-iac-author`는 이번 배치의 Terraform authoring entry point입니다. skill은 Terraform-only 전략, provider reference Progressive Disclosure, `ywc-cloud-engineer` advisory handoff, post-author review recommendation을 함께 문서화해야 합니다. Tier 1 README 4종과 `agents/openai.yaml`까지 포함해 Codex installable surface를 완성합니다.

### Out of Scope (from spec)

- provider/core shared reference authoring — `000048-010`, `000048-020`
- plugin sync와 repository-wide validation — `000050-010-infra-codex-plugin-sync-validate`

## Criticality

normal

## Dependencies

### Depends On

- `000047-010-infra-cloud-engineer-specialist` — advisory fan-out target 제공
- `000048-010-docs-infra-reference-core` — Terraform-only reference baseline 제공
- `000048-020-docs-infra-provider-packs` — provider-specific reference baseline 제공

### Depended By

- `000050-010-infra-codex-plugin-sync-validate` — generated package sync와 validation 수행

## Key Files

- `codex/skills/ywc-iac-author/SKILL.md`
- `codex/skills/ywc-iac-author/agents/openai.yaml`
- `codex/skills/ywc-iac-author/README.md`
- `codex/skills/ywc-iac-author/README.en.md`
- `codex/skills/ywc-iac-author/README.ja.md`
- `codex/skills/ywc-iac-author/README.ko.md`

## Notes

- Codex `SKILL.md` frontmatter는 `name`, `description`만 허용됩니다.
- `ywc-docker-isolate`는 anti-trigger로 명시합니다.
- `README.zh.md`, `README.es.md`는 v1 범위에서 제외합니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance
- Targeted evidence: skill validator, file-existence checks, wording grep

### Interface Contract

- Contract: Codex `ywc-iac-author` skill is installable with required metadata and locale docs.
- Inputs: design input, provider choice, Terraform-only authoring request
- Outputs: skill instructions, UI metadata, Tier 1 README set
- Error model: missing locale files, invalid frontmatter, or stale `openai.yaml` keys fail validation
- Impacted tests: `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-iac-author`, `bash scripts/validate.sh`

### Critical Surface Review

- Review requirement: anti-trigger wording과 Terraform-only scope가 sibling skill과 충돌하지 않는지 reviewer 확인

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-iac-author/**`

### Shared Surfaces

- Shared infra references via relative links
- Codex skill validator expectations
- Generated plugin mirror regenerated later from this directory

### Conflicts With

- (None identified)

### Parallelizable After

- `000047-010-infra-cloud-engineer-specialist`
- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`

### Task Verify

- `test -f codex/skills/ywc-iac-author/SKILL.md`
- `test -f codex/skills/ywc-iac-author/agents/openai.yaml`
- `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-iac-author/$f; done`
- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-iac-author`

## Out of Scope

- Shared reference docs outside relative link usage
- Generated plugin files
