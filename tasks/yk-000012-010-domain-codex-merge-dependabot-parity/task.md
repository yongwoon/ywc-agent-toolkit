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
