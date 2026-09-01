# 000035-030-docs-executor-integrity-gates

## Purpose

sequential·parallel executor가 생성된 concurrency/idempotency Task Verify를 lint/typecheck/build 통과로 격하하지 못하도록, 두 executor의 Rationalization Defense 표에 각 1행만 추가한다.

## Scope

- `claude-code/skills/ywc-sequential-executor/SKILL.md` line 13 Rationalization Defense 표에 row 1개 (FR-5)
- `claude-code/skills/ywc-parallel-executor/SKILL.md` line 15 Rationalization Defense 표에 row 1개 (FR-5)
- executor의 다른 섹션(Step 4/4c 실행 로직)은 변경하지 않는다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#fr-5-reinforce-executor-behavior-minimal--single-rationalization-row-each`

### Summary

두 executor는 이미 Task Verify를 무조건 실행되는 Layer-1 gate로 다룬다(sequential Step 4 line 320, parallel 4c line 272). 따라서 full prose는 기존 동작 재서술(NFR 중복)이 된다. 대신 아직 어느 표에도 없는 구체적 rationalization("concurrency 검증이 느리니 lint/build로 대신")만 차단하는 1행을 각 표에 추가한다.

### Out of Scope (from spec)

- `ywc-impl-review` catalog → `000035-010`
- spec-validate / task-generator 지침 → `000035-020`
- validation 최종 게이트 → `000036-010`
- executor Step 4/4c 실행 로직 변경, README 상세 mirror → 불필요 (spec: executor README는 상세 검증 동작을 mirror할 때만)

## Criticality

`normal` — executor skill markdown만 편집. 보안 키워드 경로 아님.

## Dependencies

### Depends On

- `000035-010-docs-impl-review-integrity-catalog` — executor가 gate로 취급할 defect class 명칭(concurrency/idempotency Task Verify)을 010의 canonical 용어와 맞춘다.

### Depended By

- `000036-010-infra-claude-integrity-validation` — 최종 validation 대상

## Key Files

- `claude-code/skills/ywc-sequential-executor/SKILL.md` — Rationalization Defense 표 (line 13)
- `claude-code/skills/ywc-parallel-executor/SKILL.md` — Rationalization Defense 표 (line 15)

## Notes

- **각 표에 정확히 1행만** 추가. Step 4/4c 실행 로직·다른 섹션은 손대지 않는다.
- 추가 row 취지: "만족시키기 어려운 concurrency 검증은 Layer-4(lint/build)로 격하할 게 아니라, task의 대체 검증 note(code-level lock/transaction proof 또는 integration test plan)로 충족" — spec Edge Case "No practical concurrency harness"와 정합.
- executor README는 RD 표를 상세 mirror하지 않는 것이 일반적 — 확인 후 변경 없으면 그대로 둔다.

## Out of Scope

- `codex/skills/**` 및 `plugins/**` 편집 금지.
- executor Step 4/4c 실행 로직 재서술 금지.
- 새 script·dependency 추가 금지.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-sequential-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md`

### Shared Surfaces

- Rationalization Defense 표 규약 (010의 defect class 명칭 재사용)

### Conflicts With

- 두 executor SKILL.md를 편집하는 모든 task (현 batch에는 없음)

### Parallelizable After

- `000035-010-docs-impl-review-integrity-catalog`

### Task Verify

- `rg -n "concurrency|idempoten|lint/typecheck/build|Layer" claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md` — 두 표에 새 row hit
- 각 SKILL.md의 Rationalization Defense 표에 정확히 1행만 늘었는지 육안 확인 (다른 섹션 무변경)
- `bash scripts/install.sh --list --cc`
