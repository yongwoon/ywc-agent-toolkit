# yw-000061-010-docs-fastify-scaffold — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yw-000060-010-docs-pr-review-impact` is completed (merged)
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
- [ ] Fastify 섹션 (upstream `cc-251`)
  - [ ] `## Fastify` + `### Fastify Small` / `Medium` / `Large` 와 각 Key Points
  - [ ] TOC 에 링크 추가, anchor 확인

## Acceptance Coverage
Covers: AC-1, AC-9

## Task Verify
- [ ] `grep -c "^### Fastify" claude-code/skills/ywc-project-scaffold/references/javascript.md` → 3 + TOC 링크 존재 (AC-9)
- [ ] `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- [ ] 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Verification
- [ ] `bash scripts/validate.sh` passes (skill structure, README locale set, shellcheck, link and loop-only-tool checks)
- [ ] `npx markdownlint-cli2@0.22.1` on any changed `README*.md` passes (CI markdownlint scope)
- [ ] No `ScheduleWakeup(` call syntax introduced under `claude-code/skills/` (`scripts/validate.sh:752`)

## Implementation Notes (optional)

