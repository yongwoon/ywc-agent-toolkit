# 000060-050-docs-plan-spec-template-seam-pointer — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000060-010-docs-tdd-ritual-red-phase-guards`가 완료(merged)되어 `### Seams` 서브섹션 명칭이 확정되었다
- [ ] `ywc-skill-author`를 먼저 호출해 canonical rule set을 로드했다
- [ ] 변경 전 `grep -c "^## " claude-code/skills/ywc-plan/references/spec-template.md` 값을 기록했다

## Allowed Edit Scope
- [ ] `claude-code/skills/ywc-plan/references/spec-template.md`만 편집한다
- [ ] `ywc-tdd-ritual` 등 다른 파일 편집이 필요하면 중단하고 보고

## Stop Conditions
- [ ] 010이 실제로 merge되지 않았거나 `### Seams` 명칭이 확정되지 않았으면 중단(pointer anchor 부재)
- [ ] 신규 최상위 섹션(`## Testing Decisions` 등)을 만들어야 한다고 판단되면 중단 — AC6이 명시적으로 금지
- [ ] Seams 절차 규칙을 이 파일에 복제 서술하려는 유혹이 생기면 중단(pointer만 유지)

## Implementation Steps
- [ ] `## Acceptance Criteria` 섹션 설명 문단("Preferred form for each AC:" line 52 앞)에 한 줄 추가
  - [ ] 문구 예: "AC를 작성하기 전에 이 그룹이 검증할 test seam(공개 경계)을 한 문장으로 명명하는 것을 권장한다 — 상세 절차는 `ywc-tdd-ritual`의 Seams를 따른다."
  - [ ] 010에서 확정된 `### Seams` 명칭과 정확히 일치하도록 pointer 표기
- [ ] 신규 최상위 `## ` 섹션을 만들지 않았는지 확인

## Task Verify
- [ ] `grep -ni "seam" claude-code/skills/ywc-plan/references/spec-template.md` → Acceptance Criteria 섹션 내 한 줄 반환
- [ ] `grep -c "^## " claude-code/skills/ywc-plan/references/spec-template.md` → Prerequisites에서 기록한 변경 전 값과 동일
- [ ] pointer가 `ywc-tdd-ritual` Seams를 정식 출처로 가리키는지 육안 확인

## Verification
- [ ] `ywc-skill-author` Validation Checklist 전부 PASS
- [ ] `bash scripts/validate.sh` exit 0
- [ ] (해당 없음) markdownlint — references/*.md는 lint glob 대상 아님
