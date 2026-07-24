# Trigger Evaluation Method (S1 / A2)

Activation accuracy is the highest-weighted axis because it is a property of the **whole catalog**, not a single file. This document defines how `evals/trigger-cases.json` is built and how the activation judge turns it into precision and recall.

## Case Taxonomy

`evals/trigger-cases.json` holds three kinds of case, each a natural-language prompt a user would actually type:

| Kind | Meaning | Scoring role |
|---|---|---|
| `positive` | This item SHOULD activate | drives **recall** |
| `negative` | NO item should activate (or a non-sibling should) | drives **precision** |
| `collision` | A *sibling* should win, not this item | the hard cases — drives precision against the nearest neighbor |

Every item under evaluation needs ≥3 **independently-sourced** positives and ≥2 independently-sourced collisions naming the sibling that should win. Collisions are authored in **pairs**: the same prompt appears as a `positive` for the owner skill and a `collision` for the impostor.

**Authoring rules per kind:**

- **`collision` must name a genuinely competing sibling.** The strongest evidence is the item's own `Do not use for ...` anti-trigger — that clause is the author's own declaration of where the boundary is contested. A prompt whose ownership is obvious to any reader is not a collision; it is just a positive for the owner. If an item genuinely has no competitor, the eval owner approves a documented exception — **never substitute a `negative` for a missing `collision`**, because the two measure different failure modes.
- **Collision siblings must share a root.** The judge receives only the sibling descriptions for the same root (see Judge Procedure), so a skill↔agent collision cannot be adjudicated. Pick the competitor from the same root as the item.
- **`negative` must be in-domain.** An off-domain prompt (weather, recipes, trivia) is trivially rejected by every description and therefore measures nothing — it inflates precision without ever testing it. Write negatives that sit *inside* the development domain but that no `ywc-*` item should claim: a plain explanation request, a one-character edit, a tool lookup, a concept question, an error-message interpretation. Use `note` to record which item is most likely to over-trigger on it.

**Every case also carries a `source`** — see [Prompt Provenance and the Independence Condition](#prompt-provenance-and-the-independence-condition). It records where the *prompt* came from and decides whether the case counts toward the coverage floor.

```json
{
  "version": 1,
  "cases": [
    {
      "id": "commit-pos-1",
      "prompt": "지금까지 한 작업 커밋해줘",
      "expected": "ywc-commit",
      "kind": "positive",
      "source": "description-derived"
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
      "kind": "negative",
      "source": "description-derived"
    }
  ]
}
```

## Prompt Provenance and the Independence Condition

A case written by reading the item's own `description` is then judged by a judge that reads **that same description**. The case cannot fail — it measures the description against itself. This is not a hypothetical: the 2026-07-22 full sweep scored S1/A2 = 5 for all 60 items with three judge runs disagreeing on 0 of 353 cases. The heaviest axis in the rubric could not fail.

So each case declares where its **prompt** came from:

| `source` | Meaning | Counts toward the floor? |
|---|---|---|
| `description-derived` | authored by reading the item's own description | **no** |
| `session-trace` | verbatim user message recovered from a session transcript | yes |
| `user-prompt` | a prompt a user actually sent, captured outside a transcript | yes |

`load_coverage()` counts only independent sources toward `positives` / `collisions`, and reports every case in `positives_total` / `collisions_total`, so the gap between "cases we have" and "cases that can fail" stays visible:

```json
{ "positives": 4, "collisions": 2, "positives_total": 7,
  "collisions_total": 5, "sufficient": true }
```

**A missing `source` is read as `description-derived`.** Silence is not a claim of independence; defaulting the other way would let every legacy case keep propping up the floor it was added to test. An unrecognised value raises rather than defaulting, so a typo can neither quietly demote nor quietly promote a case.

**Provenance is about the prompt, not the label.** Deciding which sibling *should* win a mined prompt is authoring work and does not re-introduce the circularity — a `collision` is independently sourced as long as its prompt is. This matters, because the alternative reading (collisions are inherently description-derived, since the boundary comes from the anti-trigger clause) would make the floor permanently unreachable, which is exactly as useless as a floor that can never fail.

**Sanitize, do not paraphrase.** Mined prompts have internal hostnames, absolute paths and credentials removed. Typos, mixed-language phrasing and terse fragments stay — that is how prompts actually arrive, and smoothing them turns a real case back into an authored one.

**Do not mine prompts that name the item.** "ywc-create-pr skill 로 pr 을 작성해줘" is a real prompt, but the item's own name in the text makes it trivially winnable — a second way to build a case that cannot fail. Prefer prompts that describe the intent.

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

## Mechanical Coverage Signal & the Floor

The `≥3 positives / ≥2 collisions` rule above is **not just prose** — `scripts/score.py` measures it, so a hollow, under-floor S1/A2 can never pass silently as if it had been measured. Two module-level constants encode the floor:

- `COVERAGE_MIN_POSITIVES = 3` — minimum `positive` cases whose `expected` is the item.
- `COVERAGE_MIN_COLLISIONS = 2` — minimum `collision` cases naming the item.

A `collision` case credits **both** its `expected` owner and its `impostor` — one authored case raises the collision count of two items at once. `sufficient` is `positives >= COVERAGE_MIN_POSITIVES and collisions >= COVERAGE_MIN_COLLISIONS`, computed over independently-sourced cases only (see Prompt Provenance above). Duplicate case ids are counted once.

**`score.py` does not compute S1/A2 itself.** Coverage is a `signals`-only measurement; `axes.S1` / `axes.A2` stay `null` in the mechanical output, and the judgment-tier activation judge produces the actual score.

**Judge obligation.** When `sufficient` is `false`, the activation judge MUST return S1 (skill) or A2 (agent) as `"unmeasured"` with a one-line reason. It must **not** fabricate a precision/recall, and must **not** carry forward a prior run's number. An unmeasured item enters the prioritized backlog regardless of its total, because its heaviest axis is unmeasurable until the fixture is backfilled. Coverage is orthogonal to the collision cap above: an item can meet the floor and still be capped at 3 by an unresolved n-gram overlap.

Every run prints a catalog-level summary to stderr (`[coverage] N items below minimum (of M; ...)`), keeping stdout JSON-clean.

## Retired Items

A skill or agent may be retired, but **its cases stay**. Do not delete the fixture entries — mark them:

```json
{ "id": "oldskill-pos-1", "prompt": "...", "expected": "ywc-old-skill",
  "kind": "positive", "retired": true }
```

Retired cases are regression evidence: when a later model update makes the retired capability silently worse, these are the only cases that would have caught it. They do not contribute to any live item's coverage (the retired item is no longer in the catalog) and must not be treated as orphaned fixtures. This mirrors the Codex-side policy that fixtures survive retirement — see `docs/ywc-plans/codex-skill-eval-upgrade.md`.

### How an item reaches retirement

Retirement is irreversible in practice — once a skill is gone, the prompts that used to reach it fall through to whatever else claims them. So the path is deliberately narrow, and `scripts/ablation.py` enforces each step rather than leaving it to judgment.

1. **Run the ablation.** `python3 scripts/ablation.py --case <id> --suite expensive --adapter claude --loaded-skill-count <n>`. The `--suite expensive` opt-in exists because this dispatches for real money: 6 trials × 2 arms × ~$0.54 ≈ **$6.50 per case**. Select a small, deliberate set of cases.
2. **Read the verdict, not the pass counts.** `classify()` returns `CANDIDATE_FOR_REVIEW` only when all 6 pairs were valid, the cost is recorded, the loaded-skill count is recorded, and the without-arm failed at most **one** time more than the with-arm. Anything short of that is `INCONCLUSIVE` — which is not a weak yes, but "this experiment did not answer the question".
3. **A human approves, by name.** `retire(suite, approved_by=...)` raises `ApprovalRequired` without a named approver, and raises it again when the verdict is anything other than `CANDIDATE_FOR_REVIEW`. Approval is necessary and not sufficient: nobody can approve a conclusion the evidence never reached.
4. **Mark the fixture, never delete it** — `retired: true`, per the policy above.

**What the verdict claims, and what it does not.** Route N1 loads the entire installed catalog in both arms, so a sibling skill may have contributed to the with-arm result. Every report prints the loaded-skill count for exactly that reason, and the claim is limited to the *difference between the two arms* — never "this skill alone produced the outcome". A run that cannot state how many skills were loaded is `INCONCLUSIVE` by construction.

Ablation never runs in CI: it costs real money and needs the developer's subscription session, which CI does not have.

## Why Description-Only

The judge must NOT read SKILL.md bodies. Real activation happens on Tier-1 metadata before any body loads. Judging on the body would measure a capability the runtime never has, and would mask descriptions that read well in full but collide as one-liners. This is the same reason `ywc-skill-author` forbids workflow summaries in the description.

## Determinism Note

No nondeterministic sampling is used; the judge returns its single best match, and ties are broken by listing order. Re-running the judge on the same descriptions and cases should yield the same precision/recall within ±1 case. A larger swing means the descriptions are genuinely ambiguous — that is itself an S1 signal, not noise to average away.
