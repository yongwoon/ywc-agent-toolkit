# yw-000052-010-test-mobile-first-contract-eval — Implementation Checklist

## Prerequisites
- [ ] `yw-000051-010-docs-mobile-first-consumers` is completed and merged.
- [ ] `yw-000051-020-docs-mobile-first-reviewer` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only `scripts/run-codex-skill-contract-evals.sh`.
- [ ] Stop before changing any source consumer or generated package.

## Stop Conditions
- [ ] Stop if a deterministic assertion requires duplicating policy semantics without a source token/relationship.
- [ ] Stop if the checker cannot distinguish end-user UI from non-UI/admin/internal/legacy scope.
- [ ] Stop if the existing runner’s unrelated checks would need behavior changes.

## Hardening Gate
- [ ] Classify as validation behavior change.
- [ ] Establish RED-first evidence by running the runner before adding the new check, then add the named contract check.
- [ ] Preserve the `check_mobile_first_ui_contract` interface and return a failing result for missing/inconsistent source.
- [ ] Mark data integrity and critical review as N/A.

## Implementation Steps
- [ ] Add `check_mobile_first_ui_contract` to `scripts/run-codex-skill-contract-evals.sh`.
  - Require `codex/skills/references/mobile-first-ui.md` and all five named skill consumers.
  - Inspect `codex/agents/ywc-typescript-reviewer.toml` and its eval record.
  - Assert policy link/name plus trigger, `min-width`, exception, and no-retrofit tokens/relationships.
  - Reject a consumer that omits the contract or applies it to non-UI/legacy scope.
- [ ] Invoke the new checker in the existing runner sequence without weakening current JSON-shape checks.
- [ ] Invoke or retain the existing agent-eval checker in the documented verification sequence.
- [ ] Run the targeted runner and agent-eval checker, then review the diff for shell portability.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/check-codex-agent-evals.sh`
- [ ] `git diff --check`

## Verification
- [ ] lint passes (`N/A — shellcheck is a CI gate, not a repository command documented in AGENTS.md`)
- [ ] typecheck passes (`N/A — shell script only`)
- [ ] unit tests pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] integration tests pass (`N/A — source-contract validation only`)
- [ ] app builds without error (`N/A — script-only task`)

## Implementation Notes

