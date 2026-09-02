# yw-000015-010-domain-scaffold-routing — Implementation Checklist

## Prerequisites
- [ ] Confirm the source spec is `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md`.
- [ ] Confirm no other task edits `codex/skills/ywc-project-scaffold/SKILL.md` concurrently.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-project-scaffold/SKILL.md`.

## Stop Conditions
- [ ] Stop if the change requires Claude Code files, new dependencies, or project-file generation.
- [ ] Stop if explicit approval semantics cannot be expressed without permitting silent reference edits.
- [ ] Stop if the existing structured output fields would be removed rather than extended.

## Implementation Steps
- [ ] Extend the frontmatter description and trigger guidance only enough to discover review of the skill's own `references/<language>.md` files; retain the new-project-scaffold boundary.
  - Related AC/FR: AC4 / FR1
  - Contract / Behavior Change: `reference-refresh` is discoverable without routing generic documentation review.
  - Verification Command / Evidence: `rg -n 'references/<language>|reference-refresh|documentation review' codex/skills/ywc-project-scaffold/SKILL.md`
- [ ] Add conditional Trend Check instructions after reference selection and before tree finalization, including large/contested gating, `ywc-tech-research --depth 25`, baseline/delta/unavailable outcomes, and no silent edits.
  - Related AC/FR: AC1–AC3 / FR2
  - Contract / Behavior Change: only large or explicitly contested requests research; unavailable evidence yields `DONE_WITH_CONCERNS`.
  - Verification Command / Evidence: `rg -n 'Trend Check|large|contested|DONE_WITH_CONCERNS|Extras|depth 25' codex/skills/ywc-project-scaffold/SKILL.md`
- [ ] Add the separately headed `reference-refresh` flow with target inference, evidence precedence, additive-only proposal, diff display, explicit approval stop, and narrow skill-owned write exception.
  - Related AC/FR: AC4–AC6 / FR3
  - Contract / Behavior Change: refresh returns `Mode: reference-refresh` and never edits until a later approved turn.
  - Verification Command / Evidence: `rg -n 'reference-refresh|additive|approval|NEEDS_CONTEXT|diff|never removes' codex/skills/ywc-project-scaffold/SKILL.md`
- [ ] Update output, boundaries, common mistakes, and validation text so normal generation remains report-only and both new branches preserve the existing status contract.
  - Related AC/FR: AC1–AC6 / FR1–FR3
  - Contract / Behavior Change: implementation agents can distinguish proposal, concern, and completion states.
  - Verification Command / Evidence: manual section review plus `git diff --check -- codex/skills/ywc-project-scaffold/SKILL.md`.

## Task Verify
- [ ] `git diff --check -- codex/skills/ywc-project-scaffold/SKILL.md`
  - Expected Passing Signal: exit 0 with no whitespace errors.
  - Pre-change Failing Evidence / Exception: N/A — documentation contract task.
  - Contract/Test Evidence: targeted token checks and diff review.
- [ ] `awk '/^---$/{n++} n<=2{print}' codex/skills/ywc-project-scaffold/SKILL.md`
  - Expected Passing Signal: frontmatter contains only `name` and `description` fields.
  - Pre-change Failing Evidence / Exception: N/A — structure-preservation check.
  - Contract/Test Evidence: source frontmatter inspection.

## Verification
- [ ] lint passes (`npx markdownlint-cli2@0.22.1 codex/skills/ywc-project-scaffold/SKILL.md` or installed equivalent)
- [ ] typecheck passes (N/A — Markdown-only task)
- [ ] unit tests pass (N/A — contract fixture is a later task)
- [ ] app builds without error (N/A — repository has no application build)
