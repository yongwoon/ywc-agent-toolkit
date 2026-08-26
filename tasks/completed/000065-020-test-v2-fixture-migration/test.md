# 000065-020-test-v2-fixture-migration — Manual Test Plan

## Preconditions

- [ ] Foundation runner and validator tasks are merged.
- [ ] Fake adapter is selected; no cloud, Docker, GitHub, or production credentials are supplied.

## Test Scenarios

### Scenario 1: Four-skill V2 coverage

**Steps:**

1. Run the fixture validator report.
2. Execute each new happy-path and negative/boundary case through the fake adapter.

**Expected Result:**

- Each named skill has one valid happy-path and one valid safe negative/boundary case.
- Fixture commands are absent and declared verifier IDs are registered.

### Scenario 2: Agent fixture boundary

**Steps:**

1. Run the representative agent fixture with its isolated evidence packet.
2. Inspect expected status, required signals, forbidden signals, and output path validation.

**Expected Result:**

- The fixture accepts only the declared agent and local output path.
- A forbidden signal or out-of-root output produces a failure.

### Scenario 3: Legacy compatibility

**Steps:**

1. Run validation over the existing V1 fixture inventory.
2. Inspect migration counts.

**Expected Result:**

- V1 fixtures remain readable without auto-rewrite.
- Remaining V1 count is reported as a quality backlog signal.
