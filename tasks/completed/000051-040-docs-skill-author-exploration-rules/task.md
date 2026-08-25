# 000051-040-docs-skill-author-exploration-rules — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000051-010-docs-shared-exploration-references` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if the new rule would require changing Codex frontmatter schema or locale file policy
- [ ] Stop if the wording conflicts with existing progressive-disclosure rules instead of refining them
- [ ] Stop if the only way to express the guidance is with vague language lacking an operational threshold

## Implementation Steps
- [ ] Update `ywc-skill-author/SKILL.md` to add an explicit rule that exploration-heavy skills should prefer context, decision framing, and selective references over heavy static example cargo-culting.
  - Related AC/FR: `[FR9]`
  - Contract / Behavior Change: future skill authors get an explicit anti-overconstraint guideline.
  - Verification Command / Evidence: `rg -n "few-shot|worked examples|context-first|decision frame" codex/skills/ywc-skill-author/SKILL.md`
- [ ] Add or adjust anti-pattern / validation language so examples remain allowed only when they reduce fragility rather than unnecessarily constrain reasoning.
  - Related AC/FR: `[AC4]`
  - Contract / Behavior Change: skill-author validation checks now cover over-constraining examples.
  - Verification Command / Evidence: diff review of Rationalization Defense / Anti-patterns / Validation Checklist
- [ ] Sync `agents/openai.yaml` and stale locale README files for `ywc-skill-author`.
  - Related AC/FR: `[FR10]` / `[FR11]`
  - Contract / Behavior Change: metadata/localized docs stay aligned with the updated authoring rule.
  - Verification Command / Evidence: diff review of metadata + README locale files

## Task Verify
- [ ] `rg -n "few-shot|worked examples|context-first|decision frame|exploration-heavy" codex/skills/ywc-skill-author/SKILL.md`
  - Expected Passing Signal: the new exploration-authoring rule is present in operational wording.
  - Pre-change Failing Evidence / Exception: those rule terms are absent or incomplete before the task.
  - Contract/Test Evidence: diff review of touched sections in `SKILL.md`.
- [ ] `find codex/skills/ywc-skill-author -maxdepth 2 \\( -name 'openai.yaml' -o -name 'README*.md' \\) | sort`
  - Expected Passing Signal: metadata and localized docs are present for sync review.
  - Pre-change Failing Evidence / Exception: N/A — presence check plus diff review.
  - Contract/Test Evidence: touched file list matches actual edits.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (`N/A — repository has no standalone typecheck pipeline`)
- [ ] unit tests pass (`N/A — documentation/metadata task`)
- [ ] integration tests pass (if applicable)
- [ ] app builds without error (`N/A — documentation bundle repository`)
