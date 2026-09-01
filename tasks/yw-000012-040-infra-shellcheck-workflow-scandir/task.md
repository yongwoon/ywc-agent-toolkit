# yw-000012-040-infra-shellcheck-workflow-scandir — Implementation Checklist

## Prerequisites

- [ ] `yw-000012-020` is completed (merged) — `resolve-language.sh` exists
- [ ] `yw-000012-030` is completed (merged) — `resolve-initials.sh` exists

## Allowed Edit Scope

- [ ] Stay within `.github/workflows/validate.yml` and the 4 named shared shell scripts
- [ ] Do not touch `update-state.py` (Python, out of shellcheck's scope) or any other file under `claude-code/skills/`

## Stop Conditions

- [ ] Stop and report if a shellcheck finding in a shared script requires a behavior change that could affect a live consumer (`ywc-finish-branch`, etc.) — surface it rather than silently patching
- [ ] Stop if satisfying CI green requires a blanket top-of-file disable instead of a per-finding, reasoned suppression

## Implementation Steps

- [ ] Extend the ShellCheck step in `.github/workflows/validate.yml` to scan `claude-code/skills` in addition to `./scripts` (second `scandir` entry, or a matrix over both roots)
- [ ] Run `shellcheck` locally over the 4 shared scripts (`mark-complete.sh`, `poll-pr-reviews.sh`, `scan-stubs.sh`, `test-poll-pr-reviews.sh`) and triage every finding
  - Fix where the fix is small and behavior-preserving
  - Suppress with `# shellcheck disable=<code>` plus an inline reason where a fix would be riskier than the finding
- [ ] Confirm `resolve-language.sh` and `resolve-initials.sh` pass shellcheck cleanly (already required by `yw-000012-020`/`yw-000012-030`'s own Task Verify — this step confirms the CI-wired scandir actually reaches them)

## Task Verify

- [ ] `shellcheck claude-code/skills/scripts/resolve-language.sh claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` exits 0
- [ ] `shellcheck claude-code/skills/scripts/*.sh` exits 0 (post-triage)

## Verification

- [ ] `bash scripts/validate.sh` exits 0
- [ ] The workflow's ShellCheck step, run locally or via `act`/manual inspection, reports a non-empty file list for the `claude-code/skills` scandir

## Implementation Notes (optional)
