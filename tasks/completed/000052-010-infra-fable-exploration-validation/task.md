# 000052-010-infra-fable-exploration-validation — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000051-010-docs-shared-exploration-references` is completed (merged)
- [ ] `000051-020-docs-discovery-skill-exploration-hooks` is completed (merged)
- [ ] `000051-030-docs-execution-skill-implementation-notes` is completed (merged)
- [ ] `000051-040-docs-skill-author-exploration-rules` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `bash scripts/sync-codex-plugin.sh` produces unexpected generated diffs outside the Codex plugin skill package
- [ ] Stop if `bash scripts/validate.sh` fails and the failure indicates an upstream task contract break rather than a local validation-script issue
- [ ] Stop if executor line-count exceeds 500 after merge and no upstream corrective task has addressed it

## Implementation Steps
- [ ] Run `bash scripts/sync-codex-plugin.sh` so generated Codex plugin skills reflect the source-of-truth edits under `codex/skills/**`.
  - Related AC/FR: `[AC6]` / `[FR10]`
  - Contract / Behavior Change: generated plugin package catches up to source skill changes.
  - Verification Command / Evidence: sync script exit 0 + generated diff review
- [ ] Run repository validation and targeted grep checks for the new shared references, output sections, metadata sync, and executor line-cap safety.
  - Related AC/FR: `[AC1]`–`[AC9]`
  - Contract / Behavior Change: batch-level readiness is asserted with concrete commands.
  - Verification Command / Evidence: `bash scripts/validate.sh`, `wc -l ...`, targeted `rg`
- [ ] Review diff scope to ensure the batch stayed within Codex skill/reference/plugin boundaries and did not spill into unrelated surfaces.
  - Related AC/FR: `[AC5]`
  - Contract / Behavior Change: final batch remains scope-safe and auditable.
  - Verification Command / Evidence: `git diff --stat` / `git diff --name-only`

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
  - Expected Passing Signal: script exits 0 and only generated plugin package files change as a result.
  - Pre-change Failing Evidence / Exception: plugin package is stale before sync when source skill content changed.
  - Contract/Test Evidence: diff review of `plugins/ywc-agent-toolkit/skills/**`.
- [ ] `bash scripts/validate.sh`
  - Expected Passing Signal: all checks passed.
  - Pre-change Failing Evidence / Exception: validation may fail before upstream tasks finish their sync and structural updates.
  - Contract/Test Evidence: command output excerpt in completion summary.
- [ ] `wc -l codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`
  - Expected Passing Signal: both files are `<=500` lines.
  - Pre-change Failing Evidence / Exception: baseline headroom was only 2 lines per file before upstream edits.
  - Contract/Test Evidence: numeric line-count output.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (`N/A — repository has no standalone typecheck pipeline`)
- [ ] unit tests pass (`N/A — validation/sync task`)
- [ ] integration tests pass (if applicable)
- [ ] app builds without error (`N/A — documentation bundle repository`)
