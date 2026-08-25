# 000052-010-infra-fable-exploration-validation

## Purpose
Fable-inspired exploration 변경의 hard gate를 수행한다. touched skill / reference / metadata / localized docs / generated plugin sync까지 포함해 bundle이 일관되게 통과하는지 검증한다.

## Scope
- `bash scripts/sync-codex-plugin.sh` 실행 및 generated plugin package sync
- `bash scripts/validate.sh` 실행
- executor line-cap (`<=500`) 재검증
- targeted `rg` / `find`로 shared reference, skill hook, metadata sync 확인
- diff scope가 Codex batch 범위 안에 머무는지 점검

## Spec Reference

### Primary Sources
- `docs/ywc-plans/fable-inspired-codex-exploration.md#acceptance-criteria` — AC1–AC9 final gate
- `docs/ywc-plans/fable-inspired-codex-exploration.md#validation` — baseline validation commands
- `docs/ywc-plans/fable-inspired-codex-exploration.md#iteration-1-amendments` — metadata sync / line-cap safety / output placement 추가 검증

### Summary
이 task는 구현 task들의 산출물을 final gate에서 검증한다. Codex skills가 source of truth이므로 plugin package는 manual edit가 아니라 sync script로 갱신해야 하며, validation은 그 이후 상태를 기준으로 돌아야 한다. 이 task가 끝나기 전에는 batch 전체를 `DONE`으로 보면 안 된다.

### Out of Scope (from spec)
- 새 content authoring
- 추가 spec amendment
- Claude Code bundle parity 작업

## Dependencies

### Depends On
- `000051-010-docs-shared-exploration-references` — shared reference 생성 완료
- `000051-020-docs-discovery-skill-exploration-hooks` — discovery skill wiring 완료
- `000051-030-docs-execution-skill-implementation-notes` — execution skill wiring 완료
- `000051-040-docs-skill-author-exploration-rules` — skill-author rule update 완료

### Depended By
- (None — if no downstream dependency)

## Key Files
- `plugins/ywc-agent-toolkit/skills/**` — sync script로 갱신되는 generated package
- `tasks/dependency-graph.md` — batch 기록 유지

## Notes
- generated plugin package는 직접 수정하지 않는다. `bash scripts/sync-codex-plugin.sh` 결과만 반영한다.
- validation task는 source edits를 최소화하고 검증/동기화에 집중한다.

## Parallel Execution Metadata

### Ownership
- `plugins/ywc-agent-toolkit/skills/**` (generated output via sync script only)
- Validation/reporting surface for this task

### Shared Surfaces
- Whole-repo validation state
- Generated plugin package sync
- Executor line-cap gate

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000051-010-docs-shared-exploration-references`
- `000051-020-docs-discovery-skill-exploration-hooks`
- `000051-030-docs-execution-skill-implementation-notes`
- `000051-040-docs-skill-author-exploration-rules`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `wc -l codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`
- `rg -n "Unknowns Surfaced|Implementation Notes|unknown-matrix|implementation-notes" codex/skills codex/skills/references`

## Out of Scope
- 추가 behavior change
- 개별 skill wording 재설계
- Claude Code side sync
