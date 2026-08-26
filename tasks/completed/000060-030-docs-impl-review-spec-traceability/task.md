# 000060-030-docs-impl-review-spec-traceability — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] (None — root task) 선행 task 없음
- [ ] `ywc-skill-author`를 먼저 호출해 canonical rule set(A8/A14)을 로드했다
- [ ] `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md` Amendment C 문구를 대조해 용어 drift 없음 확인

## Allowed Edit Scope
- [ ] `claude-code/skills/ywc-impl-review/SKILL.md`만 편집한다
- [ ] `references/`·agent 파일(040 소관) 편집이 필요하면 중단하고 보고

## Stop Conditions
- [ ] `ywc-skill-author` 선행 호출 없이 structural edit을 시작해야 하는 상황이면 중단
- [ ] `--spec` 두 분기(생략=valid vs 공급됐으나 missing=BLOCKED)를 하나로 합치려는 유혹이 생기면 중단 — Amendment C 핵심 정밀화
- [ ] 신규 6번째 subagent가 필요하다고 판단되면 중단(aggregate-only 원칙 위반)

## Implementation Steps
- [ ] `## Output Format`의 `### Testing (QA)`와 `### Fix Priority` 사이에 `### Spec Traceability` 추가(~20줄)
  - [ ] 4열 matrix 정의: `Criterion` / `Status` / `Evidence` / `Scope-creep note`
  - [ ] Status 4단계 정의: `Implemented` / `Partial` / `Missing` / `Not Verifiable`
  - [ ] Evidence 규칙: `Implemented`/`Partial`은 file:line·named test/output·command output 필수, task 이름·commit 메시지 추론 금지
  - [ ] Evidence 출처: Architecture "Structural Spec Conformance" + Design "Contract Spec Conformance" aggregation(신규 워커 없음)
  - [ ] `Not Verifiable`(AC 존재하나 evidence 없음) vs "No spec available"(spec 부재) 구분 명시
  - [ ] Scope creep은 각 행 `Scope-creep note` 또는 별도 sub-bullet으로 보고
- [ ] `--spec` argument를 required → optional로 변경(argument table 갱신)
  - [ ] 생략 시: 5개 lane 정상 실행, aggregate에 `### Spec Traceability` → "No spec available"만, AC 행 미생성
  - [ ] 공급됐으나 파일 없음/읽기불가: BLOCKED(현행 line 169 semantics 유지)
- [ ] HTML parity: `--format html` 모드에서 matrix 동일 렌더(html-output 규약 준수), Markdown surface 보존
- [ ] `## Confidence Gate`의 "Evidence quality" 차원과 1줄 pointer 교차 참조(중복 서술 없이)
- [ ] 기존 `[P1]`/`[P2]` 마커·severity 기호·5-subagent Phase1/Phase2 구조 불변 확인

## Task Verify
- [ ] `grep -n "Spec Traceability" claude-code/skills/ywc-impl-review/SKILL.md` → Testing과 Fix Priority 사이 line 반환
- [ ] `grep -ni "not verifiable" claude-code/skills/ywc-impl-review/SKILL.md` → 4단계 Status 정의 반환
- [ ] `--spec` argument 항목이 optional로 갱신되었는지 육안 확인

## Verification
- [ ] `wc -l claude-code/skills/ywc-impl-review/SKILL.md` ≤ 500 (A8)
- [ ] `ywc-skill-author` Validation Checklist 전부 PASS
- [ ] `bash scripts/validate.sh` exit 0
- [ ] (해당 없음) markdownlint — SKILL.md는 lint glob 대상 아님
