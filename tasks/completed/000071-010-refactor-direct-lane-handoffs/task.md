# 000071-010-refactor-direct-lane-handoffs — Implementation Checklist

## Prerequisites
- [ ] `000070-020-refactor-impl-review-merge-base` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within the two named Codex skill directories and their required metadata/readmes.
- [ ] If inspection finds no needed wording change, make no edits.

## Stop Conditions
- [ ] Stop if the change would broaden `ywc-code-gen` or executor ownership.
- [ ] Stop if a shared routing contract needs behavioral edits in another task.
- [ ] Stop if generated marketplace files appear as required edits.

## Hardening Gate
- [ ] Classify as documentation-only routing maintenance.
- [ ] Use existing contract evals and diff inspection as the named exception to RED-first behavior coverage.
- [ ] Confirm no public runtime contract changes.
- [ ] No critical-surface review is required unless inspection reveals behavior changes; then stop and report.

## Implementation Steps
- [ ] Inspect current descriptions and handoff sections in `ywc-code-gen/SKILL.md` and `ywc-sequential-executor/SKILL.md`.
- [ ] Add only the direct single-item alternative wording required to prevent activation overlap.
- [ ] Update locale README or `agents/openai.yaml` files only when the repository contract requires metadata parity.
- [ ] Verify the existing generator and executor routes remain explicitly intact.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `git diff --check -- codex/skills/ywc-code-gen codex/skills/ywc-sequential-executor`

## Verification
- [ ] `bash scripts/run-codex-skill-contract-evals.sh` passes.
- [ ] Diff inspection confirms documentation-only scope.

## Implementation Notes
