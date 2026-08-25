# yw-000003-010-eval-bundle-validation — Implementation Checklist

## Prerequisites
- [ ] `yw-000001-030-parser-prefixed-task-ids` is completed and merged.
- [ ] `yw-000002-020-consumer-legacy-compatibility` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only generated sync output and this task graph entry; source docs/evals belong to predecessor tasks.

## Stop Conditions
- [ ] Stop if synchronization would modify `claude-code/**` or unrelated files.
- [ ] Stop if pre-existing deleted `docs/ywc-plans/` files change state.
- [ ] Stop if source/generated parity cannot be established without hand-editing generated output.

## Hardening Gate
- [ ] Record predecessor verification results before finalization.
- [ ] Record the source-to-generated parity contract.
- [ ] Mark Data Integrity Hardening N/A for generated/documentation-only work.

## Implementation Steps
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the source tree.
- [ ] Run targeted setup, generator, parser, executor, and finish-branch fixtures from predecessor tasks.
- [ ] Run `bash scripts/install.sh --list` and `bash scripts/validate.sh`.
- [ ] Review source/generated parity, `git diff --stat`, and status to confirm unrelated deletions remain untouched.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/install.sh --list`
- [ ] `bash scripts/validate.sh`
- [ ] Run all focused fixtures for this spec.
- [ ] Confirm generated copies match source copies and no `claude-code/**` files changed.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — documentation/tooling repository)
- [ ] unit tests pass (all focused fixtures)
- [ ] integration tests pass (N/A — no external integration)
- [ ] app builds without error (N/A — documentation/tooling repository)
