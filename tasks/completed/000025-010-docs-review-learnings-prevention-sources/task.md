# Task: 000025-010-docs-review-learnings-prevention-sources

## Prerequisites
- [ ] None (root task).

## Allowed Edit Scope
`claude-code/skills/ywc-review-learnings/**` only.

## Stop Conditions
- Stop and report if extending `--source` would require changing the existing update-mode confirmation gate (spec forbids it).
- Stop if `ywc-skill-author` rules cannot be satisfied within the 500-line body cap.

## Implementation Steps
- [ ] Change the `--source` Arguments row from `feedback|review|pr` to `feedback|review|pr|debug|incident`.
- [ ] Add two rows to the `## Capture Sources` table: `debug` (root-cause statement → why; polarity; provenance `debug <symptom>`) and `incident` (recurrence-preventing item → why; provenance `incident <id>`).
- [ ] Add a Mode-Detection note so an update invoked with `--source debug|incident` routes through the existing Steps 1–6 body unchanged.
- [ ] Extend `references/capture-sources.md` with the harvest procedure for `debug` and `incident`.
- [ ] Keep ≥5 domain-specific Rationalization Defense rows.
- [ ] Update review-learnings README locale set only if the source list is user-facing there.

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] `grep -n "debug" claude-code/skills/ywc-review-learnings/SKILL.md` shows the new source in Arguments + Capture Sources.
- [ ] SKILL.md body ≤500 lines.

## Verification
- [ ] `bash scripts/validate.sh` passes.
