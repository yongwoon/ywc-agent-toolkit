# yk-000012-010-domain-codex-merge-dependabot-parity — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] `yk-000011-010-domain-ci-gate-and-dependabot-lows` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `codex/skills/ywc-merge-dependabot/**`
  - `plugins/ywc-agent-toolkit/skills/ywc-merge-dependabot/**` (generated)
  - `plugins/ywc-agent-toolkit/README.md` (generated)
  - `scripts/validate.sh` (run_script_test_suites only)
  - `tests/codex_executable_resolution_test.py`
  - `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a spec premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] Implement `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md` **FR-1, FR-2, FR-3** and the API Contract table exactly, in `codex/skills/ywc-merge-dependabot/` (start from the T0-updated Claude Code script and test). Keep every clause pinned by `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` verbatim and the Dockerfile-detector marker block byte-identical; do not edit that fixture.
- [ ] Tests first (RED): the trimmed `test_merge_dependabot_scripts.py` with `SkillContractTest` must be seen failing on the pre-change Codex `SKILL.md` (record in Implementation Notes).
- [ ] Resolve the residual review Warnings from `docs/ywc-plans/20261107-p1-hardening-before-main-pr.review-5.md` while implementing (record each decision as a Ruling):
- [ ]   - W1 auto-intent-redundant: drop persisted `auto_intent` if the resume path reads live `autoMergeRequest,headRefOid` anyway; otherwise give it a real reader. Update the matching `SkillContractTest` assertion.
- [ ]   - W2 stage3-add-vs-uncertain-exclusion: limit "any non-zero result … adds it to `stage3`" to after the `autoMergeRequest` re-read, so `auto-merge-uncertain` PRs are never in Stage 3.
- [ ]   - W3 resume-no-state-reread: the resume read includes PR `state`; MERGED/CLOSED are recorded as terminal (also for `stage3` / `ci_wait` entries) instead of restarting.
- [ ]   - W4 uncertain-pr-advances-lane: an `auto-merge-uncertain` PR holds its lane (or moves the lane remainder to `stage3`), so two same-lockfile PRs can never auto-merge concurrently.
- [ ]   - W6 run-wide-deadline-vs-pinned-161: reword the unpinned parts of `SKILL.md:161` and the Stage 2 `deadline=$(…+1800)` illustration (~:224-225) to the run-wide deadline, keeping pinned phrases.
- [ ]   - W7 deadline-unreached-label-vs-167: amend the unpinned part of `SKILL.md:167` ("failed/stalled") so never-started PRs are `Skipped (deadline reached)`.
- [ ] Add the skill to `CALLER_FILES` in `tests/codex_executable_resolution_test.py` and raise both `== 20` counts by the new `bash "$RESOLVER_LAUNCHER"` call sites. Wire the Codex test into `scripts/validate.sh` `run_script_test_suites` (T0's pattern); break one assertion once to show validate.sh reports the ERROR, then revert (record in Implementation Notes).
- [ ] Update the Codex README lines FR-2/FR-3 name (ko/en/ja/default by hand; zh/es via the translation flow — if none exists, stop and report).
- [ ] Run `score.py --ci` last and stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (this task runs after every Phase 000011 task).
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: AC1, AC2, AC3 (FR-1, FR-2, FR-3)

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `cmp claude-code/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh codex/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh`
- [ ] `! grep -rq 'wait-dependabot-rebase' codex/skills/ywc-merge-dependabot`
- [ ] `python3 codex/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`
- [ ] `grep -q 'match-head-commit' codex/skills/ywc-merge-dependabot/SKILL.md`
- [ ] `! grep -nE 'gh pr merge (\{number\}|"\$)' codex/skills/ywc-merge-dependabot/SKILL.md | grep -v -- '--match-head-commit' | grep -v -- '--disable-auto' | grep -q .`
- [ ] `! grep -q 'gh pr checkout' codex/skills/ywc-merge-dependabot/SKILL.md`
- [ ] `grep -q 'codex/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py' scripts/validate.sh`
- [ ] `python3 tests/codex_executable_resolution_test.py`
- [ ] `python3 tests/codex_issue69_contract_test.py`
- [ ] `python3 tests/codex_issue69_behavior_test.py` (not run by validate.sh; re-run once on a single failure)
- [ ] `shellcheck codex/skills/ywc-merge-dependabot/scripts/*.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit if it changed
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" codex/skills/ywc-merge-dependabot/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->

- **RED (AC2):** the new `test_merge_dependabot_scripts.py` was run against the unchanged Codex `SKILL.md` and failed with 29 failures and 8 errors (`FAILED (failures=29, errors=8)`, 32 tests). All 15 `SkillContractTest` tests failed. All 8 `SequentialCiGateTest` tests raised `StopIteration` because the 3a gate marker did not exist yet. `CheckBaseRequiredChecksTest` passed (the script was already copied). After the change: `Ran 32 tests … OK`.
- **AC3 mutation:** `self.assertEqual(calls, 2)` was changed to `3` in `SkillContractTest`. `bash scripts/validate.sh` then exited 1 and printed `ERROR: merge-dependabot test suite failed: codex/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py` with the `2 != 3` tail. The change was reverted from a saved copy and checked with `grep`.
- **Resolver call sites:** there are 2 new `bash "$RESOLVER_LAUNCHER"` lines (the 3a gate and the Stage 1 lane start block that Stage 2 reuses). Both `== 20` counts are now `== 22`.
- **Line budget:** the `SKILL.md` body is 391 lines, so the `references/lane-state.md` fallback was not needed.
- **W1:** `auto_intent` was dropped. Every `--auto` start, including a resume, first reads `gh pr view {number} --json state,autoMergeRequest,headRefOid`. If that read finds auto-merge enabled, the PR is treated as active. So a persisted intent would have had no reader. The `SkillContractTest` assertion was changed to require that `auto_intent` is absent and that this pre-start read comes before the base check.
- **W2:** only an empty `autoMergeRequest` re-read after a non-zero `--auto` adds the PR to `stage3`. `auto-merge-uncertain` PRs are "never in `stage3`".
- **W3:** a resume first reads `state` for every PR in `active`, `stage3` and `ci_wait`. A `MERGED` or `CLOSED` PR is recorded as terminal.
- **W4:** an `auto-merge-uncertain` PR closes its lane, and the lane's remaining PRs move to `stage3`.
- **W6:** the unpinned part of the old `:161` now names one run-wide deadline, set once at the start of Step 3. The Stage 2 illustration reads `deadline=$RUN_DEADLINE` and no longer computes `+1800`.
- **W7:** at the deadline, PRs that never started are `Skipped (deadline reached)`. Only started PRs are marked failed/stalled.
- **zh/es:** these were edited by hand on the changed lines only. `scripts/translate.sh` was not run (it would rewrite `.claude/settings.json`). The AUTO-GENERATED headers are unchanged.
- **Review fixes:**
  - **M1:** after the resume state reads, each lane whose active PR was removed is advanced through the lane start block before polling. Its pre-start read adopts a PR whose auto-merge is already enabled as active. Stage 3 "drained" is now defined as `active` empty and every lane's queue empty.
  - **L4:** the second resolver line now maps any failure to `BLOCKED` with exit 3. The resolver call count stays at 22.
  - **RED:** `test_resume_advances_lanes_whose_active_pr_was_removed` and the updated `RESOLVER_RESOLVE` check both failed before the SKILL.md edit (`FAILED (failures=2)`). After the edit: `Ran 33 tests … OK`.
