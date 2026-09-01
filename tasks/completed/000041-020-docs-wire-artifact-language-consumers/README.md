# 000041-020-docs-wire-artifact-language-consumers

## Purpose

Task/spec/testcase/project documentation을 생성하는 Codex skills가 새 shared language resolution policy를 사용하도록 정렬한다. 이 task 는 artifact prose 언어를 결정하는 skill-local defaults를 제거하고, config/guidance/user fallback 순서를 적용한다.

## Scope

- `ywc-task-generator`, `ywc-spec-writer`, `ywc-gen-testcase`, `ywc-project-docs`의 language resolution 섹션 갱신.
- 각 skill의 language-policy reference와 README locale files 중 old default 를 설명하는 부분 갱신.
- 기존 alias 및 locale writing rules 보존.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-ywc-language-setup.md` — AC4-AC9, FR-4, FR-5, FR-6, Edge Cases.

### Summary

현재 artifact-generating skills는 서로 다른 language fallback을 가진다. 이 task 는 explicit `--lang`이 없을 때 `.codex/ywc.json`, project guidance, `~/.codex/ywc.json`, ask user 순서로 resolve 하도록 문구를 정렬한다. `ywc-project-docs`의 `kr` alias 같은 기존 user-facing alias는 유지하되 canonical config 저장값은 `ko`로 맞춘다.

### Out of Scope (from spec)

- PR/orchestration language flags — `000041-030-docs-wire-pr-orchestration-consumers`.
- `ywc-setup` 신규 skill — `000041-010-docs-codex-ywc-setup-skill`.
- Catalog/root docs — `000041-040-docs-catalog-language-setup`.

## Dependencies

### Depends On

- `000040-010-docs-codex-language-resolution-reference` — shared policy exists.

### Depended By

- `000042-010-infra-codex-language-setup-validation` — targeted search and validation.

## Key Files

- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/language-policy.md`
- `codex/skills/ywc-task-generator/README*.md`
- `codex/skills/ywc-spec-writer/SKILL.md`
- `codex/skills/ywc-spec-writer/references/language-policy.md`
- `codex/skills/ywc-spec-writer/README*.md`
- `codex/skills/ywc-gen-testcase/SKILL.md`
- `codex/skills/ywc-gen-testcase/README*.md`
- `codex/skills/ywc-project-docs/SKILL.md`
- `codex/skills/ywc-project-docs/README*.md`

## Notes

- Do not change task granularity mode behavior.
- Do not remove technical-term-in-English writing rules.
- `ywc-gen-testcase` currently uses recent testsheets and README language as heuristics; decide in implementation whether those become lower-priority artifact-local hints after user config or are removed for strict policy. Preserve AC8: no final English fallback.
- README updates should focus on user-visible default behavior, not a full rewrite.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only skill instruction changes; targeted grep plus `bash scripts/validate.sh`.

### Interface Contract

- Contract: artifact language resolution for generated Markdown/HTML prose.
- Inputs: `--lang`, `.codex/ywc.json`, project guidance, `~/.codex/ywc.json`, user answer.
- Outputs: resolved prose language for task docs, specs, testsheets, project docs.
- Error model: unresolved config/guidance falls through; no skill default.
- Impacted tests: targeted `rg`, repository validation.

### Critical Surface Review

- Review requirement: N/A — docs-only skill instruction changes.

### Data Integrity Hardening

- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-task-generator/**`
- `codex/skills/ywc-spec-writer/**`
- `codex/skills/ywc-gen-testcase/**`
- `codex/skills/ywc-project-docs/**`

### Shared Surfaces

- Shared language resolution reference (read-only).
- Generated artifact language policy.

### Conflicts With

- (None identified)

### Parallelizable After

- `000040-010-docs-codex-language-resolution-reference`

### Task Verify

- `grep -q "language-resolution.md" codex/skills/ywc-task-generator/SKILL.md`
- `grep -q "language-resolution.md" codex/skills/ywc-spec-writer/SKILL.md`
- `grep -q "language-resolution.md" codex/skills/ywc-gen-testcase/SKILL.md`
- `grep -q "language-resolution.md" codex/skills/ywc-project-docs/SKILL.md`
- `! rg -n "Default:.*(ko|en)|default:.*(ko|en)|Default is Korean|Fallback.*English" codex/skills/ywc-task-generator codex/skills/ywc-spec-writer codex/skills/ywc-gen-testcase codex/skills/ywc-project-docs`

## Out of Scope

- Editing PR/executor/orchestration skills.
- Adding or changing scripts.
- Generated plugin package sync.
