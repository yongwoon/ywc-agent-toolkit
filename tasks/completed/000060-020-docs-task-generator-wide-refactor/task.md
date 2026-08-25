# 000060-020-docs-task-generator-wide-refactor — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] (None — root task) 선행 task 없음
- [ ] `ywc-skill-author`를 먼저 호출해 canonical rule set(A8/A14/B9)을 로드했다

## Allowed Edit Scope
- [ ] `claude-code/skills/ywc-task-generator/SKILL.md` 편집
- [ ] (조건부) `claude-code/skills/ywc-task-generator/references/example-decomposition.md` 신규 생성 — worked example이 20줄 초과 시에만
- [ ] 그 외 파일 편집이 필요하면 중단하고 보고

## Stop Conditions
- [ ] `ywc-skill-author` 선행 호출 없이 structural edit을 시작해야 하는 상황이면 중단
- [ ] 원칙 본문 + worked example inline 합계가 SKILL.md를 500줄 초과로 만들 위험이면 중단(먼저 reference 분리)
- [ ] Wide Refactor 예외가 Safety Invariant(DB/library 분리)를 완화하는 방향으로 해석되면 중단 — 이 예외는 Reviewability에만 적용

## Implementation Steps
- [ ] `## Task Design Principles`에 `### 5. Wide Refactor Exception (Expand-Contract)` 추가(15~20줄)
  - [ ] blast-radius가 전체 코드베이스인 기계적 변경은 vertical-slice 원칙의 예외임을 1문장으로 명시
  - [ ] expand → migrate → contract 3단계 시퀀싱 규칙 기술
  - [ ] 각 migrate batch는 독립 task이며 이전 batch를 `Depends On`으로 chain(병렬 금지)함을 명시
  - [ ] migrate batch task의 category는 "primary nature of the change" 규칙을 따름을 명시(신규 category 불필요)
- [ ] (조건부) worked example 분리
  - [ ] inline 설명이 20줄 초과 시 `references/example-decomposition.md` 생성 후 worked example 이동
  - [ ] SKILL.md에는 1줄 pointer만 남김(force-load `@` 금지)
- [ ] Rationalization Defense 표에 row 1개 추가
  - [ ] "컬럼 하나 바꾸는 거라 작은 task다" → "caller 전체가 blast radius, expand→migrate→contract 적용" 반박
  - [ ] 5번째 원칙(Wide Refactor)으로 wiring(B9)

## Task Verify
- [ ] `grep -n "Wide Refactor" claude-code/skills/ywc-task-generator/SKILL.md` → 신규 5번째 원칙 서브섹션 반환
- [ ] `grep -n "expand" claude-code/skills/ywc-task-generator/SKILL.md` → 시퀀싱 규칙 반환
- [ ] (조건부 분리 시) `grep -n "example-decomposition" claude-code/skills/ywc-task-generator/SKILL.md` → pointer 1줄 반환

## Verification
- [ ] `wc -l claude-code/skills/ywc-task-generator/SKILL.md` ≤ 500 (A8, 매 편집 후 재확인)
- [ ] `ywc-skill-author` Validation Checklist 전부 PASS
- [ ] `bash scripts/validate.sh` exit 0
- [ ] (해당 없음) markdownlint — SKILL.md/references는 lint glob 대상이 아님
