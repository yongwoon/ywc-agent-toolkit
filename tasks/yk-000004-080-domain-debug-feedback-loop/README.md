# yk-000004-080-domain-debug-feedback-loop

## Purpose
Port the 'red-capable feedback loop' discipline into `ywc-debug-rootcause` (AC7).

Spec item: A6 (#335) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- New `claude-code/skills/ywc-debug-rootcause/references/feedback-loop.md` from the snapshot.
- `SKILL.md` Phase 1 step 2 (`:85`) becomes 'build a red-capable loop, then minimize it'; Phase 3 (`:108`) becomes 'rank 3–5 hypotheses' (the single-hypothesis sentence is removed).
- Keep fix-attempt rule #4 consistent with the exception for an analyst 'fix harder' verdict.
- Update `references/architectural-stop-signals.md` and `references/four-phase-checklist.md` to match.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 6 (A6), AC7
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-debug-rootcause` — upstream final text (T0 snapshot)

### Summary
A failing test (or equivalent signal) that reproduces the bug cheaply comes before hypothesizing; hypotheses are then ranked rather than tried one at a time.

### Out of Scope (from spec)
- Changes to `ywc-root-cause-analyst` agent

## Criticality
normal — Debugging workflow guidance; no security-sensitive surface.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream debug-rootcause text

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-debug-rootcause/references/feedback-loop.md` — new
- `claude-code/skills/ywc-debug-rootcause/SKILL.md` — Phase 1 step 2, Phase 3, fix #4
- `claude-code/skills/ywc-debug-rootcause/references/architectural-stop-signals.md` — align
- `claude-code/skills/ywc-debug-rootcause/references/four-phase-checklist.md` — align

## Notes
- Wording of fix #4 must not contradict the analyst 'fix harder' exception.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-debug-rootcause/**`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `test -f claude-code/skills/ywc-debug-rootcause/references/feedback-loop.md`
- `[ "$(grep -c -- 'Form a single hypothesis' claude-code/skills/ywc-debug-rootcause/SKILL.md | tr -d ' ')" = 0 ]`
- `grep -q 'feedback-loop' claude-code/skills/ywc-debug-rootcause/SKILL.md`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-debug-rootcause/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
