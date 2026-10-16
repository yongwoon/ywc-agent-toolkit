# yw-000062-020-docs-model-hint-routing — Implementation Checklist

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
- [ ] routing 계약 (upstream `cc-288`, 적응)
  - [ ] `references/model-routing.md`: Values / Assignment Rules (M1 적응식) / Consumption / Version floor / effective model source 라벨
  - [ ] Escalation 문단 제외
- [ ] task-generator
  - [ ] `README.md.template` 의 `### Ownership` 앞에 Model Hint 줄
  - [ ] `parallel-execution-metadata.md` 에 할당 규칙 pointer + 판정 순서
  - [ ] `SKILL.md` 에 할당 단계 pointer 1 줄 + Step 11 항목 1 줄
- [ ] parallel-executor
  - [ ] Step 1 TaskInfo 파싱 목록에 Model Hint
  - [ ] Step 3 Agent Hint override 다음에 Model Hint 처리 1 줄 (subagent_type 과 독립)
  - [ ] Step 4b implementer dispatch 에 `model` 전달, Step 5 에 `<model> (<source>)` 1 줄 (FM-3)
- [ ] README Tier 1
  - [ ] 두 skill 의 README.md / en / ja / ko 에 Model Hint 설명 동기 추가

## Acceptance Coverage
Covers: AC-1, AC-10, AC-13, AC-16, AC-17 (README 부분)

## Task Verify
- [ ] `grep -c "Model Hint" claude-code/skills/references/model-routing.md claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md` 각 ≥1 (AC-10)
- [ ] `grep -c "CLAUDE_CODE_SUBAGENT_MODEL" claude-code/skills/references/model-routing.md` ≥1, `grep -c "Model Hint" claude-code/skills/ywc-task-generator/references/README.md.template claude-code/skills/ywc-task-generator/references/parallel-execution-metadata.md` 각 ≥1 (AC-16)
- [ ] `grep -c "Model Hint" claude-code/skills/ywc-parallel-executor/README.md claude-code/skills/ywc-parallel-executor/README.en.md claude-code/skills/ywc-parallel-executor/README.ja.md claude-code/skills/ywc-parallel-executor/README.ko.md` 및 task-generator 동일 각 ≥1 (AC-17)
- [ ] `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- [ ] 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Verification
- [ ] `bash scripts/validate.sh` passes (skill structure, README locale set, shellcheck, link and loop-only-tool checks)
- [ ] `npx markdownlint-cli2@0.22.1` on any changed `README*.md` passes (CI markdownlint scope)
- [ ] No `ScheduleWakeup(` call syntax introduced under `claude-code/skills/` (`scripts/validate.sh:752`)

## Implementation Notes (optional)

