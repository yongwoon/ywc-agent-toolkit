# yw-000019-030-test-mine-review-history-contract

## Purpose
Lock the new mining workflow with hermetic helper tests, contract evals, classification fixtures, and recurrence/confirmation scenarios.

## Scope
Add the new skill `evals/evals.json`, a PATH-mocked helper test, and fixtures covering input safety, merged-window selection, anchored bot allowlisting, NDJSON shape, per-PR failure continuation, evidence drops, exact hunk overlap, distinct-PR recurrence, confirmation-before-write, and proposal-only catalog behavior. Extend the sibling mining-source fixture as needed, without changing production contracts.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#acceptance-criteria`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#fr4--eval-and-catalog-integration`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#verification`

### Summary
This task supplies the evidence required by the spec's outcome oracle. The helper test must prove invalid/repeated arguments exit 2 without invoking `gh`, while successful paths preserve bounded order, anchored allowlisting, NDJSON fields, and failure status. Skill fixtures cover the confirmation and conservative evidence model without introducing runner logic.

### Out of Scope (from spec)
- Production skill/helper implementation — handled by `yw-000019-020-domain-mine-review-history-skill`.
- Catalog/root README/package changes — handled by `yw-000020-010-docs-codex-catalog-distribution`.
- Full repository validation — handled by `yw-000020-020-infra-final-validation`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000019-010-domain-review-learnings-mining-contract` — provides the mining-source fixture contract.
- `yw-000019-020-domain-mine-review-history-skill` — provides the helper and skill behavior under test.

### Depended By
- `yw-000020-010-docs-codex-catalog-distribution` — requires source evals and tests before packaging.

## Key Files
- `codex/skills/ywc-mine-review-history/evals/evals.json`
- `codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- `codex/skills/ywc-review-learnings/evals/evals.json` — only if mining fixture completion is needed.

## Notes
Mock `gh` and `jq` through `PATH`; do not add dependencies or alter the shared eval runner. Assert the exact exit status and no-`gh` witness for invalid input.

## Hardening Evidence
### Test Feedback Path
- RED-first target: `bash codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh` against the helper contract.
- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh`.

### Interface Contract
- Contract: helper exit/status/NDJSON behavior
- Owner task: `yw-000019-020-domain-mine-review-history-skill`
- Canonical signature: documented helper grammar → NDJSON records or specified nonzero status
- Consumers: this task's hermetic harness and downstream distribution validation
- Implementation opacity: tests assert the public contract, not implementation structure.
- Mismatch action: `NEEDS_CONTEXT`
- Inputs: repository, limit, optional date
- Outputs: exact fields and diagnostics/status
- Error model: invalid usage 2; individual API failure continues and final status nonzero
- Impacted tests: `test_fetch_bulk_review_comments.sh`

### Critical Surface Review
- Review requirement: N/A — test-only task; production retry/write review remains in task 020.

### Data Integrity Hardening
- Trigger surface: retryable command/API
- Atomic / locking strategy: hermetic mocks isolate each invocation
- Transaction boundary: one test case per helper invocation
- Idempotency guard: duplicate PR fixture asserts one recurrence
- Required tests: failure injection and duplicate recurrence

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-mine-review-history/evals/**`
- `codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- Mining fixture entries in `codex/skills/ywc-review-learnings/evals/evals.json`

### Shared Surfaces
- Helper CLI/NDJSON contract
- Contract-eval discovery schema

### Conflicts With
- `yw-000019-020-domain-mine-review-history-skill` — tests consume its finalized interface.

### Parallelizable After
- `yw-000019-010-domain-review-learnings-mining-contract`
- `yw-000019-020-domain-mine-review-history-skill`

### Task Verify
- `bash codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- `python3 -m json.tool codex/skills/ywc-mine-review-history/evals/evals.json >/dev/null`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
- Production CLI/helper edits, catalog mutation, generated package edits, and custom-agent changes.
