# 000062-010-docs-wayfinder-core

## Purpose

대형·불확실·multi-session discovery 전용 `ywc-wayfinder` Codex skill bundle과 deterministic local map/ticket contract를 추가한다.

## Scope

- strict `SKILL.md`, Tier 1/maintained Tier 2 README, `agents/openai.yaml`, map/ticket reference, evals를 만든다.
- `docs/ywc-plans/<slug>-wayfinder.md` map path, one-active-ticket, ticket state, resume/terminal/no-write semantics를 정의한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-a--deterministic-wayfinder-map-and-ticket-contract`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-h--two-phase-autonomous-preview-and-terminal-map-behavior`

### Summary

Wayfinder는 구현이나 tracker write가 아니라 local Markdown discovery map을 관리한다. 매 session 하나의 ticket만 해결하고 terminal map은 상태에 맞춰 `DONE` 또는 `NEEDS_CONTEXT`를 반환하며 write하지 않는다.

### Out of Scope (from spec)

- 인접 skill routing/catalog — `000062-020`.
- task generation, research persistence, implementation.

## Dependencies

### Depends On

- Phase 000061 — global source metadata/fixture baseline.

### Depended By

- `000062-020-docs-wayfinder-routing-catalog` — stable skill contract 제공.
- `000062-060-docs-tech-research-persistence` — consumer handoff target 제공.

## Key Files

- `codex/skills/ywc-wayfinder/**`

## Notes

생성/구조 변경 전 `ywc-skill-author` RED baseline을 실행한다. description은 500-character gate를 통과해야 한다.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-wayfinder/**`

### Shared Surfaces

- `docs/ywc-plans/<slug>-wayfinder.md` artifact schema.

### Conflicts With

- `(None identified)` — 신규 directory 단독 소유.

### Parallelizable After

- Phase 000061 complete

### Task Verify

- `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-wayfinder`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

- existing skill routing text 및 catalog/release metadata.
