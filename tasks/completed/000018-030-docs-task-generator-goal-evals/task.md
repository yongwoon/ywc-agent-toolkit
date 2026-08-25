# 000018-030-docs-task-generator-goal-evals — Implementation Checklist

## Prerequisites

- [ ] `000018-010-docs-principles-foundation` 완료(merged)

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-task-generator/**`만 편집
- [ ] Ownership 밖 편집 필요 시 중단·보고

## Stop Conditions

- [ ] task.md.template 간결 구조를 해체해야 하면 중단(필드 추가만)
- [ ] evals 하니스 패턴이 없어 객관적 케이스 작성이 불가하면 사유 기록 후 진행

## Implementation Steps

- [ ] **FR-4 Final Validation 체크 추가** — "각 Task Verify는 태스크 동작이 없으면 실패하는 태스크별 단언 ≥1개 포함(전역 build/lint만은 불충분)"
- [ ] **FR-4 Rationalization 행** — "Task Verify=build면 충분 → green build는 컴파일만 증명; 태스크 산출을 단언해야"
- [ ] **FR-4 per-task Acceptance Criteria 하위절** — task.md Core Elements에 When/does/observable-as 형태, Implementation Steps와 구분
- [ ] **FR-4 Assumptions 필드** — Notes에 분해 중 해소한 모호성·선택 해석 기록
- [ ] **FR-12 eval 회귀** — `evals/evals.json` 기존 형식 확인 후 (a)verifiable Task Verify (b)AC (c)Assumptions 단언 케이스 ≥1개 추가; 불가 시 구현 노트에 사유
- [ ] **README 동기화(§A7)** — README.md/ko/en/ja 4종

## Task Verify

- [ ] `rg -n "Acceptance Criteria|Assumptions" claude-code/skills/ywc-task-generator/SKILL.md`
- [ ] `rg -n "verifiable|태스크별 단언|build" claude-code/skills/ywc-task-generator/SKILL.md`
- [ ] eval 케이스 추가 확인 또는 구현 노트의 불가 사유 존재
- [ ] README 4종 반영

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] markdownlint 통과(변경 README)
- [ ] eval JSON 파싱 유효(`python3 -c "import json;json.load(open('claude-code/skills/ywc-task-generator/evals/evals.json'))"` 또는 동등)
