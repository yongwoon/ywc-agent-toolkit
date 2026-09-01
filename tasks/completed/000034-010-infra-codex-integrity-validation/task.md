# 000034-010-infra-codex-integrity-validation - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000033-010-docs-impl-review-integrity-catalog` is completed and merged.
- [ ] `000033-020-docs-spec-task-integrity-guidance` is completed and merged.
- [ ] `000033-030-docs-executor-integrity-gates` is completed and merged.

## Allowed Edit Scope

- [ ] Prefer generated sync output under `plugins/ywc-agent-toolkit/skills/**` only.
- [ ] Source skill edits are allowed only for direct validation fixes caused by this batch.
- [ ] If validation reveals unrelated existing drift, report it separately instead of broad cleanup.

## Stop Conditions

- [ ] Stop if `bash scripts/sync-codex-plugin.sh` would overwrite unrelated user changes.
- [ ] Stop if `bash scripts/validate.sh` fails for a reason unrelated to this batch and remediation would require out-of-scope edits.
- [ ] Stop if generated plugin output differs from source in a way the sync script does not explain.

## Hardening Gate

- [ ] Classify this task: infra validation / generated-file sync.
- [ ] Existing coverage: `bash scripts/validate.sh`.
- [ ] Interface contract: source `codex/skills/**` and generated `plugins/ywc-agent-toolkit/skills/**` must be consistent.
- [ ] Critical surface review: final diff must be reviewed because this batch changes review and execution guidance.

## Implementation Steps

- [ ] Inspect final source diff from Phase `000033`.
  - [ ] Confirm no `claude-code/**` edits are present.
  - [ ] Confirm no direct manual edits under `plugins/ywc-agent-toolkit/skills/**` predate sync.
  - [ ] Confirm README mirror decisions were recorded by source tasks.
- [ ] Run targeted evidence search.
  - [ ] `rg -n "race condition|concurrent write|partial write|transaction boundary|idempotency" codex/skills/ywc-impl-review codex/skills/ywc-spec-validate codex/skills/ywc-task-generator codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`
  - [ ] Confirm each intended skill surface has evidence or an explicit no-change rationale.
- [ ] Run install list scan.
  - [ ] `bash scripts/install.sh --list --codex`
  - [ ] Fix only source/package issues caused by this batch.
- [ ] Sync generated Codex plugin package if source skill files changed.
  - [ ] `bash scripts/sync-codex-plugin.sh`
  - [ ] Review generated diff to ensure it mirrors `codex/skills/**`.
- [ ] Run full validation.
  - [ ] `bash scripts/validate.sh`
  - [ ] If it fails because of pre-existing stale package or `__pycache__` drift, report exact output and classify as `DONE_WITH_CONCERNS` unless source validation is blocked.
  - [ ] If it fails because of this batch, fix and rerun.

## Task Verify

- [ ] `rg -n "race condition|concurrent write|partial write|transaction boundary|idempotency" codex/skills/ywc-impl-review codex/skills/ywc-spec-validate codex/skills/ywc-task-generator codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `bash scripts/validate.sh`

## Verification

- [ ] Final diff reviewed for Codex-only boundary.
- [ ] Generated plugin package is synced or a blocker is reported.
- [ ] Completion report includes validation command, exit code, and relevant output excerpt.
