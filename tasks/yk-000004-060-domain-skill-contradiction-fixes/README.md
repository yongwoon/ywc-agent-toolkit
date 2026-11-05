# yk-000004-060-domain-skill-contradiction-fixes

## Purpose
Apply the Model Hint column rule to `ywc-task-generator` and the independent contradiction fixes in seven other skills plus the skill template (AC3, AC8b).

Spec item: A2 (#337) + A8 (small fixes) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- A2: in `ywc-task-generator/SKILL.md:450` ('Task list summary') require columns Task ID / Title / Model Hint (value copied from each README's Model Hint bullet).
- `ywc-changelog-release-notes`: refactor/chore also excluded from CHANGELOG with an `Omitted:` line in the run summary; insert under `## [Unreleased]`; update README table.
- `ywc-code-gen`: `NEEDS_CONTEXT` also covers a REVIEW band / `--review` result; 'Execute all steps (0 → 7.5)'.
- `ywc-refactor-clean`: require a clean working tree before deleting (step 0); on red use `git checkout -- <files>`; Status line.
- `ywc-security-audit`: prompt-injection severity adjusts only by the item's own row condition (`references/prompt-injection-checklist.md:11`, row `:109`); Phase 1 text matches the real 3-cluster parallel structure.
- `ywc-spec-validate`: Status table limited to 'Pre-gate status'; gate decision status comes only from the Band-to-status table.
- `ywc-infra-review`: with `--scope`, check apply-history evidence once and print `Scope evidence:`; read `ywc-infra-reviewer` results inline (it has no Write tool).
- `ywc-iac-author`: add per-module dispatch (`ywc-infra-engineer`) to anti-triggers.
- `ywc-verify-done`: delete only the `requires: []` line (description is already `>-`). `ywc-skill-author/references/skill-template.md`: description as `>-` block scalar, keep the `requires:` placeholder (rules A5/B1 still define it).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` items 2 (A2) and 8 (A8 bullets except executors and scan-secrets), AC3, AC8b
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills` — upstream final text of each skill (T0 snapshot)

### Summary
Each fix is small and independent; they are bundled because none touches a shared file with another Phase A task. Sentence-level corrections without a grep have review-only verification: quote the before/after row in Implementation Notes.

### Out of Scope (from spec)
- Executors, scan-secrets (own tasks)
- Removing `requires:` from the template (rule change is out of this spec)
- `ywc-task-generator` script-path edits (B2)

## Criticality
normal — Documentation corrections across independent skills; no security-sensitive surface.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream text for all listed skills

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-task-generator/SKILL.md` — :450 summary row
- `claude-code/skills/ywc-changelog-release-notes/**` — SKILL.md + README table
- `claude-code/skills/ywc-code-gen/SKILL.md` — NEEDS_CONTEXT, step range
- `claude-code/skills/ywc-refactor-clean/SKILL.md` — step 0, red handling, Status
- `claude-code/skills/ywc-security-audit/**` — SKILL.md + prompt-injection-checklist.md
- `claude-code/skills/ywc-spec-validate/SKILL.md` — Pre-gate status
- `claude-code/skills/ywc-infra-review/SKILL.md` — Scope evidence, inline read
- `claude-code/skills/ywc-iac-author/SKILL.md` — anti-trigger
- `claude-code/skills/ywc-verify-done/SKILL.md` — drop requires: []
- `claude-code/skills/ywc-skill-author/references/skill-template.md` — description `>-`

## Notes
- `ywc-verify-done/SKILL.md` and `ywc-task-generator/SKILL.md` are edited again by B2 — keep this task free of path-form changes.
- If a snapshot sentence names a skill absent locally, drop the sentence (FR3).

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-changelog-release-notes/**`
- `claude-code/skills/ywc-code-gen/SKILL.md`
- `claude-code/skills/ywc-refactor-clean/SKILL.md`
- `claude-code/skills/ywc-security-audit/**`
- `claude-code/skills/ywc-spec-validate/SKILL.md`
- `claude-code/skills/ywc-infra-review/SKILL.md`
- `claude-code/skills/ywc-iac-author/SKILL.md`
- `claude-code/skills/ywc-verify-done/SKILL.md`
- `claude-code/skills/ywc-skill-author/references/skill-template.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `grep 'Task list summary' claude-code/skills/ywc-task-generator/SKILL.md | grep -q 'Model Hint'`
- `grep -q 'Omitted:' claude-code/skills/ywc-changelog-release-notes/SKILL.md`
- `grep -q 'REVIEW band' claude-code/skills/ywc-code-gen/SKILL.md`
- `grep -q 'Pre-gate status' claude-code/skills/ywc-spec-validate/SKILL.md`
- `grep -q 'Scope evidence:' claude-code/skills/ywc-infra-review/SKILL.md`
- `grep -q 'ywc-infra-engineer' claude-code/skills/ywc-iac-author/SKILL.md`
- `[ "$(grep -c -- '^requires:' claude-code/skills/ywc-verify-done/SKILL.md | tr -d ' ')" = 0 ]`
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-changelog-release-notes/SKILL.md claude-code/skills/ywc-code-gen/SKILL.md claude-code/skills/ywc-refactor-clean/SKILL.md claude-code/skills/ywc-security-audit/SKILL.md claude-code/skills/ywc-spec-validate/SKILL.md claude-code/skills/ywc-infra-review/SKILL.md claude-code/skills/ywc-iac-author/SKILL.md claude-code/skills/ywc-verify-done/SKILL.md`
- Review-only: quote before/after for refactor-clean step 0 and the security-audit severity rule in Implementation Notes
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
