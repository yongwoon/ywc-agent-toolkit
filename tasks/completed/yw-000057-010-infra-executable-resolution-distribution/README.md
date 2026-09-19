# yw-000057-010-infra-executable-resolution-distribution

## Purpose

Deliver the hardened Codex resolver consistently in source and generated marketplace bundles.

## Scope

Run source-to-plugin synchronization, verify resolver file modes in temporary installation and generated output, and perform the final required validation gates.

## Spec Reference

### Primary Sources

- [Executable-resolution hardening spec](../../../docs/ywc-plans/20260919-codex-executable-resolution-hardening.md#fr-4-preserve-agent-contracts-and-synchronize-delivery-artifacts)
- [Codex repository guidance](../../../codex/AGENTS.md)

### Summary

The Codex source tree is authoritative and the marketplace package is generated. After the resolver, callers, and regressions pass, synchronize the plugin and verify both resolver files retain usable modes in a temporary `CODEX_HOME` install and under `plugins/ywc-agent-toolkit/skills/`. Agent evaluation and repository validation are final delivery gates.

### Out of Scope (from spec)

- Resolver implementation, caller migration, and focused regression work are completed by predecessor tasks.
- No edits to `codex/agents/*.toml`, Claude surfaces, evidence collectors, or runtime dependencies.

## Criticality

critical

## Dependencies

### Depends On

- `yw-000056-010-test-executable-resolution-regression` — provides passing regression, complement, and validation gates.

### Depended By

- (none) — final task in this batch.

## Key Files

- `plugins/ywc-agent-toolkit/skills/` generated Codex mirror
- `codex/skills/scripts/resolve-bundle-executable.sh`
- `codex/skills/scripts/resolve-bundle-executable.py`

## Notes

Generated files must be synchronized rather than hand-edited. Source and generated changes must be delivered together according to Codex guidance.

## Hardening Evidence

- Test feedback path: `bash scripts/sync-codex-plugin.sh`, temporary install mode checks, `scripts/check-codex-agent-evals.sh`, and `bash scripts/validate.sh`.
- Interface Contract: generated resolver files preserve the source launcher/Python CLI contract and executable/readability modes.
- Data Integrity: N/A — delivery artifact synchronization only.
- Critical surface review: required before declaring the generated bundle current.

## Out of Scope

All feature implementation and agent configuration changes.

## Parallel Execution Metadata

- **Ownership:** Generated Codex plugin resolver files and distribution validation output
- **Shared Surfaces:** Source/plugin parity; file modes; repository validation gates
- **Conflicts With:** Any concurrent source-to-plugin synchronization or generated plugin edits
- **Parallelizable After:** `yw-000056-010`
- **Task Verify:** Sync is clean, source/plugin files match, modes are valid, agent eval and full validation pass

