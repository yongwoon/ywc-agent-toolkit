# Skill Quota-Evidence Pilot and Invocation-Tier Enforcement

> **This spec produces evidence and labels. It deletes nothing.** Actual pruning is a separate, human-reviewed change downstream of this one.

> Status: Draft (consolidated after Iteration 2)
> Scale: Medium
> Created: 2026-07-13
> Author: ywc-plan (agent)
> Parent spec: `docs/ywc-plans/skill-engineering-hardening.md` — **read it first.** This spec is the follow-up change that parent's FR-6 and Out-of-Scope defer ("the pruning pilot is a subsequent change after evidence is reviewed").
> Spec Reference: `develop-with-llm/docs/studies/insights/MATT_POCOCK_SKILL_HELL_ENGINEERING.md` — principles 1 (Trigger) and 4 (Pruning)
> Loop history: `docs/ywc-plans/skill-pruning-pilot.spec-ready-log.md`. Iterations 1–2 of `ywc-spec-ready` found 12 Criticals across two passes; 5 of them were artifacts of an append-only amendment pattern, so this document was **consolidated** — the amendments are folded into the body and no `Iteration N Amendments` section remains. Every number below is measured or computed, never asserted.
>
> **Post-validation amendment (task decomposition, 2026-07-13).** Decomposing this spec into tasks surfaced a Critical the five `ywc-spec-validate` passes missed: **FR-5's `invocation:` tier contradicted `score.py:288`'s `A4_multilingual` check**, which every one of the 46 skills currently passes and which the Existing Constraints table never listed. A `callee-only` description stripped of non-ASCII triggers would have dropped its `S2` score and failed `score.py --ci` — violating AC13, this spec's own global invariant. Measurement of the fix showed the tier was buying only 5–10 pp over a flat cap anyway. **FR-5 is now a flat ≤80-word cap; the tier is deferred to its own spec.** FR-5a (extractor repair) survives unchanged — a cap cannot be enforced on a broken extractor. The lesson is recorded rather than smoothed over: five adversarial validation passes read `score.py:290` (A7) closely and never looked two lines up.

## Purpose

The parent spec builds the *capability* to audit and deletion-test skills, and deliberately stops short of using it: its audit is report-only, its findings advisory, and it nominates a pruning pilot without executing one. This spec executes the evidence half of that pilot and converts the result into enforceable rules.

The target is rule **A7** (`claude-code/skills/ywc-skill-author/SKILL.md:54`), which mandates **at least 5** Excuse/Reality rows in every skill's `## Rationalization Defense` table. A quota manufactures padding whenever a skill's real failure-mode count falls below it — Pocock's "no-op sediment." Whether that has actually happened is an empirical question, and the only honest way to answer it is a Deletion Test.

Measured corpus, using the **canonical counter** `_rationalization_data_rows()` (`score.py:379`) — canonical because it is the function that decides the CI gate, so a count that disagrees with it is wrong by definition: **46 skills, 419 data rows**, min 5, max 21, mean 9.11. **Zero skills sit below the floor and the minimum is exactly 5** — there is no slack anywhere, which is why the rule change is a *precondition* for any future pruning, not a follow-up to it. (Section *line* counts are deliberately not quoted here: independent measurements disagreed by exactly one line per skill depending on whether the heading is counted, and no AC or script depends on the figure.)

The second half of the spec attacks Pocock's Trigger principle. Every skill carries full multilingual fuzzy-match triggers in its `description` — resident context on every turn. The measured corpus is **4,154 words ≈ 5,900 tokens** across 46 descriptions, mean **90.3 words**, and **29 of 46 exceed 80 words** while **zero fall below 30**. (The exact figure is still not a literal an implementer may trust: see AC14, and AC12a for why the tool that would measure it was broken.)

**An earlier draft of this spec proposed an `invocation:` tier (`user` / `orchestrator` / `callee-only`) with a per-tier budget. That has been cut, and the reason is this spec's own thesis turned on itself.** Measurement during task decomposition showed:

1. **A flat 80-word cap alone captures 17 % (709 words).** The tier's *additional* contribution is only **5–10 pp**, because it depends entirely on the `callee-only` set being large.
2. **That set is almost certainly small.** FR-5's own — correct — rule was "default to `user` when uncertain," and the skills it nominated as `callee-only` candidates (`ywc-impl-review`, `ywc-spec-validate`, `ywc-verify-done`, `ywc-security-audit`) are all things a human plausibly types. Applied honestly, the rule yields perhaps 4–8 skills, i.e. the 5 pp end of that range.
3. **It contradicted a check the spec never noticed.** `score.py:288` scores `"A4_multilingual": bool(HANGUL.search(desc) and JAPANESE.search(desc))` — currently **46/46 pass** — while AC12 required a `callee-only` description to contain **no non-ASCII trigger strings**. Trimming one skill to `callee-only` would flip A4, drop its `S2` from 5 to 4 (`round(9/10*5)` = 4), and fail `score.py --ci` as a regression — violating AC13, this spec's own global invariant. A4 was absent from the Existing Constraints table entirely.

Shipping a tier system across 46 files, plus an amendment to the **Critical Surface**, to buy 5 pp — with no evidence that the `callee-only` set is non-trivial — is precisely the move this spec exists to argue against. **A4 is the same defect as A7: a blanket quota that ignores the skill's invocation contract.** Both deserve evidence before enforcement, and neither gets it here. The tier is deferred to its own spec (see Out of Scope), which must gather that evidence first.

What remains is the part that pays for itself: **a flat ≤80-word cap on every description** (FR-5).

## Scope

- **Extend `ywc-skill-author`'s audit mode** (parent FR-1) with a decidable Deletion Test: the parent specifies the protocol shape but leaves "compare" without a decision rule.
- **Two new bundled scripts**: a row-range enumerator and a variant builder.
- **Run the pilot** on a stratified sample of the Rationalization Defense corpus; publish an evidence report with per-row **labels** (`inert` / `load-bearing` / `indeterminate`).
- **Conditionally amend the A7 quota** — all five copies of the rule, plus the eval baseline — if and only if the evidence supports it.
- **Add a flat ≤80-word `description` cap**, enforced by `validate-skill.sh` on the repaired extractor. 29 of 46 descriptions are rewritten to fit.
- **Unify `validate-skill.sh`'s A2/A3 checks with `score.py`'s**, which are strictly stricter and are the ones that gate CI.
- **Fix the one A8 violation** (`ywc-parallel-executor`, 502 lines against its own 500 cap).
- **Sync `ywc-skill-author`'s README locale set** with the rules it documents.

Files in scope: `claude-code/skills/**`, `.claude/skills/ywc-toolkit-eval/**` (the eval scorer that mechanically enforces A7), and `docs/ywc-plans/`.

## Out of Scope

Each item is an **explicit deferral**, with its reason. None is a silent narrowing.

- **Deleting anything.** The pilot labels; it does not edit, excise, or commit. This is the single most important boundary in the spec: it removes the irreversible surface entirely, so a wrong label costs a re-run rather than a silently-removed guardrail. Pruning consumes this spec's report in a separate, human-reviewed change.
- **`codex/skills/**` and `plugins/ywc-agent-toolkit/skills/**`.** The parent covers both bundles; this follow-up covers claude-code only, by scope decision recorded here. `plugins/` is generated exclusively from `codex/skills/` (`scripts/sync-codex-plugin.sh:5`, `SOURCE_DIR="$ROOT_DIR/codex/skills"`), so a claude-code-only change provably cannot desync its parity checks. The two out-of-scope prose copies of the A7 rule live at `codex/skills/ywc-skill-author/SKILL.md:58` and `plugins/ywc-agent-toolkit/skills/ywc-skill-author/SKILL.md:58`.
- **Creating a separate `ywc-skill-prune` / `ywc-skill-audit` skill.** Forbidden by parent Out-of-Scope (`:39-40`) and parent Risks ("do not add a second meta-skill"): a second meta-skill worsens activation ambiguity among 46 fuzzy-matching siblings. The counter-argument — an agent inside an authoring body that says "you MUST include X" is biased against deleting X — is real, and is answered by FR-1's blind dispatch instead: **the judging subagents never see the authoring rules, and are never told which variant they hold.**
- **The `invocation:` tier (`user` / `orchestrator` / `callee-only`) and its per-tier budget.** Deferred to its own spec, not decided against. Three reasons, all measured (see Purpose): the flat cap already captures 17 % and the tier adds only 5–10 pp; that increment depends on a `callee-only` set which the tier's own "default to `user` when uncertain" rule keeps small (4–8 skills ⇒ the 5 pp end); and it collides with `score.py:288`'s `A4_multilingual`, forcing an amendment to the **Critical Surface** and a `history.mechanical.json` regeneration. **The successor spec's first job is to count how many skills a human genuinely never invokes** — the same evidence-before-enforcement discipline this spec applies to A7. If that count is large, the tier is worth its permanent cost; if it is 4, it is not.

  *For the successor: the A4 amendment should be **score-neutral** — `"A4_multilingual": inv == "callee-only" or bool(HANGUL.search(desc) and JAPANESE.search(desc))` keeps the denominator at 10, leaves all 46 current scores unmoved, and needs no baseline regeneration. That is the minimum-blast-radius edit to a critical surface.*

- **`ywc-agentic` trigger narrowing** — owned by parent FR-5.
- **Pocock principle 3 (Hiding the Future)** — `ywc-plan`'s Step 5 handoff and `ywc-agentic`'s fully-exposed pipeline reveal downstream intent and invite shortcut heuristics. A behavior change to shipping skills, not a prose prune; belongs with the parent's `ywc-agentic` work or a third spec.
- **Retrofitting `evals/evals.json` to the 38 skills lacking one.** FR-1 synthesizes a scenario when no eval exists, so this is not a prerequisite.

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | This spec's interaction |
|---|---|---|
| `skill-engineering-hardening.md:39-40` (parent Out of Scope) | Forbids a separate audit skill — it "duplicates the existing `ywc-skill-author` audit trigger and would worsen activation ambiguity" | **Comply.** All work lands in `ywc-skill-author`. No new skill directory. |
| `skill-engineering-hardening.md:41-42` | "the pruning pilot is a subsequent change after evidence is reviewed" | **This spec is that subsequent change** — and it stops at evidence, per Out of Scope. |
| `skill-engineering-hardening.md:45-47` | Mechanical output stays **advisory** "until representative evaluations demonstrate a stable signal" | **Extend, on the parent's own condition.** FR-3 produces those evaluations. FR-4/FR-5's hard-fail enforcement ships **only if** the evidence gate (FR-3) passes; otherwise they ship advisory and no script changes. |
| `skill-engineering-hardening.md:99-108` (parent FR-2) | Protocol: baseline prompts → one bounded removal → rerun → compare → retain/revert/escalate. **"Do not ask a test agent to validate against a leaked expected answer."** | **Comply and complete.** FR-1 supplies the missing decision rule. The judge never sees `expected_output` — which is fortunate, since that field is prose, not an assert (last row of this table). |
| `skill-engineering-hardening.md:121-131` (parent FR-4) | Role model is prose — interface / orchestrator / discipline — documented in `cross-skill-graph.md` | **Untouched.** With the tier deferred, this spec adds no machine-checkable counterpart and no mapping row. The parent's prose model stands alone; the successor spec is what would have to reconcile with it. |
| `skill-engineering-hardening.md:140-145` (parent FR-6) | Nominates a pilot among the near-500-line skills, and requires the pilot choice to **cite findings** from the report-only audit | **Extend.** Parent's axis is *one oversized skill*; this spec's corpus is a *cross-cutting section across all 46*. Complementary. FR-6 handles `ywc-parallel-executor`, which is on the parent's list. The report must still cite the parent's audit — see FR-3's SHA requirement. |
| `skill-engineering-hardening.md:152` (parent NFR Portability) | "Scripts use portable Bash with `set -euo pipefail`" | **Comply** for the two new scripts. `validate-skill.sh:9` uses `set -uo pipefail` (no `-e`) **deliberately** — its `fail()` accumulator must survive a failing `grep -q`. That deviation is pre-existing and stays. |
| `skill-engineering-hardening.md:178-179` (parent Edge Cases) | "A proposed deletion changes an output's safety gate or required artifact: **retain** the instruction and record the failed deletion test." | **Comply.** Inherited as the `load-bearing` label and the uncertainty default (AC5). |
| **`.claude/skills/ywc-toolkit-eval/scripts/score.py:290`** | `"A7_rationalization": _rationalization_data_rows(body) >= 5` — **mechanically enforces the quota.** `.github/workflows/validate.yml:37` runs `score.py --ci`, which diffs every axis against the committed baseline `evals/history.mechanical.json` and **fails the build on any score drop** | **Override** (FR-4), conditionally. This is the copy that actually bites: a row deleted below 5 flips the check to `False`, drops the skill's `s2` score, and fails CI as a regression. |
| **`.claude/skills/ywc-toolkit-eval/scripts/test_score.py:112, 123-130`** | Unit tests asserting the gate (`assertFalse(rows >= 5)` at 4 rows, `assertTrue` at 5) | **Override** (FR-4). Amending `score.py:290` alone breaks the suite. |
| `.claude/skills/ywc-toolkit-eval/scripts/score.py:379-395` (`_rationalization_data_rows`) | Returns an **`int` count only.** It filters `section.splitlines()` and takes length differences; it never retains line numbers and discards row content. There is no companion enumerator anywhere in the repo | **Extend** (FR-2). Stratifying by row ordinal and feeding a line range to the variant builder both require `[(start,end), …]`, which does not exist. FR-2 builds it and asserts count parity against this function. |
| **`.claude/skills/ywc-toolkit-eval/scripts/score.py:288`** | `"A4_multilingual": bool(HANGUL.search(desc) and JAPANESE.search(desc))` — one of the ten `S2` structure checks. **46/46 currently pass.** It is a *presence* test, not a length test: two Hangul characters and two Japanese characters satisfy it | **Comply — and this is why the `invocation:` tier was cut.** A `callee-only` description stripped of non-ASCII triggers flips A4, drops `S2` from `round(10/10*5)`=5 to `round(9/10*5)`=4, and `score.py --ci` fails it as a regression against `history.mechanical.json` — breaking AC13. The earlier draft never saw this row. FR-5's flat cap leaves A4 untouched, so no skill's `S2` moves. |
| **`score.py:286-287` vs `validate-skill.sh:37-42`** | The two validators **disagree on A2/A3.** `score.py`: `desc.startswith("(ywc) Use when")` and `re.search(r"Do not use (?:for\|during\|when\|in)\b", desc)`. `validate-skill.sh`: substring `"(ywc) Use "` and `"Do not use "` **or `"Do not invoke "`**. The local gate is strictly looser — a description opening `(ywc) Use before …` or anti-triggering with `Do not invoke …` passes locally and **fails CI**. Latent today (46/46 pass both) | **Fix** (FR-5). FR-5 rewrites 29 descriptions; a rewrite that lands on the looser gate's blind spot would pass every local check and break the build. Tighten `validate-skill.sh` to match `score.py` exactly. `score.py` is canonical and is **not** edited — the local validator moves. |
| `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md:42` | `` `## Rationalization Defense` with ≥5 data rows `` — third copy of the rule | **Override** (FR-4). |
| `claude-code/skills/CLAUDE.md:84-85` | "…`## Rationalization Defense` table with ≥5 domain-specific Excuse / Reality pairs" — second copy | **Override** (FR-4). |
| `claude-code/skills/ywc-skill-author/SKILL.md:54` (rule A7) | "at least 5 domain-specific Excuse / Reality pairs" — the canonical prose copy | **Override** (FR-4). The quota goes; the section stays mandatory. |
| `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh:46` | Checks only that the section is **present** (`grep -q`) — never counts rows | **Comply.** This is why the quota's real teeth are in `score.py`, not here, and why the original single-copy claim was wrong. |
| **`claude-code/skills/ywc-skill-author/scripts/validate-skill.sh:31-35`** | `awk` extractor for the `description` value. **It is broken twice over.** (1) It has **no frontmatter `---` boundary** — its only stop condition is a body line matching `^[A-Za-z_]+:` — so for the **15 of 46 skills whose `description:` is the last frontmatter key** it swallows the entire body: `ywc-parallel-executor` yields **8,465 "words"** against an actual **72**; `ywc-plan` 6,019 against 106; `ywc-impl-review` 3,510 against 92. (2) That same regex **does not match a hyphen**, so `ywc-handle-pr-reviews/SKILL.md:5`'s `allowed-tools:` key is swallowed into the value. The bug is invisible today because A2/A3 are boolean substring checks (`contains "(ywc) Use "`) that a longer capture cannot break | **Fix, then reuse** (FR-5a). A precise word count cannot be built on it: AC12 would hard-fail those skills regardless of their real description length. Fixing the extractor in place is strictly better than adding a second parser — it repairs A2/A3's latent fragility at the same time. |
| `claude-code/skills/ywc-skill-author/scripts/validate-skill.sh:60-69` | Every `references/*.md` needs a pointer from a skill `.md` and must be **≥30 lines** | **Comply.** FR-1's rubric reference must clear 30 lines and be pointed to. |
| `claude-code/skills/ywc-skill-author/SKILL.md:93` | Workflow / **Rationalization Defense** / Validation Checklist are **Tier 2 by definition — never extract to Tier 3** | **Comply.** This is why the corpus is worth *pruning* rather than *extracting*: it is pinned to activation-time context by rule, so deletion is its only cost reduction. FR-6 must therefore extract a static table, never workflow prose or an RD table. |
| `claude-code/skills/*/SKILL.md` frontmatter | **`category:` already exists** on 27–30 of 46 skills, sanctioned by rule A5, and **`category: discipline` is already in production** on `ywc-brainstorm`, `ywc-confidence-gate`, `ywc-debug-rootcause`, `ywc-tdd-ritual`, `ywc-verify-done` — where it means a *genre*. No `role:` key exists anywhere | **Untouched.** With the tier cut, this spec adds **no frontmatter key at all**. Recorded for the successor spec: any new key must avoid the token `discipline`, because the collision lives in the *token*, not the key — an author or LLM reading `category: discipline` will infer the new key's value from it and skip the judgment the rule exists to force. |
| `scripts/validate.sh:88` | Rejects `^(version\|category\|phase\|requires\|advisor_budget\|allowed tools):` as non-Codex frontmatter for `codex/skills/*` | **Untouched** — no new key to blocklist. |
| `scripts/validate.sh:579-590, 691-694` | Both blocks concern the **codex-local** eval tool (`.codex/skills/ywc-codex-toolkit-eval`, whose `SKILL_ROOT` is `codex/skills`): `:579-590` checks its files exist, `:691-694` executes it. **`scripts/validate.sh` never references `.claude/skills/ywc-toolkit-eval` at all** (grep returns zero hits) — the scorer that actually gates claude-code skills is neither checked nor run locally | **Comply, and correct the AC.** The A7 gate is therefore **invisible to `bash scripts/validate.sh`** and fires only in CI (`.github/workflows/validate.yml:37`). AC13 adds the missing command. |
| `claude-code/skills/CLAUDE.md:282-309` | Bundled scripts live in `<skill>/scripts/`, are mode `100755`, and are registered without a `bash` prefix | **Extend.** FR-2's two scripts add two rows and match the convention. |
| `claude-code/skills/references/subagent-status-actions.md` §3.5 | Subagent return payload: `Status \| 1-line summary \| artifact paths \| (Concerns/Blocker)`. Full outputs go to files | **Comply.** FR-1's judges return artifact **paths**. Without this, an 80-candidate sweep saturates the orchestrator in the first wave. |
| `claude-code/skills/ywc-parallel-executor/SKILL.md` | **502 lines** — violates A8's 500-line cap | **Override** (FR-6). |
| `claude-code/skills/ywc-skill-author/README*.md` | Documents rules "A1–A13" (the skill is already at A14) and "18개 production ywc-* skill" (there are 46) — **pre-existing drift** | **Override** (FR-7). FR-4/FR-5 would widen it. |
| `claude-code/skills/*/evals/evals.json` (8 of 46) | `{skill_name, evals: [{id, prompt, expected_output, files}]}` — `expected_output` is **natural-language prose**, not a machine-checkable assert | **Extend.** FR-1 reuses `prompt` as the scenario when present; the other 38 get a synthesized one. `expected_output` is never read — which also satisfies parent FR-2's no-leaked-answer rule. |
| Repository root | No `package.json`. Bash + **Python 3** (the eval scorer) + the Task tool. CI: `.github/workflows/validate.yml` | **Comply.** Python is a conditional hard dependency via FR-4, not a new one. |

## Acceptance Criteria

- [ ] **AC1 — No second meta-skill exists** *(global invariant)*: `ls claude-code/skills/ | grep -E 'ywc-skill-(prune|audit)'` returns no match at every phase; the Deletion Test is reachable only through `ywc-skill-author`.

- [ ] **AC2 — Nothing is deleted** *(global invariant)*: no commit this spec produces removes a row from any `## Rationalization Defense` table. Verified mechanically, not by inspection — for the branch range, `git diff <base>..HEAD -- 'claude-code/skills/ywc-*/SKILL.md'` must contain **zero** removed lines (`^-`) that fall inside a Rationalization Defense section. The pilot's only write is its report.

- [ ] **AC3 — The row enumerator agrees with the CI gate**: `bash claude-code/skills/ywc-skill-author/scripts/enumerate-rd-rows.sh <skill-dir>` prints one `<start>-<end>` line range per Rationalization Defense data row, and the **count of lines it prints equals `_rationalization_data_rows()`'s return value for the same file, for all 46 skills**. Observable as a self-check mode exiting `0` with `PARITY OK: 46/46`. A disagreement is a defect in the enumerator, never in the counter — the counter is canonical because it is the function that decides CI.

- [ ] **AC4 — Variant construction is deterministic and lossless**: `bash claude-code/skills/ywc-skill-author/scripts/build-variant.sh <skill-dir> <start> <end>` writes the deleted variant to a temp path and prints it. The variant's line count equals `original − (end − start + 1)` **exactly**, and a re-run on identical inputs is byte-identical (`cmp` exits `0`). Exits `1` **without writing** when the range is out of bounds, inverted, or would leave a table header with zero data rows.

- [ ] **AC5 — Every label is backed by six artifacts and a pooled floor**: for each sampled candidate the report row carries **6 artifact paths** (3 original-body runs, 3 deleted-body runs), the within-variant disagreement count (0–6), the cross-variant disagreement count (0–9), the floor threshold in force, the scenario used, the stratum (A/B), and the label.

  **The rate-to-count conversion is a tail bound, not a mean.** The pooled floor is a *rate*: `floor_rate = (total within-variant disagreements across the sample) / (6 × 80)`. Under the null hypothesis (the deleted row was truly inert), a candidate's cross-variant disagreement count is distributed `Binomial(9, floor_rate)` — cross comparisons become statistically identical to within-variant ones. The threshold must therefore be an **upper-tail quantile of that null**, not its mean:

  > `T` = the smallest `t` such that `P(X ≤ t) ≥ 0.95` for `X ~ Binomial(9, floor_rate)`.

  The naive `T = floor(floor_rate × 9)` sits at the null's *mean*, which mislabels **37–61 % of truly inert rows as `load-bearing`** across the entire plausible noise range — silently erasing the very signal the pilot exists to detect. The tail bound holds that error at ≤ 5 % by construction:

  | `floor_rate` | `T` | P(false `load-bearing` \| truly inert) |
  |---|---|---|
  | 0.00 | 0 | 0.0 % |
  | 0.05 | 2 | 0.8 % |
  | 0.10 | 3 | 0.8 % |
  | 0.15 | 3 | 3.4 % |
  | 0.20 | 4 | 2.0 % |
  | 0.25 | 4 | 4.9 % |

  Labels are exactly:

  | Label | Condition |
  |---|---|
  | `inert` | cross-variant disagreement count **≤ T** (**boundary inclusive** — equal to `T` is `inert`) |
  | `load-bearing` | cross-variant disagreement count **> T** |
  | `indeterminate` | any of the 6 runs returned BLOCKED / NEEDS_CONTEXT, so the comparison could not be made |

  A row with a label but fewer than 6 artifact paths is a defect. **No retry-until-agreement:** re-running a candidate because its variants disagreed is forbidden — it converts the test into one that always passes.

  **The bound is one-sided, and it is bounded on the *cheap* side. Say so out loud.** `T` controls `P(label = load-bearing | truly inert) ≤ 5 %` — the harmless error, which merely preserves a row. It does **not** bound `P(label = inert | truly load-bearing)` — the dangerous error — and cannot, because that requires an alternative-hypothesis distribution this design never defines. The threshold that maximizes the aggregate test's power is therefore *not* the threshold that maximizes safety: raising `T` sharpens the stratum contrast while making `inert` easier to earn by chance.

  This is an accepted trade, and it is only acceptable because of what the label is for:

  > **An `inert` label is evidence for the aggregate stratum contrast (AC9). It is not a license to delete that row.** The downstream pruning change is human-reviewed and must re-verify each row it touches. No mechanism in this spec, and none built on its report, may treat an `inert` label as sufficient authority to remove a guardrail.

- [ ] **AC5a — The harness has a validity ceiling, not just a floor**: the tail-bound `T` controls the *false-`load-bearing`* error, but it cannot rescue a harness whose noise swamps the signal. As `floor_rate` rises, `T` rises with it, and at `floor_rate = 0.5` a row would earn `inert` while 4 of its 9 cross comparisons disagreed — a verdict dressed as a measurement.

  **Ceiling: if the measured `floor_rate` exceeds `0.25`, the run is `INCONCLUSIVE`.** No candidate receives `inert` or `load-bearing`; all 80 become `indeterminate`, and the report states that the harness — not the corpus — is what got measured. The correct response is to reduce harness variance (a more constrained scenario, lower sampling temperature) and re-run. **Never lower the ceiling to make a run "succeed."** AC9's evidence gate cannot pass on an `INCONCLUSIVE` run.

  **Why 0.25 — and why it is *not* about the error budget.** The tail bound holds `P(false load-bearing) ≤ 5 %` at *every* `floor_rate` in `[0,1]` by construction; that budget never runs out. What collapses past 0.25 is **separability**: the null's spread already covers most of the 0–9 range, so no realistic load-bearing signal remains distinguishable from noise. The ceiling is a power (Type II) limit, not a Type I one. *(An earlier draft justified this ceiling with the "error budget runs out" story — the same mean-vs-tail conflation this AC exists to correct, recurring inside the correction itself.)*

- [ ] **AC6 — The sample is the specified stratified draw**: the report enumerates 80 candidates — **40 from Stratum A (row positions 1–4) and 40 from Stratum B (positions 5+), at most one row per skill per stratum**, drawn across ≥40 distinct skills per stratum. Verified feasible: all 46 skills have ≥1 row in each stratum (Stratum A pool = 184 rows, Stratum B pool = 235 rows). A candidate outside the frame, or a skill contributing two rows to one stratum, is a defect.

- [ ] **AC7 — Resume is keyed, not hoped for**: each report row is keyed `<file>:<start>-<end>`. Before dispatching a candidate the audit checks whether the report already holds that key and skips if so. Observable: killing the run mid-sweep and restarting it re-dispatches **zero** already-recorded candidates and produces **zero** duplicate rows.

- [ ] **AC8 — The report cites the parent audit**: the report header records the **git SHA** of the commit in which the parent spec's report-only audit landed, and the run refuses to start without it. This replaces an unenforceable "the parent must have run first" narrative with checkable evidence — the parent's audit output is terminal-only, so no other artifact exists to check.

- [ ] **AC9 — The evidence gate is a real test with real power**: the report states the per-stratum `inert` rate and a two-sided Fisher exact p-value. **Gate: p < 0.05 AND the Stratum-B `inert` rate exceeds Stratum A's.** Power was computed by exact enumeration at n=40 per group for a true 35-point gap: **85.8 % – 93.5 %** across baselines 0.10–0.50 (all ≥ 80 %). A null result is reported as "quota not shown to manufacture padding" and **FR-4 does not ship** — a legitimate, durable outcome, not a failed run.

- [ ] **AC10 — All five copies of the quota fall together, or none do**: if AC9's gate passes, a single change amends (1) `ywc-skill-author/SKILL.md:54`, (2) `claude-code/skills/CLAUDE.md:84-85`, (3) `skill-rubric.md:42`, (4) `score.py:290`, (5) `test_score.py:112, 123-130`, and regenerates + commits `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` per `validate.yml:33-34`. Observable: `grep -rn "at least 5\|≥5 data rows\|>= 5" ` over those five files returns no match **in the A7 context**, while `## Rationalization Defense` remains a **mandatory section** in all of them. If AC9's gate fails, none of the five is touched.

- [ ] **AC11 — The two validators agree on A2/A3**: `validate-skill.sh`'s opener and anti-trigger checks are byte-for-byte equivalent in effect to `score.py:286-287` — opener is `startswith("(ywc) Use when")`, anti-trigger is `Do not use (for|during|when|in)`. Observable: a fixture opening `(ywc) Use before …` and a fixture anti-triggering with `Do not invoke …` each **fail** `validate-skill.sh`, as they already fail `score.py`. All 46 real skills still pass both. `score.py` is **not** modified — the local validator moves to it.

- [ ] **AC12a — The description extractor is repaired first, against a *named* reference and a *pinned* counting method**:

  **Reference parser**: `score.py::split_frontmatter()` **then** `parse_yaml_lite()` — **both**, in that order. `parse_yaml_lite(fm_raw)` (`score.py:91`) takes *only the frontmatter block*; the `---` boundary split is done by `split_frontmatter()` (`:66-75`). Calling `parse_yaml_lite` on a whole file reproduces the exact bug this FR exists to fix — it swallows the body for the 15 last-key skills. (This is not hypothetical: it happened during review, one step after the same class of mistake was written into this spec as a lesson.) Strict YAML is **not** usable — `yaml.safe_load` fails outright on **8 of 46** skills (`ywc-gen-testcase`, `ywc-merge-dependabot`, `ywc-product-review`, `ywc-release-pr-list`, `ywc-setup-language`, `ywc-spec-validate`, `ywc-spec-writer`, `ywc-tech-research`), whose unquoted `description:` values contain a mid-line `Triggers: ` — a colon-space inside a plain scalar is invalid YAML. `parse_yaml_lite` is the repo's own line-oriented parser and already tolerates this; it is canonical here for the same reason `_rationalization_data_rows()` is canonical for row counts.

  **Word-counting method**: whitespace-delimited token count, computed **without a locale-aware `wc -w`**. `wc -w` disagrees with itself across locales on 30 of 46 CJK-heavy descriptions — the same file yields a different count on a dev machine and in CI with zero content change. Count in awk or Python, or pin `LC_ALL=C`.

  **Observable**: for all 46 skills, the repaired extractor's count equals the reference (`split_frontmatter` → `parse_yaml_lite`) count. Regression fixtures under the pinned method — `ywc-parallel-executor` **72** (not 8,465), `ywc-plan` **106**, `ywc-impl-review` **92**, `ywc-handle-pr-reviews` **112** (the hyphenated-key case). Corpus baseline: **4,154 words**. All four were verified against the reference parser during review; a repaired extractor that disagrees on any of the 46 is not the fix.

  **This AC gates AC12 and AC14: neither is meaningful until it passes.**

- [ ] **AC12 — The flat description cap is enforced, boundary inclusive**: `validate-skill.sh` exits `1` with `FAIL: description is <N> words (> 80 word cap)` when the count **exceeds** 80. **80 words PASS, 81 FAIL.** Word count = whitespace-delimited tokens of the joined description via the **repaired** extractor (AC12a), counted locale-independently. All 46 skills pass — which requires rewriting the **29** that exceed 80 today (measured; mean 90.3, max 148 `ywc-design-renew`).

  **A description is never trimmed below what its trigger accuracy needs.** The cap is a budget, not a target: if a skill genuinely needs 78 words of triggers to be reachable, it keeps them. A skill that cannot be made reachable within 80 words is a finding to report, not a description to mutilate — see FR-5's stop condition.

- [ ] **AC13 — Both gates stay green** *(global invariant)*: after every phase, `bash scripts/validate.sh` passes **and** `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` passes, **and** `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` prints no `FAILED:` line. The `score.py --ci` command is required because `scripts/validate.sh` never executes the claude-code scorer (`:691-694` runs only the codex one) — omitting it was how the earlier draft of this spec gave itself false confidence.

- [ ] **AC14 — The reduction is measured against a *defined* baseline, not a remembered number** *(measurement obligation — this AC has no failure mode by design; it fails only if the measurement is not taken and recorded)*: the baseline is **whatever the repaired extractor (AC12a) outputs across the 46 skills, recorded before any rewrite** — it is not a literal in this spec. Three independent attempts to state this number during review produced 4,187, 4,154, and 4,162, because each used a different boundary rule. A count without a canonical extractor is an opinion, not a measurement; this is the same failure the row-count had, and it gets the same fix (define the tool, then the number is its output). Post-rewrite, re-measure with the same tool and record both figures plus the delta. **Projected: 4,154 → 3,445 words (−17 %, ≈ 1,000 tokens off every turn's resident context), if every over-budget description lands exactly at 80.** Real rewrites land under the cap, so the actual delta should exceed this. The AC is the *measurement*: a smaller-than-projected reduction is a valid recorded outcome, never a reason to trim a description below what its trigger accuracy needs.

- [ ] **AC15 — A8 violation cleared**: `wc -l claude-code/skills/ywc-parallel-executor/SKILL.md` reports ≤ 500 and its `validate-skill.sh` run exits `0`.

- [ ] **AC16 — `ywc-skill-author`'s README set matches its rules**: after any change to A7/A15/A16, `README{,.en,.ja,.ko,.es,.zh}.md`'s rule enumeration and skill count are updated in the **same commit**. Observable: no README states a rule range ending below the highest rule ID in `SKILL.md`, and none states a skill count other than the actual one.

## Functional Requirements

### FR-1: A decidable Deletion Test inside `ywc-skill-author`'s audit mode

Parent FR-2 specifies the protocol's shape but not how `compare` reaches a verdict. Without a decision rule, "compare" collapses into the agent judging its own prose — the bias the Deletion Test exists to eliminate.

1. **Enumerate** candidates via `enumerate-rd-rows.sh` (FR-2). One candidate = one data row, keyed `<file>:<start>-<end>`.
2. **Draw the stratified sample** (AC6): 40 from Stratum A (positions 1–4), 40 from Stratum B (positions 5+), ≤1 row per skill per stratum. **The drawn candidate list is written to the report before any dispatch**, and a resumed run reads it rather than re-drawing — otherwise a crash could silently change the sample universe that AC7's keyed resume assumes is stable.
3. **Bind a scenario.** Reuse an eval's `prompt` verbatim if the skill has `evals/evals.json`; otherwise synthesize one from the skill's `description` triggers. Record it in the report so the run is reproducible. Never read `expected_output`.
4. **Build the variant** via `build-variant.sh` (FR-2). The LLM never hand-edits it: an incidental edit invalidates the contrast.
5. **Dispatch 3 + 3, blind.** Three subagents against the original body, three against the deleted body, all six on the same scenario. **No subagent is told which variant it holds, that a deletion test is running, or that the authoring rules exist.** This is what keeps the "you MUST include X" authoring bias out of the judge — and is why the audit can safely live inside `ywc-skill-author` rather than needing a second meta-skill. Each returns artifact **paths** only (§3.5).
6. **Compare.** *Within-variant* disagreement = the 3 pairs among the original runs plus the 3 among the deleted runs (C(3,2)=3 each). *Cross-variant* disagreement = the full 3×3 = 9 original-vs-deleted comparisons. Equivalence is judged by `references/deletion-test-rubric.md`: cosmetic differences (wording, ordering of equivalent items) are equivalence; a difference in actions taken, files touched, gates enforced, or refusals issued is not.
7. **Pool the noise floor globally, and check it against the validity ceiling.** Three pairs per candidate is far too few to estimate a floor — a 0/3 observation admits a 95 % CI of roughly [0 %, 71 %]. So the floor is **not** computed per candidate. It is pooled across the whole sample: 6 within-variant comparisons × 80 candidates = **480 pooled comparisons**, yielding one global disagreement rate every candidate is judged against (AC5). This is what makes the inference statistically meaningful rather than a coin flip. **Then apply AC5a's ceiling**: if the pooled rate exceeds 0.25, the harness — not the corpus — is what got measured, and the run is `INCONCLUSIVE`. Compute and check the floor **before** labelling anything.
8. **Label and record** (AC5). Nothing is deleted, edited, or committed.

The rubric goes to `ywc-skill-author/references/deletion-test-rubric.md` (≥30 lines, pointed to from `SKILL.md` — `validate-skill.sh:64,68`).

### FR-2: Two bundled scripts

Both are `set -euo pipefail`, mode `100755`, and registered in the `claude-code/skills/CLAUDE.md` table **without** a `bash` prefix (matching every sibling).

**`enumerate-rd-rows.sh <skill-dir>`** — prints one `<start>-<end>` line range per Rationalization Defense data row. Built by extending the line-filtering logic already in `_rationalization_data_rows()` (`score.py:379-395`) to *retain* positions instead of discarding them. **`--self-check` mode asserts count parity against that function across all 46 skills** (AC3). This script exists because the cited function returns an `int` and nothing else — the sampling frame cannot be built from it, a gap the earlier draft asserted away.

**`build-variant.sh <skill-dir> <start> <end>`** — excises the inclusive range, writes to a temp path, prints it. Exit `1` **without writing** on an out-of-bounds, inverted, or structurally-breaking range (AC4). The RD corpus is verified 100 % single-table content, so the structural check is table-only; a non-table branch is out of scope for this pilot.

### FR-3: Run the pilot

Output: `docs/ywc-plans/prune-report-rationalization-defense.md`. 80 candidates × 6 dispatches = **480 dispatches**, append-only, resumable (AC7), with a per-session ceiling of **60** — so the run spans ~8 sessions and a session boundary is a resume point, not a restart. The label-producing phase may fan out across skills; the report has a **single writer** (the orchestrator appends; subagents return paths).

The report must carry the parent-audit SHA (AC8), the drawn candidate list (written before dispatch), the pooled noise floor **and its ceiling verdict** (`VALID` / `INCONCLUSIVE`, AC5a), the per-stratum inert rates, and the Fisher exact p-value (AC9). An `INCONCLUSIVE` run reports the floor and stops — it labels nothing and the evidence gate cannot pass.

### FR-4: Conditionally retire the A7 quota

**Gated on AC9.** If the evidence gate passes, amend all five copies together and regenerate the eval baseline (AC10). The `## Rationalization Defense` **section** remains mandatory everywhere; only the numeric floor goes, replaced by "only observed failure modes, no lower bound."

If the gate fails, **nothing here ships** — and the corpus is then *proven load-bearing*, which is exactly as durable a result as proven-inert.

### FR-5a: Repair the description extractor (prerequisite for FR-5) (AC12a)

`validate-skill.sh:31-35` has no frontmatter `---` boundary. For the **15 of 46 skills whose `description:` is the last frontmatter key**, it captures the entire skill body: `ywc-parallel-executor` measures 8,465 words against an actual 72. Today this is harmless — A2/A3 are boolean substring checks that a longer capture cannot break — but it makes an exact word count impossible, and AC12 would hard-fail those skills regardless of their real description length.

The repair has **two** parts, and shipping only the first still leaves the extractor wrong:

1. **Bound it to the frontmatter block** — stop at the closing `---`.
2. **Broaden the next-key regex to `^[A-Za-z_][A-Za-z0-9_-]*:`** — exactly what `score.py::parse_yaml_lite:97` already uses (`^([A-Za-z_][\w-]*):`). The original `^[A-Za-z_]+:` **does not match a hyphen**, so `ywc-handle-pr-reviews/SKILL.md:5`'s `allowed-tools:` key is swallowed into the description value (120 words vs an actual 112). It is the only hyphenated top-level key in the corpus today, and it alone is enough to break AC12a's all-46 parity claim.

An earlier attempt at this fix specified only part 1 and was verified by an implementation that had *silently* broadened the regex as well — so the check passed while the specified fix was still broken. Both parts are load-bearing; state both.

Fix the extractor **in place** rather than adding a second parser: a divergent parser would eventually disagree with A2/A3, and repairing the shared extractor removes their latent fragility too. AC12a is the regression gate.

### FR-5: A flat ≤80-word description cap (AC11, AC12, AC14)

**Scope note (this FR exceeds what the parent licenses, deliberately).** Every other FR here traces to a parent line that hands off its work. FR-5 does not: the parent's only named subsequent change is the pruning pilot, and its Out-of-Scope restricts editing skills other than `ywc-skill-author` / `ywc-agentic`. FR-5 rewrites 29 descriptions. It is included because it is the *other half* of the same Pocock diagnosis (Trigger, not Pruning) and shares this spec's tooling, but **it is severable** from FR-1 – FR-4, FR-6, FR-7. Severable is not the same as independent: FR-5's *enforcement mode* (hard-fail vs advisory) is gated on FR-3's evidence per parent `:45-47`, so the dependency runs one way — FR-5 needs FR-3, never the reverse. FR-5 also needs FR-5a: a cap cannot be enforced on an extractor that reports 8,465 words for a 72-word description.

**The cap is flat and tier-free.** Measured: 46 descriptions, **4,154 words**, mean **90.3**, max **148** (`ywc-design-renew`), **29 over 80**, **0 under 30**. A flat cap at 80 recovers **709 words (17 %)** — roughly 1,000 tokens off the resident context of *every* turn. The `invocation:` tier that an earlier draft layered on top of this bought only 5–10 pp more, at the cost of a new frontmatter key on all 46 skills, 46 classification judgments, and an amendment to the Critical Surface it had not noticed it needed (`score.py:288`'s `A4_multilingual`). It is deferred to its own spec, which must first count how many skills a human genuinely never invokes. See Out of Scope for the full reasoning and the score-neutral A4 amendment that successor will need.

**Two edits to `validate-skill.sh`, both on the repaired extractor (FR-5a):**

1. **The cap.** `FAIL: description is <N> words (> 80 word cap)` when the count exceeds 80. **80 PASS, 81 FAIL.** Count whitespace-delimited tokens locale-independently — `wc -w` disagrees with itself across locales on 30 of the 46 CJK-heavy descriptions (AC12a).
2. **A2/A3 unification.** The local gate is strictly looser than the CI gate and they disagree (Existing Constraints, `score.py:286-287` row). Since FR-5 rewrites 29 descriptions, a rewrite landing in the looser gate's blind spot — opening `(ywc) Use before …`, or anti-triggering with `Do not invoke …` — would pass every local check and break the build. Tighten `validate-skill.sh` to `score.py`'s exact predicates. **`score.py` is canonical and is not edited here**; the local validator moves to it. This keeps FR-5 off the Critical Surface entirely.

Per parent `:45-47`, both checks are hard-fail only if FR-3's evidence gate passes; otherwise they ship advisory and no rewrite is forced.

**The rewrite has a stop condition, and it is not negotiable.** A description is trimmed by removing redundancy — repeated trigger phrasings, anti-trigger lists that restate the trigger in the negative, prose that duplicates the skill's own body. It is **never** trimmed by removing the triggers a user actually needs to reach the skill. A skill that cannot be made both reachable and ≤80 words is a **finding to report, not a description to mutilate**: record it, leave it over budget, and let the cap be the thing that gets revisited. AC14's measurement obligation exists precisely so a smaller-than-projected reduction is a legitimate recorded outcome.

**A4 is left untouched, and every skill keeps its Hangul and Japanese triggers.** `score.py:288` requires both to be present in every description; all 46 pass today and all 46 must still pass after the rewrite. This is a *presence* check, not a length check — it costs a handful of words, not sixty.

### FR-6: Clear the A8 violation (`ywc-parallel-executor`) (AC15)

502 lines against the 500 cap. Extract a ≥30-line block of **static** content (a lookup table or decision tree) to `references/`, leaving a one-line pointer. Per `SKILL.md:93`, workflow prose and the Rationalization Defense table are Tier 2 and must **not** be what gets extracted. Cite the parent's audit findings for this skill (parent FR-6).

### FR-7: Sync `ywc-skill-author`'s README locale set

Its READMEs document rules "A1–A13" (the skill is at A14) and "18개 production ywc-* skill" (there are 46). Any change landing an amended A7 or a new A15/A16 updates `README{,.en,.ja,.ko,.es,.zh}.md` in the same commit (AC16).

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Safety | The spec deletes nothing (AC2). Uncertainty resolves to `indeterminate`, never to `inert` (AC5). The judge never sees the authoring rules, the variant identity, or `expected_output`. **The statistical bound is one-sided and protects the cheap error, not the dangerous one — so an `inert` label is evidence, never deletion authority (AC5). Human review, not the threshold, is what guards a guardrail.** |
| Statistical validity | The noise floor is pooled across 480 within-variant comparisons, never estimated per candidate from 3 pairs (FR-1 step 7). It has a **validity ceiling**: above a 0.25 pooled disagreement rate the run is `INCONCLUSIVE` and labels nothing (AC5a). The evidence gate has 85.8–93.5 % power for a true 35-point gap, computed by exact Fisher enumeration at n=40/group (AC9). |
| Cost | 480 dispatches, ceiling 60/session, append-only and resumable (AC7). A crash is a resume point. |
| Determinism | Variant construction is a script, never an LLM edit (AC4). Same candidate ⇒ byte-identical variant. |
| Context efficiency | Subagents return artifact paths, never artifacts (§3.5). The flat description cap takes **≈1,000 tokens off every turn's resident context** (4,154 → 3,445 words projected, AC14) without adding a frontmatter key or touching the CI scorer. |
| Reachability | The cap is a budget, not a target. A description is **never** trimmed below the triggers a user needs to reach the skill; an unreachable-under-80 skill is a reported finding, not a mutilated description (FR-5, AC12). |
| Blast radius | FR-5 stays **off the Critical Surface**: `score.py` is read, never written — the local validator moves to match it (AC11). Only FR-4, gated on evidence, may edit `.claude/skills/ywc-toolkit-eval/**`. |
| Portability | New scripts use `set -euo pipefail`, mode `100755`. |

## Critical Surfaces

**`.claude/skills/ywc-toolkit-eval/**` (FR-4)** — amending `score.py:290`, `test_score.py`, and the `history.mechanical.json` baseline changes the **CI gate for every skill in the bundle**. A wrong edit here silently weakens or breaks quality enforcement repo-wide, and `bash scripts/validate.sh` will not catch it (it never runs this scorer). Tasks owning this surface are `Criticality: critical` and must not be gray-box delegated; AC13's `score.py --ci` run is mandatory evidence.

*(The deletion-application path is **not** a critical surface of this spec, because this spec does not delete — see Out of Scope. It becomes one in the downstream pruning change.)*

## Data Model

N/A — no database, and **no new frontmatter key** (the `invocation:` tier that would have added one is deferred). The persisted artifacts are Markdown reports.

## API Contract

N/A — no network surface. The invocable interfaces are `ywc-skill-author`'s audit mode (arguments in its `## Arguments` table, rule B2) and the two scripts, whose contracts are fully specified in AC3/AC4 and FR-2 (argv shape; stdout = line ranges or variant path; exit `0` success / `1` refusal-without-write).

## Edge Cases

- **Candidate is a table's last data row**: excising it orphans the header. `build-variant.sh` exits `1` rather than emit a header-only table (AC4).
- **The two variants differ only in wording**: cosmetic per the rubric ⇒ within the floor ⇒ `inert`. This is the intended common case; a rubric treating *any* textual difference as behavioral would never label anything inert and the pilot would itself be a no-op.
- **A run returns BLOCKED / NEEDS_CONTEXT**: `indeterminate` (AC5). Never retried until the variants agree.
- **The pooled floor comes out at zero** (every within-variant pair agreed): the null is degenerate, `T = 0`, and *any* cross-variant disagreement labels the row `load-bearing`. Correct — with a noiseless harness, any observed difference is attributable to the deletion.
- **The pooled floor comes out high** (> 0.25): the run is `INCONCLUSIVE` (AC5a). Nothing is labelled; the evidence gate cannot pass. Fix the harness variance and re-run — never lower the ceiling to make the run "succeed."
- **A deletion would remove a safety gate or required artifact**: `load-bearing`, recorded with the failed test (parent Edge Case `:178-179`).
- **A description cannot be both reachable and ≤80 words**: leave it over budget, record it as a finding, and revisit the cap (FR-5). Never trim triggers a user needs. The cap is a budget, not a target.
- **A rewritten description passes `validate-skill.sh` but fails `score.py`**: impossible after FR-5's A2/A3 unification (AC11) — which is why that unification is in the same FR as the rewrite, not a follow-up.
- **The audit is asked to test `ywc-skill-author` itself**: allowed, and a useful smoke test. A proposed `inert` label on AC5's uncertainty rule is exactly what the `indeterminate` default exists to catch.
- **AC9's gate fails**: FR-4 does not ship, FR-5's checks ship advisory-only, no script is touched, and the corpus is recorded as proven load-bearing. The spec still delivers the report, the two scripts, FR-6's A8 fix, and FR-7's README sync.

## Dependencies

- **`docs/ywc-plans/skill-engineering-hardening.md` must land first.** Its FR-1 (audit mode), FR-2 (deletion-test protocol), FR-3 (audit script), and FR-4 (role model) are prerequisites, not parallel work. AC8 makes the dependency checkable via the parent-audit SHA.
- `claude-code/skills/references/subagent-status-actions.md` §3.5 — the return-payload contract FR-1 step 5 injects verbatim.
- `claude-code/skills/CLAUDE.md:74-95` — the authoring gate every task invokes first.
- Bash, **Python 3** (the eval scorer, conditionally via FR-4), and the Task tool. No new libraries, no external services.

## Open Questions

- [ ] **Is one scenario per candidate enough?** One scenario proves a row inert *for that scenario*. N scenarios multiplies a 480-dispatch run by N. Default: one scenario, recorded per row, so a disputed label is cheap to re-test. Revisit if reviewers dispute specific `inert` labels.
- [ ] **Should the codex bundle receive the same pilot?** Deferred, not decided against. `plugins/` is generated from codex, so a codex port would also need its own baseline regeneration.
- [ ] **How many skills does a human genuinely never invoke?** This is the successor spec's gating question — the `invocation:` tier is worth its permanent cost only if that count is large, and the call-graph reference counts recorded here (`ywc-impl-review` 24, `ywc-sequential-executor` 16, …) are a *seed*, not an answer, since several heavily-called skills are also directly user-typed. Counting it needs usage evidence this repo does not currently collect. Until then the flat cap (FR-5) stands alone.
- [ ] **Should A4's multilingual requirement itself get a deletion test?** A4 mandates Hangul + Japanese in every description — a blanket quota structurally identical to A7, and never justified by evidence. This spec's own harness (FR-1) could answer it. Deliberately not attempted here: one quota per pilot, and A7 is the one with 419 rows behind it.

## References

- `docs/ywc-plans/skill-engineering-hardening.md` — **parent spec**
- `docs/ywc-plans/skill-pruning-pilot.spec-ready-log.md` — the convergence log that produced this consolidation
- `develop-with-llm/docs/studies/insights/MATT_POCOCK_SKILL_HELL_ENGINEERING.md` — principles 1 (Trigger) and 4 (Pruning)
- `claude-code/skills/CLAUDE.md` — authoring gate (`:74-95`), script registry (`:282-309`)
- `claude-code/skills/ywc-skill-author/SKILL.md` — rules touched: A7 (`:54`), A8 (`:55`), A14 (`:66`), Tier-2 pinning (`:93`)
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` — the canonical row counter (`:379`) and the CI-enforced A7 gate (`:290`)
