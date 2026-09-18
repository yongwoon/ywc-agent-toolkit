# yw-000046-020-infra-readonly-contract-validator — Implementation Checklist

## Prerequisites
- [ ] `yw-000045-010-docs-readonly-inline-contract-source` is completed and merged.
- [ ] The exact FR-3 qualifier is present in all eight source read-only agents.

## Allowed Edit Scope
- [ ] Edit only `scripts/validate.sh` and temporary files created inside a disposable test directory for negative checks.
- [ ] Stop before changing agent TOMLs, installer tests, generated package files, or validation architecture.

## Stop Conditions
- [ ] Stop if the exact qualifier cannot be bounded to the `developer_instructions` TOML value.
- [ ] Stop if the check would require a new parser/library or would inspect comments as valid evidence.
- [ ] Stop if workspace-write workers become subject to the read-only assertion.

## Hardening Gate
- [ ] Classify as validation behavior change.
- [ ] Establish RED-first evidence by removing the qualifier in a temporary copy and confirming nonzero validation before production edits.
- [ ] Record the validator interface contract in the README before implementation.
- [ ] Data Integrity Hardening: N/A — no mutable state or persistent side effect.
- [ ] Critical review: N/A — not a critical surface.

## Implementation Steps
- [ ] Add a canonical qualifier variable or equivalent exact-string check within `check_codex_agent_file()` after sandbox classification.
  - Apply it only when the file contains `sandbox_mode = "read-only"`.
  - Inspect the `developer_instructions` value and reject a comment-only or cross-file occurrence.
- [ ] Emit `ERROR: codex/agents/<name>.toml ...` when the qualifier is missing, and increment the existing `ERRORS` counter without bypassing other checks.
- [ ] Add temporary negative verification for a removed qualifier and for a workspace-write worker to prove the gate is correctly scoped.

## Task Verify
- [ ] `bash scripts/validate.sh`.
- [ ] Run a temporary-copy negative test that removes the exact qualifier from one read-only TOML and asserts `bash scripts/validate.sh` exits nonzero with that agent path/name.
- [ ] Verify the two workspace-write workers are not rejected for lacking the qualifier.
- [ ] `git diff --check`.

## Verification
- [ ] Repository has no project lint, typecheck, unit-test, integration-test, or build command; use `bash scripts/validate.sh` and the targeted negative checks.

