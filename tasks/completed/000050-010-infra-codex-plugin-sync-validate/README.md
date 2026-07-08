# 000050-010-infra-codex-plugin-sync-validate

## Purpose

Phase `000049`까지의 Codex source 변경을 generated plugin package에 반영하고 전체 validation gate를 통과시킵니다. 이 task는 source edits가 끝난 뒤 `plugins/ywc-agent-toolkit/skills/**` mirror와 repository validator를 정합시키는 최종 hard gate입니다.

## Scope

- `bash scripts/sync-codex-plugin.sh` 실행
- `plugins/ywc-agent-toolkit/skills/**` generated mirror 갱신
- `.codex-plugin` generated metadata 갱신 여부 확인
- `bash scripts/validate.sh` 실행
- 신규 skill / agent 노출 확인과 Codex-only diff boundary 확인

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-infra-skill-suite-port.md#acceptance-criteria`
- `docs/ywc-plans/codex-infra-skill-suite-port.md#fr-7-plugin-sync-및-validator-친화적인-rollout-순서를-제공한다`
- `codex/AGENTS.md` — source-of-truth와 generated plugin sync 규칙
- `AGENTS.md` — repository validation command

### Summary

Codex source of truth는 `codex/skills/**`이고 plugin package는 generated mirror입니다. 따라서 최종 단계에서는 source tasks를 더 수정하지 않고 sync script와 validator로 package/state를 정합시켜야 합니다. 이 task는 신규 infra skill 4종과 신규 agent가 source tree와 generated mirror 모두에서 유효한지 확인하는 배치 마감 작업입니다.

### Out of Scope (from spec)

- 신규 source content authoring — `000047-*`, `000048-*`, `000049-*`
- `claude-code/**` parity 작업

## Criticality

normal

## Dependencies

### Depends On

- `000047-010-infra-cloud-engineer-specialist`
- `000047-020-infra-agent-lens-extensions`
- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`
- `000049-010-docs-iac-author-skill`
- `000049-020-docs-infra-design-skill`
- `000049-030-docs-infra-review-skill`
- `000049-040-docs-infra-optimize-skill`

### Depended By

- (None — final hard gate)

## Key Files

- `plugins/ywc-agent-toolkit/skills/**`
- `plugins/ywc-agent-toolkit/.codex-plugin/plugin.json`
- `plugins/ywc-agent-toolkit/README.md`

## Notes

- generated mirror를 수동 편집하지 않습니다.
- source issue가 발견되면 owning task로 되돌아가야 하며 generated files만 패치해서 우회하지 않습니다.

## Hardening Evidence

### Test Feedback Path

- Existing coverage: `bash scripts/validate.sh`
- Targeted evidence: sync script output, install/list checks, diff scope review

### Interface Contract

- Contract: `codex/skills/**` source state is mirrored into `plugins/ywc-agent-toolkit/skills/**`.
- Inputs: completed source tasks in phases `000047`-`000049`
- Outputs: synced generated package and validation evidence
- Error model: stale mirror, missing required files, invalid metadata, or unexpected `claude-code/**` changes fail the gate
- Impacted tests: sync script, repository validator, install/list checks

### Critical Surface Review

- Review requirement: N/A

## Parallel Execution Metadata

### Ownership

- `plugins/ywc-agent-toolkit/skills/**`
- `plugins/ywc-agent-toolkit/.codex-plugin/plugin.json`
- `plugins/ywc-agent-toolkit/README.md`

### Shared Surfaces

- Generated Codex plugin package
- Repository validation gate
- Codex install/list surfaces

### Conflicts With

- All `000047-*`, `000048-*`, `000049-*` tasks — source edits must be complete first

### Parallelizable After

- `000047-010-infra-cloud-engineer-specialist`
- `000047-020-infra-agent-lens-extensions`
- `000048-010-docs-infra-reference-core`
- `000048-020-docs-infra-provider-packs`
- `000049-010-docs-iac-author-skill`
- `000049-020-docs-infra-design-skill`
- `000049-030-docs-infra-review-skill`
- `000049-040-docs-infra-optimize-skill`

### Task Verify

- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list --codex | rg 'ywc-(iac-author|infra-design|infra-review|infra-optimize)'`
- `bash scripts/install.sh --list --codex-agents | rg 'ywc-cloud-engineer'`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- Source file edits under `codex/skills/**` or `codex/agents/**`
- Manual generated-file patching
