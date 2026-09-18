# yw-000049-010-infra-granularity-distribution — Implementation Checklist

## Prerequisites
- [ ] `yw-000048-010-docs-granularity-contract` is completed and merged.
- [ ] `yw-000048-020-docs-granularity-readmes` is completed and merged.
- [ ] `yw-000048-030-test-granularity-evals` is completed and merged.

## Allowed Edit Scope
- [ ] Run the standard synchronization into `plugins/ywc-agent-toolkit/skills/**`.
- [ ] Do not hand-edit generated files or modify source contract files in this task.

## Stop Conditions
- [ ] Stop if synchronization reports an error or generated output does not match source after one clean sync.
- [ ] Stop if targeted searches find superseded thresholds in affected source or generated surfaces.
- [ ] Stop if validation or contract evals fail; report the exact command and preserve the failure for follow-up.

## Hardening Gate
- [ ] Classify as generated-file/distribution validation work.
- [ ] Record named exception: no production behavior; sync inspection and full validation replace RED-first evidence.
- [ ] Record the source-to-mirror contract before running synchronization.
- [ ] Mark Data Integrity and critical-surface review as N/A.

## Implementation Steps
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the repository root.
- [ ] Inspect the generated `plugins/ywc-agent-toolkit/skills/ywc-task-generator/**` diff for source parity and absence of unrelated changes.
- [ ] Run targeted searches for `~15/~500`, `~35/~1,200`, and absence of superseded `~10/~300` and `~25/~800` values across affected source and mirror files.
- [ ] Run `git diff --check`, `bash scripts/validate.sh`, and `bash scripts/run-codex-skill-contract-evals.sh`.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `git diff --check`
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — documentation/distribution change)
- [ ] unit tests pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] integration tests pass (N/A — generated package validation)
- [ ] app builds without error (N/A — repository has no application build command)

## Implementation Notes

