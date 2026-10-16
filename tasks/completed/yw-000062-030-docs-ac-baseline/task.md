# yw-000062-030-docs-ac-baseline — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yw-000061-010-docs-fastify-scaffold` is completed (merged)
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
- [ ] Baseline (upstream `cc-282`, Baseline 부분)
  - [ ] ywc-plan Pass B 에 Baseline 행, Validation 에 체크 항목
  - [ ] spec-template AC 예시를 `… Baseline: <exit code> — <one-line output on the pre-change tree>.` 형식으로
  - [ ] spec-validate Phase 1 Feasibility 행과 Review Dimensions 에 allowlist 재실행 / `unverifiable-ac` / `missing-ac-baseline` 규칙

## Acceptance Coverage
Covers: AC-1, AC-11, AC-13

## Task Verify
- [ ] `grep -n "Baseline:" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-plan/references/spec-template.md claude-code/skills/ywc-spec-validate/SKILL.md` → Pass B 행, Validation, template AC 형식, Feasibility 에 각각 존재 (AC-11)
- [ ] `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- [ ] 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Verification
- [ ] `bash scripts/validate.sh` passes (skill structure, README locale set, shellcheck, link and loop-only-tool checks)
- [ ] `npx markdownlint-cli2@0.22.1` on any changed `README*.md` passes (CI markdownlint scope)
- [ ] No `ScheduleWakeup(` call syntax introduced under `claude-code/skills/` (`scripts/validate.sh:752`)

## Implementation Notes (optional)

