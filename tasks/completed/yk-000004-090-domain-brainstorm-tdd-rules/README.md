# yk-000004-090-domain-brainstorm-tdd-rules

## Purpose
Port brainstorm question-ordering rules and unify the tdd-ritual unit-test setup threshold at ~50 lines (AC7b).

Spec item: A7 (#335, #345) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- `ywc-brainstorm`: add the two question-ordering rules from the snapshot.
- `ywc-tdd-ritual/SKILL.md`: add a horizontal-slicing Rationalization Defense row, a one-line 'catches / misses' note for the seam, and the row 'Unit test setup over ~50 lines signals the design is wrong …' (absent locally, so it is added).
- `references/test-shape-cookbook.md:77`: '50+ lines' → 'over ~50 lines'; `references/red-green-checklist.md:18`: '~10 lines' → '~50 lines'.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 7 (A7), AC7b
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-tdd-ritual/SKILL.md` — upstream `:40` row (T0 snapshot)

### Summary
Three documents disagreed on how large a test setup may be before it signals bad design; all now say ~50 lines. The brainstorm and slicing additions come from the same upstream PR.

### Out of Scope (from spec)
- Anything in `ywc-wayfinder` / `ywc-mission` (absent locally)

## Criticality
normal — Authoring guidance; no security-sensitive surface.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream brainstorm / tdd-ritual text

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-brainstorm/SKILL.md` — two ordering rules
- `claude-code/skills/ywc-tdd-ritual/SKILL.md` — Rationalization rows, seam note
- `claude-code/skills/ywc-tdd-ritual/references/test-shape-cookbook.md` — :77
- `claude-code/skills/ywc-tdd-ritual/references/red-green-checklist.md` — :18

## Notes
- Brainstorm ordering rules have no grep AC; verify by quoting the added lines in Implementation Notes (review-only).

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-brainstorm/SKILL.md`
- `claude-code/skills/ywc-tdd-ritual/**`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `grep -q '~50 lines' claude-code/skills/ywc-tdd-ritual/references/test-shape-cookbook.md`
- `grep -q '~50 lines' claude-code/skills/ywc-tdd-ritual/references/red-green-checklist.md`
- `[ "$(grep -c -- '~10 lines' claude-code/skills/ywc-tdd-ritual/references/red-green-checklist.md | tr -d ' ')" = 0 ]`
- `grep -q '~50 lines' claude-code/skills/ywc-tdd-ritual/SKILL.md`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-brainstorm/SKILL.md claude-code/skills/ywc-tdd-ritual/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
