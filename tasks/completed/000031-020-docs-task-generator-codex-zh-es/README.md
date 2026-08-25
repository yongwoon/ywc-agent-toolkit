# 000031-020-docs-task-generator-codex-zh-es

## Purpose

Codex `ywc-task-generator`가 task document output language로 Chinese와 Spanish를 지원하도록 확장합니다. 이 task는 지금 생성 중인 skill 자체를 포함하므로, 기존 `korean|japanese|english` contract와 backward compatibility를 유지하는 것이 핵심입니다.

## Scope

- `codex/skills/ywc-task-generator/SKILL.md`의 `--lang` option, inference prompt, supported-language wording을 확장합니다.
- `codex/skills/ywc-task-generator/references/language-policy.md`에 Chinese와 Spanish writing rules를 추가합니다.
- `README*.md`, `agents/openai.yaml`, `evals/evals.json`을 갱신합니다.
- Chinese/Spanish task-document generation eval을 추가합니다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ywc-task-generator` — Codex `ywc-task-generator` 변경 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#fr-1-establish-a-canonical-language-code-policy` — alias와 Technical terms policy.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#edge-cases` — mixed-language input, `chinese`, `spanish`, `espanol` alias.

### Summary

이 task는 `ywc-task-generator`의 language support를 넓힙니다. 기존 word-style values인 `korean|japanese|english`는 계속 동작해야 하며, 새 language values는 `chinese|spanish`와 `zh|es` aliases를 함께 문서화합니다. Task 문서의 prose는 선택 language를 따르되 Technical terms는 English로 유지합니다.

### Out of Scope (from spec)

- `ywc-project-docs` 변경.
- `claude-code/**` 변경.
- Plugin mirror 수동 수정 — `000032-010`에서 sync.
- Runtime implementation이나 product code 변경.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000032-010-infra-codex-plugin-sync-validation` — source 변경 후 generated package와 validation을 처리합니다.

## Key Files

- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/language-policy.md`
- `codex/skills/ywc-task-generator/README.md`
- `codex/skills/ywc-task-generator/README.en.md`
- `codex/skills/ywc-task-generator/README.ja.md`
- `codex/skills/ywc-task-generator/README.ko.md`
- `codex/skills/ywc-task-generator/README.zh.md`
- `codex/skills/ywc-task-generator/README.es.md`
- `codex/skills/ywc-task-generator/agents/openai.yaml`
- `codex/skills/ywc-task-generator/evals/evals.json`

## Notes

- 이 task는 `ywc-task-generator` 자신을 바꾸므로 output template의 machine-facing surfaces는 English로 유지해야 합니다.
- 기존 default가 `english`인 문구는 유지합니다.
- `zh/es` aliases를 추가해도 기존 `korean/japanese/english` examples는 삭제하지 않습니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance. JSON eval validation과 skill validation으로 대체합니다.

### Interface Contract

- Contract: `ywc-task-generator --lang korean|japanese|english|chinese|spanish` plus aliases `ko|ja|en|zh|es`.
- Inputs: spec path and optional `--lang`.
- Outputs: localized `tasks/**/README.md`, `task.md`, optional `test.md`, `dependency-graph.md`.
- Error model: unsupported language는 clarification 또는 documented fallback behavior를 따릅니다.
- Impacted tests: `codex/skills/ywc-task-generator/evals/evals.json`

### Critical Surface Review

- Review requirement: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-task-generator/**`

### Shared Surfaces

- Task document language policy
- `codex/skills/ywc-task-generator/evals/evals.json`
- `scripts/validate.sh` read-only validation gate

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-task-generator`
- `python3 -m json.tool codex/skills/ywc-task-generator/evals/evals.json >/dev/null`
- `rg -n "chinese|spanish|zh|es|中文|Español" codex/skills/ywc-task-generator`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- Existing task directories or generated task content outside this batch.
- `plugins/ywc-agent-toolkit/skills/**` direct edits.
- New `--tasks-dir` behavior or granularity behavior changes.
