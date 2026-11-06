# yk-000010-060-test-reviewer-trigger-coverage

## Purpose
`score.py --ci` reports 9 of 64 items below the coverage minimum (≥3 positives and ≥2 collisions from independently-sourced cases). Most are dispatch-only reviewer agents (e.g. `ywc-python-reviewer` has 0 positive cases) whose descriptions route every user-typed request to `ywc-impl-review`, so no honest user-prompt positive exists for them.

## Scope
- List the 9 items and their counts (read `score.py`'s coverage code to print them).
- For each item, decide: (a) add real cases only from an actual source (`session-trace` / `user-prompt` with a citable origin) — never synthesize a source; or (b) if the item's description says a user-typed request belongs to another skill (dispatch-only), exempt it from the positives minimum in `score.py` via an explicit, documented list or a frontmatter-derived rule, still requiring its collision cases. Record each decision as a Ruling.
- Do not lower the global minimums.
- Run `score.py --ci` last and stage the auto-updated `history.mechanical.json` (this task runs after all Wave 1 tasks so the baseline covers them).

## Spec Reference

### Primary Sources
- Deferred findings in the Completion Reports of yk-000004..yk-000009 runs on `feature/improvement-20261106` (rulings ledger: yk-000004-020, yk-000005-040, yk-000005-050, yk-000006-010, yk-000009-010).
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; other Phase 000010 tasks' items.

## Criticality
normal

## Dependencies

### Depends On
- `yk-000010-010-domain-scan-secrets-hunk-filter`
- `yk-000010-020-domain-merge-dependabot-hardening`
- `yk-000010-030-domain-retro-readonly-lenses`
- `yk-000010-040-domain-finish-branch-guard-review`
- `yk-000010-050-docs-metadata-followups`

### Depended By
- (None)

## Key Files
- `.claude/skills/ywc-toolkit-eval/scripts/score.py`
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

## Parallel Execution Metadata

- Model Hint: sonnet

### Ownership
- `.claude/skills/ywc-toolkit-eval/scripts/score.py`
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

### Owned Interface
- `score.py --ci` coverage report format

### Shared Surfaces
- `docs/review-learnings.md` L001-L006 (read only)

### Conflicts With
- Every Wave 1 task (shared `history.mechanical.json` baseline)

### Parallelizable After
- `yk-000010-010-domain-scan-secrets-hunk-filter`
- `yk-000010-020-domain-merge-dependabot-hardening`
- `yk-000010-030-domain-retro-readonly-lenses`
- `yk-000010-040-domain-finish-branch-guard-review`
- `yk-000010-050-docs-metadata-followups`

### Task Verify
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci 2>&1 | grep -q '0 items below minimum\|coverage.*OK'` — or, if exemptions are used, the report names each exempt item
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
