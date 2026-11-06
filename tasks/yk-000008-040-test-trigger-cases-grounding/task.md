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

<!-- Starts empty at generation time. -->
