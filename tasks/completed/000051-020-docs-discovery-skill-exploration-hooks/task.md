# 000051-020-docs-discovery-skill-exploration-hooks — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000051-010-docs-shared-exploration-references` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a required wording change would push a touched SKILL body beyond bundle constraints without a clear extraction path
- [ ] Stop if `Unknowns Surfaced` placement conflicts with another hard-coded report contract that cannot be reconciled in scope
- [ ] Stop if README locale sync would require inventing unsupported Tier 2 files for a skill that does not ship them

## Implementation Steps
- [ ] Update `ywc-brainstorm/SKILL.md` and `ywc-plan/SKILL.md` to point at `references/unknown-matrix.md` for blind-spot / missing-design-assumption passes without weakening existing `NEEDS_CONTEXT` rules.
  - Related AC/FR: `[FR2]` / `[FR3]`
  - Contract / Behavior Change: Discovery/planning skills gain explicit unknown-surfacing hooks.
  - Verification Command / Evidence: `rg -n "unknown-matrix|blind-spot" codex/skills/ywc-brainstorm/SKILL.md codex/skills/ywc-plan/SKILL.md`
- [ ] Update `ywc-tech-research/SKILL.md` output format and workflow to add `### Unknowns Surfaced`, plus status guidance when the recommendation depends on unresolved unknowns.
  - Related AC/FR: `[FR4]`
  - Contract / Behavior Change: Research report shape changes in a deterministic place.
  - Verification Command / Evidence: `rg -n "Unknowns Surfaced|DONE_WITH_CONCERNS" codex/skills/ywc-tech-research/SKILL.md`
- [ ] Update `ywc-onboard-repo/SKILL.md` so reconnaissance can surface unknown-but-worth-verifying questions without over-claiming conventions.
  - Related AC/FR: `[FR5]`
  - Contract / Behavior Change: Onboarding can explicitly preserve high-value unknowns.
  - Verification Command / Evidence: `rg -n "worth verifying|Unknown" codex/skills/ywc-onboard-repo/SKILL.md`
- [ ] Sync `agents/openai.yaml` and stale locale README files for the four touched skills.
  - Related AC/FR: `[FR10]` / `[FR11]`
  - Contract / Behavior Change: UI metadata and localized docs stay aligned with the revised skill behavior.
  - Verification Command / Evidence: diff review + targeted `rg` over touched README/openai files

## Task Verify
- [ ] `rg -n "unknown-matrix|blind-spot|Unknowns Surfaced|worth verifying" codex/skills/ywc-brainstorm codex/skills/ywc-plan codex/skills/ywc-tech-research codex/skills/ywc-onboard-repo`
  - Expected Passing Signal: each target skill contains the intended hook or output section.
  - Pre-change Failing Evidence / Exception: these strings are absent or incomplete before the task.
  - Contract/Test Evidence: diff review of each touched skill and metadata file.
- [ ] `find codex/skills/ywc-brainstorm codex/skills/ywc-plan codex/skills/ywc-tech-research codex/skills/ywc-onboard-repo -path '*/agents/openai.yaml' -o -name 'README*.md' | sort`
  - Expected Passing Signal: touched metadata/localized docs exist and can be reviewed for sync.
  - Pre-change Failing Evidence / Exception: N/A — existence check plus diff review.
  - Contract/Test Evidence: review touched file list against actual edits.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (`N/A — repository has no standalone typecheck pipeline`)
- [ ] unit tests pass (`N/A — documentation/metadata task`)
- [ ] integration tests pass (if applicable)
- [ ] app builds without error (`N/A — documentation bundle repository`)
