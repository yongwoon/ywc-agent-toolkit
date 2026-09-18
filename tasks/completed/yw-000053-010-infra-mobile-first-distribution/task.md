# yw-000053-010-infra-mobile-first-distribution — Implementation Checklist

## Prerequisites
- [ ] `yw-000052-010-test-mobile-first-contract-eval` is completed and merged.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh` passes on source files.
- [ ] `bash scripts/check-codex-agent-evals.sh` passes.

## Allowed Edit Scope
- [ ] Run the sync tool and inspect generated output under the declared Ownership.
- [ ] Do not hand-edit generated plugin files; fix source files in an earlier task if parity is wrong.

## Stop Conditions
- [ ] Stop if source contract checks fail.
- [ ] Stop if synchronization produces unexpected files outside the generated Codex plugin package.
- [ ] Stop if generated output disagrees with source beyond the sync script’s documented rewrites.

## Hardening Gate
- [ ] Classify as generated-file/package validation work.
- [ ] Use source-contract, agent-eval, sync, diff-check, and full validation evidence as the named verification path.
- [ ] Mark interface, data integrity, and critical review as N/A.

## Implementation Steps
- [ ] Run `bash scripts/run-codex-skill-contract-evals.sh` and `bash scripts/check-codex-agent-evals.sh` before synchronization.
- [ ] Run `bash scripts/sync-codex-plugin.sh` so `codex/skills/` remains the source of truth.
- [ ] Inspect `git diff -- plugins/ywc-agent-toolkit/skills plugins/ywc-agent-toolkit/.codex-plugin/plugin.json` for expected generated parity.
- [ ] Run `git diff --check` and `bash scripts/validate.sh`.
- [ ] Confirm no Claude Code files, hand-authored generated edits, or unrelated package changes are present.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/check-codex-agent-evals.sh`
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `git diff --check`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] lint passes (`covered by bash scripts/validate.sh and CI shellcheck gate`)
- [ ] typecheck passes (`N/A — repository contains no application typecheck command`)
- [ ] unit tests pass (`bash scripts/run-codex-skill-contract-evals.sh` and `bash scripts/check-codex-agent-evals.sh`)
- [ ] integration tests pass (`N/A — package/documentation change`)
- [ ] app builds without error (`N/A — package distribution repository`)

## Implementation Notes

