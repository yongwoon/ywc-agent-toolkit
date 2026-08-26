# yw-000009-010-infra-codex-package-sync — Implementation Checklist

## Prerequisites
- [ ] `yw-000008-010-test-collector-contract-harness` is completed and merged.
- [ ] The source focused unittest passes before synchronization.

## Allowed Edit Scope
- [ ] Run the existing sync command and allow it to update generated `plugins/ywc-agent-toolkit/skills/**` output.
- [ ] Do not edit `scripts/sync-codex-plugin.sh` or source behavior as part of this task.

## Stop Conditions
- [ ] Stop if the source test is absent or its focused test fails.
- [ ] Stop if sync produces Claude, Nitpick, `raw_fallback`, or production collector changes.
- [ ] Stop if source/generated parity cannot be established without manually editing generated files.

## Hardening Gate
- [ ] Classify this as generated-file-only mechanical maintenance.
- [ ] Use the predecessor focused test as existing coverage and the parity diff as the task-specific feedback path.
- [ ] Record the source-to-generated bundle contract before running sync.
- [ ] Mark Data Integrity Hardening and critical-surface review N/A.

## Implementation Steps
- [ ] Verify `yw-000008-010-test-collector-contract-harness` output and run its focused unittest.
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the repository root.
  - [ ] Confirm `plugins/ywc-agent-toolkit/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py` exists.
  - [ ] Confirm generated output is derived from `codex/skills/`, not independently authored.
- [ ] Compare the source and generated test files byte-for-byte with `diff -u`.
- [ ] Run `bash scripts/install.sh --list --codex` and `bash scripts/validate.sh`.
- [ ] Inspect `git diff --name-only` and confirm no Claude files, Nitpick parser/producer, `raw_fallback`, or production collector file changed.

## Task Verify
- [ ] `python3 -m unittest codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `diff -u codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py plugins/ywc-agent-toolkit/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --name-only | rg -v '^(codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py|plugins/ywc-agent-toolkit/skills/ywc-handle-pr-reviews/)'` is empty or contains only pre-existing user changes.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — tooling repository has no typecheck command)
- [ ] unit tests pass (focused unittest command above)
- [ ] integration tests pass (N/A — package sync validation only)
- [ ] app builds without error (N/A — tooling repository has no build pipeline)
