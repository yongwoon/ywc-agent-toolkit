# Codex Evaluation Report Template

Use this file when writing Codex-only evaluation outputs under
`docs/skill-agent-eval/codex/`.

## Per-run Report

````markdown
# Codex Skill/Agent Evaluation - <YYYY-MM-DD> - <scope>

## Verdict

| Field | Value |
|---|---|
| Status | PASS / PASS_WITH_ACTIONS / REVIEW_REQUIRED / FAIL |
| Scope | <full sweep / skills only / agents only / targeted> |
| Assets evaluated | <n> |
| Gate failures | <n> |
| Lowest grade | <A/B/C/D> |

## Gate Summary

```text
<inventory_gate.py command>
<short result excerpt>
```

## Mechanical Scorecard

```text
<score.py --format markdown command>
<short result excerpt or attached table>
```

Mechanical mode is partial. Judgment axes must be rendered as `·`, and no final
quality total should be claimed until the judgment pass is complete.

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `path` | skill/agent | B | 3.1 | S7 Codex runtime fit | <one-line evidence> |

## Priority Backlog

1. [Critical] `asset` - <finding>
   Evidence: <path, gate field, or rubric dimension>
   Owner: <ywc-skill-author / Codex agent authoring / bundle docs>
   Re-score target: <dimension and expected movement>

## Decisions

- <Any scoring assumptions, gate caps, or excluded assets>

## Next Cycle

- Recommended scope: <scope>
- Highest-priority item: <asset/finding>
- Mechanical baseline update needed: yes/no
````

## Scoreboard

```markdown
# Codex Skill/Agent Evaluation Scoreboard

| Asset | Kind | Current | Previous | Trend | Last evaluated | Weakest dimension | Next action |
|---|---|---:|---:|---|---|---|---|
| `codex/skills/ywc-plan` | skill | A / 3.6 | B / 3.3 | up | 2026-06-12 | S5 | Add eval fixture |
```

## Status Rules

| Status | Use when |
|---|---|
| PASS | No gate failures and no High/Critical backlog |
| PASS_WITH_ACTIONS | Evaluation completed with Medium/Low backlog |
| REVIEW_REQUIRED | Any High backlog or score uncertainty that affects release readiness |
| FAIL | Any Critical gate failure or asset below grade C |
