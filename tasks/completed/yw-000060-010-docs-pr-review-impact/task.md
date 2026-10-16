# yw-000060-010-docs-pr-review-impact — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yw-000059-010-docs-spec-plan-omission-checks` is completed (merged)
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
- [ ] create-pr Impact (upstream `cc-258`)
  - [ ] Rationalization Defense 에 diff 재조회 금지 행
  - [ ] `:264` 를 "Step 6.5 에서 읽은 diff 재사용" 으로
  - [ ] Step 7 에 optional Impact (behavior change 판정, 5 언어 heading 표, template, diff 근거 한정)
- [ ] gen-testcase Impact (upstream `cc-260`, Impact 부분만)
  - [ ] `:96` 에 Impact 블록 lift 문장
  - [ ] `:195` 시나리오 소스 1 번에 Impact Before/After
- [ ] impl-review SDK 예외 계층 (upstream `cc-262`)
  - [ ] `devex-agent.md` §3 에 bullet
  - [ ] `coderabbit-methodology.md` §4 근처에 verify-before-surface 문단

## Acceptance Coverage
Covers: AC-1, AC-8, AC-12 (FR-C3 부분), AC-13

## Task Verify
- [ ] `grep -n "Impact" claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-gen-testcase/SKILL.md` → create-pr Step 7 5 언어 표 + gen-testcase 시나리오 소스 1 번 (AC-8)
- [ ] `grep -c "exception hierarchy\|exception taxonomy" claude-code/skills/ywc-impl-review/references/devex-agent.md claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md` 각 ≥1 (AC-12 C3)
- [ ] `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- [ ] 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Verification
- [ ] `bash scripts/validate.sh` passes (skill structure, README locale set, shellcheck, link and loop-only-tool checks)
- [ ] `npx markdownlint-cli2@0.22.1` on any changed `README*.md` passes (CI markdownlint scope)
- [ ] No `ScheduleWakeup(` call syntax introduced under `claude-code/skills/` (`scripts/validate.sh:752`)

## Implementation Notes (optional)

