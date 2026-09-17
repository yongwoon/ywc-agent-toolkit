# yw-000041-010-docs-verify-done-ledger

## Purpose
Teach Codex users about the optional Gate Ledger while preserving fresh-evidence workflow and localized discoverability.

## Scope
Add the optional section after Step 6, one focused eval fixture, and localized summaries in all six maintained README files.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md#fr-4-skill-eval-metadata-and-locales` — docs/eval/locale contract
- `docs/ywc-plans/20260917-codex-verify-done-gate-ledger-port.md#existing-constraints-touched` — preserved workflow boundaries
### Summary
Document installed-path CLI examples, arbitrary-shell warnings, status/resume/reverify, MANUAL and positive-control rules, and separate PR polling proof. Keep Steps 1–6, Claim Classification, `agents/openai.yaml`, and normal verification blocks unchanged.
### Out of Scope (from spec)
- Checker and grammar — Phase `yw-000040`
- Generated marketplace — `yw-000042-010-infra-verify-done-package-sync`
- Custom agents, root release files, cosmetic agent metadata, and Claim Classification changes

## Criticality
normal

## Dependencies
### Depends On
- `yw-000040-010-domain-gate-ledger-checker` — CLI/grammar source
- `yw-000040-020-test-gate-ledger-checker` — verified behavior
### Depended By
- `yw-000042-010-infra-verify-done-package-sync` — syncs finished source

## Key Files
- `codex/skills/ywc-verify-done/SKILL.md`
- `codex/skills/ywc-verify-done/evals/evals.json`
- `codex/skills/ywc-verify-done/README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md`

## Notes
Use `${CODEX_HOME:-$HOME/.codex}/skills/ywc-verify-done/scripts/gate-check.py` in every user-facing example. Keep `agents/openai.yaml` byte-identical.

## Hardening Evidence
- Test feedback path: predecessor checker suite plus `bash scripts/run-codex-skill-contract-evals.sh`.
- Interface Contract: consume the Phase `yw-000040` checker signature and grammar; do not synthesize a second parser contract.
- Data Integrity Hardening: N/A — docs/eval-only.
- Critical surface review: N/A for prose-only edits; preserve checker safety language.

## Ownership
`codex/skills/ywc-verify-done/SKILL.md`, its `evals/evals.json`, and six `README*.md` files only.

## Shared Surfaces
- Installed CLI examples, optional-ledger boundary, Steps 1–6, Claim Classification, eval schema, locale set

## Conflicts With
- `yw-000042-010-infra-verify-done-package-sync` — generated mirror waits for source finalization

## Parallelizable After
- `yw-000040-010-domain-gate-ledger-checker`
- `yw-000040-020-test-gate-ledger-checker`

## Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `jq empty codex/skills/ywc-verify-done/evals/evals.json`
- `git diff --check -- codex/skills/ywc-verify-done`

## Out of Scope
Do not edit checker code, generated files, agents, polling scripts, or release metadata.
