# 000027-020-refactor-pr-health-handler — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] GitHub CLI `gh` and `jq` are available locally for script syntax and shape checks.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-handle-pr-reviews/**`.

## Stop Conditions
- [ ] Stop if GitHub API permissions prevent understanding the required helper payload shape.
- [ ] Stop if changing the artifact schema requires changing executor files.
- [ ] Stop if a stale `fetch-unresolved-comments.sh` reference is required by another active skill contract.

## Implementation Steps
- [ ] Replace the comments-only retrieval step in `codex/skills/ywc-handle-pr-reviews/SKILL.md`.
  - [ ] Rename the retrieved data concept to review artifacts, CI status, and merge-readiness.
  - [ ] State that an empty review artifact array still proceeds through CI and merge-readiness gates.
  - [ ] Update final summary fields from comments-only counts to artifact / CI / merge-readiness state.
- [ ] Add `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`.
  - [ ] Resolve repository from `GH_REPO` or `gh repo view`.
  - [ ] Fetch unresolved review threads, PR comments, review submissions, `statusCheckRollup`, `mergeable`, `mergeStateStatus`, and `url`.
  - [ ] Emit one normalized JSON array with required fields.
  - [ ] Use exit code `3` for `gh` or API failures and a distinct usage failure code.
- [ ] Remove or deprecate `fetch-unresolved-comments.sh`.
  - [ ] Ensure no runtime instruction points to the old helper name.
  - [ ] Preserve executable bit on the new helper.
- [ ] Update `codex/skills/ywc-handle-pr-reviews/agents/openai.yaml`.
  - [ ] Expand display text from review comments to review, CI, and merge blockers.
  - [ ] Adjust default prompt to call the handler as a PR health sweep.

## Task Verify
- [ ] `bash -n codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- [ ] `test -x codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- [ ] `rg -n "review artifacts, CI status, and merge-readiness|fetch-pr-review-artifacts|merge_readiness|status_check" codex/skills/ywc-handle-pr-reviews`
- [ ] `rg -n "fetch-unresolved-comments" codex/skills/ywc-handle-pr-reviews`

## Verification
- [ ] Repository validation is deferred to `000028-010-infra-plugin-sync-validation`.
- [ ] `git diff --name-only` for this task contains only `codex/skills/ywc-handle-pr-reviews/**`.
