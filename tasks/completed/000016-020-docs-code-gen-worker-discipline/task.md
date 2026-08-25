# 000016-020-docs-code-gen-worker-discipline — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000016-010-docs-principles-guideline-gap` is completed (merged).

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-code-gen/prompts/implementer-base.md`.
- [ ] Stay within `codex/skills/ywc-code-gen/evals/evals.json` if adding objective eval coverage.
- [ ] If the task requires edits outside Ownership, stop and report before proceeding.

## Stop Conditions
- [ ] Stop if fixing the behavior requires rewriting `ywc-code-gen/SKILL.md` rather than propagating existing parent discipline.
- [ ] Stop if eval changes require changing the eval runner or global rubric.
- [ ] Stop if README locale changes become necessary; report before adding translation churn.

## Implementation Steps
- [ ] Add a concise `Simplicity + Surgical Changes` worker rule to `codex/skills/ywc-code-gen/prompts/implementer-base.md`.
  - Related AC/FR: AC3, FR-2
  - Contract / Behavior Change: every dispatched implementer must prefer the smallest complete change and avoid speculative abstractions.
  - Verification Command / Evidence: `rg -n "Simplicity|Surgical|smallest|speculative" codex/skills/ywc-code-gen/prompts/implementer-base.md`
- [ ] Add missing/ambiguous contract handling to the same prompt.
  - Related AC/FR: AC3, FR-2
  - Contract / Behavior Change: worker returns `NEEDS_CONTEXT` instead of inventing a contract.
  - Verification Command / Evidence: `rg -n "NEEDS_CONTEXT|ambiguous contract|missing contract" codex/skills/ywc-code-gen/prompts/implementer-base.md`
- [ ] Inspect `codex/skills/ywc-code-gen/evals/evals.json` and add an objective regression case if the harness supports checking the new prompt behavior.
  - Related AC/FR: AC9, FR-6
  - Contract / Behavior Change: mechanical eval catches missing simplicity/scope/contract behavior.
  - Verification Command / Evidence: `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-code-gen --format json`
- [ ] If no eval is added, record the reason in the implementation notes for this task.
  - Related AC/FR: AC9, FR-6
  - Contract / Behavior Change: eval omission is explicit and reviewable.
  - Verification Command / Evidence: implementation final report includes eval decision.

## Task Verify
- [ ] Run `rg -n "Simplicity|Surgical|NEEDS_CONTEXT|speculative|adjacent" codex/skills/ywc-code-gen/prompts/implementer-base.md`.
- [ ] Run `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-code-gen --format json`.

## Verification
- [ ] Targeted grep checks pass.
- [ ] Skill eval score command completes or its failure is reported with cause.
- [ ] Full repository validation is deferred to `000017-010-infra-codex-karpathy-validation`.
