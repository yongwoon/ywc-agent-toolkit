# yk-000008-040-test-trigger-cases-grounding — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] `yk-000008-010-domain-security-doc-followups` is completed (merged)
- [ ] `yk-000008-020-domain-codex-scan-secrets-guard` is completed (merged)
- [ ] `yk-000008-030-refactor-skill-author-script-paths` is completed (merged)
- [ ] `yk-000008-050-docs-low-followups` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
  - `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` `go-reviewer-pos-1`, `python-reviewer-pos-1`, `typescript-reviewer-pos-1` (and any other case with `expected: ywc-impl-review`): rephrase so the prompt no longer contains a verbatim trigger phrase from `ywc-impl-review`'s description ("Go 코드 리뷰", "Python 코드 리뷰", "TypeScript 코드 리뷰", "コードレビュー", ...), keeping the language-specific intent.
- [ ] Every collision case added or changed by merge `7b23a3bf` (yk-000006-010; list them with `git diff 7b23a3bf^1 7b23a3bf -- .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`): per L003, quote the `expected` item's own `Do not use for` clause naming the `impostor`; per L006 decide the winner from the prompt first. Fix the direction, rewrite the prompt, or drop the case; record each decision in Implementation Notes.
- [ ] Run `score.py --ci` last and stage the auto-updated `history.mechanical.json` (this task runs after the other Phase 000008 tasks so the baseline covers them all).
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `python3 -c "import json;c=[x for x in json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json'))['cases'] if x.get('expected')=='ywc-impl-review'];bad=[x['id'] for x in c if any(p in x['prompt'] for p in ['Go 코드 리뷰','Python 코드 리뷰','TypeScript 코드 리뷰','コードレビュー','구현 검증','実装レビュー'])];assert not bad,bad"`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

Basis: `ywc-impl-review`'s own `Do not use for` clause names only ywc-spec-validate, ywc-product-review, ywc-review-learnings, ywc-security-audit (SKILL.md frontmatter line 4) -- no language reviewer and no ywc-performance-engineer. Per L006 the winner of every user-typed review prompt below is `ywc-impl-review` (each reviewer's own clause says "a user-typed code review request ... ywc-impl-review owns it"); per L003 the reverse direction (reviewer as `expected`) is untruthful and impl-review as `expected` is ungrounded for these impostors. Agent body trigger lists checked per L005: only ywc-performance-engineer has a body `Natural language:` list, and none of its phrases appear in the touched prompts.

Positives (verbatim ywc-impl-review trigger phrase removed, L001/L004; expected unchanged): go-reviewer-pos-1 ("Go 코드 리뷰"), python-reviewer-pos-1 ("Python 코드 리뷰"), typescript-reviewer-pos-1 ("TypeScript 코드 리뷰"), impl-review-pos-1 ("구현 검증", "코드 리뷰"), impl-review-pos-2 ("implementation review"), impl-review-pos-3 ("実装レビュー"); collisions impl-review-vs-security-audit-1 ("구현 리뷰", impostor security-audit is grounded) and impl-review-vs-typescript-reviewer-1 ("구현 리뷰").

Collision decisions (merge 7b23a3bf; all 13 DROPPED -- no reviewer can win a user-typed prompt, impl-review's clause does not name the impostor):
- typescript-reviewer-vs-impl-review-1 / go-reviewer-vs-impl-review-1 / python-reviewer-vs-impl-review-1: drop -- impl-review wins but its clause names no language reviewer (L003); reviewer-as-expected would be backwards (L006).
- go-reviewer-vs-python-reviewer-1, python-reviewer-vs-typescript-reviewer-1, typescript-reviewer-vs-python-reviewer-1, go-reviewer-vs-typescript-reviewer-1, agent-tsreviewer-vs-pyreviewer-1: drop -- user-typed language review, true winner impl-review, impostor (other language reviewer) unnamed in impl-review's clause.
- go-reviewer-vs-typescript-reviewer-2, go-reviewer-vs-python-reviewer-2, typescript-reviewer-vs-python-reviewer-2, typescript-reviewer-vs-go-reviewer-1: drop -- same; prompts are verbatim user prompts so they cannot be rewritten without losing `user-prompt` provenance.
- python-reviewer-vs-performance-engineer-1: drop -- prompt explicitly negates speed measurement and asks an idiom review, so winner is impl-review (impostor performance-engineer unnamed in its clause); reversing to python-reviewer or performance-engineer would contradict the prompt. Floor impact: ywc-performance-engineer independent collisions 2 -> 1 (a rewrite cannot keep it: any rewritten prompt is no longer a verbatim user prompt).

Left untouched (outside the 7b23a3bf set): impl-review-vs-typescript-reviewer-1 still has the same L003 ungrounded impostor (typescript-reviewer); only its L001 phrase was fixed.
- Review follow-up (orchestrator): dropped `impl-review-vs-typescript-reviewer-1` (pre-7b23a3bf, same L003 gap: impl-review's own clause does not name typescript-reviewer; description-derived, no coverage cost) and rephrased `ui-ux-review-vs-impl-review-1` to drop the verbatim impl-review trigger "코드 리뷰" from an impostor prompt (L004).
