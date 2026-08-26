# 000001-020-infra-codex-plugin-validation

## Purpose

Codex plugin manifest와 plugin-local skill package가 stale 또는 broken 상태로 merge되지 않도록 local CI mirror인 `scripts/validate.sh`에 검증을 추가한다.

## Scope

- `.codex-plugin/plugin.json` JSON parse와 required fields 검증
- Manifest `skills` 값이 `"./skills/"`인지 검증
- `.codex-plugin/skills/ywc-plan/SKILL.md` 존재 검증
- `codex/skills/`와 `.codex-plugin/skills/` freshness 검증
- stale copy 발견 시 refresh command를 error message에 포함

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-plugin-distribution.md#iteration-1-amendments` — AC5a, FR-4a
- `docs/ywc-plans/codex-plugin-distribution.md#existing-constraints-touched` — existing validation behavior

### Summary

이 task는 package layout이 merge 후 drift하지 않도록 검증을 추가한다. `scripts/validate.sh`는 CI에서 실행되므로 portable Bash로 유지해야 한다. `jq`는 이 repo의 existing scripts and README prerequisites에서 이미 사용되는 tool이다.

### Out of Scope (from spec)

- Manifest and package layout creation — `000001-010-infra-codex-plugin-package-layout`
- README install guidance and translations — `000002-010-docs-codex-plugin-installation`
- Official marketplace submission — out of this feature scope

## Dependencies

### Depends On

- `000001-010-infra-codex-plugin-package-layout` — provides `.codex-plugin/plugin.json` and plugin-local skill package layout

### Depended By

- `000002-010-docs-codex-plugin-installation` — documents verification behavior and install confidence

## Key Files

- `scripts/validate.sh` — add plugin manifest and freshness checks
- `.codex-plugin/plugin.json` — validation target
- `.codex-plugin/skills/**` — freshness validation target
- `codex/skills/**` — source-of-truth comparison target
- `scripts/sync-codex-plugin.sh` — optional command referenced by validation error output

## Notes

- Keep validation failure messages actionable and specific.
- Do not weaken existing Codex skill checks.
- If freshness comparison excludes generated or non-deterministic files, document the exact exclusion.
- Preserve `set -euo pipefail` compatibility.

## Parallel Execution Metadata

### Ownership

- `scripts/validate.sh`
- `scripts/sync-codex-plugin.sh` if task 1 introduced it and validation must reference it
- Validation contract for `.codex-plugin/plugin.json`
- Validation contract for `.codex-plugin/skills/**`

### Shared Surfaces

- CI validation behavior
- Workspace-level script requirements
- Plugin packaging freshness contract

### Conflicts With

- `000001-010-infra-codex-plugin-package-layout` — cannot run in parallel because validation depends on final layout decisions

### Parallelizable After

- `000001-010-infra-codex-plugin-package-layout`

### Task Verify

- `bash scripts/validate.sh`
- `bash scripts/install.sh --list`
- `test "$(jq -r '.skills' .codex-plugin/plugin.json)" = "./skills/"`

## Out of Scope

- Do not update README files in this task.
- Do not change plugin display copy unless needed to satisfy validation fields.
- Do not alter install destinations for `scripts/install.sh`.

