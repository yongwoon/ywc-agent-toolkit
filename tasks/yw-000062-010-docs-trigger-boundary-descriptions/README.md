# yw-000062-010-docs-trigger-boundary-descriptions

## Purpose
형제 skill/agent 와의 trigger 충돌을 줄이기 위해 description 경계 문구를 보강한다 (Phase E, FR-E1).

## Scope
- code-gen / security-audit / tech-research / ui-ux-review description, product-review verify-before-surface 문장, agents qa-engineer / refactor-cleaner description (FR-E1)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.md` — FR-E1, AC-12(E1), AC-17(description 부분)
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.spec-ready-log.md` — spec 수렴 이력 (ywc-spec-ready DONE)

### Summary
upstream #263 의 description 변경 중 이 저장소에 존재하는 대상만 반영한다. 식별 token: refactor-cleaner `repo-wide`, code-gen `spec-verification`, ui-ux-review `AI-generated`, tech-research `ROI`, security-audit `ad-hoc threat-model`, qa-engineer `manual verification testsheet`. skill description 은 `ywc-skill-author` A15 (≤80 words, 권고) 를 목표로 하고 이미 초과인 ui-ux-review (86 단어) 는 순증가 0. agent description 은 A15 대상 외.

### Out of Scope (from spec)
- #263 의 evaluation artifact (scorecard / history)
- ywc-team-assemble

## Criticality
`normal` — skill 문서 / 검증 script 변경이며 인증·결제·secret 등 security-sensitive surface 를 다루지 않음 (spec 에 Critical Surfaces 선언 없음)

## Dependencies

### Depends On
- `yw-000061-010-docs-fastify-scaffold` — Phase D 머지 base

### Depended By
- (None — no downstream dependency)

## Key Files
- `claude-code/skills/ywc-{code-gen,security-audit,tech-research,ui-ux-review,product-review}/SKILL.md`
- `claude-code/agents/ywc-qa-engineer.md`
- `claude-code/agents/ywc-refactor-cleaner.md`

## Notes
- Phase A 가 같은 SKILL.md 들에 callout 을 이미 추가한 상태 위에서 frontmatter / 지정 문장만 수정한다.
- FM-5 (anchor 불일치로 링크 깨짐) 는 AC-1 의 `validate.sh` 로 검출.

## Parallel Execution Metadata

- Model Hint: haiku — M2 (Ownership 전부 `*.md`, category docs)

### Ownership
- `claude-code/skills/ywc-code-gen/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-security-audit/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-tech-research/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-ui-ux-review/SKILL.md` (frontmatter description)
- `claude-code/skills/ywc-product-review/SKILL.md` (verify-before-surface 문장)
- `claude-code/agents/ywc-qa-engineer.md`
- `claude-code/agents/ywc-refactor-cleaner.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- skill activation (description) — 형제 skill 과의 trigger 경계

### Conflicts With
- (None identified — 같은 phase 의 020 / 030 과 파일 겹침 없음)

### Parallelizable After
- `yw-000061-010-docs-fastify-scaffold`

### Task Verify
- `grep -c "manual verification testsheet" claude-code/agents/ywc-qa-engineer.md` ≥1 (AC-12 E1)
- `grep -c "repo-wide" claude-code/agents/ywc-refactor-cleaner.md`, `grep -c "spec-verification" claude-code/skills/ywc-code-gen/SKILL.md`, `grep -c "AI-generated" claude-code/skills/ywc-ui-ux-review/SKILL.md`, `grep -c "ROI" claude-code/skills/ywc-tech-research/SKILL.md`, `grep -c "ad-hoc threat-model" claude-code/skills/ywc-security-audit/SKILL.md` 각 ≥1 (AC-17)
- `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Out of Scope
- description 이외의 본문 변경
