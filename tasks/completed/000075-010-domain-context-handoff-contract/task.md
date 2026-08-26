# 000075-010-domain-context-handoff-contract — Implementation Checklist

## Prerequisites
- [ ] Confirm the approved spec is `docs/ywc-plans/20260812-codex-agentic-context-safety.md`.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/references/context-handoff.md`.
- [ ] Stop before editing executor skills or generated plugin files.

## Stop Conditions
- [ ] Stop if the contract requires changing checkpoint or worktree state schemas.
- [ ] Stop if a required field cannot be defined without storing raw response or tool output.
- [ ] Stop if atomic replacement semantics would mutate authoritative checkpoint state.

## Hardening Gate
- [ ] Record RED-first fixture targets before writing the contract.
- [ ] Record the closed JSON interface, rejection model, and checkpoint fallback order.
- [ ] Apply privacy and atomic-write hardening; require full implementation review.

## Implementation Steps
- [ ] Create `codex/skills/references/context-handoff.md` with required top-level fields and closed nested-key rules.
- [ ] Define `.ywc-context-handoff.json` locations for root, sequential worktree, and parallel aggregate runs.
- [ ] Define checkpoint identity matching, stale/malformed/mismatched discard, and checkpoint → current `README.md`/`task.md` reconstruction.
- [ ] Define bounded strings, forbidden recursive field names, canonical repository-relative paths, and command-status-only verification evidence.
- [ ] Define temporary-sibling fsync/rename replacement and failure-preservation behavior.

## Task Verify
- [ ] `rg -n "schema_version|checkpoint_identity|\.ywc-context-handoff\.json|raw_response|fsync|rename" codex/skills/references/context-handoff.md`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] lint/structure validation passes (`bash scripts/validate.sh`)
- [ ] targeted handoff fixture validation is added by `000077-010-test-context-safety-evaluation-matrix`

## Implementation Notes

