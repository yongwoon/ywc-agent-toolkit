# 000051-040-docs-skill-author-exploration-rules

## Purpose
`ywc-skill-author`가 future exploratory skill authoring에서 excessive few-shot/example cargo-culting을 막고, context-first decision framing을 권장하도록 업데이트한다.

## Scope
- `codex/skills/ywc-skill-author/SKILL.md` rule / anti-pattern / validation guidance 업데이트
- `codex/skills/ywc-skill-author/agents/openai.yaml` sync
- `codex/skills/ywc-skill-author` locale README stale 여부 반영

## Spec Reference

### Primary Sources
- `docs/ywc-plans/fable-inspired-codex-exploration.md#functional-requirements` — FR9
- `docs/ywc-plans/fable-inspired-codex-exploration.md#iteration-1-amendments` — metadata/locale sync expectation
- `codex/skills/references/unknown-matrix.md` — exploration-heavy skill이 참조할 shared model
- `codex/skills/references/implementation-notes.md` — reporting/decision-capture shared model

### Summary
이 task는 `ywc-skill-author`에 future-proofing rule을 추가한다. 목적은 examples 자체를 금지하는 것이 아니라, exploration-heavy skill이 static worked example 때문에 reasoning space를 과도하게 잃지 않도록 만드는 것이다. 기존 progressive disclosure와 trigger-only frontmatter discipline은 유지한다.

### Out of Scope (from spec)
- discovery/planning skill wiring — `000051-020-docs-discovery-skill-exploration-hooks`
- execution skill wiring — `000051-030-docs-execution-skill-implementation-notes`
- plugin sync / 전체 validation — `000052-010-infra-fable-exploration-validation`

## Dependencies

### Depends On
- `000051-010-docs-shared-exploration-references` — 새 shared exploration references를 반영해야 함

### Depended By
- `000052-010-infra-fable-exploration-validation` — skill-author rule / metadata / README sync를 최종 검증함

## Key Files
- `codex/skills/ywc-skill-author/SKILL.md`
- `codex/skills/ywc-skill-author/agents/openai.yaml`
- `codex/skills/ywc-skill-author/README*.md`

## Notes
- 추가 rule은 “예시를 줄여라”가 아니라 “fragility를 낮추는 example만 남겨라”여야 한다.
- 기존 3-tier loading model과 충돌하지 않도록 Tier 1/Tier 2/Tier 3 guidance 안에서 정리한다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-skill-author/**`

### Shared Surfaces
- Progressive disclosure rules
- Skill metadata sync rules
- Exploration-heavy skill authoring conventions

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000051-010-docs-shared-exploration-references`

### Task Verify
- `rg -n "few-shot|worked examples|context-first|decision frame|exploration-heavy" codex/skills/ywc-skill-author/SKILL.md`

## Out of Scope
- Other skill directories
- shared reference creation
- plugin sync / repository-wide validation
