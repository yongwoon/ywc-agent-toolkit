# yw-000033-010-domain-sequential-quality-gate — Implementation Checklist

## Prerequisites
- [ ] All Phase `yw-000032` tasks are completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-sequential-executor/**` and its evals.

## Stop Conditions
- [ ] Stop if packet validation requires inferred commands or ownership.
- [ ] Stop if a later worker result would overwrite a stronger earlier status.

## Hardening Gate
- [ ] Classify as critical lifecycle behavior.
- [ ] Capture RED-first executor-eval evidence before changing routing.
- [ ] Record the completion-status/evidence interface and require full review.
- [ ] Apply retry/idempotency checks in `README.md`.

## Implementation Steps
- [ ] Add the opt-in packet resolution stage after normal Step 4 verification and before optional review/delivery.
- [ ] Dispatch Cleaner only for eligible state and evidence; dispatch Hardener only after Cleaner permits it.
- [ ] Aggregate `BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`, retain residuals, and preserve N/A/report-only behavior.
- [ ] Add eval cases for unavailable tools, missing packet fields, no-contract omission, and later-DONE masking prevention.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `rg -n "N/A — no quality gate contract|Cleaner|Hardener|BLOCKED|NEEDS_CONTEXT|DONE_WITH_CONCERNS" codex/skills/ywc-sequential-executor`

## Verification
- [ ] Contract evals pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] Typecheck/build: N/A — skill/eval repository.
