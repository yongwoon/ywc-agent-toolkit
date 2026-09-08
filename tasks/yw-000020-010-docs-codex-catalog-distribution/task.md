# yw-000020-010-docs-codex-catalog-distribution — Implementation Checklist

## Prerequisites
- [ ] `yw-000019-030-test-mine-review-history-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Edit only the catalog/root README source files and generated output produced by the sync script.
- [ ] Do not edit custom-agent files or generated package files by hand.

## Stop Conditions
- [ ] Stop if the calculated source count differs from the requested catalog count.
- [ ] Stop if sync reveals unrelated source drift or executable-mode loss.

## Hardening Gate
- [ ] Classify as documentation/generated-file-only distribution work.
- [ ] Record existing sync and validation coverage before edits.
- [ ] Treat source/package parity as the shared contract; return `NEEDS_CONTEXT` on unexpected drift.

## Implementation Steps
- [ ] Add the `ywc-mine-review-history` skill-table row near `ywc-review-learnings` in `codex/skills/README.md`.
- [ ] Add the periodic/batch routing boundary row to the routing guide in the same catalog.
- [ ] Count `codex/skills/*` directories and update the Codex count consistently in `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, and `README.es.md`.
- [ ] Run `bash scripts/sync-codex-plugin.sh`, inspect the generated skill tree, confirm helper executable mode, and leave custom-agent catalog files unchanged.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `bash scripts/install.sh --list --codex-agents`
- [ ] `git diff --check`

## Verification
- [ ] lint: N/A — documentation/generated distribution change
- [ ] typecheck: N/A
- [ ] tests: `bash scripts/install.sh --list --codex`
- [ ] build: `bash scripts/sync-codex-plugin.sh`
