# yw-000033-020-domain-parallel-quality-gate — Implementation Checklist

## Prerequisites
- [ ] All Phase `yw-000032` tasks are completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-parallel-executor/**` and its evals.

## Stop Conditions
- [ ] Stop if worker dispatch crosses task Ownership or loses worktree preservation.
- [ ] Stop if wave aggregation can mask an earlier concern.

## Hardening Gate
- [ ] Classify as critical parallel lifecycle behavior.
- [ ] Capture RED-first executor-eval evidence before changing wave routing.
- [ ] Record the wave aggregate interface and require full review.
- [ ] Apply retry/idempotency checks in `README.md`.

## Implementation Steps
- [ ] Add per-task Cleaner dispatch after task verification and before wave delivery.
- [ ] Gate Hardener dispatch on Cleaner terminal permission and aggregate mutation evidence only at the safe wave boundary.
- [ ] Preserve blocked task worktrees/branches and existing rerouting/triage behavior.
- [ ] Add eval cases for no-contract, unavailable tools, residual survivors, and earlier-concern precedence.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `rg -n "Cleaner|Hardener|wave boundary|preserve|BLOCKED|NEEDS_CONTEXT|DONE_WITH_CONCERNS" codex/skills/ywc-parallel-executor`

## Verification
- [ ] Contract evals pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] Typecheck/build: N/A — skill/eval repository.
