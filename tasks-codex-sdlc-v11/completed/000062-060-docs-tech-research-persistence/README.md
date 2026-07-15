# 000062-060-docs-tech-research-persistence

## Purpose

`ywc-tech-research`에 safe output persistence, overwrite gate, provenance contract를 추가하고 downstream handoff를 Codex 흐름에 맞춘다.

## Scope

- `--output`, `--overwrite`, `--confirm-overwrite`, `--non-interactive` 조합과 허용 저장 경로를 정의한다.
- research report에 fetch date, source URLs, version hints, `[INFERRED]`, known gaps를 남기는 provenance contract를 정의한다.
- plan/spec-ready/task-generator/wayfinder와의 handoff 문구를 Codex 계약에 맞춰 정렬한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-e--safe-research-artifact-persistence-with-overwrite-guardrails`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-i--research-reports-must-separate-evidence-from-inference`
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md#amendment-n--safe-preview-destinations-and-standard-agentic-spec-propagation`

### Summary

research artifact는 repository-relative Markdown으로만 안전하게 저장되어야 하며, overwrite는 명시적 확인 없이는 불가하다. 저장된 문서는 evidence와 inference를 구분하고, 후속 skill이 provenance를 추적할 수 있어야 한다.

### Out of Scope (from spec)

- Wayfinder routing catalog 자체 설계 — `000062-020`.
- task-generator preview core/assets contract — `000062-030`, `000062-040`.
- release checklist와 plugin sync — `000063-010`.

## Dependencies

### Depends On

- `000062-020-docs-wayfinder-routing-catalog` — research caller routing and entry points.
- `000062-040-docs-task-generator-preview-assets` — preview/report artifact language consistency.

### Depended By

- `000063-010-infra-codex-release-evidence` — final evidence matrix and validation log.

## Key Files

- `codex/skills/ywc-tech-research/SKILL.md`
- `codex/skills/ywc-tech-research/references/`
- `codex/skills/ywc-plan/SKILL.md`
- `codex/skills/ywc-spec-ready/SKILL.md`
- `codex/skills/ywc-task-generator/SKILL.md`

## Notes

Allowed output roots must stay repository-relative and deterministic. Absolute paths, `..` escape, symlink escape, and non-Markdown persistence are rejected unless the spec explicitly introduces a new safe root.

## Parallel Execution Metadata

### Ownership

- `ywc-tech-research` persistence/overwrite/provenance contract and related consumer handoff wording

### Shared Surfaces

- report artifact schema, consumer examples, and safe-path language shared with plan/spec/task skills.

### Conflicts With

- `000062-020-docs-wayfinder-routing-catalog`
- `000062-040-docs-task-generator-preview-assets`

### Parallelizable After

- `000062-020-docs-wayfinder-routing-catalog`
- `000062-040-docs-task-generator-preview-assets`

### Task Verify

- `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-tech-research`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

- browsing policy changes, network behavior changes, or non-research skills writing arbitrary files.
