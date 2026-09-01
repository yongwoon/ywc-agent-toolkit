# yw-000014-010-docs-skill-claude-md-policy-amendment — Implementation Checklist

## Prerequisites

- [ ] `yw-000013-010` is completed (merged)
- [ ] `yw-000013-020` is completed (merged)

## Allowed Edit Scope

- [ ] Stay within `claude-code/skills/CLAUDE.md`
- [ ] Do not edit any SKILL.md or reference file — this task documents the pattern, it does not implement it

## Stop Conditions

- [ ] Stop if `ywc-sequential-executor:78` (the cited exemplar) does not actually match the shape being documented — re-verify against the live file rather than assuming `yw-000013-020` left it unchanged as expected

## Implementation Steps

- [ ] Amend "Bot Review Polling Parameters" (~line 97) and "PR Conflict & Merge-Readiness Resolution" (~line 124): change "read the file" to "read the file on entering the branch that needs it"; keep everything else (the parameter tables, the merge/rebase rule) unchanged
- [ ] Amend "Language Resolution" (~line 390) and "Task Initials Resolution" (~line 418): make `bash claude-code/skills/scripts/resolve-language.sh` / `bash claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` the canonical mechanism these sections point to, while explicitly retaining `references/language-resolution.md` / `references/initials-resolution.md` as the human-maintained source of truth (not deprecated, not removed)
- [ ] Add two new rows to the "Bundled Execution Scripts" table (~line 296): `resolve-language.sh` and `resolve-initials.sh`, following the existing table's column format (script, skill, purpose)
- [ ] Correct or remove the `ywc-confidence-gate/scripts/score-gate.py` row (~line 321) — verify the path is genuinely absent before editing, then either point it at the correct location if one exists, or remove the row

## Task Verify

- [ ] Manual diff review: all 4 checkpoints from README.md's Task Verify are met

## Verification

- [ ] `bash scripts/validate.sh` exits 0 (sanity check — `CLAUDE.md` isn't itself validated, but this confirms nothing else broke)

## Implementation Notes (optional)
