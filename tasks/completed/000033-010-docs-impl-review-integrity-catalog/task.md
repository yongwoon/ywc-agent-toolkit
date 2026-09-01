# 000033-010-docs-impl-review-integrity-catalog - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] Working tree state is understood; do not overwrite unrelated user changes.
- [ ] `docs/ywc-plans/codex-data-integrity-skill-hardening.md` is readable.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/ywc-impl-review/**`.
- [ ] If generated plugin files need updates, stop and leave that to `000034-010-infra-codex-integrity-validation`.

## Stop Conditions

- [ ] Stop if the source research document is unavailable and the spec does not provide enough detail to write the defect guidance.
- [ ] Stop if changes require editing shared references outside `codex/skills/ywc-impl-review/**`.
- [ ] Stop if README locale updates would require translation policy decisions not captured in the spec.

## Hardening Gate

- [ ] Classify this task: docs-only skill behavior guidance.
- [ ] Record named exception: no executable behavior in this task; replacement verification is targeted `rg` plus repository validation.
- [ ] Record interface contract: `ywc-impl-review` must surface evidence-backed Critical/High findings for data integrity defects.
- [ ] Require full review before DONE because this changes review behavior for payment/order/data integrity paths.

## Implementation Steps

- [ ] Update `codex/skills/ywc-impl-review/references/recurring-defects.md`.
  - [ ] Add a compact subsection under data-layer integrity for concurrent write safety.
  - [ ] Cover application-level `read -> modify -> write` and preferred mechanisms: atomic conditional update, row lock, optimistic version check.
  - [ ] Add transaction boundary guidance for multi-step writes.
  - [ ] Add durable idempotency guidance for duplicate-sensitive side effects.
- [ ] Add concise severity guidance in the same reference file.
  - [ ] Critical examples: oversell, double-charge, cross-ledger inconsistency, duplicate provisioning.
  - [ ] High examples: missing transaction on money/order/provisioning path, in-memory idempotency on production retry path.
  - [ ] QA signal: missing concurrency/idempotency test for affected code.
- [ ] Update `codex/skills/ywc-impl-review/SKILL.md`.
  - [ ] Extend the recurring defects summary with race condition / concurrent write safety.
  - [ ] Mention transaction boundary / partial write prevention.
  - [ ] Mention durable idempotency for retryable side effects.
  - [ ] Do not duplicate the detailed checklist in `SKILL.md`.
- [ ] Review `codex/skills/ywc-impl-review/README*.md`.
  - [ ] If README mirrors the recurring defects catalog, update the relevant locale files.
  - [ ] If README does not mirror that detail, record no README change needed in the task completion notes.

## Task Verify

- [ ] `rg -n "concurrent write|read-modify-write|transaction boundary|partial write|idempotency" codex/skills/ywc-impl-review`
- [ ] `bash scripts/install.sh --list --codex`

## Verification

- [ ] repository validation deferred to `000034-010-infra-codex-integrity-validation`
- [ ] generated plugin sync deferred to `000034-010-infra-codex-integrity-validation`
