# yw-000008-010-test-collector-contract-harness

## Purpose
Lock the current `fetch-pr-review-artifacts.sh` normalized artifact contract with deterministic subprocess tests.

## Scope
Add one Python standard-library `unittest` harness, a fake `gh` executable, temporary JSON fixtures, strict invocation validation, and assertions for all currently supported artifact paths and failure behavior.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-codex-pr223-review-artifact-test-hardening.md#acceptance-criteria` — AC1–AC5 define the collector behaviors to preserve.
- `docs/ywc-plans/20260826-codex-pr223-review-artifact-test-hardening.md#functional-requirements` — FR1–FR4 define the harness boundary and normalized fields.
- `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh` — authoritative implementation under test.

### Summary
The test must execute the real collector as a subprocess while intercepting every `gh` call with a temporary fake command. Fixtures cover review-thread resolution, marker suppression, review filtering, status-check normalization, merge readiness, optional health fields, and exit-3 failures. Production collector behavior and schema remain unchanged.

### Out of Scope (from spec)
- Package sync and generated marketplace copy — `yw-000009-010-infra-codex-package-sync`.
- Claude Nitpick parser, `raw_fallback`, Nitpick producer, and review-ID suppression logic.
- Any production collector refactor or normalized schema change.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000009-010-infra-codex-package-sync` — syncs and validates the finalized source test into the generated package.

## Key Files
- `codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py` — new subprocess test harness and fixtures.

## Notes
- Use only Python 3 standard-library modules named by the spec.
- The fake `gh` must reject unexpected argv and unexpected call order.
- Assertions should include artifact type and fingerprint in failure messages.

## Hardening Evidence
### Test Feedback Path
- RED-first target: `codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py` against the current collector before implementation is complete.

### Interface Contract
- Contract: collector stdout JSON and exit/stderr behavior.
- Inputs: explicit repository, PR number, fake `gh` responses, and fixture JSON.
- Outputs: normalized artifact objects with current fields plus exit 3 and current error messages on API failures.
- Error model: usage exit 2; GitHub/API failures exit 3; successful JSON output on stdout.
- Impacted tests: the new focused unittest module.

### Critical Surface Review
- Review requirement: N/A — no critical surface declared by the spec.

### Data Integrity Hardening
- Trigger surface: N/A — read-only test harness and fixture files.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`

### Shared Surfaces
- `fetch-pr-review-artifacts.sh` normalized JSON contract
- Fake `gh` argv and fixture protocol

### Conflicts With
- `yw-000009-010-infra-codex-package-sync` — generated copy must be produced only after this source test is finalized.
- Any task editing `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`.

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 -m unittest codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`
- `bash -n codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`

## Out of Scope
- Editing the collector production script.
- Adding third-party Python dependencies or persistent fixtures outside the test module's temporary directories.
- Editing any generated marketplace file.
