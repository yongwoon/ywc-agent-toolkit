# 000016-030-docs-task-template-goal-verification

## Purpose
`ywc-task-generator` task template이 generated task마다 goal, AC/FR, verification evidence를 명시하도록 개선한다. 이 task는 future implementation tasks가 "무엇을 왜 검증하는지"를 잃지 않게 만든다.

## Scope
- `codex/skills/ywc-task-generator/references/task.md.template`의 Implementation Steps 구조 보강
- Task Verify section에 pre-change failing evidence / exception, contract/test evidence 추가
- `ywc-task-generator` eval에 objective regression case 추가 또는 기존 coverage 근거 문서화

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-3-update-task-generator-template` — template 요구사항
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-6-update-evals-where-objective` — eval 요구사항
- `codex/skills/ywc-task-generator/references/task.md.template` — 수정 대상 template

### Summary
이 task는 task generator가 만드는 `task.md`에 traceability를 추가한다. 각 Implementation Step은 target file/module, related AC/FR, contract/behavior change, verification command/evidence를 드러내야 한다. Template은 짧게 유지하고 tutorial처럼 길어지지 않아야 한다.

### Out of Scope (from spec)
- Shared principles 변경 — handled by `000016-010-docs-principles-guideline-gap`
- `ywc-code-gen` worker prompt 변경 — handled by `000016-020-docs-code-gen-worker-discipline`
- generated plugin sync/validation — handled by `000017-010-infra-codex-karpathy-validation`

## Dependencies

### Depends On
- `000016-010-docs-principles-guideline-gap` — goal-driven execution vocabulary

### Depended By
- `000017-010-infra-codex-karpathy-validation` — generated plugin sync and validation

## Key Files
- `codex/skills/ywc-task-generator/references/task.md.template` — generated task checklist template
- `codex/skills/ywc-task-generator/evals/evals.json` — objective eval cases if supported

## Notes
- This repository's current task template is itself the behavior being improved; generated files in this batch may already model the desired shape.
- Keep the template concise and placeholder-driven.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-task-generator/references/task.md.template`
- `codex/skills/ywc-task-generator/evals/evals.json`

### Shared Surfaces
- Generated task contract: `task.md` template
- Eval harness: `codex/skills/ywc-task-generator/evals/evals.json`

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000016-010-docs-principles-guideline-gap`

### Task Verify
- `rg -n "Related AC/FR|Contract / Behavior Change|Verification Command / Evidence|Pre-change Failing Evidence|Exception" codex/skills/ywc-task-generator/references/task.md.template`
- `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-task-generator --format json`

## Out of Scope
- Rewriting the task generator workflow.
- Changing task numbering, category, or phase rules.
- Editing generated plugin package manually.
