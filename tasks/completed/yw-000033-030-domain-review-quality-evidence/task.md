# yw-000033-030-domain-review-quality-evidence — Implementation Checklist

## Prerequisites
- [ ] All Phase `yw-000032` tasks are completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-impl-review/**` and its evals.

## Stop Conditions
- [ ] Stop if review rules require raw worker output or gate execution.
- [ ] Stop if missing evidence is treated as a clean pass.

## Hardening Gate
- [ ] Classify as critical review-evidence behavior.
- [ ] Capture RED-first review-eval evidence before changing report rules.
- [ ] Record the sanitized evidence interface and require full review.
- [ ] Data Integrity Hardening: N/A for read-only evidence consumption.

## Implementation Steps
- [ ] Extend `references/qa-agent.md` and `SKILL.md` to accept only contract state, approved identity/digest, sanitized artifact path, and residual-survivor evidence.
- [ ] Add missing-boundary, unavailable-tool, residual, no-contract, and raw-data rejection behavior to review/report rules.
- [ ] Add positive and negative eval cases proving confidence downgrade and no gate execution.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `rg -n "sanitized|approved.*digest|residual|missing.*evidence|raw command|full diff|do not execute" codex/skills/ywc-impl-review`

## Verification
- [ ] Contract evals pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] Typecheck/build: N/A — skill/eval repository.
