# 000064-020-domain-isolated-runner-adapter — Manual Test Plan

## Preconditions

- [ ] `000064-010-infra-evaluator-discovery-schema-registry` is merged.
- [ ] Fake adapter fixture and a supported local Codex CLI fixture are available; no production credential is configured.

## Test Scenarios

### Scenario 1: Consecutive run isolation

**Steps:**

1. Run a fake-adapter case that writes a sentinel into its workspace and retained failed-artifact directory.
2. Run the same case again with a new attempt ID.
3. Inspect the second run's prepared workspace and temporary `CODEX_HOME` metadata.

**Expected Result:**

- The second run cannot observe the first sentinel, workspace, `CODEX_HOME`, or artifact directory.
- The report records separate run IDs and workspace lifecycle metadata.

### Scenario 2: Unavailable credential provider

**Steps:**

1. Invoke the runner with provider `unavailable` and a live-adapter-selected fixture.
2. Inspect the result status and command metadata.

**Expected Result:**

- The result is `SKIPPED_UNAVAILABLE`.
- Persistent developer `CODEX_HOME`, credential values, and raw environment dumps are absent from the report.

### Scenario 3: Undeclared output and verifier mutation

**Steps:**

1. Make the fake adapter write outside declared `output_paths`.
2. Make a fake readonly verifier alter an allowlisted source-checkout file.

**Expected Result:**

- Each attempt returns `FAIL` with a bounded diff summary.
- No unapproved file is silently retained or treated as a quality pass.
