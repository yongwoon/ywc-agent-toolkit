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

Extending `scandir` to `claude-code/skills` scans recursively (confirmed via the action's
`action.yaml`) and surfaced pre-existing `shellcheck` findings in 10 files across 5 sibling
skills outside this task's declared Ownership (`ywc-create-pr`, `ywc-docker-isolate`,
`ywc-onboard-repo`, `ywc-skill-author`, `ywc-spec-writer`) — the task's premise that only the 4
named scripts had lint debt was incomplete. Flagged as `NEEDS_CONTEXT`; orchestrator resolved:
add a second `ShellCheck (claude-code/skills)` step with `ignore_paths` carving out those 10
files by exact relative path (not a directory or the whole scandir), so every other file under
`claude-code/skills` — including `resolve-language.sh`, `resolve-initials.sh`, and the 4 named
scripts — stays genuinely linted. Verified locally by reproducing the action's exact
word-splitting exclude-building logic (`ignore_paths` matches via `find ... ! -path
<exact-path>`) and running it against this repo — confirmed the 10 files are excluded and every
other `.sh` file, including the ones that must stay linted, is not.

Excluded files (pre-existing debt, tracked for a follow-up cleanup task — fix or suppress each
finding, then drop the corresponding `ignore_paths` entry):
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` (SC2001)
- `claude-code/skills/ywc-docker-isolate/scripts/_lib.sh` (SC2034 ×5)
- `claude-code/skills/ywc-docker-isolate/scripts/audit-docker-stacks.sh` (SC1091)
- `claude-code/skills/ywc-docker-isolate/scripts/setup-docker-ports.sh` (SC1091)
- `claude-code/skills/ywc-docker-isolate/scripts/teardown-docker.sh` (SC1091)
- `claude-code/skills/ywc-onboard-repo/scripts/recon.sh` (SC2012)
- `claude-code/skills/ywc-skill-author/scripts/build-variant.sh` (SC1091)
- `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh` (SC2086)
- `claude-code/skills/ywc-skill-author/tests/audit-skills-test.sh` (SC1007 ×2, SC2016)
- `claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh` (SC2221, SC2222)

The 4 named scripts (`mark-complete.sh`, `poll-pr-reviews.sh`, `scan-stubs.sh`,
`test-poll-pr-reviews.sh`) and both resolver scripts already passed `shellcheck` cleanly on
first run — nothing to fix or suppress in them, so no inline `# shellcheck disable=` comments
were needed anywhere in this batch.
