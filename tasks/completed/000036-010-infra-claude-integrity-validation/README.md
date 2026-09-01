# 000036-010-infra-claude-integrity-validation

## Purpose

Claude Code data integrity skill hardening batch의 모든 source 변경(FR-1~FR-5)과 README mirror 일관성(FR-6)을 최종 hard gate로 검증한다. `bash scripts/validate.sh`와 markdownlint를 통과시키고, spec 핵심 용어가 의도한 skill surface에 반영됐는지 targeted `rg`로 확인하며, claude-code-only 경계를 assert한다.

## Scope

- Phase `000035`의 모든 claude-code source 변경 결과 검토 (FR-6 README consistency 포함)
- `bash scripts/validate.sh` 실행 및 실패 원인 분류(기존 stale/cache vs 이번 batch)
- 변경된 README에 대해 markdownlint 실행
- targeted `rg`로 write-consistency 용어·scan cue가 intended surface에 있는지 확인
- `git diff --name-only`로 claude-code-only 경계 확인 (no `codex/**`, no `plugins/**`)

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#fr-6-keep-documentation-mirrors-consistent`
- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#ac7--scope-leak-없음` — claude-code-only 경계
- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#ac8--repository-validation-통과`
- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#verification-commands`

### Summary

source guidance task(000035-010/020/030)가 모두 병합된 뒤 실행하는 hard gate다. claude-code에는 generated plugin sync가 없으므로(Codex 전용) 이 gate는 validate.sh + markdownlint + rg 증거 + 경계 확인만 수행한다. 검증 실패가 기존 cache/stale 때문인지 이번 batch 변경 때문인지 구분해 보고한다.

### Out of Scope (from spec)

- Source guidance 작성 → `000035-010`, `000035-020`, `000035-030`
- Codex skill / `plugins/**` 변경 → spec Out of Scope (Codex는 Batch 16)
- 실제 application code 변경 → spec Out of Scope

## Criticality

`normal` — 검증 전용 task. source는 validation 실패를 직접 유발한 경우에만 수정.

## Dependencies

### Depends On

- `000035-010-docs-impl-review-integrity-catalog`
- `000035-020-docs-spec-task-integrity-guidance`
- `000035-030-docs-executor-integrity-gates`

### Depended By

- (None — final hard gate)

## Key Files

- `claude-code/skills/ywc-impl-review/**`
- `claude-code/skills/ywc-spec-validate/**`
- `claude-code/skills/ywc-task-generator/**`
- `claude-code/skills/ywc-sequential-executor/**`
- `claude-code/skills/ywc-parallel-executor/**`
- `scripts/validate.sh`

## Notes

- `plugins/ywc-agent-toolkit/**`(generated)와 `codex/**`는 이 batch에서 건드리지 않는다 — 변경 시 경계 위반으로 보고.
- validation 실패가 pre-existing `__pycache__`/cache drift 때문이면 별도로 보고하고 source validation status를 숨기지 않는다.
- README mirror가 source에서 갱신됐다면 6 locale 일관성을 확인한다.

## Out of Scope

- Claude Code 외 스킬 변경 금지.
- 새 validation script 추가 금지.
- generated plugin/cache artifact 편집 금지 (경계 검증 목적 외).

## Parallel Execution Metadata

### Ownership

- validation command 출력 및 그로 인한 직접 수정만. source skill 파일은 Phase `000035`가 유발한 validation 실패 fix에 한해 접근.

### Shared Surfaces

- Repository validation status
- 다섯 대상 스킬의 README locale 일관성

### Conflicts With

- `claude-code/skills/ywc-impl-review/**` 편집 중인 task
- `claude-code/skills/ywc-spec-validate/**` 편집 중인 task
- `claude-code/skills/ywc-task-generator/**` 편집 중인 task
- `claude-code/skills/ywc-sequential-executor/**` / `ywc-parallel-executor/**` 편집 중인 task

### Parallelizable After

- `000035-010-docs-impl-review-integrity-catalog`
- `000035-020-docs-spec-task-integrity-guidance`
- `000035-030-docs-executor-integrity-gates`

### Task Verify

- `rg -n "concurrent write|read . modify . write|partial write|transaction boundary|durable idempotency|concurrency-safe" claude-code/skills/ywc-impl-review claude-code/skills/ywc-spec-validate claude-code/skills/ywc-task-generator claude-code/skills/ywc-sequential-executor claude-code/skills/ywc-parallel-executor`
- `git diff --name-only` 결과에 `codex/**` 또는 `plugins/**` 경로가 없음
- `bash scripts/install.sh --list --cc`
- `bash scripts/validate.sh`
