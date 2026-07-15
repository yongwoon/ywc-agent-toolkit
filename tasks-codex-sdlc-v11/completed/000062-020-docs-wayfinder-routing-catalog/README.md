# 000062-020-docs-wayfinder-routing-catalog

## Purpose

Wayfinder와 기존 planning/discovery skill 간 activation boundary, handoff, catalog discoverability를 일관되게 연결한다.

## Scope

- `ywc-plan`, `ywc-brainstorm`, `ywc-tech-research`, `ywc-agentic`, `ywc-spec-ready`, `ywc-task-generator`의 relevant routing text를 Wayfinder contract에 맞춘다.
- Codex catalog/README에 Wayfinder를 등록하고 routing eval을 추가한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#fr-5-metadata-routing-and-documentation`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-e--safe-research-persistence-and-consumer-handoff`

### Summary

Wayfinder는 ordinary plan/brainstorming을 대체하지 않고 destination은 있으나 여러 unresolved decision이 있는 large discovery만 받는다. downstream consumer는 persisted research와 map handoff를 project-relative reference로 보존한다.

### Out of Scope (from spec)

- research output/overwrite implementation — `000062-060`.

## Dependencies

### Depends On

- `000062-010-docs-wayfinder-core` — stable map/ticket terminology와 asset 제공.

### Depended By

- `000062-060-docs-tech-research-persistence` — consumer persistence handoff wording 제공.
- `000063-010-infra-codex-release-evidence` — catalog source completion 필요.

## Key Files

- `codex/skills/{ywc-plan,ywc-brainstorm,ywc-tech-research,ywc-agentic,ywc-spec-ready,ywc-task-generator}/SKILL.md`
- `codex/skills/README.md`

## Notes

각 skill 본문이 길어지면 existing direct reference pattern을 사용한다. task-generator detailed preview rule은 `000062-030/040`만 소유한다.

## Parallel Execution Metadata

### Ownership

- listed routing paragraphs and `codex/skills/README.md`

### Shared Surfaces

- cross-skill activation/handoff vocabulary.

### Conflicts With

- `000062-030-refactor-task-generator-preview-core`, `000062-040-docs-task-generator-preview-assets` — `ywc-task-generator` shared skill; coordinate and do not edit their argument/template sections.

### Parallelizable After

- `000062-010-docs-wayfinder-core`

### Task Verify

- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

- preview gate, research path implementation, plugin sync.
