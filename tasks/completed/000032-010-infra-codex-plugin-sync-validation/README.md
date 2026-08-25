# 000032-010-infra-codex-plugin-sync-validation

## Purpose

Phase `000031`의 Codex source 변경을 generated plugin package에 반영하고 전체 validation gate를 통과시킵니다. 이 task는 `codex/skills` source edits 이후에만 실행되는 hard gate입니다.

## Scope

- `bash scripts/sync-codex-plugin.sh`를 실행해 `plugins/ywc-agent-toolkit/skills/**`를 `codex/skills/**` source에서 재생성합니다.
- touched Codex eval JSON files를 validation합니다.
- targeted skill validation과 `bash scripts/validate.sh`를 실행합니다.
- final diff scope를 확인해 `claude-code/**`가 포함되지 않았는지 검증합니다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#fr-4-keep-claudecodex-syntax-and-packaging-correct` — Codex syntax와 plugin sync 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#fr-5-validation-and-regression-checks` — required validation commands.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ac10---plugin-mirror-is-synced` — plugin sync Acceptance Criteria.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ac12---no-unrelated-scope-creep` — final diff scope boundary.

### Summary

이 task는 source edits를 하지 않고 generated mirror와 validation만 담당합니다. `codex/skills`가 source of truth이고 `plugins/ywc-agent-toolkit/skills`는 sync output입니다. 모든 Phase `000031` source tasks가 끝난 뒤에만 실행합니다.

### Out of Scope (from spec)

- 새로운 zh/es behavior를 source skill에 직접 추가하는 작업 — Phase `000031` tasks.
- `claude-code/**` parity 작업.
- Release version, CHANGELOG, plugin manifest metadata 변경.

## Dependencies

### Depends On

- `000031-010-docs-spec-writer-codex-zh-es` — `ywc-spec-writer` source/eval updates.
- `000031-020-docs-task-generator-codex-zh-es` — `ywc-task-generator` source/eval updates.
- `000031-030-docs-gen-testcase-codex-zh-es` — `ywc-gen-testcase` source/eval updates.
- `000031-040-docs-pr-creation-language-zh-es` — `ywc-create-pr` / `ywc-finish-branch` source/eval updates.
- `000031-050-docs-executor-pr-lang-zh-es` — executor/agentic source/eval updates.
- `000031-060-docs-pr-review-reply-zh-es` — review reply source/eval updates.

### Depended By

- (None — final hard gate)

## Key Files

- `plugins/ywc-agent-toolkit/skills/**` — generated mirror from Codex source.
- `plugins/ywc-agent-toolkit/.codex-plugin/plugin.json` — generated package manifest mirror, if sync updates it.
- `plugins/ywc-agent-toolkit/README.md` — generated package README, if sync updates it.

## Notes

- Do not hand-edit generated plugin files before running sync.
- If `bash scripts/validate.sh` fails because plugin package is stale, rerun sync once and revalidate.
- If validation fails for a source skill issue, return to the owning Phase `000031` task rather than patching generated files directly.

## Hardening Evidence

### Test Feedback Path

- Existing coverage: `bash scripts/validate.sh`
- JSON validation: touched Codex eval files with `python3 -m json.tool`.

### Interface Contract

- Contract: `codex/skills/**` source state is mirrored into `plugins/ywc-agent-toolkit/skills/**`.
- Inputs: completed Phase `000031` source changes.
- Outputs: generated plugin mirror plus validation evidence.
- Error model: stale mirror or invalid metadata fails validation.
- Impacted tests: repository validation script.

### Critical Surface Review

- Review requirement: N/A.

## Parallel Execution Metadata

### Ownership

- `plugins/ywc-agent-toolkit/skills/**`
- `plugins/ywc-agent-toolkit/.codex-plugin/plugin.json`
- `plugins/ywc-agent-toolkit/README.md`

### Shared Surfaces

- Generated Codex plugin package
- Repository validation gate
- All touched Codex eval JSON files are read for validation

### Conflicts With

- All Phase `000031` tasks — this task must wait until their source edits are complete.

### Parallelizable After

- `000031-010-docs-spec-writer-codex-zh-es`
- `000031-020-docs-task-generator-codex-zh-es`
- `000031-030-docs-gen-testcase-codex-zh-es`
- `000031-040-docs-pr-creation-language-zh-es`
- `000031-050-docs-executor-pr-lang-zh-es`
- `000031-060-docs-pr-review-reply-zh-es`

### Task Verify

- `bash scripts/sync-codex-plugin.sh`
- `python3 -m json.tool codex/skills/ywc-spec-writer/evals/evals.json >/dev/null`
- `python3 -m json.tool codex/skills/ywc-task-generator/evals/evals.json >/dev/null`
- `python3 -m json.tool codex/skills/ywc-gen-testcase/evals/evals.json >/dev/null`
- `bash scripts/validate.sh`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- Source behavior edits in `codex/skills/**`.
- Manual generated-file patching to bypass sync.
- Release metadata updates.
