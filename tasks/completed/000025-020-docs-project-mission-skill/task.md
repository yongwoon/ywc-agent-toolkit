# Task: 000025-020-docs-project-mission-skill

## Prerequisites
- [ ] None (root task).

## Allowed Edit Scope
`claude-code/skills/ywc-project-mission/**` (new). Do NOT edit ywc-plan / ywc-brainstorm here.

## Stop Conditions
- Stop and report if the four-mode + format cannot fit the 500-line body cap even after extracting to `references/mission-format.md`.
- Stop if `ywc-skill-author` validation cannot pass.

## Implementation Steps
- [ ] Invoke `ywc-skill-author` (repo rule for new skills) and scaffold `claude-code/skills/ywc-project-mission/`.
- [ ] Write `SKILL.md`: Announce line; `(ywc) Use when ...` description with KR/EN/JA triggers + `Do not use for ...`; `## Rationalization Defense` ≥5 domain-specific rows; `## Arguments` (`--mode read|update|list|curate`, `--output`, `--dry-run`); `## Workflow` per mode; `## Validation`; `## Integration` (read by ywc-plan, written from ywc-brainstorm).
- [ ] Write `references/mission-format.md`: full schema — Mission/North-Star bullets; Success Criteria table `| ID | Criterion (measurable) | Source | Added | Status |`; Out of Scope; Change Log (auto-maintained metadata); deprecation via `~~strikethrough~~`; provenance grammar.
- [ ] Implement first-creation activation prompt (print `@docs/project-mission.md` once; file-exists detection).
- [ ] Implement idempotent update (empty CHANGESET → no write, no date bump).
- [ ] Write full README locale set per `skills/CLAUDE.md` language policy.
- [ ] Write `evals/evals.json` (create-file, idempotent no-op, deprecate-on-contradiction scenarios).

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] `wc -l claude-code/skills/ywc-project-mission/SKILL.md` ≤ 500.
- [ ] README locale set + `evals/evals.json` all present.

## Verification
- [ ] `bash scripts/validate.sh` passes.
