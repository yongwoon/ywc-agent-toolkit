# 000060-010-docs-tdd-ritual-red-phase-guards — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] (None — root task) 선행 task 없음
- [ ] `ywc-skill-author`를 먼저 호출해 canonical rule set(A8/A14/B9)을 로드했다

## Allowed Edit Scope
- [ ] `claude-code/skills/ywc-tdd-ritual/SKILL.md`만 편집한다
- [ ] Ownership 밖(다른 skill·references·README locale) 편집이 필요하면 중단하고 보고한다

## Stop Conditions
- [ ] `ywc-skill-author` 선행 호출 없이 structural edit을 시작해야 하는 상황이면 중단
- [ ] Seams 절차가 30줄을 넘어 reference 분리를 요구하는 경우 — A14상 workflow prose는 본문 유지가 원칙이므로, 분리가 불가피하면 중단하고 보고
- [ ] SKILL.md 본문이 500줄에 근접(현재 188줄이라 여유 충분하나, 초과 위험 시 중단)

## Implementation Steps
- [ ] Step 1(RED)에 `### Seams` 서브섹션 추가
  - [ ] "새 behavior 테스트 전, 관측할 public seam을 한 문장으로 적는다" 규칙 명시
  - [ ] "기존 seam 우선, 신규 seam 추가는 최후 수단" 규칙 명시
  - [ ] "seam이 불명확/복수이면 진행 전 사용자 확인(질문 예시 포함)" 규칙 명시
  - [ ] `references/test-shape-cookbook.md`를 예시 pointer로 교차 참조(파일명만 언급, force-load `@` 금지)
- [ ] Common Mistakes 섹션에 6번째 항목 "Tautological assertion" 추가
  - [ ] 정의: 기댓값을 production 코드와 동일 로직으로 재계산해 구조적으로 실패 불가능한 테스트
  - [ ] 예시: `expect(add(a, b)).toBe(a + b)`, 손으로 동일 파생한 snapshot, 자기 자신과 비교하는 constant assertion
  - [ ] 교정 방향: 기댓값은 독립 출처(리터럴 값·worked example·spec)에서 가져온다
- [ ] Rationalization Defense 표에 대응 row 추가 및 Workflow wiring(B9)
  - [ ] FR-1용: "seam 확인은 오버헤드다 / 테스트 대상이 뻔하다" → 반박 + Seams 단계로 wiring (1개 이상)
  - [ ] FR-2용: "테스트 통과했으니 됐다 / 로직이 코드와 같아도 상관없다" → 반박 + Common Mistakes 항목으로 wiring (1개)

## Task Verify
- [ ] `grep -n "Seam" claude-code/skills/ywc-tdd-ritual/SKILL.md` → `### Seams` 서브섹션 + RD row 반환
- [ ] `grep -ni "tautolog" claude-code/skills/ywc-tdd-ritual/SKILL.md` → 신규 Common Mistakes 항목 반환
- [ ] `grep -n "test-shape-cookbook" claude-code/skills/ywc-tdd-ritual/SKILL.md` → Seams 절 pointer 반환

## Verification
- [ ] `wc -l claude-code/skills/ywc-tdd-ritual/SKILL.md` ≤ 500 (A8 준수)
- [ ] `ywc-skill-author` Validation Checklist(Frontmatter/Body/Filesystem/Progressive Disclosure) 전부 PASS
- [ ] `bash scripts/validate.sh` exit 0
- [ ] (해당 없음) markdownlint — 대상 glob이 README*/CONTRIBUTING*만 포함하므로 SKILL.md 편집에는 적용되지 않음
