# 000001-010-infra-codex-plugin-package-layout

## Purpose

Codex CLI/App plugin distribution을 위한 self-contained package layout을 만든다. `.codex-plugin/plugin.json`은 plugin-local `"skills": "./skills/"`를 사용하고, `.codex-plugin/skills/`는 `codex/skills/`에서 만들어지는 packaging copy로 취급한다.

## Scope

- `.codex-plugin/plugin.json` 추가
- `.codex-plugin/assets/` 추가 여부 결정 및 필요한 asset 추가
- `.codex-plugin/skills/`를 `codex/skills/`에서 동기화하는 방식 구현
- symlink 없이 실제 file copy 또는 deterministic generation step 사용
- source-of-truth가 `codex/skills/`임을 packaging script/comment에 명시

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-plugin-distribution.md#iteration-1-amendments` — plugin-root-local layout, amended AC/FR
- `docs/ywc-plans/codex-plugin-distribution.md#existing-constraints-touched` — 기존 manifest와 install path 제약

### Summary

Iteration 1은 Codex plugin manifest path를 plugin-local `.codex-plugin/skills/`로 확정한다. Manifest는 `"skills": "./skills/"`를 사용해야 하며, `codex/skills/`는 source-of-truth로 남는다. 이 task는 package layout과 sync/generation mechanism을 먼저 만든다.

### Out of Scope (from spec)

- Validation failure logic — `000001-020-infra-codex-plugin-validation`
- README install guidance and translations — `000002-010-docs-codex-plugin-installation`
- Official Codex marketplace submission — out of this feature scope
- Claude Code marketplace behavior changes — out of this feature scope

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000001-020-infra-codex-plugin-validation` — validates manifest and plugin-local skill copy freshness
- `000002-010-docs-codex-plugin-installation` — documents the final install/package layout

## Key Files

- `.codex-plugin/plugin.json` — Codex plugin manifest
- `.codex-plugin/skills/**` — plugin-local skill package copy or generated package output
- `.codex-plugin/assets/**` — optional app icon/logo assets
- `scripts/sync-codex-plugin.sh` or equivalent — deterministic sync command if copy is generated from source
- `codex/skills/**` — read-only source-of-truth input for sync

## Notes

- Do not use symlinks for `.codex-plugin/skills/`.
- If committing all copied skills makes the PR too large, implement a clear package generation command and document why generated output is not committed.
- The manifest must not point at `./codex/skills/`.
- Reuse repository metadata from `plugin.json` where appropriate, but keep Codex plugin layout separate from Claude Code plugin layout.

## Parallel Execution Metadata

### Ownership

- `.codex-plugin/**`
- `scripts/sync-codex-plugin.sh`
- Packaging contract: `codex/skills/` → `.codex-plugin/skills/`

### Shared Surfaces

- Workspace-level plugin distribution metadata
- Codex skill bundle packaging boundary
- Release packaging behavior

### Conflicts With

- `000001-020-infra-codex-plugin-validation` — validation contract depends on this task's layout decisions

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `jq -r '.skills' .codex-plugin/plugin.json`
- `test "$(jq -r '.skills' .codex-plugin/plugin.json)" = "./skills/"`
- `test -f .codex-plugin/skills/ywc-plan/SKILL.md`
- `test -f codex/skills/ywc-plan/SKILL.md`

## Out of Scope

- Do not update README files in this task.
- Do not change skill content under `codex/skills/**` except through a pure sync/copy operation.
- Do not modify `scripts/validate.sh`; validation belongs to the next task.

