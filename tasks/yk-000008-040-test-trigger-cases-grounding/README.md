# yk-000008-040-test-trigger-cases-grounding

## Purpose
Bring the trigger-case fixture back in line with its own review learnings (final-review M6): reviewer positive prompts quote `ywc-impl-review` trigger phrases verbatim (L001/L004), and collision cases added by yk-000006-010 have one-sided grounding (L003/L006).

## Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` `go-reviewer-pos-1`, `python-reviewer-pos-1`, `typescript-reviewer-pos-1` (and any other case with `expected: ywc-impl-review`): rephrase so the prompt no longer contains a verbatim trigger phrase from `ywc-impl-review`'s description ("Go 코드 리뷰", "Python 코드 리뷰", "TypeScript 코드 리뷰", "コードレビュー", ...), keeping the language-specific intent.
- Every collision case added or changed by merge `7b23a3bf` (yk-000006-010; list them with `git diff 7b23a3bf^1 7b23a3bf -- .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`): per L003, quote the `expected` item's own `Do not use for` clause naming the `impostor`; per L006 decide the winner from the prompt first. Fix the direction, rewrite the prompt, or drop the case; record each decision in Implementation Notes.
- Run `score.py --ci` last and stage the auto-updated `history.mechanical.json` (this task runs after the other Phase 000008 tasks so the baseline covers them all).

## Spec Reference

### Primary Sources
- Issue 69 port final review (Lows, M3, M6) and the yk-000007-010 review (Lows), recorded in those runs' Completion Reports.
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; other Phase 000008 tasks' items.

## Criticality
normal

## Dependencies

### Depends On
- `yk-000008-010-domain-security-doc-followups`
- `yk-000008-020-domain-codex-scan-secrets-guard`
- `yk-000008-030-refactor-skill-author-script-paths`
- `yk-000008-050-docs-low-followups`

### Depended By
- (None)

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

## Parallel Execution Metadata

- Model Hint: sonnet

### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `docs/review-learnings.md` L001-L006 (read only)

### Conflicts With
- Every other Phase 000008 task (shared `history.mechanical.json` baseline)

### Parallelizable After
- `yk-000008-010-domain-security-doc-followups`
- `yk-000008-020-domain-codex-scan-secrets-guard`
- `yk-000008-030-refactor-skill-author-script-paths`
- `yk-000008-050-docs-low-followups`

### Task Verify
- `python3 -c "import json;c=[x for x in json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json'))['cases'] if x.get('expected')=='ywc-impl-review'];bad=[x['id'] for x in c if any(p in x['prompt'] for p in ['Go 코드 리뷰','Python 코드 리뷰','TypeScript 코드 리뷰','コードレビュー','구현 검증','実装レビュー'])];assert not bad,bad"`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
