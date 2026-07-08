# 000049-030-docs-infra-review-skill

## Purpose

Codex `ywc-infra-review` skill을 작성합니다. security, cost, reliability 세 렌즈를 bounded specialist agent로 fan-out하고, CRITICAL/HIGH finding 시 apply 차단 권고를 내리는 review skill surface를 Codex bundle 규약에 맞게 추가합니다.

## Scope

- `codex/skills/ywc-infra-review/SKILL.md`
- `codex/skills/ywc-infra-review/agents/openai.yaml`
- `codex/skills/ywc-infra-review/README.md`
- `codex/skills/ywc-infra-review/README.en.md`
- `codex/skills/ywc-infra-review/README.ja.md`
- `codex/skills/ywc-infra-review/README.ko.md`

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-1-codex용-infra-taxonomy를-신규-skill-4종으로-포트한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-4-기존-specialist-agent를-infra-review-흐름에-맞게-확장한다`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-6-신규-skill-간-dispatch-경계와-anti-trigger를-codex-스타일로-명시한다`
- `AGENTS.md`

### Summary

`ywc-infra-review`는 이번 배치에서 가장 routing-sensitive한 skill입니다. security와 cost는 기존 specialist, reliability는 신규 `ywc-cloud-engineer`로 분기해야 하며, skill 본문은 이 dispatch contract를 정확히 명시해야 합니다. review 결과가 CRITICAL/HIGH이면 apply를 막고 후속 authoring 또는 redesign로 되돌리는 conservative policy도 포함해야 합니다.

### Out of Scope (from spec)

- agent wording 자체 수정 — `000047-010`, `000047-020`
- optimization workflow — `000049-040-docs-infra-optimize-skill`

## Criticality

critical — 다중 specialist dispatch와 apply-blocking policy를 다루므로 routing drift가 위험함

## Dependencies

### Depends On

- `000047-010-infra-cloud-engineer-specialist`
- `000047-020-infra-agent-lens-extensions`
- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`

### Depended By

- `000050-010-infra-codex-plugin-sync-validate`

## Key Files

- `codex/skills/ywc-infra-review/SKILL.md`
- `codex/skills/ywc-infra-review/agents/openai.yaml`
- `codex/skills/ywc-infra-review/README.md`
- `codex/skills/ywc-infra-review/README.en.md`
- `codex/skills/ywc-infra-review/README.ja.md`
- `codex/skills/ywc-infra-review/README.ko.md`

## Notes

- `ywc-cloud-engineer` routing을 `000047-010` 이름과 정확히 일치시켜 stale dispatch를 방지합니다.
- review skill은 authoring 자체를 하지 않으며, output은 findings / verdict / next action recommendation입니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance on critical routing surface
- Targeted evidence: skill validator, dispatch-name grep, policy wording review

### Interface Contract

- Contract: infra review requests route to security, cost, reliability specialists with explicit escalation policy
- Inputs: bounded IaC/spec/review scope
- Outputs: review workflow instructions, UI metadata, Tier 1 README set
- Error model: stale specialist names or ambiguous escalation wording causes caller misrouting
- Impacted tests: skill validator and repository validator

### Critical Surface Review

- Review requirement: all three specialist names, CRITICAL/HIGH apply-blocking guidance, and anti-trigger wording require reviewer confirmation

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-infra-review/**`

### Shared Surfaces

- Shared infra references via relative links
- Specialist agent dispatch names
- Review severity vocabulary

### Conflicts With

- (None identified)

### Parallelizable After

- `000047-010-infra-cloud-engineer-specialist`
- `000047-020-infra-agent-lens-extensions`
- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`

### Task Verify

- `test -f codex/skills/ywc-infra-review/SKILL.md`
- `test -f codex/skills/ywc-infra-review/agents/openai.yaml`
- `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-infra-review/$f; done`
- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-infra-review`

## Out of Scope

- Agent file changes
- Generated plugin files
