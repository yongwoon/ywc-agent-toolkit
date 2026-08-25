# 000051-030-docs-execution-skill-implementation-notes — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000051-010-docs-shared-exploration-references` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if either executor skill exceeds 500 lines after the planned change and no safe extraction/replacement path is available within scope
- [ ] Stop if the implementation-notes surface would require introducing a new mandatory artifact instead of reusing an existing report surface
- [ ] Stop if `ywc-code-gen`'s prompt/report contract would become inconsistent between `SKILL.md` and `prompts/implementer-base.md`

## Implementation Steps
- [ ] Update `ywc-code-gen/SKILL.md` and, if required, `prompts/implementer-base.md` so workers return implementation notes only for non-obvious decisions that materially affect final code shape.
  - Related AC/FR: `[FR7]`
  - Contract / Behavior Change: code-gen output gains a deterministic `Implementation Notes` surface.
  - Verification Command / Evidence: `rg -n "Implementation Notes|implementation notes" codex/skills/ywc-code-gen/SKILL.md codex/skills/ywc-code-gen/prompts/implementer-base.md`
- [ ] Update `ywc-sequential-executor/SKILL.md` and `ywc-parallel-executor/SKILL.md` so implementation-discovery notes are preserved in existing summaries without adding noisy per-task chatter.
  - Related AC/FR: `[FR8]`
  - Contract / Behavior Change: executor completion surfaces retain hidden decision context.
  - Verification Command / Evidence: `rg -n "implementation-notes|Implementation Notes" codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] Keep both executor SKILL bodies at `<=500` lines, using no-net-growth replacements or reference extraction before adding new pointers.
  - Related AC/FR: `[FR12]`
  - Contract / Behavior Change: bundle structural limits remain intact.
  - Verification Command / Evidence: `wc -l codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] Sync `agents/openai.yaml` and stale locale README files for the three touched skills.
  - Related AC/FR: `[FR10]` / `[FR11]`
  - Contract / Behavior Change: metadata/localized docs reflect the new reporting convention.
  - Verification Command / Evidence: diff review + targeted `find` / `rg`

## Task Verify
- [ ] `rg -n "Implementation Notes|implementation-notes" codex/skills/ywc-code-gen codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`
  - Expected Passing Signal: the convention appears in all three target skill surfaces.
  - Pre-change Failing Evidence / Exception: these strings are absent or incomplete before the task.
  - Contract/Test Evidence: diff review of touched skill/prompt/metadata files.
- [ ] `wc -l codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`
  - Expected Passing Signal: both files remain `<=500` lines.
  - Pre-change Failing Evidence / Exception: baseline is already 498 lines, leaving only minimal headroom.
  - Contract/Test Evidence: numeric line-count output captured in task completion summary.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (`N/A — repository has no standalone typecheck pipeline`)
- [ ] unit tests pass (`N/A — documentation/metadata task`)
- [ ] integration tests pass (if applicable)
- [ ] app builds without error (`N/A — documentation bundle repository`)
