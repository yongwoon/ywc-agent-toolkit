# yk-000005-020-domain-user-invoked-skills

## Purpose
Make `ywc-merge-dependabot` and `ywc-setup-language` user-invoked, add rule A16 and Writing Levers, and teach the validators and eval fixtures about the exception in the same task so CI never goes red (AC12 partial, AC13).

Spec item: B3 (#335, #345) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- Both skills: `disable-model-invocation: true` and a one-line description; four Tier 1 READMEs each get a user-invoked blockquote.
- Root `CLAUDE.md:88` and `claude-code/skills/CLAUDE.md:83`: add the exception 'user-invoked skills are exempt from trigger / anti-trigger rules'.
- `ywc-skill-author`: rule A16 and a `## Writing Levers` section; `references/cross-skill-graph.md:52,78,157` mark the two skills 'user-invoked — not a model-routing target'; `references/language-resolution.md:108` uses slash notation (`/ywc-setup-language`).
- Validators: `validate-skill.sh:63-69` and `.claude/skills/ywc-toolkit-eval/scripts/score.py:376-378` skip A2/A3/A4 for skills with `disable-model-invocation: true`; add one `test_score.py` case; keep S2 for both skills at the current baseline value (5) — `ci_gate` exits 1 on any axis drop and cannot absorb it.
- Record `score.py --ci` BEFORE and AFTER (both PASS) and commit the auto-updated `history.mechanical.json`.
- `trigger-cases.json`: remove or relabel as 'user-invoked, not routed' every case whose expected/impostor is either skill (re-grep at implementation time; ~42 lines, first at `:419`); the file must still pass `test_fixture_schema.py`.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 11 (B3), FR8, AC12, AC13, Existing Constraints Touched 'user-invoked', Failure Modes 'user-invoked' / 'CI red'
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-skill-author/SKILL.md` — upstream A16 + Writing Levers (T0 snapshot)

### Summary
`ywc-merge-dependabot` and `ywc-setup-language` are things a user types, not things a model should route to. The root rule demands trigger phrases and anti-triggers in every description, so the exception, the validators and the eval fixtures must all change together.

### Out of Scope (from spec)
- `validate.sh` gate for script paths (follow-up)
- `ywc-gen-testcase/SKILL.md:329` (no change needed)
- Description changes in other skills (no references to the two skills exist)

## Criticality
normal — Policy and validator exception; CI gate is protected by the before/after `score.py --ci` record.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream A16 / Writing Levers / frontmatter
- `yk-000005-010-domain-skill-path-convention` — serializes `ywc-skill-author/SKILL.md` and `claude-code/skills/CLAUDE.md` (B1 → B3)

### Depended By
- `yk-000005-030-refactor-skill-script-paths` — needs the output of this task
- `yk-000005-050-domain-handoff-retro-skills` — needs the output of this task

## Key Files
- `claude-code/skills/ywc-merge-dependabot/SKILL.md` — frontmatter
- `claude-code/skills/ywc-setup-language/SKILL.md` — frontmatter
- `claude-code/skills/ywc-skill-author/SKILL.md` — A16, Writing Levers
- `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh` — A2/A3/A4 skip
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` — A2/A3/A4 skip
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` — one new case
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` — case cleanup
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — auto-updated baseline
- `CLAUDE.md` — :88 exception
- `claude-code/skills/CLAUDE.md` — :83 exception

## Notes
- `validate-skill.sh` is not run in CI; its edit is for rule consistency. The CI gate is `score.py --ci`.
- Do not write the forbidden repo-relative script-path literal in rule text (AC10).

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-merge-dependabot/SKILL.md`
- `claude-code/skills/ywc-merge-dependabot/README*.md`
- `claude-code/skills/ywc-setup-language/**`
- `claude-code/skills/ywc-skill-author/**`
- `claude-code/skills/CLAUDE.md`
- `CLAUDE.md`
- .claude/skills/ywc-toolkit-eval/**

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Description rules A2–A4 (root and skills CLAUDE.md)
- CI gate `score.py --ci` baseline
- `trigger-cases.json` fixture schema

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`
- `yk-000005-010-domain-skill-path-convention`

### Task Verify
- Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` BEFORE editing and record PASS in Implementation Notes
- `[ "$(grep -l '^disable-model-invocation: true' claude-code/skills/*/SKILL.md | wc -l | tr -d ' ')" = 2 ]`
- `[ "$(grep -c 'user-invoked' claude-code/skills/ywc-skill-author/references/cross-skill-graph.md | tr -d ' ')" -ge 2 ]`
- `grep -q 'A16' claude-code/skills/ywc-skill-author/SKILL.md`
- `[ "$(grep -c -- '^## Writing Levers' claude-code/skills/ywc-skill-author/SKILL.md | tr -d ' ')" = 1 ]`
- `grep -q 'disable-model-invocation' claude-code/skills/ywc-skill-author/scripts/validate-skill.sh`
- `grep -q 'disable-model-invocation' .claude/skills/ywc-toolkit-eval/scripts/score.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` (AFTER; must PASS) and stage the updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-skill-author/SKILL.md`

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
