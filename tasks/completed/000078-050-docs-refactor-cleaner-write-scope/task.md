# 000078-050-docs-refactor-cleaner-write-scope — Implementation Checklist

## Prerequisites

- [ ] (None — root task)
- [ ] 변경 전 `grep -c "DONE_WITH_CONCERNS" claude-code/agents/ywc-refactor-cleaner.md` 값을 기록했다 (증가 확인용 baseline)
- [ ] `claude-code/agents/ywc-refactor-cleaner.md` 의 6개 section 순서를 확인했다 (Mission / Triggers / Boundaries / Success Criteria / Return Contract / Anti-patterns)

## Allowed Edit Scope

- [ ] `claude-code/agents/ywc-refactor-cleaner.md` 만 편집한다
- [ ] frontmatter `tools:` 행(`:19`)은 편집하지 않는다
- [ ] Ownership 밖 편집이 필요하면 중단하고 보고한다

## Stop Conditions

- [ ] Boundaries "Will NOT" 목록(`:45`)을 특정할 수 없으면 중단
- [ ] Anti-patterns 표(`:118-128`)의 행 구조를 특정할 수 없으면 중단
- [ ] `Write` grant를 제거해야 한다고 판단되면 중단 (spec이 검토 후 기각한 안)
- [ ] Return Contract를 inline으로 재정의해야 한다고 판단되면 중단 (AC13 위반)
- [ ] `permissionMode` 를 추가해야 한다고 판단되면 중단

## Implementation Steps

- [ ] **FR-5a — Mission 1문장 추가** (`:29` 부근)
  - [ ] 삭제는 `Edit` **전용**임을 명시한다 (기존 "surgical removal via the `Edit` tool" 규정과 정합)
  - [ ] `Write` 의 **유일한 정당 용도**가 parent artifact directory 아래의 per-item evidence 파일임을 명시한다
- [ ] **FR-5b — Boundaries "Will NOT" 항목 1개 추가** (`:45` 목록)
  - [ ] 다음 취지의 항목을 추가한다: "does NOT use `Write` for production source or any file outside the parent's artifact directory; if such a need arises, return `DONE_WITH_CONCERNS` to the parent instead."
  - [ ] `DONE_WITH_CONCERNS` 단어가 문자 그대로 포함되어야 한다 (AC12 필수)
  - [ ] 기존 8개 항목은 삭제하거나 재작성하지 않는다
- [ ] **FR-5c — Anti-patterns 표 1행 추가** (`:118-128`)
  - [ ] anti-pattern: "삭제 대신 `Write` 로 파일을 통째로 재작성"
  - [ ] 사유: bisect 대상 오염 + Mission의 Edit-only 규정 위반
  - [ ] 대체 행동: `Edit` 기반 surgical 삭제
  - [ ] 기존 `:128` 의 evidence 파일 산출 요구 행은 유지한다 (`Write` grant의 존재 근거)
- [ ] **AC13 — 구조 보존 확인**
  - [ ] 6개 section의 존재와 순서가 유지되었는지 확인한다
  - [ ] Return Contract가 inline 재정의 없이 참조만 유지하는지 확인한다
  - [ ] frontmatter `name:` / `description:` 이 온전한지 확인한다 (`scripts/validate.sh:524,529`)

## Task Verify

- [ ] `grep -c "DONE_WITH_CONCERNS" claude-code/agents/ywc-refactor-cleaner.md` — Prerequisites baseline 보다 **증가**
- [ ] `git diff -- claude-code/agents/ywc-refactor-cleaner.md | grep -c "^[+-]tools:"` — **0** (AC12)
- [ ] `grep -nE "^## (Mission|Triggers|Boundaries|Success Criteria|Return Contract|Anti-patterns)" claude-code/agents/ywc-refactor-cleaner.md` — 6개가 원래 순서대로 출력 (AC13)
- [ ] `grep -c "permissionMode" claude-code/agents/ywc-refactor-cleaner.md` — **0**
- [ ] Anti-patterns 표에 새 행 1개가 추가되고 기존 행이 삭제되지 않았음을 육안 확인

## Verification

- [ ] `bash scripts/validate.sh` 통과 (agent frontmatter `name:` / `description:` 검증 포함)
- [ ] markdownlint 통과 — `.github/workflows/markdownlint.yml` 의 실제 invocation 형태를 재현한다
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --format json` 으로 read-only 확인
- [ ] `git diff --name-only | grep -c '^codex/'` — 0 (AC17)

## Implementation Notes
