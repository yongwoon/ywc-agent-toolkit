# 000028-010-infra-plugin-sync-validation

## Purpose
All Codex source changes를 generated plugin package에 sync하고 repository validation을 최종 수행한다.

## Scope
- `bash scripts/sync-codex-plugin.sh`로 `plugins/ywc-agent-toolkit/skills/**`를 갱신한다.
- Helper syntax/executable bit, JSON fixtures, stale pattern scan, Codex-only boundary를 확인한다.
- `bash scripts/validate.sh`를 실행하고 실패를 이 task Ownership 내에서 수정한다.
- Root `CHANGELOG.md`는 final diff가 user-visible behavior change로 판단될 때만 Unreleased에 concise Codex entry를 추가한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-8-sync-and-release-metadata`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#verification-commands`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#ac16---codex-plugin-package-is-synced`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#ac17---codex-only-boundary-holds`

### Summary
`codex/skills/`가 source of truth이고 `plugins/ywc-agent-toolkit/skills/`는 generated package다. 모든 source task가 끝난 뒤 sync를 실행해야 validation이 plugin freshness를 통과한다. Version bump는 release workflow가 요구하지 않으면 하지 않고, Release Please에 맡긴다.

### Out of Scope (from spec)
- New source skill behavior 구현은 Phase `000027` tasks에서 처리한다.
- Manual version bump는 current release workflow가 요구할 때만 수행한다.

## Dependencies

### Depends On
- `000027-010-refactor-plan-pr-spec-contracts` — planning/PR/spec validation contract source changes
- `000027-020-refactor-pr-health-handler` — PR health handler source changes
- `000027-030-refactor-executor-health-sweeps` — executor PR lifecycle source changes
- `000027-040-refactor-agent-context-compaction` — onboarding/agentic source changes
- `000027-050-refactor-parity-doc-hygiene` — active docs hygiene source changes
- `000027-060-test-codex-parity-evals` — eval fixture changes

### Depended By
- (None — final hard gate)

## Key Files
- `plugins/ywc-agent-toolkit/skills/**`
- `CHANGELOG.md`
- `.release-please-manifest.json`
- `VERSION`

## Notes
Do not hand-edit generated plugin package before running sync. If stale-pattern `rg` finds historical non-active docs, name them in the implementation report rather than forcing unrelated cleanup. Existing unrelated deleted files under `docs/ywc-plans/` must not be reverted.

## Parallel Execution Metadata

### Ownership
- `plugins/ywc-agent-toolkit/skills/**`
- `CHANGELOG.md` only if needed for Unreleased entry
- Verification-only read access to `codex/skills/**`, `scripts/**`, `.release-please-manifest.json`, and `VERSION`

### Shared Surfaces
- Generated plugin package freshness
- Release metadata
- Repository validation command output

### Conflicts With
- All Phase `000027` tasks — this task must run after source edits are complete.

### Parallelizable After
- `000027-010-refactor-plan-pr-spec-contracts`
- `000027-020-refactor-pr-health-handler`
- `000027-030-refactor-executor-health-sweeps`
- `000027-040-refactor-agent-context-compaction`
- `000027-050-refactor-parity-doc-hygiene`
- `000027-060-test-codex-parity-evals`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `git diff --name-only | rg '^(claude-code/|tools/codex-skill/)' && exit 1 || true`
- `git diff --stat`

## Out of Scope
- Source behavior implementation that belongs to Phase `000027`
- Editing `claude-code/**`
- Blind version bump
