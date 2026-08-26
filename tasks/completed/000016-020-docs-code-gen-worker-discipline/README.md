# 000016-020-docs-code-gen-worker-discipline

## Purpose
`ywc-code-gen`의 parent skill에 이미 있는 Simplicity First / Surgical Changes 규율을 worker base prompt까지 전달한다. 이 task는 dispatched implementer가 speculative abstraction이나 adjacent cleanup을 수행하지 않도록 막는다.

## Scope
- `codex/skills/ywc-code-gen/prompts/implementer-base.md`에 concise worker rule 추가
- missing/ambiguous contract는 추측하지 않고 `NEEDS_CONTEXT`로 돌려보내도록 명시
- `ywc-code-gen` eval에 objective regression case 추가 또는 기존 coverage 근거 문서화

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-2-update-code-generation-worker-base-prompt` — worker prompt 요구사항
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-6-update-evals-where-objective` — eval 요구사항
- `codex/skills/ywc-code-gen/SKILL.md` — parent skill Rationalization Defense source
- `codex/skills/ywc-code-gen/prompts/implementer-base.md` — 수정 대상 prompt

### Summary
이 task는 `ywc-code-gen` parent instruction과 worker prompt 사이의 behavior drift를 줄인다. 구현 worker가 smallest sufficient change, no speculative abstraction, no adjacent cleanup, `NEEDS_CONTEXT` behavior를 직접 상속하도록 만든다. 변경은 worker base prompt와 objective eval로 제한한다.

### Out of Scope (from spec)
- Shared principles 변경 — handled by `000016-010-docs-principles-guideline-gap`
- Task generator template 변경 — handled by `000016-030-docs-task-template-goal-verification`
- generated plugin sync/validation — handled by `000017-010-infra-codex-karpathy-validation`

## Dependencies

### Depends On
- `000016-010-docs-principles-guideline-gap` — shared assumption/scope terminology

### Depended By
- `000017-010-infra-codex-karpathy-validation` — generated plugin sync and validation

## Key Files
- `codex/skills/ywc-code-gen/prompts/implementer-base.md` — worker prompt source
- `codex/skills/ywc-code-gen/evals/evals.json` — objective eval cases if supported

## Notes
- Do not duplicate the full parent Rationalization Defense table.
- Keep the prompt concise and operational.
- README locale updates are not expected unless implementation changes user-facing usage semantics.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-code-gen/prompts/implementer-base.md`
- `codex/skills/ywc-code-gen/evals/evals.json`

### Shared Surfaces
- Worker prompt contract: `ywc-code-gen` implementer base prompt
- Eval harness: `codex/skills/ywc-code-gen/evals/evals.json`

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000016-010-docs-principles-guideline-gap`

### Task Verify
- `rg -n "Simplicity|Surgical|NEEDS_CONTEXT|speculative|adjacent" codex/skills/ywc-code-gen/prompts/implementer-base.md`
- `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-code-gen --format json`

## Out of Scope
- Editing role-specific backend/frontend/qa references unless implementation proves the base prompt cannot carry the rule.
- Editing `ywc-sequential-executor` or `ywc-parallel-executor`.
- Editing generated plugin package manually.
