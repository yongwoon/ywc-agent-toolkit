# 000051-010-docs-shared-exploration-references — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] No prerequisite task — root task

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if the shared reference needs to redefine an existing bundle principle instead of supplementing it
- [ ] Stop if the only workable wording would require a new mandatory artifact for every implementation task
- [ ] Stop if the reference starts depending on Claude-only runtime assumptions instead of Codex bundle behavior

## Implementation Steps
- [ ] Create `codex/skills/references/unknown-matrix.md` with the four quadrants, usage timing, compact prompt pattern, and anti-speculation guardrails.
  - Related AC/FR: `[FR1]`
  - Contract / Behavior Change: Discovery/planning skills gain a shared blind-spot surfacing reference.
  - Verification Command / Evidence: `rg -n "Known Knowns|Known Unknowns|Unknown Knowns|Unknown Unknowns" codex/skills/references/unknown-matrix.md`
- [ ] Create `codex/skills/references/implementation-notes.md` defining what belongs in implementation notes, what does not, when notes are required, and how existing report surfaces should carry them.
  - Related AC/FR: `[FR6]`
  - Contract / Behavior Change: Code-producing skills gain a canonical lightweight decision-capture rule.
  - Verification Command / Evidence: `rg -n "unexpected constraints|rejected alternatives|verified or invalidated" codex/skills/references/implementation-notes.md`
- [ ] Cross-check both reference files against shared principles so they explicitly preserve evidence, scope, and safety discipline instead of weakening them.
  - Related AC/FR: `[AC5]`
  - Contract / Behavior Change: Shared reference semantics remain bundle-compatible.
  - Verification Command / Evidence: diff review against `codex/skills/references/principles.md`

## Task Verify
- [ ] `rg -n "Known Knowns|Known Unknowns|Unknown Knowns|Unknown Unknowns" codex/skills/references/unknown-matrix.md`
  - Expected Passing Signal: four quadrants appear exactly once in the new reference with operational wording.
  - Pre-change Failing Evidence / Exception: file absent before task start.
  - Contract/Test Evidence: diff review of the new reference content.
- [ ] `rg -n "unexpected constraints|rejected alternatives|verified or invalidated" codex/skills/references/implementation-notes.md`
  - Expected Passing Signal: required implementation-notes content appears in the new reference.
  - Pre-change Failing Evidence / Exception: file absent before task start.
  - Contract/Test Evidence: diff review of the new reference content.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (`N/A — repository has no standalone typecheck pipeline`)
- [ ] unit tests pass (`N/A — docs/reference-only task`)
- [ ] integration tests pass (if applicable)
- [ ] app builds without error (`N/A — documentation bundle repository`)
