# yw-000046-030-test-installed-readonly-contract

## Purpose
Extend the temporary Codex-agent installation smoke test to prove the read-only inline/no-artifact contract survives installation and model fallback substitution.

## Scope
- Define the explicit eight-agent read-only set in `tests/install-codex-agents-test.sh`.
- Check installed destination files, not source files, for the exact qualifier.
- Run checks across unsupported fallback and supported/current CLI branches while preserving worker assertions.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#fr-4-installed-agent-regression-coverage` — installed smoke test behavior.
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#ac5--installed-parity` — supported and fallback acceptance criterion.

### Summary
The smoke test already installs agents into temporary `CODEX_HOME` directories for multiple CLI versions. It must additionally assert that every installed read-only TOML retains the exact qualifier while existing model and sandbox checks continue to pass. The two workspace-write workers remain explicit negative cases.

### Out of Scope (from spec)
- Source contract edits — handled by `yw-000045-010-docs-readonly-inline-contract-source`.
- Validator implementation — handled by `yw-000046-020-infra-readonly-contract-validator`.
- Generated marketplace sync — handled by `yw-000047-040-infra-readonly-contract-distribution`.

## Criticality
normal

## Dependencies

### Depends On
- `yw-000045-010-docs-readonly-inline-contract-source` — supplies the qualifier that installation must preserve.

### Depended By
- `yw-000047-040-infra-readonly-contract-distribution` — waits for installed parity before final validation.

## Key Files
- `tests/install-codex-agents-test.sh` — add installed-agent contract assertions.

## Notes
Assertions must target `$codex_home/agents/` within each temporary branch. Keep the existing model threshold cases and temporary-home cleanup intact.

## Hardening Evidence

### Test Feedback Path
- RED-first target: installed destination assertions for one missing qualifier or model substitution regression.
- Existing coverage: `bash tests/install-codex-agents-test.sh`.

### Interface Contract
- Contract: installed Codex-agent parity.
- Owner task: `yw-000046-030-test-installed-readonly-contract`.
- Canonical signature: installer branch × temporary `CODEX_HOME` → all eight read-only files preserve qualifier, model, and sandbox assertions.
- Consumers: `yw-000047-040-infra-readonly-contract-distribution`, local CI.
- Implementation opacity: callers trust destination checks rather than source-only grep.
- Mismatch action: return `NEEDS_CONTEXT` if installer output paths or the eight-agent inventory changes.

### Data Integrity Hardening
- Trigger: N/A — temporary test directories are disposable and no repository data is mutated.

### Critical Surface Review
- N/A — not a critical surface under the spec's criticality rules.

## Out of Scope
No source agent edits, installer behavior changes, validator logic, or generated package edits.

## Parallel Execution Metadata
- **Ownership:** `tests/install-codex-agents-test.sh` and its disposable temporary test directories.
- **Shared Surfaces:** Installed Codex-agent destination; model fallback substitution behavior.
- **Conflicts With:** `yw-000046-020-infra-readonly-contract-validator` only when both run repository-wide checks concurrently.
- **Parallelizable After:** Merge of `yw-000045-010-docs-readonly-inline-contract-source`.
- **Task Verify:** `bash tests/install-codex-agents-test.sh`.

