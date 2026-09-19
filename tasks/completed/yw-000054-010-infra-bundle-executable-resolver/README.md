# yw-000054-010-infra-bundle-executable-resolver

## Purpose

Create the single trusted executable-resolution contract for Codex skills.

## Scope

Add the shipped Bash launcher, stdlib-only Python resolver, and shared reference defining installed-first resolution, explicitly authorized development fallback, invocation-aware file eligibility, and deterministic `BLOCKED` behavior.

## Spec Reference

### Primary Sources

- [Executable-resolution hardening spec](../../../docs/ywc-plans/20260919-codex-executable-resolution-hardening.md#fr-1-define-the-canonical-codex-executable-resolution-contract)
- [Codex repository guidance](../../../codex/AGENTS.md)

### Summary

The resolver must select an executable from the installed Codex bundle first. Source fallback is permitted only with explicit development opt-in, canonical Git-root and origin/layout validation, and contained candidate validation. The Bash launcher is the safe bootstrap path; the Python resolver owns the testable CLI contract.

### Out of Scope (from spec)

- Caller migration is handled by `yw-000055-010-domain-executable-fallback-migration`.
- Regression and validation wiring is handled by `yw-000056-010-test-executable-resolution-regression`.
- Marketplace synchronization is handled by `yw-000057-010-infra-executable-resolution-distribution`.
- PR #240 evidence collectors, Claude surfaces, agents, runtime dependencies, and data-model changes remain out of scope.

## Criticality

critical

## Dependencies

### Depends On

- (root) — establishes the existing Codex source/install layout and security scope.

### Depended By

- `yw-000055-010-domain-executable-fallback-migration` — consumes the canonical launcher block and resolver contract.

## Key Files

- `codex/skills/scripts/resolve-bundle-executable.sh`
- `codex/skills/scripts/resolve-bundle-executable.py`
- `codex/skills/references/shared-script-resolution.md`

## Notes

No architecture contract applies. The contract must not authorize changed arguments, shell evaluation, target-repository discovery, or file-existence-only fallback.

## Hardening Evidence

- Test feedback path: resolver fixtures in `tests/codex_executable_resolution_test.py` (downstream task).
- Interface Contract: launcher CLI accepts a bundle-relative path and fixed invocation kind; success prints one absolute path, failure returns `BLOCKED` without invoking candidates.
- Data Integrity: N/A — no database or persistent data change.
- Critical surface review: required; review trust predicates, symlink containment, origin identity, and fail-closed diagnostics.

## Out of Scope

Caller migration, validation harness, and generated plugin output.

## Parallel Execution Metadata

- **Ownership:** `codex/skills/scripts/resolve-bundle-executable.*`; `codex/skills/references/shared-script-resolution.md`
- **Shared Surfaces:** Installed Codex layout; source-root trust predicate; resolver CLI contract
- **Conflicts With:** None identified
- **Parallelizable After:** Root checkout only
- **Task Verify:** `python3 codex/skills/scripts/resolve-bundle-executable.py --help`; targeted resolver fixture command added by the implementation

