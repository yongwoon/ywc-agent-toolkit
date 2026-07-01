# Codex Skill/Agent Evaluation - 2026-07-01 - post-improvement

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | targeted improvement after full sweep |
| Assets evaluated | 48 (41 skills, 7 agents) |
| Gate failures | 0 |
| Lowest grade | A |

## Improvement Summary

This pass addressed the 2026-07-01 full-sweep backlog for S5 output/verification contracts and S7 Codex runtime fit.

Changed source skills:

- `ywc-changelog-release-notes`
- `ywc-code-gen`
- `ywc-commit`
- `ywc-confidence-gate`
- `ywc-create-pr`
- `ywc-handle-pr-reviews`
- `ywc-merge-dependabot`
- `ywc-onboard-repo`
- `ywc-parallel-executor`
- `ywc-project-scaffold`
- `ywc-receive-review`
- `ywc-task-generator`
- `ywc-ubiquitous-language`
- `ywc-verify-done`

Generated plugin copies under `plugins/ywc-agent-toolkit/skills/` were refreshed with `bash scripts/sync-codex-plugin.sh`.

## Gate Summary

```text
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Exit code: 0.
Result: PASS.
skill_count=41, agent_count=7.
skills_missing_openai_yaml=[].
skills_incomplete_locale_readmes=[].
skills_without_evals=[].
```

## Mechanical Scorecard

```text
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target all --format markdown
Exit code: 0.
Result: PASS mechanically, partial only.
codex/skills: 41 items. codex/agents: 7 items.
All 41 Codex skills now score 57.0/57.0 on deterministic axes.
All 7 Codex agents remain 60.0/60.0 on deterministic axes.
```

Mechanical mode is still partial. Judgment axes remain report-owned, not scorer-owned.

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `codex/skills/ywc-agentic` | skill | A | 3.92 | S8 | Broad orchestration scope remains documented but still a watch item. |
| `codex/skills/ywc-brainstorm` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-changelog-release-notes` | skill | A | 4.00 | none | Replaced `AskUserQuestion` literal with Codex-native conversational prompt wording. |
| `codex/skills/ywc-code-gen` | skill | A | 4.00 | none | Added explicit `## Validation`; clarified downstream/out-of-scope ownership. |
| `codex/skills/ywc-commit` | skill | A | 4.00 | none | Replaced slash-command examples with Codex skill invocation text. |
| `codex/skills/ywc-confidence-gate` | skill | A | 4.00 | none | Replaced sibling relative-link reference with plain skill name. |
| `codex/skills/ywc-create-pr` | skill | A | 4.00 | none | Replaced `AskUserQuestion`; added Integration/out-of-scope ownership. |
| `codex/skills/ywc-debug-rootcause` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-design-renew` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-docker-isolate` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-e2e-test-strategy` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-finish-branch` | skill | A | 3.92 | S8 | Broad delivery scope remains documented but still a watch item. |
| `codex/skills/ywc-gen-testcase` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-handle-pr-reviews` | skill | A | 4.00 | none | Replaced sibling relative-link reference with plain skill name. |
| `codex/skills/ywc-impl-review` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-incident-postmortem` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-merge-dependabot` | skill | A | 4.00 | none | Replaced slash-command downstream reference with plain skill name. |
| `codex/skills/ywc-onboard-repo` | skill | A | 4.00 | none | Replaced sibling relative-link references with plain skill names. |
| `codex/skills/ywc-parallel-executor` | skill | A | 4.00 | none | Replaced sibling relative-link references with plain skill names. |
| `codex/skills/ywc-plan` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-product-review` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-project-docs` | skill | A | 3.92 | S8 | Broad docs surface remains documented but still a watch item. |
| `codex/skills/ywc-project-scaffold` | skill | A | 4.00 | none | Replaced slash-command examples with Codex skill invocation text. |
| `codex/skills/ywc-receive-review` | skill | A | 4.00 | none | Replaced sibling relative-link references with plain skill names. |
| `codex/skills/ywc-refactor-clean` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-release-pr-list` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-review-learnings` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-security-audit` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-sequential-executor` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-skill-author` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-spec-ready` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-spec-validate` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-spec-writer` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-task-generator` | skill | A | 4.00 | none | Added explicit `## Validation`. |
| `codex/skills/ywc-tdd-ritual` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-team-assemble` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-tech-research` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-ubiquitous-language` | skill | A | 4.00 | none | Added `Status:` contract and Codex-first agent instruction integration prompt. |
| `codex/skills/ywc-ui-ux-review` | skill | A | 4.00 | none | No score below 4. |
| `codex/skills/ywc-verify-done` | skill | A | 4.00 | none | Replaced literal `run_in_background: true` field with generic Codex runtime wording. |
| `codex/skills/ywc-worktrees` | skill | A | 4.00 | none | No score below 4. |
| `codex/agents/*.toml` | agent | A | 4.00 | none | Agent rows unchanged; smoke-backed A8 evidence remains valid. |

## Priority Backlog

1. [Low] Broad S8 watch list - `ywc-agentic`, `ywc-finish-branch`, and `ywc-project-docs` still own broad workflows or document surfaces.
   Evidence: S8=3 judgment watch item.
   Owner: `ywc-skill-author`
   Re-score target: S8 -> 4 after a future pass tightens scope boundaries or confirms current boundaries are sufficient.

## Scoreboard Update

- Added: 0
- Improved: 14
- Regressed: 0
- Unchanged: 34
- Next review scope: targeted S8 watch list only
