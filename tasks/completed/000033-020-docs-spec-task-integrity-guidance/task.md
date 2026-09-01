# 000033-020-docs-spec-task-integrity-guidance - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000033-010-docs-impl-review-integrity-catalog` is completed or its terminology/severity wording is available.
- [ ] `docs/ywc-plans/codex-data-integrity-skill-hardening.md` is readable.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/ywc-spec-validate/**` and `codex/skills/ywc-task-generator/**`.
- [ ] If changes spill into executor skills, stop; that belongs to `000033-030-docs-executor-integrity-gates`.

## Stop Conditions

- [ ] Stop if the spec-validation wording would contradict existing Completion Status rules.
- [ ] Stop if task-generator changes would require a new script or new dependency.
- [ ] Stop if README locale update scope becomes larger than mirror text maintenance.

## Hardening Gate

- [ ] Classify this task: docs-only skill behavior guidance.
- [ ] Record named exception: no executable behavior; replacement verification is targeted `rg` plus final repository validation.
- [ ] Record interface contract: specs with duplicate-sensitive writes must produce completeness findings or concrete task verification.
- [ ] Require full review before DONE because the guidance affects data integrity implementation tasks.

## Implementation Steps

- [ ] Update `codex/skills/ywc-spec-validate/SKILL.md`.
  - [ ] Add Completeness guidance for duplicate-sensitive writes: payment, order creation, provisioning, credit/balance/stock/quota mutation.
  - [ ] Require checks for concurrent requests against the same resource.
  - [ ] Require checks for transaction boundary or equivalent consistency boundary.
  - [ ] Require checks for duplicate client retries, double-clicks, and idempotency behavior.
  - [ ] State severity guidance: Critical for double charge, oversell, lost ledger entry, duplicate provisioning; Warning otherwise.
- [ ] Update `codex/skills/ywc-task-generator/SKILL.md`.
  - [ ] Add a task.md / Task Verify rule for duplicate-sensitive write flows.
  - [ ] Require generated tasks to name the selected mechanism: atomic conditional update, row lock, optimistic lock, idempotency key, unique constraint, or persisted request/result record.
  - [ ] Require observable expected results for lock/version conflicts, exhausted stock/balance/quota, rollback, and duplicate retry.
- [ ] Update `codex/skills/ywc-task-generator/references/task.md.template`.
  - [ ] Add a concise note under `## Task Verify` for concurrent request, rollback, and idempotency retry verification.
  - [ ] Keep the note generic enough not to force tests on unrelated docs-only/config tasks.
- [ ] Review README mirrors for `ywc-spec-validate` and `ywc-task-generator`.
  - [ ] Update only if the README mirrors these detailed behavior rules.
  - [ ] Record no-change rationale if README remains high-level.

## Task Verify

- [ ] `rg -n "concurrent request|transaction|idempotency|rollback|duplicate-sensitive|stock|balance|quota|payment|order|provisioning" codex/skills/ywc-spec-validate codex/skills/ywc-task-generator`
- [ ] `bash scripts/install.sh --list --codex`

## Verification

- [ ] repository validation deferred to `000034-010-infra-codex-integrity-validation`
- [ ] generated plugin sync deferred to `000034-010-infra-codex-integrity-validation`
