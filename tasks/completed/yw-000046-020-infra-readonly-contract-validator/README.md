# yw-000046-020-infra-readonly-contract-validator

## Purpose
Make `scripts/validate.sh` mechanically enforce the exact local inline/no-artifact qualifier for every read-only Codex agent while excluding write-enabled workers.

## Scope
- Extend `check_codex_agent_file()` with a sandbox-gated exact-string check inside `developer_instructions`.
- Include the agent path/name in failures.
- Preserve existing identity, model, sandbox, and Claude-only-field checks.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#fr-3-mechanical-validator` — exact qualifier and gating behavior.
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#ac4--mechanical-regression-guard` — regression acceptance criterion.

### Summary
The validator must inspect each TOML's `sandbox_mode` and require the canonical qualifier only for `read-only` agents. The check must search the `developer_instructions` body, not comments or another file, and must report the affected agent. The two `workspace-write` workers remain valid without the qualifier.

### Out of Scope (from spec)
- Source contract wording — handled by `yw-000045-010-docs-readonly-inline-contract-source`.
- Installed destination checks — handled by `yw-000046-030-test-installed-readonly-contract`.
- Marketplace synchronization — handled by `yw-000047-040-infra-readonly-contract-distribution`.

## Criticality
normal

## Dependencies

### Depends On
- `yw-000045-010-docs-readonly-inline-contract-source` — supplies the exact qualifier and source contract.

### Depended By
- `yw-000047-040-infra-readonly-contract-distribution` — uses the validator as the final source/package freshness oracle.

## Key Files
- `scripts/validate.sh` — add the sandbox-gated qualifier assertion.

## Notes
Do not parse or mutate TOML with a new dependency. Keep the existing portable Bash style and make error output identify the agent path/name.

## Hardening Evidence

### Test Feedback Path
- RED-first target: temporary copies of read-only agent TOMLs with the qualifier removed or sandbox changed, checked through `bash scripts/validate.sh`.
- Existing coverage: `bash scripts/validate.sh`.

### Interface Contract
- Contract: validator read-only qualifier gate.
- Owner task: `yw-000046-020-infra-readonly-contract-validator`.
- Canonical signature: Codex agent TOML → PASS or file-specific nonzero validation error when `sandbox_mode = "read-only"` lacks the exact qualifier.
- Consumers: `yw-000047-040-infra-readonly-contract-distribution`, contributors and local CI.
- Implementation opacity: callers rely on the gate and must not duplicate divergent qualifier rules.
- Mismatch action: return `NEEDS_CONTEXT` if the source qualifier or sandbox inventory differs from the predecessor contract.

### Data Integrity Hardening
- Trigger: N/A — validation-only shell logic with no persistent mutation.

### Critical Surface Review
- N/A — not a critical surface under the spec's criticality rules.

## Out of Scope
No agent TOML wording, installer behavior, generated files, or new libraries.

## Parallel Execution Metadata
- **Ownership:** `scripts/validate.sh`, specifically `check_codex_agent_file()` and its immediate Codex-agent validation flow.
- **Shared Surfaces:** Agent TOML contract; final repository validation command.
- **Conflicts With:** `yw-000046-030-test-installed-readonly-contract` only when both run repository-wide checks concurrently.
- **Parallelizable After:** Merge of `yw-000045-010-docs-readonly-inline-contract-source`.
- **Task Verify:** `bash scripts/validate.sh`; targeted negative checks proving a missing qualifier fails with the agent path/name.

