# 000060-020-docs-task-generator-wide-refactor

## Purpose
`ywc-task-generator`의 `## Task Design Principles`에 5번째 원칙 `### 5. Wide Refactor Exception (Expand-Contract)`을 추가한다(FR-3/AC3). Blast radius가 코드베이스 전체에 걸치는 기계적 변경(컬럼 rename, 공유 타입 retype 등)은 vertical-slice 원칙의 예외이며 expand → migrate(batch) → contract로 시퀀싱해야 함을 명시한다.

## Scope
- `## Task Design Principles`에 5번째 원칙 서브섹션 추가(inline 15~20줄 이내로 제한).
- 시퀀싱 규칙 명시: expand(신구 병존) → migrate(blast-radius 단위 batch, 각 batch 독립 task, CI green 유지, 이전 batch를 `Depends On`) → contract(구형 제거, 모든 migrate batch 완료 후).
- Rationalization Defense 표에 "이것도 결국 컬럼 하나 바꾸는 거라 작은 task다" 류 row 1개 추가 + Wide Refactor 원칙으로 wiring.
- **조건부 신규 파일**: inline 설명이 20줄을 초과하면 worked example을 `references/example-decomposition.md`(신규)로 이동하고 SKILL.md에는 1줄 pointer만 남긴다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` FR-3(line 87), AC3(line 58) — Wide Refactor Exception 요구사항과 observable
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` Edge Cases(line 150) — 500줄 cap 초과 시 example-decomposition.md 이동 규칙
- `claude-code/skills/ywc-skill-author/SKILL.md` 및 `references/` — A8(≤500), A14(≥30줄 static content Tier 3 분리), B9(RD wiring)

### Summary
Reviewability 원칙(vertical slice)의 명시적 예외를 5번째 원칙으로 문서화한다. 현재 SKILL.md는 423줄(cap 500, headroom ~77줄)이라 여유는 있으나 절제를 위해 원칙 본문은 15~20줄로 제한한다. 상세 worked example이 그 한도를 넘으면 A14에 따라 `references/example-decomposition.md`로 분리한다(이 파일은 repo에 아직 미존재 — 조건부 신규 생성). 새 discretionary discipline이므로 대응 RD row를 추가한다.

### Out of Scope (from spec)
- 기존 4개 원칙(Reviewability/Dependency Safety/DB Migration Separation/Library Introduction Separation)의 재작성.
- Safety Invariant(DB migration·library 분리) 규칙 변경 — Wide Refactor 예외는 Reviewability의 vertical-slice 번들링에만 적용된다.

## Criticality
`normal` — skill prompt 텍스트 변경. 보안·데이터 surface 없음.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- (None — no downstream dependency)

## Key Files
- `claude-code/skills/ywc-task-generator/SKILL.md` — 5번째 원칙 서브섹션 + RD row 추가
- `claude-code/skills/ywc-task-generator/references/example-decomposition.md` — (조건부 신규) worked example이 20줄 초과 시에만 생성

## Notes
- **ywc-skill-author 선행 실행 필수**: body section 추가·조건부 신규 참조 파일 생성은 structural edit(typo/link fix 예외 아님).
- **500줄 cap 상시 감시**: 매 편집 후 `wc -l`로 확인. 20줄 초과 시 즉시 example-decomposition.md로 이동.
- 신규 파일을 만들 경우 references/에 이미 `granularity-modes.md` 등 static content가 다수 있어 관례와 합치한다.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-task-generator/references/example-decomposition.md`(조건부 신규)

### Shared Surfaces
- `(None identified)` — 다른 skill과 참조 관계 없음.

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `grep -n "Wide Refactor" claude-code/skills/ywc-task-generator/SKILL.md` — 5번째 원칙 서브섹션 반환
- `wc -l claude-code/skills/ywc-task-generator/SKILL.md` — ≤ 500
- `bash scripts/validate.sh` — exit 0

## Out of Scope
- expand-contract 실제 실행 로직(이 task는 원칙 문서화만 담당).
- README locale 파일 변경.
