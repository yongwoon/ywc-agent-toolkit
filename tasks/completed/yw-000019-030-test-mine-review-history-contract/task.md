# yw-000019-030-test-mine-review-history-contract — Implementation Checklist

## Prerequisites
- [ ] `yw-000019-010-domain-review-learnings-mining-contract` is completed and merged.
- [ ] `yw-000019-020-domain-mine-review-history-skill` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within the eval/test paths declared in README.md.
- [ ] Do not change the helper or skill contract to make a test pass.

## Stop Conditions
- [ ] Stop and report if a failing test indicates a public-contract mismatch.
- [ ] Stop if the shared eval runner or custom-agent catalog would need modification.

## Hardening Gate
- [ ] Classify as test-only contract coverage.
- [ ] Establish RED-first helper assertions before considering the helper behavior complete.
- [ ] Treat the owner Interface Contract as bounded input; return `NEEDS_CONTEXT` on mismatch.
- [ ] Use failure injection and duplicate recurrence cases for the retryable/duplicate-sensitive surfaces.

## Implementation Steps
- [ ] Add `codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh` with temporary PATH fixtures for `gh` and `jq`, invocation logging, cleanup, and strict failure handling.
- [ ] Assert invalid and repeated flags return exit 2 before the mocked `gh` is called; cover positive integer and ISO-date rejection.
- [ ] Assert merged-window selection preserves returned order, applies inclusive UTC date filtering, rejects near-match human logins, and emits only the six NDJSON fields including null anchors.
- [ ] Assert one per-PR API failure emits a diagnostic, continues later PRs, and returns nonzero; add exact hunk overlap, unrelated/renamed/null-anchor, evidence-drop, and distinct-PR recurrence fixtures.
- [ ] Add five new-skill eval scenarios for scope-before-default, recurrence, confirmation-before-write, insufficient-evidence drop, and shared-catalog proposal-only behavior; extend the sibling mining fixture without changing the runner.

## Task Verify
- [ ] `bash codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- [ ] `python3 -m json.tool codex/skills/ywc-mine-review-history/evals/evals.json >/dev/null`
- [ ] `python3 -m json.tool codex/skills/ywc-review-learnings/evals/evals.json >/dev/null`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] lint: `bash -n codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- [ ] typecheck: N/A — shell/JSON fixture task
- [ ] tests: `bash codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- [ ] build: N/A — package freshness is verified in Phase `yw-000020`
