# yk-000011-020-domain-codex-finish-branch-guard — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `codex/skills/ywc-finish-branch/SKILL.md`
  - `codex/skills/ywc-finish-branch/README*.md`
  - `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` (finish-branch check only)
  - `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json` (finish-branch cases only)
  - `tests/codex_issue69_contract_test.py`
  - `plugins/ywc-agent-toolkit/skills/ywc-finish-branch/**` (generated)
  - `plugins/ywc-agent-toolkit/README.md` (generated)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a spec premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] Implement `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md` **FR-4** exactly, in `codex/skills/ywc-finish-branch/SKILL.md` (guard at ~:309-315), keeping Codex numbering/style and every fixture-pinned clause verbatim. `check-ref-format --branch` and `If deletion relies on a merge` must appear nowhere in that file.
- [ ] Fixtures first (RED): update `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` (replace the `--branch` clause; add the required/forbidden clauses FR-4 lists) and `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json` (the `invalid-branch`, reorder and input changes FR-4 lists). Show `python3 tests/codex_issue69_contract_test.py` failing before the `SKILL.md` edit; record it in Implementation Notes.
- [ ] Residual review Warning 5 (`docs/ywc-plans/20261107-p1-hardening-before-main-pr.review-5.md`, completeness:finish-guard-order-not-regression-pinned): add a regression test to `tests/codex_issue69_contract_test.py` (run by `validate.sh`) asserting the step order by index (ls-remote tip < `--state merged` < `--state open` < `--force-with-lease`), and add required fixture clauses for the remaining sub-rules: url must not start with `-`, the exact `refs/heads/$branch` ls-remote line, fork-of-fork → `NEEDS_CONTEXT`, open-PR count printing exactly `0`.
- [ ] Update the guard description lines in the Codex finish-branch `README.md`, `README.en.md`, `README.ko.md`, `README.ja.md` by hand; regenerate `README.zh.md` / `README.es.md` through the repo's translation flow if one exists (never hand-edit an `AUTO-GENERATED` file; if no flow exists, stop and report).
- [ ] Let the pre-commit hook regenerate `plugins/ywc-agent-toolkit`; never hand-edit it.
- [ ] Read the Claude Code reference guard `claude-code/skills/ywc-finish-branch/SKILL.md:215-225` for wording; do not edit it.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: AC4 (FR-4)

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -c 'check-ref-format --branch' codex/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `grep -qF 'check-ref-format "refs/heads/$branch"' codex/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -q 'get-url --push' codex/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -q 'env -u GH_HOST' codex/skills/ywc-finish-branch/SKILL.md`
- [ ] `[ "$(grep -c 'If deletion relies on a merge' codex/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `python3 -c "t=open('codex/skills/ywc-finish-branch/SKILL.md').read(); assert t.index('--state merged') < t.index('--state open') < t.index('force-with-lease')"`
- [ ] `python3 tests/codex_issue69_contract_test.py`
- [ ] `python3 tests/codex_issue69_behavior_test.py` (not run by validate.sh; on a single failure re-run once — AC3 notes a known flake)
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Wave 1 tasks do NOT commit the baseline; yk-000012-010 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" codex/skills/ywc-finish-branch/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
- RED (fixtures + order test before the `SKILL.md` edit): `python3 tests/codex_issue69_contract_test.py` → `FAILED (failures=1, errors=1)`; failure: `missing 'must match \`^[A-Za-z0-9._/-]+$\` over the whole string, ...'`; error: order test `ValueError: substring not found` (no `check-ref-format "refs/heads/$branch"`). The order check over the four Warning-5 steps on the old text gave positions `[908, 1194, 577, 1565]` (ls-remote, merged, open, lease) → not sorted, so the open-before-tip order is caught.
- GREEN: after the guard rewrite the contract test passes (4 tests OK). A first draft wrote "Only a successful, ..." and the pinned lowercase clause caught it; reworded to keep it verbatim.
- `wrong-base` / `moved-tip` traces drop the "parsed empty open query" step: under FR-4 a failed merged check stops before step 6, so that step is unreachable.
- Review fix round: `scripts/translate.sh` garbled the guard terms and drifted sibling terms, so zh/es were restored from `feature/improvement-20261106` and only the guard paragraph was hand-patched (AUTO-GENERATED header kept).
- Review fix round RED: the open-PR clause was changed from `--jq length` / "print exactly `0`" to an in-process array check (`the parsed array must have exactly 0 entries`; `--jq length` is now forbidden), and required clauses were added for `BLOCKED: invalid branch name` and the `--jq` ban. The contract test then failed (`missing 'the parsed array must have exactly 0 entries'`) before the `SKILL.md` step 6 edit, and passed after it. The two new required clauses already existed in the text; the behavior test's per-clause removal is their negative control. `invalid-branch` input is now `feature/a$b`, which fails the allowlist itself rather than the leading-`-` rule.
