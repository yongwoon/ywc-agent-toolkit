# 000066-010-infra-eval-ci-workflow-docs — Manual Test Plan

## Preconditions

- [ ] Phase `000065` is fully merged.
- [ ] Fake adapter and test artifact root are available.
- [ ] No live credential provider or API-egress exception is configured.

## Test Scenarios

### Scenario 1: PR-safe mocked suite

**Steps:**

1. Trigger the mocked suite path with fake fixtures.
2. Inspect executed commands and generated summary.

**Expected Result:**

- Only schema, lint, mocked verifier, and fake-adapter checks run.
- No live credential, model invocation, or live-suite status is required.

### Scenario 2: Live suite gate without provider

**Steps:**

1. Select `live` with no credential provider or API-egress policy.
2. Inspect exit behavior and report.

**Expected Result:**

- The job reports `SKIPPED_UNAVAILABLE` and exits 3 as an infrastructure alert.
- It does not fall back to developer configuration or silently pass.

### Scenario 3: Artifact cleanup and exit mapping

**Steps:**

1. Seed fake retained failed-run directories older/newer than seven days, including an oversized artifact.
2. Run cleanup and fake result-status mapping.

**Expected Result:**

- Only stale directories beneath the evaluator artifact root are deleted; newer data remains.
- Oversized data is not uploaded, and status exits map to the documented values.
