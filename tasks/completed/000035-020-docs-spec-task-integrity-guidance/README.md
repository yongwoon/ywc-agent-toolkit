# 000035-020-docs-spec-task-integrity-guidance

## Purpose

`ywc-spec-validate`가 duplicate-sensitive write flow의 concurrency/transaction/idempotency 요구 누락을 Completeness finding으로 잡고, `ywc-task-generator`가 그런 task에 대해 구체적 Task Verify(atomic update / rollback / idempotent retry)를 생성하도록 지침을 보강한다.

## Scope

- `claude-code/skills/ywc-spec-validate/SKILL.md` line 80 Step 4 Completeness worker Focus 컬럼 확장 + Rationalization Defense row 1개 (FR-3). line 113 Review Dimensions 표는 generic 유지.
- `claude-code/skills/ywc-task-generator/SKILL.md` Task Verify 생성 규칙(line 327/383 근처) + Rationalization Defense row 1개 (FR-4).
- `claude-code/skills/ywc-task-generator/references/task.md.template` line 24 `## Task Verify` 섹션에 note 1개 (FR-4).
- 두 스킬의 `README*.md` (6 locale) mirror는 user-facing 변경 시에만 갱신.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#fr-3-add-spec-validation-completeness-check`
- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#fr-4-make-task-generation-produce-concrete-verification`
- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#terminology` — duplicate-sensitive write flow 정의

### Summary

`000035-010`이 확정한 write-consistency 용어(concurrent write safety / transaction boundary / durable idempotency)와 severity 기준을 spec/task 단계 지침에 재사용한다. spec-validate는 Completeness 3-tier(Critical/Warning/Suggestion)를 쓰고, double charge/oversell/lost ledger/duplicate provisioning 유발 가능 시 Critical, 그 외 Warning. task-generator는 duplicate-sensitive task에 concurrent write / rollback / idempotent retry 검증을 요구한다.

### Out of Scope (from spec)

- `ywc-impl-review` catalog 변경 → `000035-010-docs-impl-review-integrity-catalog`
- executor 지침 변경 → `000035-030-docs-executor-integrity-gates`
- validation 최종 게이트 → `000036-010-infra-claude-integrity-validation`
- Codex skill / 실제 코드 구현 → spec Out of Scope

## Criticality

`normal` — Ownership이 skill markdown 디렉토리이며 보안 키워드 경로가 아니다. review-behavior 회귀는 `000036-010`에서 확인.

## Dependencies

### Depends On

- `000035-010-docs-impl-review-integrity-catalog` — write-consistency 용어·severity 기준의 canonical source. 용어 drift를 막기 위해 010 이후 시작.

### Depended By

- `000036-010-infra-claude-integrity-validation` — 최종 validation/README consistency 대상

## Key Files

- `claude-code/skills/ywc-spec-validate/SKILL.md` — Step 4 Completeness worker Focus(line 80), Rationalization Defense 표
- `claude-code/skills/ywc-task-generator/SKILL.md` — task.md Core Elements Task Verify(line 327), task.md Quality checklist(line 383), Rationalization Defense 표
- `claude-code/skills/ywc-task-generator/references/task.md.template` — `## Task Verify`(line 24)
- 두 스킬의 `README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.zh.md` / `README.es.md`

## Notes

- spec-validate: **Step 4 worker Focus 컬럼이 단일 operative anchor**. line 113 Review Dimensions 표는 의도적으로 generic 유지 (spec W5).
- severity 어휘를 스킬별로 정확히: spec-validate는 Critical/Warning/Suggestion. impl-review의 5-tier를 여기 끌어오지 말 것.
- task-generator note는 간결하게 — 모든 counter에 row lock 강요 금지(atomic update / row lock / optimistic lock 허용). "No practical concurrency harness" edge case의 대체 검증 note를 허용.
- 두 스킬은 **서로 다른 디렉토리**라 한 task 안에서 편집해도 Ownership 충돌 없음.

## Out of Scope

- `codex/skills/**` 및 `plugins/ywc-agent-toolkit/skills/**` 편집 금지.
- `ywc-impl-review` / executor / `ywc-agentic` 편집 금지.
- 새 script·dependency 추가 금지.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-spec-validate/**`
- `claude-code/skills/ywc-task-generator/**`

### Shared Surfaces

- spec/task 단계 write-consistency guidance (010이 정한 용어·severity 재사용)
- README locale mirror set for `ywc-spec-validate` and `ywc-task-generator`

### Conflicts With

- `claude-code/skills/ywc-spec-validate/**` 또는 `claude-code/skills/ywc-task-generator/**`를 편집하는 모든 task (현 batch에는 없음)

### Parallelizable After

- `000035-010-docs-impl-review-integrity-catalog` (용어 canonical source 병합 후)

### Task Verify

- `rg -n "duplicate-sensitive|concurrent request|transaction|idempoten" claude-code/skills/ywc-spec-validate/SKILL.md` — Completeness 지침 hit
- `rg -n "concurrent|rollback|idempoten|atomic" claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-task-generator/references/task.md.template` — Task Verify 생성 규칙·template note hit
- `bash scripts/install.sh --list --cc`
