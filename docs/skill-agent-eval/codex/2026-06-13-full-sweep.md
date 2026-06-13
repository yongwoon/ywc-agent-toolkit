# Codex Skill/Agent Evaluation - 2026-06-13 - full sweep

## Verdict

| Field | Value |
|---|---|
| Status | REVIEW_REQUIRED |
| Scope | full sweep (`--mode full --target all`) |
| Assets evaluated | 46 (39 skills, 7 agents) |
| Gate failures | 0 |
| Lowest grade | B (`codex/skills/ywc-product-review`, 3.05) |

## Gate Summary

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Result: PASS. skill_count=39, agent_count=7, skill_gate_passed=true, agent_gate_failures=0, skills_missing_openai_yaml=[], skills_incomplete_locale_readmes=[]
Agent warnings: ywc-performance-engineer and ywc-root-cause-analyst output contract wording does not show the shared Status line.
```

## Mechanical Scorecard

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all
Result: PASS mechanically, partial only. Skills: S2/S3/S6 broadly 4; weakest deterministic axis is S5 on several skills. Agents: most deterministic axes 4; root-cause/security have A7=1 because no caller references were found.
```

Mechanical mode is partial. This report fills judgment axes S1/S4/S8 and A1/A3/A8 from the rubric pass; trigger fixture coverage remains incomplete and is called out in the backlog.

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `codex/skills/ywc-agentic` | skill | A | 3.77 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-brainstorm` | skill | A | 3.77 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-changelog-release-notes` | skill | B | 3.44 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-code-gen` | skill | A | 3.51 | S1=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-commit` | skill | A | 3.64 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-confidence-gate` | skill | A | 3.77 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-create-pr` | skill | B | 3.08 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-debug-rootcause` | skill | A | 3.87 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-design-renew` | skill | A | 4.00 | S1=4 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-e2e-test-strategy` | skill | A | 3.87 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-finish-branch` | skill | A | 3.77 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-gen-testcase` | skill | A | 3.61 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-handle-pr-reviews` | skill | B | 3.34 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-impl-review` | skill | A | 3.74 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-incident-postmortem` | skill | A | 3.61 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-merge-dependabot` | skill | A | 3.51 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-onboard-repo` | skill | A | 3.90 | S7=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-parallel-executor` | skill | A | 3.64 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-plan` | skill | A | 3.67 | S7=2 | S7=2: Codex runtime wording/fallback needs tightening. |
| `codex/skills/ywc-product-review` | skill | B | 3.05 | S5=0 | S5=0: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-project-docs` | skill | B | 3.05 | S5=0 | S5=0: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-project-scaffold` | skill | B | 3.05 | S5=0 | S5=0: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-receive-review` | skill | A | 3.64 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-refactor-clean` | skill | A | 3.77 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-release-pr-list` | skill | B | 3.34 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-review-learnings` | skill | A | 4.00 | S1=4 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-security-audit` | skill | A | 3.74 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-sequential-executor` | skill | A | 3.64 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-skill-author` | skill | A | 3.90 | S7=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-spec-validate` | skill | A | 3.64 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-spec-writer` | skill | A | 3.90 | S7=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-task-generator` | skill | A | 3.87 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-tdd-ritual` | skill | A | 3.77 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-team-assemble` | skill | B | 3.05 | S5=0 | S5=0: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-tech-research` | skill | B | 3.31 | S5=2 | Strong trigger, workflow, schema, and scope evidence across rubric axes. |
| `codex/skills/ywc-ubiquitous-language` | skill | A | 3.87 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-ui-ux-review` | skill | A | 3.61 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/skills/ywc-verify-done` | skill | A | 3.87 | S5=3 | Judgment pass found strong structure with one axis below reference quality. |
| `codex/skills/ywc-worktrees` | skill | B | 3.36 | S5=1 | S5=1: mechanical scorer found weak or missing concrete output/verification contract. |
| `codex/agents/ywc-architect.toml` | agent | A | 3.92 | A8=3 | A8=3: edge/refusal behavior is covered, but no smoke fixture evidence exists. |
| `codex/agents/ywc-go-reviewer.toml` | agent | A | 3.92 | A8=3 | A8=3: edge/refusal behavior is covered, but no smoke fixture evidence exists. |
| `codex/agents/ywc-performance-engineer.toml` | agent | A | 3.92 | A8=3 | A8=3: edge/refusal behavior is covered, but no smoke fixture evidence exists. |
| `codex/agents/ywc-python-reviewer.toml` | agent | A | 3.92 | A8=3 | A8=3: edge/refusal behavior is covered, but no smoke fixture evidence exists. |
| `codex/agents/ywc-root-cause-analyst.toml` | agent | A | 3.65 | A7=1 | A7=1: mechanical scorer found no Codex skill caller references. |
| `codex/agents/ywc-security-engineer.toml` | agent | A | 3.65 | A7=1 | A7=1: mechanical scorer found no Codex skill caller references. |
| `codex/agents/ywc-typescript-reviewer.toml` | agent | A | 3.92 | A8=3 | A8=3: edge/refusal behavior is covered, but no smoke fixture evidence exists. |

## Priority Backlog

1. [High] `codex/agents/ywc-root-cause-analyst.toml` - A7=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex custom-agent authoring conventions
   Re-score target: A7 -> >=3
2. [High] `codex/agents/ywc-security-engineer.toml` - A7=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex custom-agent authoring conventions
   Re-score target: A7 -> >=3
3. [High] `codex/skills/ywc-changelog-release-notes` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
4. [High] `codex/skills/ywc-create-pr` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
5. [High] `codex/skills/ywc-gen-testcase` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
6. [High] `codex/skills/ywc-handle-pr-reviews` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
7. [High] `codex/skills/ywc-incident-postmortem` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
8. [High] `codex/skills/ywc-merge-dependabot` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
9. [High] `codex/skills/ywc-product-review` - S5=0
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
10. [High] `codex/skills/ywc-project-docs` - S5=0
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
11. [High] `codex/skills/ywc-project-scaffold` - S5=0
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
12. [High] `codex/skills/ywc-release-pr-list` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
13. [High] `codex/skills/ywc-team-assemble` - S5=0
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
14. [High] `codex/skills/ywc-ui-ux-review` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
15. [High] `codex/skills/ywc-worktrees` - S5=1
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex skill structure/content via ywc-skill-author
   Re-score target: S5 -> >=3
16. [Medium] `codex/agents/ywc-performance-engineer.toml` - Inventory warning: output contract does not show the shared Status line.
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex custom-agent authoring conventions
   Re-score target: A6 gate warning cleared
17. [Medium] `codex/agents/ywc-root-cause-analyst.toml` - Inventory warning: output contract does not show the shared Status line.
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: Codex custom-agent authoring conventions
   Re-score target: A6 gate warning cleared
18. [Medium] `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json` - Only 16 trigger cases cover 9 expected items, not all 46 assets.
   Evidence: rubric/mechanical dimension or inventory warning
   Owner: This internal eval skill fixtures
   Re-score target: Expand trigger/collision fixture coverage

## Decisions

- No gate caps were applied because `inventory_gate.py` passed for skills and agents.
- S1/A1 were judged from Tier-1 descriptions and sibling collision wording; trigger fixtures are too sparse to serve as full-catalog evidence.
- A8 is capped at 3 for all agents because edge/refusal behavior is documented but no smoke fixtures or eval evidence were found.
- `ywc-codex-toolkit-eval` remained internal under `tools/codex-internal/skills/`; no Claude-only paths were scored as Codex assets.

## Next Cycle

- Recommended scope: skills with S5 below 2, then agents with A7 below 2.
- Highest-priority item: add concrete output/verification contracts to S5=0 skills (`ywc-product-review`, `ywc-project-docs`, `ywc-project-scaffold`, `ywc-team-assemble`).
- Mechanical baseline update needed: no.
