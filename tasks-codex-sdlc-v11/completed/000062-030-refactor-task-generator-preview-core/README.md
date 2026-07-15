# 000062-030-refactor-task-generator-preview-core

## Purpose

`ywc-task-generator`에 deterministic `--spec`, `--preview-only`, `--preview-path`, revision/digest, approval write gate의 core contract를 추가한다.

## Scope

- repository-relative safe spec/preview real-path validation과 canonical identity를 정의한다.
- preview-only no-task-write, approved consume-only, mismatch/collision `NEEDS_CONTEXT` behavior를 정의한다.
- wide-refactor phase/batch/dependency digest binding을 Codex contract로 보완한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-b--preview-approval-is-a-replay-safe-write-gate`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-m--deterministic-task-input-and-auditable-release-evidence`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-n--safe-preview-destinations-and-standard-agentic-spec-propagation`

### Summary

write artifact에는 project-relative `docs/` spec이 필수다. preview digest는 spec path, tasks dir, language, mode, preview path/revision, task rows와 wide-refactor metadata를 bind하며 mismatched identity는 write 전 `NEEDS_CONTEXT`다.

### Out of Scope (from spec)

- README/template/eval asset expansion — `000062-040`.
- agentic caller — `000062-050`.

## Dependencies

### Depends On

- Phase 000061 — validation baseline.

### Depended By

- `000062-040-docs-task-generator-preview-assets` — stable command/identity semantics.
- `000062-050-docs-agentic-preview-flow` — approved two-call contract.
- `000062-060-docs-tech-research-persistence` — consumer input/persistence reference.

## Key Files

- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/wide-refactor-decomposition.md`

## Notes

Main SKILL body must remain <=500 lines; move static examples to direct references. The pre-existing `tasks/000060-*` batch is Claude-oriented reference material only and neither satisfies nor blocks this Codex task.

## Parallel Execution Metadata

### Ownership

- task-generator `SKILL.md` command/workflow contract and new core reference

### Shared Surfaces

- preview artifact schema and wide-refactor representation.

### Conflicts With

- `000062-020-docs-wayfinder-routing-catalog` — shared `SKILL.md`; routing-only edits must be coordinated.

### Parallelizable After

- Phase 000061 complete

### Task Verify

- `wc -l codex/skills/ywc-task-generator/SKILL.md`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

- templates, README locales, agentic logging, task directories themselves.
