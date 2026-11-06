# yk-000004-010-domain-plan-auto-converge

## Purpose
Replace the y/n question in `ywc-plan` Step 5 with an automatic `ywc-spec-ready` run for Medium/Large specs, add `--no-converge`, and keep recursion/double-run impossible (AC1, AC2, AC2b, AC2c, FR6, FR7).

Spec item: A1 (#371) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- `ywc-plan/SKILL.md`: Step 5 calls `/ywc-spec-ready --spec <path>` without asking; Arguments table gains `--no-converge`; `--non-interactive` also skips the Step 5 auto-run (caller owns the next step).
- Step 4c (Re-plan Mode `--update-spec`) gains a new step 7: compact confirmation `✅ Spec amended: <path> (Iteration N)` then stop, so Step 5 is never reached (prevents spec-ready recursing into itself).
- If the auto-run `ywc-spec-ready` ends `BLOCKED` / `NEEDS_CONTEXT` / `DONE_WITH_CONCERNS`, `ywc-plan` surfaces its Completion Report verbatim and leaves the spec drafted (no retry, no auto-fix).
- Update Rationalization Defense (2 rows), the Validation checklist (`:381`) and Integration (`:397`) so no stale 'ask the user' claim remains.
- Update the option table and the `ywc-spec-ready` introduction line in the four Tier 1 `ywc-plan` READMEs (currently described as 'opt-in').
- `ywc-auth-implement/SKILL.md`: add the new Step 3 sentence passing the policy interview to `/ywc-plan --no-converge` (it has no `ywc-plan` call today).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 1 (A1), FR6, FR7, AC1, AC2, AC2b, AC2c, Failure Modes rows on recursion / double execution / non-DONE
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-plan/SKILL.md` — upstream final Step 5 / Step 4c wording (T0 snapshot)
- `claude-code/skills/ywc-agentic/SKILL.md` — `:93-104` — caller that must stay unchanged

### Summary
Upstream replaced the y/n prompt with an automatic convergence run. Locally `ywc-agentic` already calls `ywc-plan --non-interactive` and then `ywc-spec-ready` itself, so the `--non-interactive` skip prevents a double loop. `ywc-spec-ready` calls `ywc-plan --update-spec`, so Re-plan Mode must stop before Step 5.

### Out of Scope (from spec)
- `ywc-agentic` changes (explicitly unchanged — FR7)
- `README.zh.md` / `README.es.md` regeneration (Tier 2 policy)
- Changes to `ywc-spec-ready` itself

## Criticality
critical — INFERRED by keyword heuristic: Ownership includes `ywc-auth-implement` (matches `auth`); the spec's Critical Surfaces do not list it. The edit there is one documentation sentence — downgrade to `normal` if you agree.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream `ywc-plan`, `ywc-auth-implement` text

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-plan/SKILL.md` — Step 4c step 7, Step 5, Arguments, Rationalization Defense, Validation, Integration
- `claude-code/skills/ywc-plan/README{,.en,.ja,.ko}.md` — option table and `ywc-spec-ready` line
- `claude-code/skills/ywc-auth-implement/SKILL.md` — new `/ywc-plan --no-converge` sentence

## Notes
- `ywc-plan/SKILL.md` is ~400 lines; keep body ≤500.
- Wording follows the upstream snapshot; adapt only skill names via FR3 mapping.

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-plan/**`
- `claude-code/skills/ywc-auth-implement/SKILL.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Cross-skill contract: `ywc-plan` ↔ `ywc-spec-ready` ↔ `ywc-agentic` call chain

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `grep -q 'ywc-spec-ready --spec' claude-code/skills/ywc-plan/SKILL.md`
- `[ "$(grep -c -- 'responds \*\*y\*\*' claude-code/skills/ywc-plan/SKILL.md | tr -d ' ')" = 0 ]`
- `[ "$(grep -c 'no-converge' claude-code/skills/ywc-plan/SKILL.md | tr -d ' ')" -ge 3 ]`
- `grep -q 'Spec amended' claude-code/skills/ywc-plan/SKILL.md`
- `[ "$(grep -c 'ywc-plan --no-converge' claude-code/skills/ywc-auth-implement/SKILL.md | tr -d ' ')" -ge 1 ]`
- `for f in README.md README.en.md README.ja.md README.ko.md; do [ "$(grep -c 'opt-in' claude-code/skills/ywc-plan/$f | tr -d ' ')" = 0 ] || exit 1; done`
- `[ "$(grep -c 'ywc-plan --non-interactive' claude-code/skills/ywc-agentic/SKILL.md | tr -d ' ')" = 1 ] && git diff --quiet -- claude-code/skills/ywc-agentic`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-auth-implement/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
