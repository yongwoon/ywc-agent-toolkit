# 000031-040-docs-pr-creation-language-zh-es

## Purpose

Codex PR 생성/마무리 skill이 PR title/body language로 Chinese(`zh`)와 Spanish(`es`)를 first-class option으로 다루도록 확장합니다. 이 task는 `ywc-create-pr`와 `ywc-finish-branch`의 language prompt, title format, pass-through 계약을 함께 정리합니다.

## Scope

- `codex/skills/ywc-create-pr/**`의 `--lang` / `--language` prompt와 PR body guidance를 5-language로 확장합니다.
- `codex/skills/ywc-finish-branch/**`의 `--pr-lang` contract와 title examples를 `en|ja|ko|zh|es`로 확장합니다.
- 각 skill의 README locale set, `agents/openai.yaml`, `evals/evals.json`을 갱신합니다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ywc-create-pr` — PR title/body language 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ywc-finish-branch` — `--pr-lang` pass-through 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ac5---workflow-skills-pass-zhes-unchanged` — workflow language pass-through Acceptance Criteria.

### Summary

`ywc-create-pr`는 실제 PR title/body를 작성하는 downstream target입니다. `ywc-finish-branch`는 task name 기반 title을 만들고 `--lang <pr-lang>`을 `ywc-create-pr`로 넘기므로 두 skill을 같은 task에서 맞춥니다. Branch name, task ID, file path, command, label은 번역하지 않습니다.

### Out of Scope (from spec)

- Executor flow 변경 — `000031-050`에서 처리.
- Review reply language — `000031-060`에서 처리.
- Plugin mirror 직접 수정 — `000032-010`.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000032-010-infra-codex-plugin-sync-validation` — final sync/validation.

## Key Files

- `codex/skills/ywc-create-pr/SKILL.md`
- `codex/skills/ywc-create-pr/README*.md`
- `codex/skills/ywc-create-pr/agents/openai.yaml`
- `codex/skills/ywc-create-pr/evals/evals.json`
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-finish-branch/README*.md`
- `codex/skills/ywc-finish-branch/agents/openai.yaml`
- `codex/skills/ywc-finish-branch/evals/evals.json`
- `codex/skills/ywc-finish-branch/scripts/build-pr-title.py` (read first; edit only if necessary)

## Notes

- `build-pr-title.py`가 English title formatting만 담당한다면 translation guidance는 `SKILL.md`에 남기고 script는 그대로 둘 수 있습니다.
- `--title` provided path는 user-provided title을 verbatim 유지해야 합니다.

## Hardening Evidence

### Test Feedback Path

- Existing coverage / named exception: docs-only surface plus eval fixture. If `build-pr-title.py` changes, run `python3 codex/skills/ywc-finish-branch/scripts/build-pr-title.py ...` smoke checks.

### Interface Contract

- Contract: `ywc-create-pr --lang en|ja|ko|zh|es`, `ywc-finish-branch --pr-lang en|ja|ko|zh|es`
- Inputs: language hint or user choice.
- Outputs: PR title/body prose in requested language.
- Error model: explicit `--title` remains verbatim; no prompt when title is provided.
- Impacted tests: `codex/skills/ywc-create-pr/evals/evals.json`, `codex/skills/ywc-finish-branch/evals/evals.json`

### Critical Surface Review

- Review requirement: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-create-pr/**`
- `codex/skills/ywc-finish-branch/**`

### Shared Surfaces

- PR title/body language contract
- `ywc-create-pr` delegation contract used by other executor skills

### Conflicts With

- (None identified) — `000031-050` reads this contract but owns different skill directories.

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `python3 -m json.tool codex/skills/ywc-create-pr/evals/evals.json >/dev/null`
- `python3 -m json.tool codex/skills/ywc-finish-branch/evals/evals.json >/dev/null`
- `rg -n "zh|es|Chinese|Spanish|中文|Español|--pr-lang en\\|ja\\|ko\\|zh\\|es" codex/skills/ywc-create-pr codex/skills/ywc-finish-branch`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- `codex/skills/ywc-sequential-executor/**`, `codex/skills/ywc-parallel-executor/**`, `codex/skills/ywc-agentic/**`.
- PR bot polling, CI wait, merge conflict handling.
- Plugin mirror direct edits.
