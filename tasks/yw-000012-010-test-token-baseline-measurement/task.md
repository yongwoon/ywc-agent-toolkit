# yw-000012-010-test-token-baseline-measurement — Implementation Checklist

## Prerequisites

Verify these before starting:

- [ ] `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` status is `DONE` per its
      `spec-ready-log.md` (Iteration 2, gate 92)

## Allowed Edit Scope

- [ ] This task edits no source files — its only write is to this file's Implementation Notes
      section below
- [ ] If a measurement command fails and requires a source-level workaround, stop and report
      rather than editing anything outside this file

## Stop Conditions

- [ ] Stop if `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`
      errors out (do not attempt to fix the eval tool itself in this task)
- [ ] Stop if any of the 12 target `SKILL.md` files does not exist at the expected path

## Implementation Steps

- [ ] Run `wc -c` on `SKILL.md` for each of the 12 skills listed in README.md Notes; record
      each byte count
- [ ] For `ywc-sequential-executor`, trace its default (no `--non-interactive`,
      no `--aggregate-pr`, no external-URL branch) execution path and list which
      `**Action required**` directives it actually reads on that path (cross-reference the
      grep list already captured for this spec: `SKILL.md:78` non-interactive-mode.md is
      gated and NOT read by default; determine whether `SKILL.md:126`
      external-url-policy.md and `SKILL.md:203` non-stop-execution.md are read on the default
      path); sum `wc -c` for body + the references actually read by default
- [ ] Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`
      and extract the per-skill score for each of the 12 modified skills
- [ ] Record all three sets of numbers (per-skill SKILL.md size, `ywc-sequential-executor`
      default-path composite size, per-skill mechanical score) in the Implementation Notes
      section below, labeled clearly as the "before" baseline

## Task Verify

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json` exits 0 and produces scores for all 12 skills
- [ ] `wc -c` succeeds for all 12 `SKILL.md` files

## Verification

- [ ] `bash scripts/validate.sh` still exits 0 (no source changed, this is a regression check only)

## Implementation Notes (optional)
