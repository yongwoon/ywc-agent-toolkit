# 000060-050-docs-plan-spec-template-seam-pointer

## Purpose
`ywc-plan`의 `references/spec-template.md` Acceptance Criteria 안내 문단에 seam 명명을 권장하는 한 줄을 추가한다(FR-6/AC6). 신규 최상위 섹션은 만들지 않으며, `ywc-tdd-ritual`의 `### Seams`를 정식 출처로 가리켜 동일 규칙을 두 파일에 중복 서술하지 않는다.

## Scope
- `## Acceptance Criteria` 섹션의 설명 문단(Preferred form 예시 앞)에 seam 명명 권장 한 줄 추가.
- 문구는 `ywc-tdd-ritual`(FR-1)의 `### Seams`를 정식 출처로 pointer.
- 신규 최상위 섹션(`## Testing Decisions` 등) 생성 금지 — 그런 섹션은 존재하지 않음이 확인됨.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` FR-6(line 119), AC6(line 61) — spec-template seam pointer 요구사항과 observable
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` Edge Cases(line 153) — 존재하지 않는 "Testing Decisions" 섹션을 만들지 말라는 명시적 금지
- `claude-code/skills/ywc-plan/references/spec-template.md` `## Acceptance Criteria`(line 48), "Preferred form for each AC:"(line 52) — 삽입 지점
- `000060-010-docs-tdd-ritual-red-phase-guards` 산출물 — 인용할 `### Seams` 서브섹션 명칭의 정식 출처

### Summary
spec-template의 Acceptance Criteria 안내 문단에 "AC 작성 전 이 그룹이 검증할 test seam(공개 경계)을 한 문장으로 명명 권장 — 상세 절차는 ywc-tdd-ritual의 Seams" 형태의 한 줄만 추가한다. 원 review의 "Testing Decisions 섹션에 추가" 가정은 부정확하며(그 섹션 부재), AC6이 신규 섹션 생성을 명시적으로 금지한다. FR-1의 `### Seams` 명칭이 확정된 뒤 이 pointer 문구를 작성한다.

### Out of Scope (from spec)
- `ywc-tdd-ritual`의 Seams 절차 본문 재서술 — pointer만 두고 규칙 중복 금지(정식 출처는 FR-1).
- spec-template의 다른 섹션 변경.

## Criticality
`normal` — skill 참조 텍스트 한 줄 추가. 보안·데이터 surface 없음.

## Dependencies

### Depends On
- `000060-010-docs-tdd-ritual-red-phase-guards` — 확정된 `### Seams` 서브섹션 명칭을 pointer 문구에 정확히 인용해야 한다(FR 간 의존, spec line 125/159).

### Depended By
- (None — no downstream dependency)

## Key Files
- `claude-code/skills/ywc-plan/references/spec-template.md` — Acceptance Criteria 안내 문단에 한 줄 추가

## Notes
- **ywc-skill-author 선행 실행 필수**: 문단 내용 변경이므로 canonical rule set 로드 후 진행(단순 typo 아님).
- **의존 이유**: 010에서 Seams 서브섹션 명칭(`### Seams`)이 확정되어야 pointer가 존재하는 anchor를 가리킨다. 010 미완료 상태로 착수 금지.
- **신규 섹션 금지 재확인**: `grep -c "^## "` 값이 변경 전후 동일해야 한다(AC6 observable).

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-plan/references/spec-template.md`

### Shared Surfaces
- `Skill 참조 관계: 이 파일 → ywc-tdd-ritual/SKILL.md의 Seams 명칭`(010의 산출물에 의존)

### Conflicts With
- `(None identified)` — 다른 000060 task와 disjoint 파일.

### Parallelizable After
- `000060-010-docs-tdd-ritual-red-phase-guards`

### Task Verify
- `grep -ni "seam" claude-code/skills/ywc-plan/references/spec-template.md` — Acceptance Criteria 섹션 내 한 줄 반환
- `grep -c "^## " claude-code/skills/ywc-plan/references/spec-template.md` — 변경 전 값과 동일(신규 최상위 섹션 없음)
- `bash scripts/validate.sh` — exit 0

## Out of Scope
- `ywc-tdd-ritual` 파일 변경(010 소관).
- README locale 파일 변경.
