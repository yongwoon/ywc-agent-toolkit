# 000053-010-refactor-skill-author-audit-workflow — Implementation Checklist

## Prerequisites

- [ ] Read `docs/ywc-plans/skill-engineering-hardening.md`, including Iteration 1 Amendments.
- [ ] Invoke `ywc-skill-author` before restructuring either target skill.

## Allowed Edit Scope

- [ ] Only `claude-code/skills/ywc-skill-author/**` and `codex/skills/ywc-skill-author/**`.

## Stop Conditions

- [ ] Stop if a second `ywc-skill-audit` directory seems necessary.
- [ ] Stop if audit findings are used to auto-delete/rewrite another skill.
- [ ] Stop if paired scripts require platform-specific behavior or root/CI/plugin edits.

## Hardening Gate

- [ ] Classify: behavior change / Skill-definition maintenance.
- [ ] Named exception: no runtime code; use script fixtures and structural validation as replacement evidence.
- [ ] Record CLI, sections, exit behavior, parity requirement before implementation.
- [ ] Require manual review for trigger breadth, deletion guards, and role exceptions.

## Implementation Steps

- [ ] Add report-only audit workflow to both `SKILL.md` files.
  - [ ] Require bounded scope and mechanical evidence before model judgment.
  - [ ] Define baseline → one removal → same-prompt comparison → retain/revert/escalate.
  - [ ] Forbid auto-deletion, target edits, and executor invocation.
- [ ] Add direct references and graph rules.
  - [ ] Put detailed rubric/examples in `references/`.
  - [ ] Define interface/orchestrator/discipline roles and documented exception handling.
- [ ] Implement identical `audit-skills.sh` scripts.
  - [ ] Parse fixed CLI; invalid input exits 2.
  - [ ] Emit six sorted sections with `none` for empty content.
  - [ ] Detect only mechanical signals; do not declare semantic duplicates.
- [ ] Synchronize locale README, Codex UI metadata, and objective Codex eval fixture.
- [ ] Run valid/invalid/near-cap/missing-counterpart fixtures, both skill validators, and `cmp -s`.

## Task Verify

- [ ] Both directional valid audit commands exit 0 and emit six headings.
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/audit-skills.sh --root /missing --counterpart-root codex/skills; test $? -eq 2`
- [ ] `cmp -s claude-code/skills/ywc-skill-author/scripts/audit-skills.sh codex/skills/ywc-skill-author/scripts/audit-skills.sh`
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/ywc-skill-author && bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author`

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] Diff stays in the declared `ywc-skill-author` directories.
- [ ] No `ywc-skill-audit` directory exists.
