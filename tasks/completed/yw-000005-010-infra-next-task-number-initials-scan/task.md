# yw-000005-010-infra-next-task-number-initials-scan — Implementation Checklist

## Prerequisites
- [ ] `yw-000004-010-docs-initials-resolution-reference` is completed and merged.
- [ ] `yw-000004-020-infra-parser-optional-initials-prefix` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only `claude-code/skills/ywc-task-generator/scripts/next-task-number.sh` and the fixtures this task creates.

## Stop Conditions
- [ ] Stop if invoking the script with no `initials` argument produces output differing from the pre-change build.
- [ ] Stop if a GNU-only or non-macOS tool (`flock`, `grep -P`, GNU `sed -i`) becomes necessary.
- [ ] Stop if reservation refs would be created under `refs/heads/`.
- [ ] Stop if the drift cross-check emits a warning on this repository's current state with no `yk-` entries in the graph.

## Hardening Gate
- [ ] Capture the pre-change output of `next-task-number.sh tasks` as the NFR1 baseline before editing.
- [ ] Record the atomic reservation strategy and the retry contract in the script comments.
- [ ] Record AC11 evidence: a repeated `git update-ref` against the same ref exits non-zero.

## Implementation Steps
- [ ] Capture the NFR1 baseline: run `bash claude-code/skills/ywc-task-generator/scripts/next-task-number.sh tasks` and save stdout and stderr for later comparison.
- [ ] Add an optional second positional argument `initials` to the script, validated against `^[a-z0-9]{2,4}$`; reject an invalid value with exit 1 and a clear message.
- [ ] When `initials` is present, change the PHASE-candidate regex to `^<initials>-([0-9]{6})-[0-9]{3}-`, excluding both other-initials entries and unprefixed legacy entries from the comparison.
- [ ] When `initials` is absent, leave every existing code path byte-for-byte unchanged so legacy callers see no behavior change.
- [ ] Normalize `tasks-dir` before any worktree join: if it is absolute, strip the `git rev-parse --show-toplevel` prefix to relativize it; if it resolves outside the repository, skip the union entirely and scan only the current worktree.
- [ ] Iterate `git worktree list --porcelain`, and for each `worktree <path>` scan `<path>/<tasks-dir>` and `<path>/<tasks-dir>/completed` with the same candidate regex, folding each result into the running max.
- [ ] Skip a worktree path silently when the joined directory does not exist — absence is not an error.
- [ ] Implement the legacy seed rule: when the union yields zero `<initials>-` entries and at least one unprefixed legacy entry exists, seed the first PHASE at `legacy max + 1`; disable the rule as soon as any prefixed entry exists.
- [ ] Scope the existing `dependency-graph.md` drift cross-check to `<initials>-[0-9]{6}-[0-9]{3}-`, and skip the comparison entirely (no stderr warning) when the graph holds zero entries for those initials.
- [ ] Add the reservation step immediately before the chosen PHASE `N` is emitted: `git update-ref "refs/ywc/task-phase/<initials>/<phase>" HEAD ''`; on non-zero exit increment `N` and retry.
- [ ] Cap reservation retries at 100; on exhaustion exit 1 and report the number of refs under `refs/ywc/task-phase/<initials>/` in the error message.
- [ ] Skip reservation entirely when `initials` was not supplied, preserving the legacy no-op path.
- [ ] Add a helper that collects the unique set of existing initials prefixes matching `^([a-z0-9]{2,4})-[0-9]{6}-[0-9]{3}-` across `<tasks-dir>`, `<tasks-dir>/completed`, and every linked worktree, with the per-initials entry count, and expose it for the confirmation prompt (AC12).
- [ ] Write a comment block at the top of the script covering: the CAS semantics of the empty old-value, why refs are never released (burned numbers beat reused numbers), why `refs/ywc/**` avoids branch-list pollution, and that separate clones are explicitly out of scope.
- [ ] Build a fixture directory containing only `ab-000050-010-db-x` and run with `yk`; assert `ab-` is ignored (AC4).
- [ ] Build a legacy-only fixture and assert the first PHASE is legacy max + 1 (AC3).
- [ ] Create a throwaway linked worktree via `git worktree add` holding `yk-000012-010-db-x`, run from the primary worktree, and assert `000013-010` (AC5); remove the worktree afterwards.
- [ ] Replay the NFR1 baseline invocation and diff against the captured output.

## Task Verify
- [ ] `shellcheck claude-code/skills/ywc-task-generator/scripts/next-task-number.sh`
- [ ] No-initials invocation output matches the captured baseline exactly
- [ ] AC3 legacy-seed fixture returns legacy max + 1
- [ ] AC4 fixture with `ab-` entries returns the `yk` sequence unaffected
- [ ] AC5 linked-worktree fixture returns `000013-010`
- [ ] AC11: `git update-ref refs/ywc/task-phase/yk/000099 HEAD ''` succeeds once and fails on repeat
- [ ] AC12: the initials-advisory helper reports an existing count when `yk-` entries exist and an empty list when they do not
- [ ] `git branch -a` shows no new branches after reservation

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] shellcheck run locally (CI does not cover `claude-code/skills/**/scripts`)
- [ ] typecheck passes (N/A — shell script)
- [ ] unit tests pass (fixture runs above)
- [ ] app builds without error (N/A — documentation/tooling repository)
