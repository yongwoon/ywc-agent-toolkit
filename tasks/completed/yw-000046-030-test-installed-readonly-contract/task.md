# yw-000046-030-test-installed-readonly-contract — Implementation Checklist

## Prerequisites
- [ ] `yw-000045-010-docs-readonly-inline-contract-source` is completed and merged.
- [ ] The exact qualifier is present in all eight source read-only TOMLs.

## Allowed Edit Scope
- [ ] Edit only `tests/install-codex-agents-test.sh` and disposable temporary installation paths created by the test.
- [ ] Stop before changing installer logic, source agents, validator, or generated package files.

## Stop Conditions
- [ ] Stop if the test would inspect source files instead of the temporary installed destination.
- [ ] Stop if a CLI branch changes model selection semantics beyond the existing test contract.
- [ ] Stop if the read-only inventory no longer matches the spec without updating the task contract first.

## Hardening Gate
- [ ] Classify as regression-test coverage.
- [ ] Establish RED-first evidence by temporarily removing the destination qualifier assertion or using a fixture with a missing qualifier and confirming failure.
- [ ] Record the installed parity interface contract in the README before implementation.
- [ ] Data Integrity Hardening: N/A — temporary installation only.
- [ ] Critical review: N/A — not a critical surface.

## Implementation Steps
- [ ] Define the eight read-only agent filenames in `install_with_version()` or a shared test-local list.
  - Iterate over `$codex_home/agents/<name>.toml` so assertions inspect installed files.
  - Assert the exact canonical qualifier and `sandbox_mode = "read-only"` for every entry.
- [ ] Retain existing model assertions for unsupported, supported, and current CLI branches, plus both workspace-write worker checks.
- [ ] Run the smoke test and review temporary-home cleanup and failure messages for agent-specific diagnostics.

## Task Verify
- [ ] `bash tests/install-codex-agents-test.sh`.
- [ ] Confirm the test exercises versions `0.143.9`, `0.144.0`, and `0.144.4` and checks all eight installed read-only agents in each branch.
- [ ] `git diff --check`.

## Verification
- [ ] Repository has no project lint, typecheck, unit-test, integration-test, or build command; use the targeted installer smoke test.

