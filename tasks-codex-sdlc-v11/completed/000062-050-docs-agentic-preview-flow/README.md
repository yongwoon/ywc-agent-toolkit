# 000062-050-docs-agentic-preview-flow

## Purpose

`ywc-agentic` Medium/Large Task Phase가 fixed spec path를 두 task-generator call에 전달하고 preview identity를 검증·UTC log하는 auditable autonomous flow를 갖게 한다.

## Scope

- preview-only then approved consume의 exactly two-call invocation을 정의한다.
- `--spec docs/ywc-plans/agentic-<slug>-iter1.md`, mode/lang/tasks-dir, returned preview path/revision/digest logging을 추가한다.
- normal and error/bypass fixtures를 업데이트한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-h--two-phase-autonomous-preview-and-terminal-map-behavior`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-n--safe-preview-destinations-and-standard-agentic-spec-propagation`

### Summary

agentic만 explicit non-interactive approval을 사용할 수 있다. second call은 first call의 matching persisted preview만 소비하며, missing/stale/mismatch/bypass는 task artifacts를 만들지 않고 `NEEDS_CONTEXT`다.

### Out of Scope (from spec)

- task-generator core/assets, interactive user approval behavior.

## Dependencies

### Depends On

- `000062-040-docs-task-generator-preview-assets` — complete invocation contract and fixtures.

### Depended By

- `000063-010-infra-codex-release-evidence` — agentic changed-skill validation evidence.

## Key Files

- `codex/skills/ywc-agentic/{SKILL.md,README*,agents/openai.yaml,evals/evals.json}`

## Notes

No environment-variable or implicit-state approval bypass is allowed. Re-plan keeps the original/amended spec file path rather than inventing a new input identity.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-agentic/**`

### Shared Surfaces

- task-generator preview invocation/log schema.

### Conflicts With

- `(None identified)` after `000062-040` merge.

### Parallelizable After

- `000062-040-docs-task-generator-preview-assets`

### Task Verify

- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

- generator behavior implementation, plugin sync.
