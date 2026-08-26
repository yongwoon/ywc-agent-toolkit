# 000016-010-docs-principles-guideline-gap — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] No predecessor task is required.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/references/principles.md`.
- [ ] If implementation requires changes outside this file, stop and report before proceeding.

## Stop Conditions
- [ ] Stop if the change would create a new `karpathy-*` skill or agent.
- [ ] Stop if the new prose conflicts with the existing Safety/Evidence/Scope hierarchy.
- [ ] Stop if external guideline text would need to be copied verbatim instead of summarized as local operational rules.

## Implementation Steps
- [ ] Update `codex/skills/references/principles.md` with `Assumption & Ambiguity Discipline`.
  - Related AC/FR: AC1, AC2, FR-1
  - Contract / Behavior Change: shared Codex guidance explicitly forbids invented requirements, APIs, test results, and user intent.
  - Verification Command / Evidence: `rg -n "Assumption|Ambiguity|NEEDS_CONTEXT" codex/skills/references/principles.md`
- [ ] Add `Goal-Driven Execution` guidance near the existing evidence/scope/failure sections.
  - Related AC/FR: AC1, FR-1
  - Contract / Behavior Change: shared guidance requires work to stay tied to success criteria and goal-specific verification.
  - Verification Command / Evidence: `rg -n "Goal-Driven|success criteria|goal-specific verification" codex/skills/references/principles.md`
- [ ] Confirm the new rules are concise and do not replace the existing hierarchy.
  - Related AC/FR: AC1, AC12, NFR
  - Contract / Behavior Change: existing principle ordering remains intact.
  - Verification Command / Evidence: review `git diff -- codex/skills/references/principles.md`
- [ ] Confirm no duplicate Karpathy skill or agent was created.
  - Related AC/FR: AC2
  - Contract / Behavior Change: guideline behavior is integrated into existing surfaces.
  - Verification Command / Evidence: `find codex/skills claude-code/skills codex/agents claude-code/agents -iname '*karpathy*' -maxdepth 3`

## Task Verify
- [ ] Run `rg -n "Assumption|Ambiguity|Goal-Driven|NEEDS_CONTEXT|success criteria" codex/skills/references/principles.md`.
- [ ] Run `test ! -d codex/skills/karpathy-guidelines`.
- [ ] Run `test ! -d claude-code/skills/karpathy-guidelines`.

## Verification
- [ ] Targeted grep checks pass.
- [ ] No broad validation required until `000017-010-infra-codex-karpathy-validation`.
