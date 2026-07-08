# 000049-020-docs-infra-design-skill

## Purpose

Codex `ywc-infra-design` skill을 작성합니다. topology, service selection, IAM boundary, cost and availability trade-off를 정리하는 design skill surface를 추가하고, Terraform authoring은 `ywc-iac-author`로 넘기는 anti-trigger 경계를 명확히 합니다.

## Scope

- `codex/skills/ywc-infra-design/SKILL.md`
- `codex/skills/ywc-infra-design/agents/openai.yaml`
- `codex/skills/ywc-infra-design/README.md`
- `codex/skills/ywc-infra-design/README.en.md`
- `codex/skills/ywc-infra-design/README.ja.md`
- `codex/skills/ywc-infra-design/README.ko.md`

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-1-codex용-infra-taxonomy를-신규-skill-4종으로-포트한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-6-신규-skill-간-dispatch-경계와-anti-trigger를-codex-스타일로-명시한다`
- `AGENTS.md`

### Summary

`ywc-infra-design`는 topology와 trade-off 기록을 담당하는 설계 entry point입니다. 이 skill은 provider/core references를 읽고 설계 산출을 만들지만 Terraform code authoring은 수행하지 않아야 합니다. sibling skill overlap을 피하기 위해 `ywc-iac-author`, `ywc-infra-review`, `ywc-docker-isolate`에 대한 anti-trigger를 분명히 적어야 합니다.

### Out of Scope (from spec)

- Terraform code 작성 — `000049-010-docs-iac-author-skill`
- review/optimization execution flow

## Criticality

normal

## Dependencies

### Depends On

- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`

### Depended By

- `000050-010-infra-codex-plugin-sync-validate`

## Key Files

- `codex/skills/ywc-infra-design/SKILL.md`
- `codex/skills/ywc-infra-design/agents/openai.yaml`
- `codex/skills/ywc-infra-design/README.md`
- `codex/skills/ywc-infra-design/README.en.md`
- `codex/skills/ywc-infra-design/README.ja.md`
- `codex/skills/ywc-infra-design/README.ko.md`

## Notes

- `ywc-architect`와의 관계는 complementary이며, irreversible architecture verdict가 필요하면 architect로 route한다는 문구를 명시합니다.
- provider 결정 후 한 provider 문서만 읽는 Progressive Disclosure를 유지합니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance
- Targeted evidence: skill validator, anti-trigger wording grep

### Interface Contract

- Contract: installable Codex skill with design-specific routing boundary and required locale/UI files
- Inputs: infra design request, provider choice, constraints
- Outputs: skill instructions, UI metadata, Tier 1 README set
- Error model: missing anti-trigger or wrong file set causes validator or routing ambiguity
- Impacted tests: skill validator and repository validator

### Critical Surface Review

- Review requirement: `ywc-architect` and `ywc-iac-author` boundaries are explicit and non-overlapping

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-infra-design/**`

### Shared Surfaces

- Shared infra references via relative links
- Sibling-skill routing vocabulary

### Conflicts With

- (None identified)

### Parallelizable After

- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`

### Task Verify

- `test -f codex/skills/ywc-infra-design/SKILL.md`
- `test -f codex/skills/ywc-infra-design/agents/openai.yaml`
- `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-infra-design/$f; done`
- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-design`

## Out of Scope

- Agent file edits
- Shared reference authoring
- Generated plugin files
