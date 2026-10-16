# yw-000062-010-docs-trigger-boundary-descriptions — Implementation Checklist

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
- [ ] description 경계 (upstream `cc-263`)
  - [ ] 각 대상 파일에 upstream hunk 의 경계 문구 반영 (식별 token 포함)
  - [ ] ui-ux-review 는 기존 문구를 줄여 단어 수 순증가 0
  - [ ] product-review `:150` 근처 문장을 verify-before-surface 규칙으로 교체

## Acceptance Coverage
Covers: AC-1, AC-12 (FR-E1 부분), AC-13, AC-17 (description 부분)

## Task Verify
- [ ] `grep -c "manual verification testsheet" claude-code/agents/ywc-qa-engineer.md` ≥1 (AC-12 E1)
- [ ] `grep -c "repo-wide" claude-code/agents/ywc-refactor-cleaner.md`, `grep -c "spec-verification" claude-code/skills/ywc-code-gen/SKILL.md`, `grep -c "AI-generated" claude-code/skills/ywc-ui-ux-review/SKILL.md`, `grep -c "ROI" claude-code/skills/ywc-tech-research/SKILL.md`, `grep -c "ad-hoc threat-model" claude-code/skills/ywc-security-audit/SKILL.md` 각 ≥1 (AC-17)
- [ ] `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- [ ] 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Verification
- [ ] `bash scripts/validate.sh` passes (skill structure, README locale set, shellcheck, link and loop-only-tool checks)
- [ ] `npx markdownlint-cli2@0.22.1` on any changed `README*.md` passes (CI markdownlint scope)
- [ ] No `ScheduleWakeup(` call syntax introduced under `claude-code/skills/` (`scripts/validate.sh:752`)

## Implementation Notes (optional)

