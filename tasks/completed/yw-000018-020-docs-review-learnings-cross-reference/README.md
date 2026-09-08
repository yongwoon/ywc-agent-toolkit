# yw-000018-020-docs-review-learnings-cross-reference

## Purpose
Add a documentation-only cross-reference from `ywc-review-learnings` to the new `ywc-mine-review-history` skill so a reader landing on the single-PR capture path discovers the batch/retrospective entry point.

## Scope
- `claude-code/skills/ywc-review-learnings/SKILL.md` gains a short sentence noting `ywc-mine-review-history` as the batch/retrospective entry point that feeds `--source pr`, alongside the existing single-PR convenience path.
- `claude-code/skills/ywc-review-learnings/references/capture-sources.md` (`## --source pr` section) gains the same cross-reference.
- No change to the `--source` enum, the classification rule, or the confirmation-gate logic in either file.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#scope` — the cross-reference requirement (last bullet)
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#acceptance-criteria` — AC7
- `docs/ywc-plans/20260909-ywc-mine-review-history.md#existing-constraints-touched` — the `ywc-review-learnings/SKILL.md` confirmation-gate row this task must not disturb

### Summary
This task is a pure documentation edit adding discoverability between two sibling skills. It must not alter any behavior of `ywc-review-learnings` — the confirmation-gated write path, the `--source` flag enum, and the accept/dismiss classification table in `capture-sources.md` all stay byte-identical apart from the added sentence(s).

### Out of Scope (from spec)
- Any change to `ywc-review-learnings`'s `--source` enum, classification rule, or confirmation-gate logic — explicitly forbidden by AC7.
- Creating the new skill itself — handled by `yw-000018-010-domain-mine-review-history-skill`.

## Dependencies

### Depends On
- `yw-000018-010-domain-mine-review-history-skill` — provides the finalized skill name/path (`claude-code/skills/ywc-mine-review-history/`) this cross-reference points to.

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-review-learnings/SKILL.md` — modified (added sentence only)
- `claude-code/skills/ywc-review-learnings/references/capture-sources.md` — modified (added sentence only)

## Notes
- Keep the added sentences minimal — one or two sentences per file, placed near the existing `--source pr` documentation.
- Do not touch the `--source feedback|review|pr|debug|incident` flag table or any of the `Capture Sources` procedure text beyond the addition.

## Out of Scope
- Any behavioral edit to `ywc-review-learnings` (see Spec Reference "Out of Scope (from spec)").

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-review-learnings/SKILL.md`
- `claude-code/skills/ywc-review-learnings/references/capture-sources.md`

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000018-010-domain-mine-review-history-skill`

### Task Verify
- `git diff -- claude-code/skills/ywc-review-learnings/SKILL.md claude-code/skills/ywc-review-learnings/references/capture-sources.md` (manual inspection: only the added cross-reference sentence(s), no enum/classification/confirmation-gate change)
- `bash scripts/validate.sh`
