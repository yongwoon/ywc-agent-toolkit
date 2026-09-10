# yw-000036-060-docs-adr-hardener-isolation — Implementation Checklist

## Prerequisites
- [ ] `yw-000036-030-domain-parallel-executor-hardener-isolation-claude` is completed (merged) — read its final diff for the settled branch-name form and promotion-step label.
- [ ] `yw-000036-040-domain-parallel-executor-hardener-isolation-codex` is completed (merged).

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `docs/adr/` (new).

## Stop Conditions
- [ ] Stop if `docs/adr/` already contains an ADR covering this exact decision (would mean duplicate work — investigate rather than create a second one).
- [ ] Stop if `yw-000036-030`/`yw-000036-040`'s final branch-name/step-label decisions cannot be determined from their merged diffs.

## Implementation Steps
- [ ] Run `ywc-adr --mode new` (or the project's invocation form for that skill) to scaffold the ADR at `docs/adr/NNNN-<slug>.md`, choosing a slug reflecting "wave hardener delivery isolation".
- [ ] **Context**: state the defect (Hardener runs after delivery, cannot block anything) and cite the architecture verdict as the adjudicated decision.
- [ ] **Decision**: the permanent carve-out — `--local-merge`/`--draft`/`--aggregate-pr` route through `wave-int/<N>`; `--per-task-pr` is permanently excluded per the "isolation branch can only protect state whose point-of-no-return sits after the gate" rule; `wave-complete`'s meaning changes from "wave finished" to "wave promoted".
- [ ] **Alternatives**: record Option B (retargeting per-task PR bases — rejected: a second int→base PR per wave is a full extra CI+bot cycle, and required-checks/branch-protection are configured for the real base) and Option C (severity-scoped isolation — rejected: two branch topologies selected at runtime complicates resume) from the architecture verdict's trade-off table.
- [ ] **Consequences**: state explicitly that a future reader must not "fix" the carve-out by making it uniform — retargeting `--per-task-pr` destroys the signal the mode exists to buy (bot review + CI + branch protection evaluated against the real base).
- [ ] Cite the actual settled branch-name form and promotion-step label from `yw-000036-030`/`yw-000036-040`'s merged diffs, not the spec's placeholder forms, if they differ.

## Task Verify
- [ ] `test -d docs/adr`
- [ ] `grep -l "per-task-pr" docs/adr/*.md`
- [ ] `grep -c "^## " docs/adr/<new-file>.md` — Context/Decision/Alternatives/Consequences present.
- [ ] `grep -i "option b\|retargeting" docs/adr/<new-file>.md` — rejected alternative recorded.

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
