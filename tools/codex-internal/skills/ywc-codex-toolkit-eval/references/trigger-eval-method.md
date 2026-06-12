# Trigger Evaluation Method (S1 / A2)

Activation accuracy is the highest-weighted axis because it is a property of the **whole catalog**, not a single file. This document defines how `evals/trigger-cases.json` is built and how the activation judge turns it into precision and recall.

## Case Taxonomy

`evals/trigger-cases.json` holds three kinds of case, each a natural-language prompt a user would actually type:

| Kind | Meaning | Scoring role |
|---|---|---|
| `positive` | This item SHOULD activate | drives **recall** |
| `negative` | NO item should activate (or a non-sibling should) | drives **precision** |
| `collision` | A *sibling* should win, not this item | the hard cases — drives precision against the nearest neighbor |

Every item under evaluation needs ≥3 positives and ≥2 collisions naming the sibling that should win. Collisions are authored in **pairs**: the same prompt appears as a `positive` for the owner skill and a `collision` for the impostor.

```json
{
  "version": 1,
  "cases": [
    {
      "id": "commit-pos-1",
      "prompt": "지금까지 한 작업 커밋해줘",
      "expected": "ywc-commit",
      "kind": "positive"
    },
    {
      "id": "commit-vs-createpr-1",
      "prompt": "이 브랜치 PR 올려줘",
      "expected": "ywc-create-pr",
      "kind": "collision",
      "impostor": "ywc-commit",
      "note": "commit must NOT win — create-pr owns PR creation"
    },
    {
      "id": "neg-weather-1",
      "prompt": "오늘 도쿄 날씨 알려줘",
      "expected": null,
      "kind": "negative"
    }
  ]
}
```

## Judge Procedure

For each item the activation judge receives ONLY:
- the item's `description` (Tier-1 metadata),
- the sibling descriptions for the same root (so collisions can be adjudicated),
- the case set.

For each case the judge predicts the single best-matching item from the descriptions alone (this mirrors how Claude's auto-trigger sees skills — description only, no body). Then:

```text
TP = positive cases where predicted == expected
FN = positive cases where predicted != expected
FP = (negative cases where predicted == item)
   + (collision cases where predicted == impostor item)

recall    = TP / (TP + FN)
precision = TP / (TP + FP)        # over cases where the item was predicted or expected
```

A `collision` case counts as a false positive for the impostor **and** (if the owner was not predicted) a false negative for the owner — one authored pair stresses both sides.

## Mapping to the S1 / A2 Band

Take `min(precision, recall)` first — a skill with perfect recall but 0.5 precision is over-firing and must not score above the precision band. Then apply the band table in `skill-rubric.md` (S1) or `agent-rubric.md` (A2). Apply the mechanical collision cap last: if `score.py` flagged an unresolved n-gram overlap pair, S1/A2 is capped at 3 even when the judged precision/recall is higher, because the next sibling description edit can flip the result.

## Why Description-Only

The judge must NOT read SKILL.md bodies. Real activation happens on Tier-1 metadata before any body loads. Judging on the body would measure a capability the runtime never has, and would mask descriptions that read well in full but collide as one-liners. This is the same reason `ywc-skill-author` forbids workflow summaries in the description.

## Determinism Note

`Math.random()`-style nondeterminism is not used; the judge is asked for its single best match, and ties are broken by listing order. Re-running the judge on the same descriptions and cases should yield the same precision/recall within ±1 case. A larger swing means the descriptions are genuinely ambiguous — that is itself an S1 signal, not noise to average away.
