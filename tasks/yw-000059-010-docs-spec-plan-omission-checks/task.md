# yw-000059-010-docs-spec-plan-omission-checks — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yw-000058-010-docs-named-agent-release` is completed (merged)
- [ ] `main` 최신화 후 feature branch 생성 (`feature/<task-name>`)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if the upstream diff hunk referenced in a step no longer matches this repo's section/step numbering in a way the spec did not anticipate
- [ ] Stop if a touched SKILL.md would exceed 500 lines and the designated `references/` split target cannot absorb it

## Implementation Steps
- [ ] spec-validate UI check (upstream `cc-257`)
  - [ ] `references/ui-qa-lenses.md` 신규 (10 lens 표)
  - [ ] Data Integrity check 다음에 UI/Interaction Omission Check 단계, Review Dimensions 매핑, rationalization 행 추가 (`Action required` 링크는 `references/ui-qa-lenses.md`)
- [ ] ywc-plan Failure Modes (upstream `cc-268`)
  - [ ] `SKILL.md` must-include 목록, Pass A 행, Validation checklist 에 Failure Modes
  - [ ] `spec-template.md` 에 `## Failure Modes` 섹션 + worked example 1 행, Existing Constraints interaction `reuse`, AC seam prior-art 인용
- [ ] task-generator coverage (upstream `cc-268`, 적응)
  - [ ] Step 11 (`:398`) 에 Spec coverage / Interface consistency 항목, Principle 1 에 Right-Sizing 규칙
  - [ ] 미매핑 항목은 Step 11 결과 요약 `Unmapped spec items: <id 목록>` 으로 보고 (상태 체계 신설 없음)
- [ ] spec-ready 자동 pass (upstream `cc-266`)
  - [ ] `:40` rationalization 행, `:85-95` Step 4, `:153` Common Mistakes 를 "exactly one suggestion-focused amendment pass, never ask" 로 정합화

## Acceptance Coverage
Covers: AC-1, AC-5, AC-6, AC-7, AC-12 (FR-B3 부분), AC-13, AC-14

## Task Verify
- [ ] `grep -c "Failure Modes" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-plan/references/spec-template.md` 각 ≥1 (AC-5)
- [ ] `grep -n "ask the user" claude-code/skills/ywc-spec-ready/SKILL.md` 에 Suggestion pass 질문 문구 없음 (AC-6)
- [ ] `test -f claude-code/skills/ywc-spec-validate/references/ui-qa-lenses.md` exit 0 + SKILL.md 상대 링크 (AC-7)
- [ ] `grep -c "Spec coverage\|Interface consistency" claude-code/skills/ywc-task-generator/SKILL.md` ≥1 (AC-12 B3)
- [ ] `grep -c "exactly one suggestion-focused" claude-code/skills/ywc-spec-ready/SKILL.md` ≥1 (AC-14)
- [ ] `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- [ ] 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Verification
- [ ] `bash scripts/validate.sh` passes (skill structure, README locale set, shellcheck, link and loop-only-tool checks)
- [ ] `npx markdownlint-cli2@0.22.1` on any changed `README*.md` passes (CI markdownlint scope)
- [ ] No `ScheduleWakeup(` call syntax introduced under `claude-code/skills/` (`scripts/validate.sh:752`)

## Implementation Notes (optional)

