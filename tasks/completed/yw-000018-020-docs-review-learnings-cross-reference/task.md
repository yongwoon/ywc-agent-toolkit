# yw-000018-020-docs-review-learnings-cross-reference — Implementation Checklist

## Prerequisites
- [ ] `yw-000018-010-domain-mine-review-history-skill` is completed (merged) — `claude-code/skills/ywc-mine-review-history/` exists with its final name

## Allowed Edit Scope
- [ ] Stay within `claude-code/skills/ywc-review-learnings/SKILL.md` and `claude-code/skills/ywc-review-learnings/references/capture-sources.md`
- [ ] If any other file needs to change, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `yw-000018-010-domain-mine-review-history-skill` is not actually merged (its skill directory does not exist yet)
- [ ] Stop if the requested edit would touch the `--source` flag enum, the classification table, or the confirmation-gate logic — this task is documentation-only

## Implementation Steps
- [ ] Add one cross-reference sentence to `claude-code/skills/ywc-review-learnings/SKILL.md` (near its `--source pr` / Capture Sources section) noting `ywc-mine-review-history` as the batch/retrospective entry point that feeds `--source pr`, alongside the existing single-PR convenience path
- [ ] Add one matching cross-reference sentence to `claude-code/skills/ywc-review-learnings/references/capture-sources.md`'s `## --source pr` section
- [ ] Confirm neither file's `--source` enum, classification table, or confirmation-gate wording changed beyond the addition

## Task Verify
- [ ] `git diff -- claude-code/skills/ywc-review-learnings/SKILL.md claude-code/skills/ywc-review-learnings/references/capture-sources.md` shows only the added sentence(s)

## Verification
- [ ] `bash scripts/validate.sh` passes

## Implementation Notes
(grows during execution — none yet)
