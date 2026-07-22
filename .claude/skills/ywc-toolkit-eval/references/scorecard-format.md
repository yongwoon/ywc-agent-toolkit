# Scorecard & History Format

Two artifacts close the cycle: a human-readable `scorecard.md` (the snapshot) and a machine-readable `history.json` (the trend). The script writes the JSON; the agent renders the markdown from the same data.

## scorecard.md

One section per evaluated root, a per-item table, then the prioritized backlog. Totals are `/100`. "Weakest" is the axis with the largest `weight × (5 − score)` contribution to lost points (the highest-leverage fix), not simply the lowest raw score.

```text
# Toolkit Scorecard — <YYYY-MM-DD>

Mode: full | mechanical | judge
Advisor escalations used: <n>/<budget>

## claude-code/skills  (<count> items, mean <m>/100)

| Item | S1 | S2 | S3 | S4 | S5 | S6 | Total | Weakest |
|------|----|----|----|----|----|----|-------|---------|
| ywc-commit        | 5 | 5 | 4 | 5 | 5 | 4 | 94 | S3 |
| ywc-sample-nofx   | 5 | 5 | ? | 5 | 5 | 4 | —  | S3 |
| ywc-sample-mech   | 5 | 5 | · | 5 | 5 | · | —  | —  |
| ...               |   |   |   |   |   |   |    |    |

## claude-code/agents  (<count> items, mean <m>/100)

| Item | A1 | A2 | A3 | A4 | A5 | A6 | Total | Weakest |
|------|----|----|----|----|----|----|-------|---------|
| ywc-security-engineer | 5 | 5 | 5 | 5 | 5 | 4 | 96 | A6 |

## Notation

| Mark | Meaning | How it is resolved |
|---|---|---|
| `4` | A measured score. | — |
| `4 (read-only)` | S3 read from the body because the item has no fixture. | Add a fixture to convert it into an observation. |
| `?` | **Cannot be measured** — the fixture needed for this axis does not exist. | Backfill the fixture. |
| `·` | **Not measured this run** — the judgment tier did not run (`--mode mechanical` / `--ci`). | Re-run with `--mode full`. |
| `—` | No total, because at least one axis is `?` or `·`. | Resolve every axis first. |

`?` and `·` are never merged. They look alike on the page and are opposites in practice: one is a gap in the fixture set that someone has to fill, the other is just a cheaper run mode. Collapsing them would hide real coverage debt behind "we skipped the judges this time".

A `—` total is deliberate. An item missing S3 has at most 80 weight available, so any `/100` number it could report would be an understatement dressed as a score. `history.json` records `items.<name>: null` for these, and they are excluded from `mean_total` and `below_threshold` rather than counted as zero — but they still enter the prioritized backlog, because an unmeasurable axis is itself the finding.

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
        "claude-code/skills": {
          "count": 36,
          "mean_total": 82.4,
          "below_threshold": 3,
          "items": { "ywc-commit": 92, "ywc-tech-research": 64 }
        },
        "claude-code/agents": {
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

Each root object carries `count` (items seen), `measured` (items with a total), `unmeasured` (names with no total, sorted), `mean_total`, `below_threshold`, `items`, and `s3_source`. An unmeasured item is `items.<name>: null` and is excluded from both `mean_total` and `below_threshold` — `count` still includes it, so `count - measured` is the coverage debt. When nothing was measurable, `mean_total` is `null` rather than `0`.

`s3_source` maps item name to `"runner"` or `"read-only"`, because a 4 from six observed trials and a 4 from reading the body are different claims and the trend line is unreadable if they are stored identically.

`below_threshold` counts measured items under 70/100 (the "needs work" line). The CI `--ci` gate does not read `mean_total`; it compares per-item, per-axis mechanical sub-scores against the most recent run's stored mechanical sub-scores and fails on any drop. (Mechanical sub-scores are stored in a sibling `history.mechanical.json` written only in `--ci`/`mechanical` modes so the judgment tier's natural variance never trips the gate.)

## Threshold Reference

| Band | Total | Meaning |
|---|---|---|
| 90–100 | exemplary | reference example for new skills |
| 75–89 | healthy | no action needed this cycle |
| 70–74 | watch | fix the weakest axis next cycle |
| < 70 | needs work | enters the prioritized backlog now |

The threshold is deliberately strict on activation: any item with S1 or A2 ≤ 2 enters the backlog regardless of total, because a mis-firing item degrades siblings every conversation.
