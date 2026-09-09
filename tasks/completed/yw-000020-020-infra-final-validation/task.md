# yw-000020-020-infra-final-validation — Implementation Checklist

## Prerequisites
- [ ] `yw-000020-010-docs-codex-catalog-distribution` is completed and merged.

## Allowed Edit Scope
- [ ] Run only the commands listed in README.md Task Verify.
- [ ] Do not edit files; report failures to the owning task.

## Stop Conditions
- [ ] Stop on the first failure that identifies an upstream task owner.
- [ ] Stop if validation would require changing custom-agent files or generated output manually.

## Hardening Gate
- [ ] Classify as verification-only.
- [ ] Use the existing spec command list as the evidence path.
- [ ] Do not claim success from a partial command set.

## Implementation Steps
- [ ] Run shell syntax and hermetic helper tests for the new helper.
- [ ] Parse both eval JSON files and run the Codex contract-eval runner.
- [ ] Run both Codex and custom-agent install-list checks.
- [ ] Re-run package sync, full validation, and `git diff --check`; record any failure with its owning task.

## Task Verify
- [ ] `bash -n codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- [ ] `bash codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- [ ] `python3 -m json.tool codex/skills/ywc-mine-review-history/evals/evals.json >/dev/null`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `bash scripts/install.sh --list --codex-agents`
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --check`

## Verification
- [ ] lint: `bash scripts/validate.sh`
- [ ] typecheck: N/A — no typed application source
- [ ] tests: `bash codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh` and contract evals
- [ ] build: `bash scripts/sync-codex-plugin.sh`
