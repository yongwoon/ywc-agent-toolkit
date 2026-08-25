# 000060-010-docs-tdd-ritual-red-phase-guards

## Purpose
`ywc-tdd-ritual` skill의 Step 1(RED)에 두 가지 test-authoring guard를 추가한다: (1) 테스트할 public seam을 사전에 명명·합의하는 절차(FR-1/AC1), (2) Common Mistakes에 tautological assertion anti-pattern 문서화(FR-2/AC2). 두 항목 모두 동일 파일(`ywc-tdd-ritual/SKILL.md`)의 RED-phase 규율을 강화하는 vertical slice이므로 하나의 task로 묶는다.

## Scope
- Step 1(RED)에 `### Seams` 서브섹션 신규 추가(~15줄): seam 한 문장 스케치 → 기존 seam 우선 → 불명확 시 사용자 확인.
- Common Mistakes 섹션에 6번째 항목으로 tautological assertion 패턴 추가(~8줄, 예시 포함).
- Rationalization Defense 표에 대응 row 추가(FR-1용 1개 이상 + FR-2용 1개), 각 row를 해당 Workflow 단계로 wiring.
- `references/test-shape-cookbook.md`를 seam 절차의 예시 pointer로 교차 참조(해당 파일 편집은 없음).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` FR-1(line 68), AC1(line 56) — Seams 서브섹션 요구사항과 observable
- `docs/ywc-plans/claude-code-sdlc-v11-improvements.md` FR-2(line 78), AC2(line 57) — Tautological test 항목 요구사항과 observable
- `claude-code/skills/ywc-skill-author/SKILL.md` 및 `references/` — 이 편집이 준수해야 하는 canonical rule set(특히 B9 RD-row wiring, A14 Tier 유지 기준)

### Summary
`ywc-tdd-ritual` RED phase에 seam 사전합의 절차와 tautological-test 방어를 명시한다. Seams 절차는 workflow prose(Tier 2, A14 예외)이므로 SKILL.md 본문에 유지하고 별도 reference 파일로 분리하지 않는다. tautological 항목은 기존 5개 Common Mistakes에 1개 추가로 30줄 미만이라 인라인 유지한다. 새 discretionary discipline을 도입하므로 각각 Rationalization Defense row를 추가하고 Workflow 단계로 wiring한다.

### Out of Scope (from spec)
- `references/test-shape-cookbook.md` 내용 편집 — 이 파일은 pointer 대상일 뿐 절차 본문은 SKILL.md에 둔다.
- codex 번들(`codex/skills/ywc-tdd-ritual/`) 동일 개선 — 별도 sibling plan 범위(spec Out of Scope).

## Criticality
`normal` — skill prompt 텍스트 변경으로 runtime 코드·사용자 데이터·보안 surface를 다루지 않는다.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000060-050-docs-plan-spec-template-seam-pointer` — 확정된 `### Seams` 서브섹션 명칭을 정식 출처로 pointer 문구에 인용해야 한다.

## Key Files
- `claude-code/skills/ywc-tdd-ritual/SKILL.md` — Step 1 `### Seams` 서브섹션 추가, Common Mistakes 6번째 항목 추가, Rationalization Defense row 3개 추가

## Notes
- **ywc-skill-author 선행 실행 필수**: body section 추가·RD row 추가는 structural edit이므로 편집 전 `ywc-skill-author`를 호출해 canonical rule set을 로드한다(typo/link fix 예외 아님 — `claude-code/skills/CLAUDE.md` 규칙).
- Seams 절차 명칭(`### Seams`)은 downstream task 000060-050이 인용하므로, 명칭을 확정한 뒤 완료로 표시한다.
- A14: workflow/절차 prose는 길이와 무관하게 SKILL.md 본문(Tier 2) 유지 — reference로 분리하지 않는다.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-tdd-ritual/SKILL.md`

### Shared Surfaces
- `Skill 참조 관계: ywc-plan/spec-template.md → 이 파일의 Seams 명칭`(downstream task 000060-050이 명칭에 의존)

### Conflicts With
- `(None identified)` — 다른 000060 task는 disjoint 파일을 편집한다.

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `grep -n "Seam" claude-code/skills/ywc-tdd-ritual/SKILL.md` — `### Seams` 서브섹션과 RD row 반환
- `grep -ni "tautolog" claude-code/skills/ywc-tdd-ritual/SKILL.md` — 신규 Common Mistakes 항목 반환
- `wc -l claude-code/skills/ywc-tdd-ritual/SKILL.md` — ≤ 500
- `bash scripts/validate.sh` — exit 0

## Out of Scope
- Step 2(GREEN)·Step 3(REFACTOR) 절차 변경.
- 기존 Common Mistakes 5개 항목의 재작성.
- README locale 파일(`.ja.md`/`.ko.md` 등) 변경 — 이번 변경은 SKILL.md 본문만 대상.
