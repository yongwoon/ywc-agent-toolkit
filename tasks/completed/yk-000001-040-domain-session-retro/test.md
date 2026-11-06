# Evidence bounded retrospective — scenarios

## AC-4 — seven-category evidence classification
1. Provide supplied conversation/attachment evidence spanning Navigation, Automated checks, Coding standards, Steering files, Tool economy, No-ops, and Information access.
2. Repeat the same evidence occurrence and add distinct occurrences with different priorities.
3. Run with empty supplied evidence and with a proposed change lacking an established owner.

Expected: repeated occurrences are deduplicated; candidates sort by priority, occurrence count, first occurrence, then input order. Each candidate includes priority rationale, category, redacted evidence, proposed change, and established owner or explicit `Unassigned`. Empty evidence yields no candidates and the retrospective invents no evidence or owner.

## Failure-mode coverage
Steps: verify the new skill bundle includes Tier 1 locales, `agents/openai.yaml`, numeric eval IDs, and upstream `source_id` provenance. Inspect source assertions separately from runtime use.

Expected: missing locale/provenance is visible as a failed bundle contract; unavailable runtime tooling is UNVERIFIED. This task owns only the retro half of FR-4; handoff path, permission, symlink, and collision cases belong to the successor task.
