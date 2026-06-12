# Scorecard & History Format

Two artifacts close the cycle: a human-readable `scorecard.md` (the snapshot) and a machine-readable `history.json` (the trend). The script writes the JSON; the agent renders the markdown from the same data.

## scorecard.md

One section per evaluated root, a per-item table, then the prioritized backlog. Totals are `/100`. "Weakest" is the axis with the largest `weight × (5 − score)` contribution to lost points (the highest-leverage fix), not simply the lowest raw score.

```text
# Toolkit Scorecard — <YYYY-MM-DD>

Mode: full | mechanical | judge
Advisor escalations used: <n>/<budget>

## codex/skills  (<count> items, mean <m>/100)

| Item | S1 | S2 | S3 | S4 | S5 | S6 | Total | Weakest |
|------|----|----|----|----|----|----|-------|---------|
| ywc-commit        | 5 | 5 | 4 | 5 | 5 | 4 | 92 | S3 |
| ...               |   |   |   |   |   |   |    |    |

## codex/agents  (<count> items, mean <m>/100)

| Item | A1 | A2 | A3 | A4 | A5 | A6 | Total | Weakest |
|------|----|----|----|----|----|----|-------|---------|
| ywc-security-engineer | 5 | 5 | 5 | 5 | 5 | 4 | 96 | A6 |

## Prioritized Backlog

1. <item> (<total>) — <axis> <axis-name>: <evidence at file:line>.
   Fix: <concrete action; name ywc-skill-author for structural fixes>.
2. ...

## Regression vs <prev-date>
- <item>: <axis> <old>→<new>  (▲ improved | ▼ regressed | – flat)
```

## history.json

Append-only. Each run adds exactly one object. Never mutate prior entries — the file IS the trend line.

```json
{
  "schema": 1,
  "runs": [
    {
      "date": "2026-06-12",
      "mode": "full",
      "roots": {
        "codex/skills": {
          "count": 36,
          "mean_total": 82.4,
          "below_threshold": 3,
          "items": { "ywc-commit": 92, "ywc-tech-research": 64 }
        },
        "codex/agents": {
          "count": 12,
          "mean_total": 90.1,
          "below_threshold": 0,
          "items": { "ywc-security-engineer": 96 }
        }
      }
    }
  ]
}
```

`below_threshold` counts items under 70/100 (the "needs work" line). The CI `--ci` gate does not read `mean_total`; it compares per-item, per-axis mechanical sub-scores against the most recent run's stored mechanical sub-scores and fails on any drop. (Mechanical sub-scores are stored in a sibling `history.mechanical.json` written only in `--ci`/`mechanical` modes so the judgment tier's natural variance never trips the gate.)

## Threshold Reference

| Band | Total | Meaning |
|---|---|---|
| 90–100 | exemplary | reference example for new skills |
| 75–89 | healthy | no action needed this cycle |
| 70–74 | watch | fix the weakest axis next cycle |
| < 70 | needs work | enters the prioritized backlog now |

The threshold is deliberately strict on activation: any item with S1 or A2 ≤ 2 enters the backlog regardless of total, because a mis-firing item degrades siblings every conversation.
