# 000033-020-docs-spec-task-integrity-guidance

## Purpose

`ywc-spec-validate`와 `ywc-task-generator`가 duplicate-sensitive write flow의 concurrency, transaction, idempotency 요구사항을 spec/task 단계에서 누락하지 않도록 보강한다.

## Scope

- `codex/skills/ywc-spec-validate/SKILL.md`에 Completeness check 추가
- `codex/skills/ywc-task-generator/SKILL.md`에 Task Verify generation rule 추가
- `codex/skills/ywc-task-generator/references/task.md.template`에 write-consistency verification note 추가
- 필요 시 해당 skill README mirror 갱신

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#fr-3-add-spec-validation-completeness-checks` - spec validation 요구사항
- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#fr-4-make-task-generation-produce-concrete-verification` - task generation 요구사항
- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#edge-cases` - no harness, simple counter, distributed system 예외 처리

### Summary

이 task는 구현 전에 spec과 task가 데이터 무결성 위험을 명시하도록 만든다. Spec validation은 payment/order/provisioning/stock/balance/quota write flow에서 concurrent request, transaction boundary, idempotent retry 요구가 빠졌는지 확인한다. Task generation은 같은 위험이 있는 task에 concurrent request, rollback, idempotency retry verification을 넣도록 한다.

### Out of Scope (from spec)

- `ywc-impl-review` catalog 변경 - `000033-010-docs-impl-review-integrity-catalog`
- executor enforcement 변경 - `000033-030-docs-executor-integrity-gates`
- generated plugin package 직접 수정 - `000034-010-infra-codex-integrity-validation`
- `ywc-code-gen` 변경 - spec Open Questions에서 후속 검토로 분리

## Dependencies

### Depends On

- `000033-010-docs-impl-review-integrity-catalog` - 공통 write-consistency 용어와 severity 기준 제공

### Depended By

- `000034-010-infra-codex-integrity-validation` - 최종 sync/validation 대상

## Key Files

- `codex/skills/ywc-spec-validate/SKILL.md`
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/task.md.template`
- `codex/skills/ywc-spec-validate/README*.md`
- `codex/skills/ywc-task-generator/README*.md`

## Notes

- The spec stage should flag omissions; the task stage should create concrete verification obligations.
- Do not require row lock for every counter. Allow atomic conditional update, row lock, or optimistic lock by complexity.
- If no practical local concurrency harness exists, generated tasks may record a named exception but must include replacement verification.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only skill guidance task. Replacement verification: targeted `rg` over the two skill directories and full repository validation in `000034-010`.

### Interface Contract

- Contract: spec-to-task handoff for duplicate-sensitive writes
- Inputs: feature spec with payment/order/provisioning/stock/balance/quota style writes
- Outputs: Completeness findings before task generation, and generated task.md verification items after task generation
- Error model: `DONE_WITH_CONCERNS` in spec validation when Critical omissions exist
- Impacted tests: repository validation and generated task review

### Critical Surface Review

- Review requirement: manual full implementation review or `ywc-impl-review`, because these instructions affect money/order/data integrity planning.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-spec-validate/**`
- `codex/skills/ywc-task-generator/**`

### Shared Surfaces

- Codex spec-to-task pipeline behavior
- Task template contract: `Task Verify`
- README locale mirror sets for `ywc-spec-validate` and `ywc-task-generator`

### Conflicts With

- Any task editing `codex/skills/ywc-spec-validate/**`
- Any task editing `codex/skills/ywc-task-generator/**`

### Parallelizable After

- `000033-010-docs-impl-review-integrity-catalog`

### Task Verify

- `rg -n "concurrent request|transaction|idempotency|rollback|duplicate-sensitive|stock|balance|quota|payment|order|provisioning" codex/skills/ywc-spec-validate codex/skills/ywc-task-generator`
- `bash scripts/install.sh --list --codex`

## Out of Scope

- Do not edit executor skills in this task.
- Do not edit `plugins/ywc-agent-toolkit/skills/**`.
- Do not add new task generation scripts.
