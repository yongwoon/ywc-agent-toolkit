# 000041-030-docs-wire-pr-orchestration-consumers

## Purpose

PR title/body 및 orchestration 흐름에서 쓰이는 language flags를 shared language resolution policy와 맞춘다. 이 task 는 PR 생성, branch finishing, sequential/parallel executor, agentic orchestration의 omitted/auto language path를 정렬한다.

## Scope

- `ywc-create-pr` language initialization 갱신.
- `ywc-agentic`의 `--pr-lang auto` 및 task/spec language forwarding 설명 갱신.
- `ywc-finish-branch`, `ywc-sequential-executor`, `ywc-parallel-executor`의 `--pr-lang` auto/default 설명 갱신.
- 관련 README locale files 갱신.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-ywc-language-setup.md` — AC4-AC9, FR-5, FR-6, Edge Cases.

### Summary

PR/orchestration skills는 `--lang` 또는 `--pr-lang`이 명시되면 그대로 사용해야 한다. Auto 또는 omitted path는 `.codex/ywc.json`, project guidance, `~/.codex/ywc.json`, ask user 순서로 해석해야 하며, 최근 PR 같은 heuristic은 user config 보다 앞서면 안 된다. Explicit title/body는 user-authored content 로 보존할 수 있지만, generated prose에는 resolved language가 적용된다.

### Out of Scope (from spec)

- Artifact documentation skills — `000041-020-docs-wire-artifact-language-consumers`.
- New `ywc-setup` skill — `000041-010-docs-codex-ywc-setup-skill`.
- Root/Codex catalog docs — `000041-040-docs-catalog-language-setup`.

## Dependencies

### Depends On

- `000040-010-docs-codex-language-resolution-reference` — shared policy exists.

### Depended By

- `000042-010-infra-codex-language-setup-validation` — targeted search and validation.

## Key Files

- `codex/skills/ywc-create-pr/SKILL.md`
- `codex/skills/ywc-create-pr/README*.md`
- `codex/skills/ywc-agentic/SKILL.md`
- `codex/skills/ywc-agentic/README*.md`
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-finish-branch/README*.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/README*.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/README*.md`

## Notes

- `--pr-lang` remains a specialized explicit flag and should be forwarded unchanged when present.
- `--title` in `ywc-create-pr` remains verbatim; shared resolution controls generated body prose when body is generated.
- Do not translate branch names, task IDs, labels, code blocks, YAML/JSON keys, commands, or other machine identifiers.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only skill instruction changes; targeted grep plus repository validation.

### Interface Contract

- Contract: PR/orchestration language resolution.
- Inputs: `--lang`, `--pr-lang`, title/body arguments, shared config tiers.
- Outputs: generated PR title/body/task forwarding language.
- Error model: unresolved auto/omitted language asks user where appropriate; no skill default.
- Impacted tests: targeted `rg`, repository validation.

### Critical Surface Review

- Review requirement: N/A — docs-only PR prose policy.

### Data Integrity Hardening

- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-create-pr/**`
- `codex/skills/ywc-agentic/**`
- `codex/skills/ywc-finish-branch/**`
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`

### Shared Surfaces

- PR language contract.
- Shared language resolution reference (read-only).

### Conflicts With

- (None identified)

### Parallelizable After

- `000040-010-docs-codex-language-resolution-reference`

### Task Verify

- `grep -q "language-resolution.md" codex/skills/ywc-create-pr/SKILL.md`
- `grep -q "language-resolution.md" codex/skills/ywc-agentic/SKILL.md`
- `grep -q "language-resolution.md" codex/skills/ywc-finish-branch/SKILL.md`
- `grep -q "language-resolution.md" codex/skills/ywc-sequential-executor/SKILL.md`
- `grep -q "language-resolution.md" codex/skills/ywc-parallel-executor/SKILL.md`
- `rg -n "--pr-lang|--lang" codex/skills/ywc-create-pr codex/skills/ywc-agentic codex/skills/ywc-finish-branch codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`

## Out of Scope

- Changing git/gh behavior.
- Changing commit message conventions unless a searched Codex skill explicitly generates language-sensitive prose from shared config.
- Generated plugin package sync.
