# yw-000056-010-test-executable-resolution-regression

## Purpose

Prove the resolver boundary and enforce the closed-set complement against future unsafe target-repository execution.

## Scope

Add the stdlib-only resolver regression harness, validation integration, complement search, agent-evaluation invocation, and `mark-complete.sh` no-mutation regression.

## Spec Reference

### Primary Sources

- [Executable-resolution hardening spec](../../../docs/ywc-plans/20260919-codex-executable-resolution-hardening.md#fr-3-add-security-regression-and-complement-validation)
- [Codex validation guidance](../../../AGENTS.md#testing-guidelines)

### Summary

The harness must exercise the shipped launcher-selection block and resolver across installed, authorized source, non-`+x` interpreter, hostile target, origin mismatch, and missing-candidate fixtures. Validation must count failures, distinguish documentation examples from executable commands, prove the 20-site inventory, and verify `mark-complete.sh` does not mutate state when resolution is blocked.

### Out of Scope (from spec)

- Resolver implementation belongs to `yw-000054-010-infra-bundle-executable-resolver`.
- Caller migration belongs to `yw-000055-010-domain-executable-fallback-migration`.
- Generated marketplace synchronization belongs to `yw-000057-010-infra-executable-resolution-distribution`.
- Agent TOML changes and evidence infrastructure remain excluded.

## Criticality

critical

## Dependencies

### Depends On

- `yw-000055-010-domain-executable-fallback-migration` — supplies the migrated closed set and mutation ordering.

### Depended By

- `yw-000057-010-infra-executable-resolution-distribution` — consumes passing focused and repository validation gates.

## Key Files

- `tests/codex_executable_resolution_test.py`
- `scripts/validate.sh`

## Notes

The test must test the shipped behavior, not duplicate a model implementation. Use only the Python standard library and existing repository tools.

## Hardening Evidence

- Test feedback path: `python3 tests/codex_executable_resolution_test.py`, complement check, `scripts/check-codex-agent-evals.sh`, and `bash scripts/validate.sh`.
- Interface Contract: tests exercise the launcher and resolver as consumers, including one absolute-path result or `BLOCKED` diagnostic.
- Data Integrity trigger: unresolved compactor leaves task source/destination and Git index unchanged; regression asserts no move and no commit.
- Critical surface review: required for hostile-target and alternate-origin fixtures.

## Out of Scope

Resolver and caller source edits, marketplace output, and agent definition changes.

## Parallel Execution Metadata

- **Ownership:** `tests/codex_executable_resolution_test.py`; Codex validation section and complement logic in `scripts/validate.sh`
- **Shared Surfaces:** Validation error accounting; 20-site inventory; shipped resolver CLI
- **Conflicts With:** Any task modifying `scripts/validate.sh` or the focused test
- **Parallelizable After:** `yw-000055-010`
- **Task Verify:** Focused regression, complement check, agent eval, and full validation all pass

