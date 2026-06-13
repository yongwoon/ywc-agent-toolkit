# Codex Skill/Agent Evaluation - 2026-06-13 - post improvement

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | post-improvement full sweep (`--target all`) |
| Assets evaluated | 46 (39 skills, 7 agents) |
| Gate failures | 0 |
| Lowest grade | B / 3.31 (`codex/skills/ywc-tech-research`) |

## Gate Summary

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Result: PASS. skill_count=39, agent_count=7, skill_gate_passed=true, agent_gate_failures=0.
Target warnings cleared: ywc-performance-engineer and ywc-root-cause-analyst now have no shared Status-line inventory warning.
```

## Mechanical Scorecard

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all
Result: PASS mechanically, partial only. Target S5 gaps are cleared for the FR-1 skills; ywc-root-cause-analyst and ywc-security-engineer now have A7=4.
```

Mechanical mode is partial. This report preserves the judgment-axis assumptions from `2026-06-13-full-sweep.md` and refreshes deterministic axes from the post-improvement run.

## Acceptance Summary

| Check | Result |
|---|---|
| Structural gate | PASS |
| Repository validation | PASS (`bash scripts/validate.sh`) |
| FR-1 target S5 | PASS; targeted low S5 skills now score 4 |
| Target agent A7 | PASS; `ywc-root-cause-analyst` and `ywc-security-engineer` now score A7=4 |
| Target inventory warnings | PASS; performance/root-cause shared Status-line warnings cleared |
| Trigger fixture coverage | PASS; 75 cases, 46 catalog assets positive-covered, 23 collision cases, 1 internal eval label |

## Changed Scorecards

| Asset | Previous | Current | Current state | Evidence |
|---|---:|---:|---|---|
| `codex/skills/ywc-changelog-release-notes` | B / 3.44 | A / 3.83 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-create-pr` | B / 3.08 | B / 3.47 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-gen-testcase` | A / 3.61 | A / 4.00 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-handle-pr-reviews` | B / 3.34 | A / 3.73 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-incident-postmortem` | A / 3.61 | A / 4.00 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-merge-dependabot` | A / 3.51 | A / 3.90 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-product-review` | B / 3.05 | A / 3.57 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-project-docs` | B / 3.05 | A / 3.57 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-project-scaffold` | B / 3.05 | A / 3.57 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-release-pr-list` | B / 3.34 | A / 3.73 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-team-assemble` | B / 3.05 | A / 3.57 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-ui-ux-review` | A / 3.61 | A / 4.00 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/skills/ywc-worktrees` | B / 3.36 | A / 3.75 | Resolved S5=4 | S5 output/validation/status contract now scores 4 where this task targeted the gap. |
| `codex/agents/ywc-root-cause-analyst.toml` | A / 3.65 | A / 3.92 | Resolved A7=4 | A7 caller integration now scores 4 and inventory Status-line warning is cleared. |
| `codex/agents/ywc-security-engineer.toml` | A / 3.65 | A / 3.92 | Resolved A7=4 | A7 caller integration now scores 4 and inventory Status-line warning is cleared. |

## Mechanical Excerpt

```text
## codex/skills (39 items)
| Item | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | Mechanical points | Final |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `ywc-changelog-release-notes` | · | 4 | 4 | · | 4 | 4 | 4 | · | 57.0/57.0 | partial |
| `ywc-create-pr` | · | 4 | 4 | · | 4 | 4 | 3 | · | 54.5/57.0 | partial |
| `ywc-gen-testcase` | · | 4 | 4 | · | 4 | 4 | 4 | · | 57.0/57.0 | partial |
| `ywc-product-review` | · | 4 | 4 | · | 4 | 4 | 4 | · | 57.0/57.0 | partial |
## codex/agents (7 items)
| Item | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | Mechanical points | Final |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `ywc-root-cause-analyst` | · | 4 | · | 4 | 4 | 4 | 4 | · | 60.0/60.0 | partial |
| `ywc-security-engineer` | · | 4 | · | 4 | 4 | 4 | 4 | · | 60.0/60.0 | partial |
```

## Remaining Actions

1. [Medium] `codex/skills/ywc-create-pr` remains B / 3.47 after the S5 fix.
   Evidence: deterministic S5 is fixed; remaining gap is in carried-forward judgment quality.
   Owner: Codex skill authoring polish.
   Re-score target: raise judgment axes enough to reach A.
2. [Medium] `codex/skills/ywc-tech-research` remains B / 3.31.
   Evidence: S5 remains 2, which was outside this improvement batch's high-priority target list.
   Owner: Codex skill authoring polish.
   Re-score target: S5 -> >=3.

## Decisions

- `2026-06-13-full-sweep.md` is preserved as pre-change evidence.
- No evaluator scoring model or mechanical baseline was changed.
- The ignored trigger fixture was updated only after explicit force-add approval for `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json`.

## Next Cycle

- Recommended scope: remaining B-grade skills and optional reference-quality polish.
- Highest-priority item: `codex/skills/ywc-tech-research` S5 contract quality.
- Mechanical baseline update needed: no.
