# 000043-030-docs-agent-test-ownership-boundaries

## Purpose

2026-07-06 평가의 A1(역할 경계) 결함 4건을 4개 에이전트 정의에 반영한다. 핵심은 코더(backend/frontend)와
qa-engineer 사이의 **단위테스트 소유권 경계**를 하나의 공유 규칙("동일 태스크 co-located 테스트 vs standalone
테스트 스위트")으로 확정하고 3개 에이전트에 일관 적용하는 것. doc-writer는 glossary 라우팅 노트를 추가한다.
(FR7~FR10)

## Scope

- `claude-code/agents/` 4개 .md 편집: backend-coder, frontend-coder, qa-engineer, doc-writer.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/toolkit-eval-backlog-2026-07-06.md` — FR7~FR10, §AC10′, Existing Constraints Touched(agent 행)

### Summary
설명(description)의 anti-trigger는 이미 대체로 정확하며, 본문 Mission이 그보다 넓은 것이 결함이다. 본문을 설명에
맞춰 좁힌다. Codex 에이전트 미러는 없으므로(codex/agents 상이) Claude Code 전용.

### Out of Scope (from spec)
- Codex 에이전트 TOML, 스킬 파일, setup-language 케이스.

## Criticality
`normal` — 에이전트 정의 문서 편집.

## Dependencies
- **Depends On**: (없음).
- **Depended By**: (없음).

## Key Files
- `claude-code/agents/ywc-backend-coder.md`, `.../ywc-frontend-coder.md`, `.../ywc-qa-engineer.md`, `.../ywc-doc-writer.md`

## Notes
- **공유 규칙 먼저 확정**: "코더는 동일 태스크에서 저작한 코드에 대한 co-located 테스트만 소유; standalone/커버리지
  확장 테스트 스위트는 ywc-qa-engineer 소유." 이 문장을 backend/frontend/qa 3곳에 상호 정합되게 적용(드리프트 금지).
- **FR7 (backend-coder:21-24)**: Mission의 "unit + integration tests" → "동일 태스크 co-located 테스트"로 축소.
- **FR8 (frontend-coder:19 부근)**: 자체 테스트를 "구현 중인 컴포넌트"로 한정 + standalone은 qa-engineer 라우팅.
- **FR9 (doc-writer:25)**: "glossary 항목은 ywc-ubiquitous-language가 본 에이전트를 dispatch" 라우팅 노트 추가.
- **FR10/§AC10′ (qa-engineer:22-24, :77)**: "or reviewing them" 및 standalone E2E **전략/소유권** 주장 제거.
  단, `ywc-e2e-test-strategy`가 dispatch했을 때 codified E2E 테스트를 **작성**하는 능력은 보존.

## Out of Scope
- 스킬 파일(000043-020), setup-language 케이스(000043-010), Codex 에이전트.

## Parallel Execution Metadata
- **Ownership**: `claude-code/agents/{ywc-backend-coder,ywc-frontend-coder,ywc-qa-engineer,ywc-doc-writer}.md`
- **Shared Surfaces**: 4개 에이전트가 공유하는 "테스트 소유권" 개념(파일 미중복이나 규칙 문구 정합 필요)
- **Conflicts With**: (None identified) — 010/020과 파일 미중복
- **Parallelizable After**: (즉시)
- **Task Verify**:
  `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --format json`에서 4개
  에이전트의 A3/A4/A5 mechanical 회귀 없음. `bash scripts/validate.sh` exit 0.
