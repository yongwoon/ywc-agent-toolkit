# 000027-020-refactor-pr-health-handler — Manual Test Plan

## Preconditions
- [ ] `gh` is authenticated for a repository with at least one open PR.
- [ ] `jq` is installed.

## Test Scenarios

### Scenario 1: Helper emits PR health artifacts
**Steps:**
1. Run `bash codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh <pr-number>` in a GitHub repository.
2. Pipe the output to `jq type`.

**Expected Result:**
- Output is valid JSON.
- Top-level JSON type is `array`.
- Status or merge-readiness artifacts are present even when no unresolved review comments exist.

### Scenario 2: Empty review comments do not terminate the workflow
**Steps:**
1. Read `codex/skills/ywc-handle-pr-reviews/SKILL.md`.
2. Locate the branch handling empty review/comment artifacts.

**Expected Result:**
- The instructions explicitly continue to CI status and merge-readiness checks.
- The final summary reports artifact, CI, and merge-readiness state separately.
