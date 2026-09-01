# 000033-010-docs-impl-review-integrity-catalog

## Purpose

`ywc-impl-review`가 Race Condition, Partial Write, Idempotency 누락을 recurring defect로 직접 잡을 수 있도록 review catalog와 worker surface를 보강한다.

## Scope

- `codex/skills/ywc-impl-review/references/recurring-defects.md`에 write-consistency subsection 추가
- `codex/skills/ywc-impl-review/SKILL.md`의 recurring defects summary 갱신
- 필요 시 `codex/skills/ywc-impl-review/README*.md` mirror 갱신

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#fr-1-extend-implementation-review-recurring-defects` - catalog에 추가할 defect class와 severity 기준
- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#fr-2-wire-the-new-review-class-into-ywc-impl-review` - `SKILL.md` summary 갱신 범위
- `/Users/yongwoon/Desktop/yongwoon/source/active_others/develop-with-llm/docs/studies/research/race-condition-partial-write-idempotency.md` - 원본 연구 문서

### Summary

이 task는 상세 지식을 `recurring-defects.md`에 두고 `SKILL.md`에는 짧은 routing summary만 남긴다. 핵심 defect는 application-level read-modify-write, transaction 없는 multi-step write, in-memory idempotency다. Review severity는 oversell, double-charge, lost ledger, duplicate provisioning 같은 blast radius에 맞춰 정한다.

### Out of Scope (from spec)

- `ywc-spec-validate`, `ywc-task-generator`, executor 지침 변경 - `000033-020-docs-spec-task-integrity-guidance`, `000033-030-docs-executor-integrity-gates`
- generated plugin package 직접 수정 - `000034-010-infra-codex-integrity-validation`
- 실제 application code 구현 - 이번 spec의 Out of Scope

## Dependencies

### Depends On

- (None - root task)

### Depended By

- `000033-020-docs-spec-task-integrity-guidance` - 같은 write-consistency 용어와 severity 기준을 downstream spec/task guidance에 반영
- `000033-030-docs-executor-integrity-gates` - executor가 Task Verify gate로 취급할 defect classes를 공유
- `000034-010-infra-codex-integrity-validation` - 최종 sync/validation 대상

## Key Files

- `codex/skills/ywc-impl-review/references/recurring-defects.md` - primary defect catalog
- `codex/skills/ywc-impl-review/SKILL.md` - worker prompt references summary
- `codex/skills/ywc-impl-review/README.md`
- `codex/skills/ywc-impl-review/README.en.md`
- `codex/skills/ywc-impl-review/README.ja.md`
- `codex/skills/ywc-impl-review/README.ko.md`
- `codex/skills/ywc-impl-review/README.zh.md`
- `codex/skills/ywc-impl-review/README.es.md`

## Notes

- Do not paste the whole research document. Preserve progressive disclosure by putting concrete checks in `recurring-defects.md`.
- Keep `SKILL.md` short: update only the catalog summary so every reviewer worker knows the new class exists.
- Reuse existing terminology: recurring defects, Phase 1, Critical/High, evidence, durable idempotency.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only skill guidance task. Replacement verification: `rg -n "concurrent write|transaction boundary|partial write|idempotency|read-modify-write" codex/skills/ywc-impl-review` plus `bash scripts/validate.sh` in the validation task.

### Interface Contract

- Contract: `ywc-impl-review` reviewer guidance
- Inputs: changed implementation diff and spec
- Outputs: review findings with Critical/High severity where applicable
- Error model: `DONE_WITH_CONCERNS` when Critical/High findings exist
- Impacted tests: repository validation and targeted `rg` evidence

### Critical Surface Review

- Review requirement: `ywc-impl-review` or manual full implementation review after this batch, because the change alters review behavior for payment/order/data paths.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-impl-review/**`

### Shared Surfaces

- Codex review semantics: recurring real-world defects catalog
- README locale mirror set for `ywc-impl-review`

### Conflicts With

- Any task editing `codex/skills/ywc-impl-review/**`

### Parallelizable After

- (Root task - no predecessor required)

### Task Verify

- `rg -n "concurrent write|read-modify-write|transaction boundary|partial write|idempotency" codex/skills/ywc-impl-review`
- `bash scripts/install.sh --list --codex`

## Out of Scope

- Do not edit `plugins/ywc-agent-toolkit/skills/**`.
- Do not modify Claude Code skills.
- Do not add new scripts or dependencies.
