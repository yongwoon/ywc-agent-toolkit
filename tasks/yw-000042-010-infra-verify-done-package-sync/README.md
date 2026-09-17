# yw-000042-010-infra-verify-done-package-sync

## Purpose
Regenerate the Codex marketplace mirror from the finished source skill and prove source/package/install parity.

## Scope
Run source-first sync, verify executable modes and freshness, install into temporary `CODEX_HOME`, execute all three installed CLI modes, and run repository validation.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md#fr-5-tests-and-package-flow` — sync/install/validation requirements
- `codex/AGENTS.md#project-structure-and-module-organization` — source-of-truth rule
### Summary
The marketplace mirror is generated output and must be rebuilt only after source code, tests, docs, eval, and locales are complete. `scripts/validate.sh` is the source/package freshness and mode oracle; generated files are never hand-edited.
### Out of Scope (from spec)
- Source implementation/docs — predecessor tasks
- Custom agents, `agents/openai.yaml`, root release metadata, cross-bundle sync, and PR polling

## Criticality
normal

## Dependencies
### Depends On
- `yw-000041-010-docs-verify-done-ledger` — final source skill and locales
### Depended By
- (None — final task)

## Key Files
- `plugins/ywc-agent-toolkit/skills/ywc-verify-done/**` — generated mirror

## Notes
Run sync only after source edits; use temporary `CODEX_HOME`; keep ≥600-second PR polling and `--verify` proof separate.

## Hardening Evidence
- Test feedback path: checker suite, contract evals, temporary installed smoke test, and `bash scripts/validate.sh`.
- Interface Contract: generated mirror exposes the same installed `gate-check.py` signature and docs as source.
- Data Integrity Hardening: N/A — generated/read-only validation.
- Critical surface review: N/A for generated-only changes; source drift returns to its owner.

## Ownership
`plugins/ywc-agent-toolkit/skills/ywc-verify-done/**` generated output only.

## Shared Surfaces
- Source/package parity, executable modes, temporary `CODEX_HOME`, validation oracle

## Conflicts With
- Any task editing `codex/skills/ywc-verify-done/**` after sync

## Parallelizable After
- `yw-000041-010-docs-verify-done-ledger`

## Task Verify
- `bash scripts/sync-codex-plugin.sh`
- Temporary `CODEX_HOME` smoke test for installed `--status`, bare, and `--reverify`
- `bash scripts/validate.sh`

## Out of Scope
Do not hand-edit the mirror, source, agents, release files, or polling scripts.
