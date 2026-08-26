# 000025-010-docs-review-learnings-prevention-sources

## Purpose
Extend `ywc-review-learnings` so a confirmed root cause / incident prevention item can be promoted into the durable project review memory. Foundation edge of the harness-feedback loop — the consumers (debug-rootcause, incident-postmortem) depend on the new capture sources existing.

## Scope
- Add `debug` and `incident` to the `--source` enum (currently `feedback|review|pr`).
- Document both in the Capture Sources table and `references/capture-sources.md`.
- Each new source maps the upstream root-cause statement to the learning **why**, classifies polarity (`DO`/`DO-NOT`), scopes to the narrowest glob, records provenance (`debug <symptom>` / `incident <id>`).
- New sources enter the **existing update-mode workflow body** (SKILL.md Steps 1–6) unchanged — reuse the CHANGESET confirmation and first-creation activation-prompt gates; no parallel write path.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/tier2-harness-feedback-and-mission-persistence.md` — FR3, AC4; Existing Constraints (`ywc-review-learnings/SKILL.md:46/48/72-86/97-105`); Iteration 1 Amendments §Supersedes/pins (FR3).
### Summary
review-learnings already supports user-confirmed, why-carrying learnings with provenance. This task only widens its intake: two new `--source` values the debug/postmortem skills will call. Confirmation gate and file format unchanged.
### Out of Scope (from spec)
No new skill; no edits to debug-rootcause/incident-postmortem (000025-030); no change to the confirmation gate; codex bundle.

## Criticality
normal — skill-instruction change to `docs/review-learnings.md` tooling; no security surface (spec Critical Surfaces = none).

## Dependencies
### Depends On
- (root) — no predecessor.
### Depended By
- `000025-030-docs-rootcause-postmortem-prevention-emit` — needs the `--source debug|incident` values to route into.
- `000026-010-docs-catalog-claude-md-integration` — documents the new edges.

## Key Files
- `claude-code/skills/ywc-review-learnings/SKILL.md`
- `claude-code/skills/ywc-review-learnings/references/capture-sources.md`
- `claude-code/skills/ywc-review-learnings/README*.md` (only if the source list is user-facing)

## Notes
- Provenance grammar fixed by spec: `debug <symptom>` / `incident <id>`. OQ2 resolved: two distinct values (not a single `prevention`).

## Out of Scope
Consumer wiring, new skill creation, catalog/CLAUDE.md updates.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-review-learnings/**`
- **Shared Surfaces**: the `ywc-review-learnings --source` enum contract (consumed by 000025-030).
- **Conflicts With**: (None identified)
- **Parallelizable After**: (root) — may run concurrently with `000025-020`.
- **Task Verify**: `bash scripts/validate.sh`
