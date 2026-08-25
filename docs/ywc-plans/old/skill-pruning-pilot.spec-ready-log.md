# ywc-spec-ready Loop Log — `skill-pruning-pilot.md`

Spec: `docs/ywc-plans/skill-pruning-pilot.md`
Cap: `--max-iterations 5` · Advisor budget: `--max-advisor-calls 4`

---

## Iteration 1 — validate

**Command**: `ywc-spec-validate --spec docs/ywc-plans/skill-pruning-pilot.md --advisor-budget 2`

**Result**: `DONE_WITH_CONCERNS` — Critical 5, Warning 8, Suggestion 4. Phase 2 advisor calls used: 2 of 2.

### Critical finding signatures

| # | Dimension | Signature |
|---|---|---|
| C1 | Code Compatibility | `score.py:290` — `>= 5` A7 gate is CI-enforced; spec's "zero script impact" claim false |
| C2 | Feasibility | 856 dispatches, no sampling strategy; corpus figure overstated (905 → 821 lines) |
| C3 | Feasibility | Single A/B pair cannot separate signal from LLM sampling noise |
| C4 | Consistency / Code Compat | `role: discipline` value-collides with established `category: discipline` |
| C5 | Completeness | FR-2's two "hard" ordering constraints have no enforcement mechanism |

### Advisor verdicts (2 of 2 used)

- **Methodology** — Decouple deletion from the pilot (labels only ⇒ Critical Surface disappears). Stratified sample n=40 (20 pre-quota core rows, 20 quota-margin rows, ≥20 distinct skills). N=3 runs per variant to establish the noise floor from within-variant disagreement. **240 dispatches**, session ceiling 60. 20-vs-20 Fisher exact detects a ≥35pp inert-rate gap at p<0.05.
- **Taxonomy** — The collision is in the *token*, not the key, so an "orthogonal axes" note cannot fix it. Rename the key to `invocation:` with values `user | orchestrator | callee-only` (zero vocabulary intersection with `category:`). Keep the parent's prose vocabulary (interface / orchestrator / discipline) and add one mapping row to `cross-skill-graph.md`. Ship the validator in the same pass or the token saving never materializes.

### Guards

Iteration 1 — no prior iteration, no stall guard applicable. `1 < 5` (cap not reached). → **Re-plan.**

## Iteration 1 — re-plan

**Command**: `ywc-plan --update-spec docs/ywc-plans/skill-pruning-pilot.md --failure-context "<5 Criticals + 2 advisor verdicts>"`

Appended `## Iteration 1 Amendments` (A–F). Added an `## Operative Sections` pointer and `⚠️ SUPERSEDED` markers to Existing Constraints Touched, Acceptance Criteria, Functional Requirements, and Critical Surfaces.

**Step 4b.5 re-run on the amended whole caught two fresh defects in the amendment itself:**

1. Amendment B's rule-copy table listed **four** copies of the `≥5` rule. A complement grep found a **fifth** — `test_score.py:112, 123-130` unit-tests the gate, so amending `score.py:290` alone breaks the test suite. Table corrected to five, plus two out-of-scope codex/plugins copies recorded to close the enumeration.
2. The two independent corpus measurements **disagreed** (428 rows vs 419 rows) because they classified header/separator rows differently. Resolved by declaring the repo's own CI-gating counter — `_rationalization_data_rows()` at `score.py:379` — the canonical counter, since a count that disagrees with the function deciding the gate is wrong by definition.

Also recorded (B0): **zero skills currently sit below the 5-row floor; the minimum is exactly 5.** There is no slack — the first row deleted from any 5-row skill breaks CI, which makes the rule change a hard precondition for pruning rather than a follow-up to it.

---

## Iteration 2 — validate

**Command**: `ywc-spec-validate --spec docs/ywc-plans/skill-pruning-pilot.md --advisor-budget 0` (advisor budget exhausted at iteration 1)

**Result**: `DONE_WITH_CONCERNS` — **Critical 7** (up from 5). Critical count did **not** decrease.

Closed from iteration 1: the A7 rule-copy enumeration (verified complete — no 6th copy; the codex scorer's `SKILL_ROOT` is `codex/skills`, so it does not gate claude-code) and the ordering-constraint enforcement (parent-audit SHA + candidate-ID resume keys). Stratified sampling was confirmed empirically satisfiable.

The 7 new Criticals split into two classes:

**Class 1 — artifacts of the append-only amendment pattern itself (5).** `Purpose`, `Scope`, `Non-Functional Requirements` and `Edge Cases` still stated the revoked design (DELETE verdicts, `prune:` commits, `role: discipline`) as live instructions; `Edge Cases` was even affirmatively certified "operative as written." `AC3` still demanded "exactly two" dispatches against a six-dispatch method and was never restated despite the header claiming it was. `Amendment E1` asserted in the perfect tense that it had corrected "905 → 821" in three places — grep showed all three untouched.

**Class 2 — genuine method defects (2).**
- **Fisher exact power at n=20/group is 46–53%** for a true 35pp gap in the realistic baseline range (25–45%), computed by exact enumeration — not the "detects at p<0.05" the iteration-1 advisor claimed and this spec adopted verbatim. The design would have failed to justify the rule change roughly half the time *even when a real effect existed*.
- **`_rationalization_data_rows()` (`score.py:379-395`) returns an `int`.** It discards line positions entirely. The sampling frame ("stratify by row ordinal") and the variant builder (`<start>-<end>` line range) are both unconstructible from it, yet the spec claimed the frame was "enumerated by invoking that function."

### Guard

Critical count rose 5 → 7 (one non-decreasing iteration; the stall guard requires two consecutive). The loop could mechanically continue — but **5 of the 7 Criticals were produced by the amendment mechanism itself**, so each further append was expected to generate more. Surfaced to the user.

## Iteration 2 — consolidation (user-directed)

The user chose **consolidate** over a third append. `ywc-plan` Step 4c forbids rewriting because it "loses validated sections" — that rationale had stopped applying: `Scope`, `Purpose`, 3 of 5 NFR rows, `Edge Cases`, and 4 ACs were all stale. This repo has the same precedent: the `sync-skill-count-language-setup` spec hit identical append-only cross-reference decay and was resolved by a consolidation pass.

The user also chose **sample ×2 + pooled noise floor** for the two method defects.

**Consolidated spec** (231 lines) folds every amendment into the body; no `Iteration N Amendments` section remains. Changes beyond a mechanical merge:

- **Sample doubled to n=40 per stratum (80 candidates).** Power recomputed by exact Fisher enumeration: **85.8–93.5%** across baselines 0.10–0.50, all ≥80%. Verified independently, not adopted from the advisor.
- **Noise floor pooled globally** — 6 within-variant comparisons × 80 candidates = 480 pooled comparisons, one floor for all candidates. Per-candidate estimation from 3 pairs was unsound (a 0/3 observation admits a 95% CI of roughly [0%, 71%]).
- **New deliverable `enumerate-rd-rows.sh`** — emits per-row `<start>-<end>` line ranges and self-checks count parity against the canonical counter across all 46 skills. This closes the gap the spec had previously asserted away.
- **480 dispatches**, ceiling 60/session, append-only and resumable.
- Retitled: the spec labels; it deletes nothing. `Critical Surfaces` moved from the (now nonexistent) deletion path to `.claude/skills/ywc-toolkit-eval/**`, whose CI gate governs every skill in the bundle.

Mechanical self-check on the consolidated text: `905` 0 hits, `428` 0 hits, `DELETE`/`KEEP` verdict language 0 hits, `prune:` 0 hits, `SUPERSEDED` 0 hits. The 4 surviving `role:` / `ywc-skill-prune` mentions are all in negation or rationale context (why the key is *not* `role:`, why a separate skill is *not* created).

## Iteration 3 — validate

**Command**: `ywc-spec-validate --spec docs/ywc-plans/skill-pruning-pilot.md --advisor-budget 0`

**Result**: `DONE_WITH_CONCERNS` — **all 9 prior Criticals CLOSED**, 1 new Critical.

Independently reverified: Fisher power **85.83–93.47%** at n=40/group (matches the spec's claim at both bounds); canonical counter **419 rows, min 5 / max 21 / mean 9.11**; stratum pools **184 / 235**, 40-draw feasible. The `category: discipline` skill list is exactly the five named. No 6th copy of the A7 rule exists.

**New Critical — the description extractor is broken for 16 of 46 skills.** `validate-skill.sh:31-35`'s awk has no frontmatter `---` boundary; its only stop condition is a body line matching `^[A-Za-z_]+:`. For the 16 skills whose `description:` is the **last** frontmatter key, it swallows the entire body: `ywc-parallel-executor` → **8,467 "words"** (actual 73), `ywc-plan` → 6,023 (actual 108), `ywc-impl-review` → 3,513 (actual 94). Invisible today because A2/A3 are boolean substring checks a longer capture cannot break — but AC12's exact word count would have hard-failed all 16 regardless of their real description length, and AC14's baseline comparison was meaningless.

## Iteration 3 — re-plan (surgical, on the consolidated body)

- **FR-5a** (new): repair the extractor in place, bounded by the closing `---`. Fixing the shared extractor also removes A2/A3's latent fragility; a second parser would eventually diverge from them.
- **AC12a** (new): regression gate — `ywc-parallel-executor` must measure **73**, not 8,467. It explicitly gates AC12 and AC14.
- **AC14**: the word-count baseline is **no longer a literal in the spec**. Three attempts to state it produced 4,187 / 4,154 / 4,162, each using a different boundary rule. A count without a canonical extractor is an opinion. The baseline is now defined as *the repaired extractor's output, recorded before any rewrite* — the same fix the row count received when `score.py`'s counter was made canonical.
- **AC5**: the rate→count conversion is now stated (`floor_rate` → `T = floor(floor_rate × 9)`), not left to the reader.
- **AC5a** (new, self-found): the pooled floor had **no validity ceiling**. `T` degrades safely downward (`floor_rate < 0.111` ⇒ `T = 0` ⇒ unanimity required), but not upward: at `floor_rate = 0.5`, `T = 4` would label a row `inert` while 4 of its 9 cross comparisons disagreed. Above a **0.25** pooled rate the run is now `INCONCLUSIVE` — the harness, not the corpus, is what got measured; nothing is labelled and the evidence gate cannot pass.
- Also: FR-1 step 2 writes the drawn candidate list before dispatch (a resumed run must not re-draw); the `validate.sh:579-590/691-694` citation was corrected (both blocks concern the *codex* scorer — `scripts/validate.sh` never references `.claude/skills/ywc-toolkit-eval` at all); FR-5 carries an explicit note that it exceeds what the parent licenses and is severable.

Spec now 262 lines, 18 ACs, 8 FRs.

## Iteration 4 — validate

**Command**: `ywc-spec-validate --spec docs/ywc-plans/skill-pruning-pilot.md --advisor-budget 0`

**Result**: `DONE_WITH_CONCERNS` — **3 Critical + 1 High**, all of them downstream of Iteration 3's own patch.

Everything else re-verified clean: 30+ `file:line` citations, all 20 call-graph reference counts, the corpus statistics, the `category: discipline` set, the Fisher power table, and every parent-spec quotation. AC/FR traceability confirmed — no orphan FR; the three ACs without a single FR owner are explicitly-labelled global invariants.

**Critical — the FR-5a fix was under-specified, and the verification that "confirmed" it was measuring the wrong thing.** FR-5a said to bound the extractor at the closing `---` while keeping the `^[A-Za-z_]+:` next-key regex. That regex does not match a hyphen, so `ywc-handle-pr-reviews/SKILL.md:5`'s `allowed-tools:` is still swallowed. The reviewer implemented FR-5a *as written* and it broke on 1/46. The earlier "46/46 agreement" check had silently broadened the regex in its own implementation — **it verified the intent, not the spec.** Both parts of the repair are now stated explicitly.

**Critical — the reference parser was undefined.** AC12a said "an independent YAML-frontmatter parse." Strict YAML (`yaml.safe_load`) **fails outright on 8 of 46** skills, whose unquoted `description:` values contain a mid-line `Triggers: ` (colon-space in a plain scalar is invalid YAML). The reference is now named as `score.py::split_frontmatter()` → `parse_yaml_lite()`, **both, in that order** — and the spec now warns that calling `parse_yaml_lite` on a whole file reproduces the very bug it exists to fix. That mistake was made during this iteration's own verification, one step after the same class of error was written into the spec as a lesson.

**Critical — `T = floor(floor_rate × 9)` sat at the null distribution's *mean*, not its tail.** Under the null (the row is truly inert), cross-variant disagreement ~ `Binomial(9, floor_rate)`. The mean-based threshold mislabels **37–61 % of truly inert rows as `load-bearing`** across the entire plausible noise range — the design was erasing the very signal the pilot exists to detect. Replaced with an upper-tail quantile (`smallest t with P(X ≤ t) ≥ 0.95`), which holds that error at **0.8–4.9 %**.

**High — the word count was locale-dependent.** `wc -w` disagrees with itself across locales on 30 of 46 CJK-heavy descriptions; AC12a's cited fixtures (73/108/94) were the locale-dependent values. Canonical, locale-independent: **72/106/92**, baseline **4,154**. Counting is now pinned (awk/Python split, or `LC_ALL=C`).

## Iteration 4 — re-plan (surgical)

AC5 now derives `T` from the tail quantile with the error table inline. AC5a's ceiling rationale rewritten (0.25 is where the tail bound's error budget runs out). AC12a names the reference parser as a *function composition* and pins the counting method. FR-5a states both halves of the repair. AC2 gained a mechanical verification command; AC14 is explicitly labelled a measurement obligation with no failure mode; FR-5's severability note now says the dependency runs one way (FR-5 needs FR-3, never the reverse).

Also corrected: the "16 of 46 last-key skills" figure was itself produced by a hyphen-blind regex — **it is 15**. Every affected number re-measured under the pinned method (8,465 / 6,019 / 3,510 broken; 72 / 106 / 92 canonical) and re-verified 46/46 against the reference parser.

Spec now 288 lines, 18 ACs, 8 FRs.

## Iteration 5 — validate (iteration cap)

**Command**: `ywc-spec-validate --spec docs/ywc-plans/skill-pruning-pilot.md --advisor-budget 0`

**Result**: **`DONE` — Critical 0**, Warning 2 (Medium), Suggestion 1 (Low).

All four of Iteration 4's findings **CLOSED, verified by execution** — the reviewer implemented FR-5a's extractor exactly as specified (no silent hardening), ran it against all 46 real skill files, and got **46/46 agreement** with the named reference parser, including all four fixtures (72 / 106 / 92 / 112) and the 4,154 baseline. The tail-bound table, the naive formula's 37–61 % mislabel range, the Fisher power band, the row counter, the stratum pools, all 20 call-graph counts, and every `file:line` citation were independently recomputed and matched.

The two Mediums it surfaced were both fixed before closing:

1. **AC5a's ceiling rationale was mathematically wrong.** It claimed 0.25 is where "the tail bound's own error budget runs out." It never runs out — `P(X > T) ≤ 5 %` holds at every rate by construction. What collapses past 0.25 is **separability** (Type II), not the Type I budget. This was the *same* mean-vs-tail conflation Iteration 4 fixed, recurring inside the correction's own justification.
2. **The bound is one-sided, on the cheap side, and the spec never said so.** `T` controls `P(load-bearing | truly inert)` — the harmless error. It cannot bound `P(inert | truly load-bearing)` — the dangerous one — because that needs an alternative distribution the design never defines. So the threshold that maximizes the aggregate test's power is *not* the one that maximizes safety. The spec now states this plainly and pins the consequence: **an `inert` label is evidence for the stratum contrast, never authority to delete a row.**

## Completion Report

| | |
|---|---|
| Spec | `docs/ywc-plans/skill-pruning-pilot.md` (294 lines, 18 ACs, 8 FRs) |
| Iterations | 5 of 5 (cap reached exactly; never raised) |
| Advisor calls | 2 of 4 |
| Final status | **DONE** — 0 Critical |
| Criticals found and closed across the loop | **17** |

### What the loop was actually for

Every iteration found real defects, and the same failure recurred **seven times**: a confident claim adopted without a complement check — my own memory (the A7 rule "exists only in prose"), an Opus advisor's statistics (n=20 "detects" a 35pp gap; actual power 46–53 %), a function's contract inferred from its name (`_rationalization_data_rows` returns an `int`; `parse_yaml_lite` takes only the frontmatter block), a number counted with an unstated boundary rule (419 vs 428 rows; 4,187 vs 4,154 vs 4,162 words; 15 vs 16 last-key skills), and — twice — a verification that confirmed the *intent* rather than the *specification*.

The durable fix each time was the same, and it is the one lesson worth carrying out of this spec: **a number without a canonical extractor is an opinion.** Name the tool, then the number is whatever it outputs. `score.py::_rationalization_data_rows` became canonical for row counts; `split_frontmatter` → `parse_yaml_lite` became canonical for description words. Both disputes evaporated on contact with a named tool.

## Handoff

```text
✅ Spec ready: docs/ywc-plans/skill-pruning-pilot.md (DONE after 5/5 iterations, 2 advisor calls)
Next:
  1. /ywc-task-generator docs/ywc-plans/skill-pruning-pilot.md
  2. (after tasks generated) /ywc-sequential-executor or /ywc-parallel-executor
```

**Blocking prerequisite**: the parent spec `docs/ywc-plans/skill-engineering-hardening.md` has **zero lines landed** — no `audit-skills.sh`, no `--audit` mode, no deletion-test rubric, no role model in `cross-skill-graph.md`. This spec's Dependencies section names it and AC8 gates on it mechanically (the run refuses to start without the parent-audit git SHA). Decompose the parent first.
