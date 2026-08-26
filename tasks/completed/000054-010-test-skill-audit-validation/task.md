# 000054-010-test-skill-audit-validation — Implementation Checklist

## Prerequisites

- [ ] `000053-010-refactor-skill-author-audit-workflow` is completed and merged.
- [ ] `000053-020-refactor-agentic-autonomy-trigger` is completed and merged.

## Allowed Edit Scope

- [ ] Do not edit `claude-code/skills/**` or `codex/skills/**` during validation.
- [ ] Only task completion bookkeeping is allowed after passing checks.

## Stop Conditions

- [ ] Stop if either Phase 000053 task is unmerged or an artifact is missing.
- [ ] Stop if valid audits exit non-zero, invalid inputs fail to return 2, scripts differ, or repository validation fails.
- [ ] Stop if pilot selection requires editing a candidate skill.

## Hardening Gate

- [ ] Classify: test-only / read-only validation.
- [ ] RED-first evidence: invalid `--root` invocation returns exit 2.
- [ ] Record exact CLI sections, advisory exit behavior, and activation routing boundary.
- [ ] Manually confirm no audit finding was treated as deletion authorization.

## Implementation Steps

- [ ] Verify Phase 000053 artifacts and `cmp -s` script parity.
- [ ] Exercise both directional valid audits; verify six stable headings and `none` for empty sections.
- [ ] Exercise invalid root and invalid threshold; verify exit 2.
- [ ] Check one explicit autonomous lifecycle request, one generic planning request, and one direct-change request against descriptions.
- [ ] Run `bash scripts/validate.sh`; nominate exactly one later pruning pilot without editing it.

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/audit-skills.sh --root claude-code/skills --counterpart-root codex/skills`
- [ ] `bash codex/skills/ywc-skill-author/scripts/audit-skills.sh --root codex/skills --counterpart-root claude-code/skills`
- [ ] `bash codex/skills/ywc-skill-author/scripts/audit-skills.sh --root codex/skills --counterpart-root claude-code/skills --near-line-cap 0; test $? -eq 2`
- [ ] `cmp -s claude-code/skills/ywc-skill-author/scripts/audit-skills.sh codex/skills/ywc-skill-author/scripts/audit-skills.sh`
- [ ] `bash scripts/validate.sh`

## Verification

- [ ] Findings remain advisory; this task edits no target skill.
- [ ] Pilot recommendation has evidence beyond line count.
