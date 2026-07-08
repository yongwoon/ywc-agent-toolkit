# 000049-040-docs-infra-optimize-skill

## Purpose

Codex `ywc-infra-optimize` skill을 작성합니다. drift, right-sizing, unused resources, reliability hardening에 대한 conservative optimization planning surface를 만들고 SAFE / CAUTION / DANGER 분류와 후속 action guidance를 명시합니다.

## Scope

- `codex/skills/ywc-infra-optimize/SKILL.md`
- `codex/skills/ywc-infra-optimize/agents/openai.yaml`
- `codex/skills/ywc-infra-optimize/README.md`
- `codex/skills/ywc-infra-optimize/README.en.md`
- `codex/skills/ywc-infra-optimize/README.ja.md`
- `codex/skills/ywc-infra-optimize/README.ko.md`

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-1-codex용-infra-taxonomy를-신규-skill-4종으로-포트한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-6-신규-skill-간-dispatch-경계와-anti-trigger를-codex-스타일로-명시한다`
- `AGENTS.md`

### Summary

`ywc-infra-optimize`는 destructive or risky change를 즉시 실행하는 skill이 아니라 conservative planning and classification surface입니다. SAFE / CAUTION / DANGER buckets, right-sizing and drift guidance, reliability hardening recommendations를 제공하고 필요 시 `ywc-cloud-engineer` 또는 `ywc-infra-review`로 연결합니다. sibling skill overlap을 막기 위해 authoring/design/review와의 경계를 명확히 적습니다.

### Out of Scope (from spec)

- direct Terraform authoring — `000049-010-docs-iac-author-skill`
- security/cost/reliability review fan-out 자체 — `000049-030-docs-infra-review-skill`

## Criticality

normal

## Dependencies

### Depends On

- `000047-010-infra-cloud-engineer-specialist`
- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`

### Depended By

- `000050-010-infra-codex-plugin-sync-validate`

## Key Files

- `codex/skills/ywc-infra-optimize/SKILL.md`
- `codex/skills/ywc-infra-optimize/agents/openai.yaml`
- `codex/skills/ywc-infra-optimize/README.md`
- `codex/skills/ywc-infra-optimize/README.en.md`
- `codex/skills/ywc-infra-optimize/README.ja.md`
- `codex/skills/ywc-infra-optimize/README.ko.md`

## Notes

- optimization skill은 v1에서 eval fixture를 만들지 않습니다.
- SAFE / CAUTION / DANGER taxonomy는 실행 권고 수준을 의미하며 직접 apply를 수행하는 contract가 아닙니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance
- Targeted evidence: skill validator, SAFE/CAUTION/DANGER wording grep

### Interface Contract

- Contract: installable optimization skill with conservative classification and required metadata/docs
- Inputs: infra cost/reliability/drift optimization request
- Outputs: skill instructions, UI metadata, Tier 1 README set
- Error model: missing conservative classification or wrong routing boundary causes unsafe expectations
- Impacted tests: skill validator and repository validator

### Critical Surface Review

- Review requirement: SAFE/CAUTION/DANGER semantics and handoff boundaries require reviewer confirmation

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-infra-optimize/**`

### Shared Surfaces

- Shared infra references via relative links
- Optimization severity vocabulary
- Generated plugin mirror regenerated later from this directory

### Conflicts With

- (None identified)

### Parallelizable After

- `000047-010-infra-cloud-engineer-specialist`
- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`

### Task Verify

- `test -f codex/skills/ywc-infra-optimize/SKILL.md`
- `test -f codex/skills/ywc-infra-optimize/agents/openai.yaml`
- `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-infra-optimize/$f; done`
- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-optimize`

## Out of Scope

- Generated plugin files
- Agent file changes
