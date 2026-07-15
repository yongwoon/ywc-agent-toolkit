# 000062-040-docs-task-generator-preview-assets

## Purpose

preview core contract를 task templates, dependency graph representation, README locales, eval fixtures에 반영해 generated artifact와 approval evidence가 하나의 schema를 사용하게 한다.

## Scope

- task preview fields와 `Refactor Phase`/`Batch ID`/`Depends On`을 templates/graph/README에 추가한다.
- valid consume, stale/missing/custom preview mismatch, direct bypass, path safety, missing/inline/mismatched spec fixture를 추가한다.
- current task generator docs/UI assets의 command/output wording을 동기화한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-h--two-phase-autonomous-preview-and-terminal-map-behavior`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-l--observable-discipline-and-refactor-preview-precision`

### Summary

preview와 생성 task directory의 metadata는 같은 refactor/dependency representation을 가져야 한다. fixtures는 structural contract evidence이며 actual task write implementation을 주장하지 않는다.

### Out of Scope (from spec)

- command/identity semantics 변경 — `000062-030`.
- agentic caller update — `000062-050`.

## Dependencies

### Depends On

- `000062-030-refactor-task-generator-preview-core` — stable contract.

### Depended By

- `000062-050-docs-agentic-preview-flow` — invocation fixture basis.
- `000062-060-docs-tech-research-persistence` — current generator consumer contract.

## Key Files

- `codex/skills/ywc-task-generator/{README*,agents/openai.yaml,evals/evals.json,references/**}`

## Notes

template field additions must not overwrite unrelated user task docs; they affect only future generated output.

## Parallel Execution Metadata

### Ownership

- task-generator README/UI/eval/template/reference assets excluding core workflow text

### Shared Surfaces

- preview/task/dependency-graph metadata schema.

### Conflicts With

- `000062-020-docs-wayfinder-routing-catalog` — coordinate any shared README/SKILL routing wording.

### Parallelizable After

- `000062-030-refactor-task-generator-preview-core`

### Task Verify

- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

- agentic log and invocation changes, plugin sync.
