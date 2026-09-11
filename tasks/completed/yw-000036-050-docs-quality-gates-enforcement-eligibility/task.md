# yw-000036-050-docs-quality-gates-enforcement-eligibility — Implementation Checklist

## Prerequisites
- [ ] None — root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/references/quality-gates.md`, `codex/skills/references/quality-gates.md`.

## Stop Conditions
- [ ] Stop if either file already states an enforcement-eligibility rule referencing "point-of-no-return".
- [ ] Stop if writing the rule would require reconciling the two files' broader structural divergence (three-tier vs. `gate_state` models) — add the one rule to each in its own idiom and stop; do not attempt reconciliation.

## Implementation Steps
- [ ] In `claude-code/skills/references/quality-gates.md`, near §9 "gate_state Sentinel Vocabulary" (or §7 "Contract-Absent Fallback" if a better fit on read), add a rule stating: a delivery mode whose point-of-no-return precedes a gate may not declare `enforced` at that gate.
- [ ] In the same file, add that under `--per-task-pr`, the wave-boundary cross-task-interaction check still runs but its result is a plain descriptive note in the wave's Completion Report only — never assigned to `gate_state`.
- [ ] In `codex/skills/references/quality-gates.md`, near §2 "Contract states", add the same rule, worded to slot directly into the existing `report-only`/`advisory`/`enforced` three-tier model.
- [ ] In the same file, add that under `--per-task-pr`, the wave-boundary result is never promoted into `contract_state` — reporting-only, recorded outside that field's contract.
- [ ] Verify neither file's new text uses `gate_state` and `contract_state` interchangeably or implies they are the same field across roots.

## Task Verify
- [ ] `grep -n "point-of-no-return" claude-code/skills/references/quality-gates.md`
- [ ] `grep -n "point-of-no-return" codex/skills/references/quality-gates.md`
- [ ] `grep -A2 "per-task-pr" claude-code/skills/references/quality-gates.md` — confirm the note names `gate_state` and says "never assigned".
- [ ] `grep -A2 "per-task-pr" codex/skills/references/quality-gates.md` — confirm the note names `contract_state` and says "never promoted".

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
