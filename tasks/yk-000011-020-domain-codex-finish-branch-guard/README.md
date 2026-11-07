# yk-000011-020-domain-codex-finish-branch-guard

## Purpose
Port the Claude Code Remote deletion guard (yk-000010-040, security re-reviewed twice) rule for rule into the Codex `ywc-finish-branch` guard, and pin it with the issue69 fixtures and a contract test.

## Scope
- Implement `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md` **FR-4** exactly, in `codex/skills/ywc-finish-branch/SKILL.md` (guard at ~:309-315), keeping Codex numbering/style and every fixture-pinned clause verbatim. `check-ref-format --branch` and `If deletion relies on a merge` must appear nowhere in that file.
- Fixtures first (RED): update `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` (replace the `--branch` clause; add the required/forbidden clauses FR-4 lists) and `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json` (the `invalid-branch`, reorder and input changes FR-4 lists). Show `python3 tests/codex_issue69_contract_test.py` failing before the `SKILL.md` edit; record it in Implementation Notes.
- Residual review Warning 5 (`docs/ywc-plans/20261107-p1-hardening-before-main-pr.review-5.md`, completeness:finish-guard-order-not-regression-pinned): add a regression test to `tests/codex_issue69_contract_test.py` (run by `validate.sh`) asserting the step order by index (ls-remote tip < `--state merged` < `--state open` < `--force-with-lease`), and add required fixture clauses for the remaining sub-rules: url must not start with `-`, the exact `refs/heads/$branch` ls-remote line, fork-of-fork → `NEEDS_CONTEXT`, open-PR count printing exactly `0`.
- Update the guard description lines in the Codex finish-branch `README.md`, `README.en.md`, `README.ko.md`, `README.ja.md` by hand; regenerate `README.zh.md` / `README.es.md` through the repo's translation flow if one exists (never hand-edit an `AUTO-GENERATED` file; if no flow exists, stop and report).
- Let the pre-commit hook regenerate `plugins/ywc-agent-toolkit`; never hand-edit it.
- Read the Claude Code reference guard `claude-code/skills/ywc-finish-branch/SKILL.md:215-225` for wording; do not edit it.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md` — FR-4 (normative), AC4, Existing Constraints Touched, Failure Modes
- `docs/ywc-plans/20261107-p1-hardening-before-main-pr.review-5.md` — residual Warnings folded into Scope
- `docs/review-learnings.md`

### Summary
Spec FR-4 lists the seven steps in order (validate branch → pin push URL → bind host-qualified repo → exact tip → unconditional merged check → open-PR check last → tip-bound lease delete), the outcome map, the fixture clauses to keep verbatim, and the exact edits to the adoption and behavior fixtures.

### Out of Scope (from spec)
- P2-a (hook enforcement), P2-b (scan-secrets residual gaps), P2-c (real prompts for `ywc-mine-review-history`), P2-d (Codex `ywc-worktrees` C2 form); porting `wait-dependabot-rebase.sh`; the release gate (FR-6, post-run step).

## Criticality
critical — Spec Critical Surfaces: `codex/skills/ywc-finish-branch/SKILL.md` Remote deletion guard — remote branch deletion can auto-close an open PR.

## Dependencies

### Depends On
- (None)

### Depended By
- (None — the post-run release gate (FR-6) runs after all P1 tasks)

## Key Files
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-finish-branch/README*.md`
- `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` (finish-branch check only)
- `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json` (finish-branch cases only)
- `tests/codex_issue69_contract_test.py`
- `plugins/ywc-agent-toolkit/skills/ywc-finish-branch/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)

## Notes
- Line numbers come from the spec; re-locate each before editing. If a premise no longer matches the file, stop and report.

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-finish-branch/README*.md`
- `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` (finish-branch check only)
- `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json` (finish-branch cases only)
- `tests/codex_issue69_contract_test.py`
- `plugins/ywc-agent-toolkit/skills/ywc-finish-branch/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)

### Owned Interface
- Codex finish-branch Remote deletion guard contract (FR-4 step order and outcome map)

### Shared Surfaces
- `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` also holds the merge-dependabot check (read only here; yk-000012-010 must keep those clauses)

### Conflicts With
- (None identified — yk-000012-010 runs in the next phase)

### Parallelizable After
- (None)

### Task Verify
- `[ "$(grep -c 'check-ref-format --branch' codex/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 0 ]`
- `grep -qF 'check-ref-format "refs/heads/$branch"' codex/skills/ywc-finish-branch/SKILL.md`
- `grep -q 'get-url --push' codex/skills/ywc-finish-branch/SKILL.md`
- `grep -q 'env -u GH_HOST' codex/skills/ywc-finish-branch/SKILL.md`
- `[ "$(grep -c 'If deletion relies on a merge' codex/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 0 ]`
- `python3 -c "t=open('codex/skills/ywc-finish-branch/SKILL.md').read(); assert t.index('--state merged') < t.index('--state open') < t.index('force-with-lease')"`
- `python3 tests/codex_issue69_contract_test.py`
- `python3 tests/codex_issue69_behavior_test.py` (not run by validate.sh; on a single failure re-run once — AC3 notes a known flake)
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Wave 1 tasks do NOT commit the baseline; yk-000012-010 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" codex/skills/ywc-finish-branch/SKILL.md`

## Out of Scope
Anything not listed in Scope.
