# 000077-020-infra-distribution-validation — Implementation Checklist

## Prerequisites
- [ ] `000077-010-test-context-safety-evaluation-matrix` is completed and merged.

## Allowed Edit Scope
- [ ] Edit only affected Codex metadata, root release metadata, discovered inventory source, and generated plugin output.
- [ ] Do not edit Claude Code sources.

## Stop Conditions
- [ ] Stop if the inventory source cannot be identified from repository scripts/validation.
- [ ] Stop if generated plugin output diverges from `codex/skills/`.
- [ ] Stop if isolated install writes into the real user Codex directory.

## Hardening Gate
- [ ] Record final eval and validation evidence before metadata edits.
- [ ] Record source-of-truth/inventory/plugin synchronization contract.
- [ ] Use isolated `CODEX_HOME` for installation smoke.

## Implementation Steps
- [ ] Discover and update the actual inventory file used by install/validation scripts.
- [ ] Synchronize affected skills' Tier 1/Tier 2 READMEs and `agents/openai.yaml` metadata.
- [ ] Update `VERSION` and `CHANGELOG.md` with the context-safety release entry.
- [ ] Run `bash scripts/sync-codex-plugin.sh` and inspect source/plugin parity.
- [ ] Run repository validation, install listing, focused evals, and isolated `ywc-agentic` installation smoke.

## Task Verify
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `CODEX_HOME=$(mktemp -d) bash scripts/install.sh --codex ywc-agentic`

## Verification
- [ ] structure, metadata, and plugin parity validation passes
- [ ] focused eval matrix passes
- [ ] isolated installation succeeds without touching the real user directory

## Implementation Notes

