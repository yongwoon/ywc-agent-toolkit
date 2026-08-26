# 000031-050-docs-executor-pr-lang-zh-es

## Purpose

Codex executor/orchestration skills가 `--pr-lang zh`와 `--pr-lang es`를 PR 생성 flow 끝까지 보존하도록 문서화하고 eval coverage를 추가합니다. 대상은 `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-agentic`입니다.

## Scope

- `codex/skills/ywc-sequential-executor/**`의 `--pr-lang` docs, auto-detection examples, delegation examples를 갱신합니다.
- `codex/skills/ywc-parallel-executor/**`의 `--pr-lang` pass-through docs와 aggregate/draft guidance를 갱신합니다.
- `codex/skills/ywc-agentic/**`의 `--pr-lang` forwarding과 explicit task/spec language forwarding guidance를 갱신합니다.
- 각 skill의 README locale set, `agents/openai.yaml`, `evals/evals.json`을 갱신합니다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ywc-sequential-executor-and-ywc-parallel-executor` — executor `--pr-lang` 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ywc-agentic` — agentic forwarding 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ac5---workflow-skills-pass-zhes-unchanged` — pass-through Acceptance Criteria.

### Summary

이 task는 PR language value를 생성하지 않고 보존/전달하는 skills를 담당합니다. `zh`와 `es`가 `ywc-create-pr` 또는 `ywc-finish-branch`까지 unchanged로 전달되도록 instruction과 eval을 맞춥니다. Actual PR title/body generation은 `000031-040`의 책임입니다.

### Out of Scope (from spec)

- `ywc-create-pr` / `ywc-finish-branch` 변경 — `000031-040`.
- PR review reply language — `000031-060`.
- Plugin mirror 직접 수정 — `000032-010`.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000032-010-infra-codex-plugin-sync-validation` — final sync/validation.

## Key Files

- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/README*.md`
- `codex/skills/ywc-sequential-executor/agents/openai.yaml`
- `codex/skills/ywc-sequential-executor/evals/evals.json`
- `codex/skills/ywc-sequential-executor/references/aggregate-pr.md`
- `codex/skills/ywc-sequential-executor/references/branch-lifecycle.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/README*.md`
- `codex/skills/ywc-parallel-executor/agents/openai.yaml`
- `codex/skills/ywc-parallel-executor/evals/evals.json`
- `codex/skills/ywc-parallel-executor/references/aggregate-pr.md`
- `codex/skills/ywc-agentic/SKILL.md`
- `codex/skills/ywc-agentic/README*.md`
- `codex/skills/ywc-agentic/agents/openai.yaml`
- `codex/skills/ywc-agentic/evals/evals.json`

## Notes

- `AGENTS.md`, `CODEX.md`, `CLAUDE.md` language auto-detection examples should mention Chinese/Spanish without changing precedence rules.
- `ywc-agentic` should preserve current behavior: no task `--lang` is passed unless user or project guidance explicitly requests one.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance. Eval JSON validation and targeted grep are sufficient.

### Interface Contract

- Contract: `--pr-lang en|ja|ko|zh|es` pass-through.
- Inputs: executor/agentic invocation with optional `--pr-lang`.
- Outputs: downstream `ywc-create-pr` / `ywc-finish-branch` receives the same language value.
- Error model: absent `--pr-lang` uses existing auto-detection.
- Impacted tests: touched Codex evals.

### Critical Surface Review

- Review requirement: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`
- `codex/skills/ywc-agentic/**`

### Shared Surfaces

- PR language pass-through contract
- aggregate PR references
- executor README/eval metadata

### Conflicts With

- (None identified) — `000031-040` owns PR creation target skills but does not edit executor directories.

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `python3 -m json.tool codex/skills/ywc-sequential-executor/evals/evals.json >/dev/null`
- `python3 -m json.tool codex/skills/ywc-parallel-executor/evals/evals.json >/dev/null`
- `python3 -m json.tool codex/skills/ywc-agentic/evals/evals.json >/dev/null`
- `rg -n "zh|es|Chinese|Spanish|--pr-lang en\\|ja\\|ko\\|zh\\|es" codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor codex/skills/ywc-agentic`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- `codex/skills/ywc-create-pr/**` and `codex/skills/ywc-finish-branch/**`.
- `codex/skills/ywc-handle-pr-reviews/**`.
- Merge strategy, CI wait, bot polling, worktree state machine behavior.
