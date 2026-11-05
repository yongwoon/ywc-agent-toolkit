# yk-000004-070-domain-impl-review-linter-defects

## Purpose
Port the targeted-linter rule table and recurring defects A-005 to A-007 into `ywc-impl-review` references (AC5).

Spec item: A4 (#340) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- `coderabbit-methodology.md`: add the 'Targeted rules for recurring defect classes' table (only installed tools, only changed files, never modify config), including `zizmor` and `ruff check --select S110`.
- `recurring-defects.md`: create `## Appendix — mined entries`, register it in the Table of contents (`:53`), add the upstream ID-rule paragraph (`:286`) and entries `### A-005` (checkout `persist-credentials`), `### A-006` (unawaited Promise / Promise condition), `### A-007` (Go error discarded) with upstream IDs; first line of the appendix states 'A-001–A-004: exist only upstream, not ported'.
- `devex-agent.md` and `security-agent.md`: one reference line each pointing to the new table/entries.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 4 (A4), AC5, Existing Constraints Touched 'recurring-defects'
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-impl-review/references` — upstream final text (T0 snapshot)

### Summary
The local catalog has numbered sections 1–6 and no mined-entry appendix, so the appendix is created and the IDs are kept identical to upstream for cross-reference. Only A-005–A-007 belong to Issue #69.

### Out of Scope (from spec)
- A-001–A-004 (pre-#69 PRs)
- Any `SKILL.md` change of `ywc-impl-review`

## Criticality
normal — Review reference documents; no security-sensitive runtime surface.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream impl-review references

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md` — rule table
- `claude-code/skills/ywc-impl-review/references/recurring-defects.md` — appendix + A-005–A-007
- `claude-code/skills/ywc-impl-review/references/devex-agent.md` — reference line
- `claude-code/skills/ywc-impl-review/references/security-agent.md` — reference line

## Notes
- `recurring-defects.md` §6 starts at `:256` and runs to EOF; the appendix goes after it.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-impl-review/references/**`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Review catalog consumed by `ywc-impl-review` subagents

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `[ "$(grep -cE -- '^### A-00[567]' claude-code/skills/ywc-impl-review/references/recurring-defects.md | tr -d ' ')" = 3 ]`
- `grep -q 'zizmor' claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md`
- `grep -q 'ruff check --select S110' claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md`
- `grep -q 'Appendix' claude-code/skills/ywc-impl-review/references/recurring-defects.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
