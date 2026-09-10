# yw-000034-010-infra-quality-gate-distribution-validation — Implementation Checklist

## Prerequisites
- [ ] `yw-000033-010-domain-sequential-quality-gate` is completed and merged.
- [ ] `yw-000033-020-domain-parallel-quality-gate` is completed and merged.
- [ ] `yw-000033-030-domain-review-quality-evidence` is completed and merged.

## Allowed Edit Scope
- [ ] Modify generated package output only through `bash scripts/sync-codex-plugin.sh`; limit source edits to necessary Codex catalog/localization or targeted validation fixtures.

## Stop Conditions
- [ ] Stop if source and generated package differ after sync.
- [ ] Stop if any AC reports fabricated commands, unrun-gate pass, boundary violation, or unresolved enforced failure.

## Hardening Gate
- [ ] Classify as critical release validation.
- [ ] Preserve pre-change failing evidence from contract evals and installer validation.
- [ ] Record the source-to-generated-package interface and require full review.
- [ ] Apply generated-artifact repeatability checks in `README.md`.

## Implementation Steps
- [ ] Update only necessary Codex localized README/catalog entries and ensure both worker names are discoverable.
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the repository root and confirm source remains authoritative.
- [ ] Run contract evals, targeted agent installer test, and `bash scripts/validate.sh`; fix only release-surface failures within Ownership.
- [ ] Re-run sync and validation, then record targeted `rg` evidence for no-contract omission, worker boundaries, status precedence, sanitized evidence, and package parity.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash tests/install-codex-agents-test.sh`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] Installer test passes (`bash tests/install-codex-agents-test.sh`)
- [ ] Contract evals pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] Repository validation passes (`bash scripts/validate.sh`)
- [ ] Typecheck/build: N/A — repository is a skill/agent distribution bundle.
