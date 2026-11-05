# yk-000006-010-domain-agent-description-alignment

## Purpose
Align the three language-reviewer agents and `ywc-qa-engineer` descriptions with upstream and update affected trigger fixtures (AC15).

Spec item: C1 (#345) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- `ywc-go-reviewer`, `ywc-python-reviewer`, `ywc-typescript-reviewer`: description gains 'high-frequency error-handling, external-call resilience and validation defects', loses natural-language triggers, and anti-triggers gain 'user-typed code review request (ywc-impl-review owns it)'.
- `ywc-impl-review`: verify-only — its description already carries the per-language triggers.
- `ywc-qa-engineer`: E2E suite code only when dispatched with a strategy; frontend co-located tests belong to `ywc-frontend-coder`; wording 'While authoring tests'.
- `trigger-cases.json`: review every case with a reviewer agent as expected or impostor (~30 ids; re-grep `go-reviewer\|python-reviewer\|typescript-reviewer`); cases using the removed triggers now expect `ywc-impl-review`. Non-blocking for merge but part of done; must pass `test_fixture_schema.py`.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 14 (C1), AC15
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/agents` — upstream agent descriptions (T0 snapshot)

### Summary
User-typed code review requests are routed by `ywc-impl-review`; the reviewer agents are dispatch targets only. Fixtures that expected agent routing for natural-language phrases must follow.

### Out of Scope (from spec)
- `ywc-impl-review` description edits (verify-only)
- `ywc-performance-engineer` FinOps contract (unchanged)

## Criticality
normal — Agent description alignment; eval fixtures are local-only.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream agent files
- `yk-000005-050-domain-handoff-retro-skills` — serializes `history.mechanical.json` and `trigger-cases.json` after the Phase B chain (B3 → … → B5 → C1)

### Depended By
- `yk-000006-020-domain-worktrees-existing-branch` — needs the output of this task

## Key Files
- `claude-code/agents/ywc-go-reviewer.md, ywc-python-reviewer.md, ywc-typescript-reviewer.md` — description
- `claude-code/agents/ywc-qa-engineer.md` — ownership wording
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` — fixture review
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — baseline

## Notes
- Agent files have no SKILL.md body-line gate but `score.py` may score them; run the gate.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/agents/ywc-go-reviewer.md`
- `claude-code/agents/ywc-python-reviewer.md`
- `claude-code/agents/ywc-typescript-reviewer.md`
- `claude-code/agents/ywc-qa-engineer.md`
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `trigger-cases.json` (B3 → C1)
- Baseline `history.mechanical.json`

### Conflicts With
- `yk-000006-020-domain-worktrees-existing-branch` — both stage the auto-updated `history.mechanical.json`

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`
- `yk-000005-050-domain-handoff-retro-skills`

### Task Verify
- `for a in ywc-go-reviewer ywc-python-reviewer ywc-typescript-reviewer; do grep -q 'user-typed code review request' claude-code/agents/$a.md || exit 1; done`
- `grep -q 'While authoring tests' claude-code/agents/ywc-qa-engineer.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- `bash scripts/validate.sh`

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
