# yw-000013-020-docs-condition-gate-directives

## Purpose

Relocate the remaining 17 `**Action required**` directives (24 total − 6 language − 1 initials)
to the branch that actually consumes them, each stating an explicit condition, per FR7. This is
the bulk of the L1 token savings: most of these directives currently fire unconditionally at
step entry even though the branch they gate is only sometimes taken.

## Scope

Canonical shape: `claude-code/skills/ywc-sequential-executor/SKILL.md:78` — `**Action required
when `--non-interactive` is set**` — already compliant, needs verification only (E10: enumerate
every entry path into its consuming branch), no edit.

16 directives to actually condition-gate (exact file:line):

- `ywc-auth-implement/SKILL.md:46` (policy-interview.md), `:56` (generic-fallback.md), `:62` (subagent-status-actions.md), `:142` (security-checklist.md)
- `ywc-docker-isolate/SKILL.md:103` (port-allocation.md), `:105` (preconditions.md)
- `ywc-create-pr/SKILL.md:351` (pr-bot-polling.md), `:369` (pr-conflict-resolution.md)
- `ywc-handle-pr-reviews/SKILL.md:224` (pr-conflict-resolution.md)
- `ywc-finish-branch/SKILL.md:156` (pr-bot-polling.md — already carries "now before proceeding", verify against amended AC7 regex, likely no change needed), `:196` (pr-conflict-resolution.md)
- `ywc-merge-dependabot/SKILL.md:185` (pr-conflict-resolution.md)
- `ywc-parallel-executor/SKILL.md:88` (non-stop-execution.md — already carries "before creating any worktree", verify only), `:419` (aggregate-pr.md — currently **unconditioned**; needs an explicit "when `--draft` or `--aggregate-pr` is set" prefix, since a `--local-merge`/`--per-task-pr` run never needs it)
- `ywc-sequential-executor/SKILL.md:126` (external-url-policy.md), `:203` (non-stop-execution.md — already carries "before any range task begins", verify only)

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — FR7, AC7 (amended, Iteration 1 A1.4)

### Summary

FR7 requires every directive to state an explicit condition ("when `<flag>`", "before `<named
step>`", "when `<branch>` is entered"). AC7 (amended) checks this via
`grep -rh 'Action required' claude-code/skills/*/SKILL.md | grep -vcE '\b(when|before|if|only)\b'`
returning 0 — the qualifier can appear anywhere in the line, not just immediately after "Action
required" (the original anchored form would have rejected `ywc-finish-branch:156`'s genuinely
compliant "now before proceeding" phrasing).

### Out of Scope (from spec)

- The 6 language + 1 initials directives — handled by `yw-000013-010`.
- Any change to the referenced files themselves (`pr-bot-polling.md`, etc.) — only the directive line in the consuming `SKILL.md` changes.

## Criticality

`normal` — documentation/instruction-text change only.

## Dependencies

### Depends On

- `yw-000012-020`, `yw-000012-030` — Phase `yw-000011` is a hard gate before this phase starts (not a functional dependency; FR7 is independent of the two scripts)

### Depended By

- `yw-000014-010` — documents the finished pattern in `CLAUDE.md`
- `yw-000014-020` — verifies AC7 in the final report

## Key Files

- `claude-code/skills/ywc-auth-implement/SKILL.md`
- `claude-code/skills/ywc-docker-isolate/SKILL.md`
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `claude-code/skills/ywc-finish-branch/SKILL.md`
- `claude-code/skills/ywc-merge-dependabot/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/SKILL.md`

## Notes

E10 (spec Edge Case): a relocated directive reachable by two entry paths into its consuming
branch, where only one path is now gated, is a regression, not a fix. Each relocation must be
verified against every entry path, not just the one being edited.

## Parallel Execution Metadata

### Ownership

- The 8 `SKILL.md` files listed in Key Files

### Owned Interface

- (None — no public interface owned; SKILL.md body text only)

### Shared Surfaces

- (None beyond the file-level overlap noted below)

### Conflicts With

- `yw-000013-010` — shares `ywc-auth-implement/SKILL.md` and `ywc-create-pr/SKILL.md`; do not run these two tasks in parallel worktrees

### Parallelizable After

- `yw-000012-020`, `yw-000012-030`

### Task Verify

- `grep -rh 'Action required' claude-code/skills/*/SKILL.md | grep -vcE '\b(when|before|if|only)\b'` returns `0`

## Out of Scope

- The language/initials directives (`yw-000013-010`'s scope).
- Rewording any directive's underlying reference file.
