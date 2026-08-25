# spec-ready loop log — claude-skill-eval-runner

Append-only. One entry per iteration.

## Iteration 1 — 2026-07-22

- **Command**: `ywc-spec-validate --spec docs/ywc-plans/claude-skill-eval-runner.md --advisor-budget 2`
- **Findings**: Critical 4, Warning 4, Suggestion 2
- **Phase 2 advisor calls used**: 0 of 2 (none) — every Critical is an objective omission requiring no frontier judgment
- **Confidence gate**: 72/100 REVIEW; required dimension `Root cause identified` = 58 (>= 50, so no forced STOP)
- **spec-validate Completion Status**: `NEEDS_CONTEXT`
- **Route**: Step 3 hard stop — `stop-context`. No re-plan performed (NEEDS_CONTEXT never triggers `ywc-plan --update-spec`).
- **Deviation recorded**: Phase 1 four-dimension review was executed inline rather than as a parallel subagent fan-out. Reason: the prior fan-out attempt in this session returned no usable findings from 3 of 4 subagents while consuming >100k tokens each. Dimension separation was preserved by analysing each dimension independently.

### Critical (all four are Step 3.5 precedent omissions)

1. `SKILL.md:115` — the Behavioral judge (S3) bullet, the site that actually produces S3, is never named by the spec. Phase 3 says "S3 배선" without instructing that this bullet change; a copy-faithful implementer leaves the judge reading SKILL.md and the runner output has no consumer.
2. `evals/history.json` — never named. `SKILL.md` Step 6 appends one run row per cycle and the file **does** carry per-item totals under `roots.<root>.items` (`{schema:1, runs:[{date, mode, roots:{<root>:{count, mean_total, below_threshold, items:{<name>: <total>}}}}]}`). Because those values are `/100` **totals** and S3 carries weight 20, an item whose S3 is `"unmeasured"` has no honest total to store, and the spec defines none.

   > **Correction (post-review)**: an earlier reading of this file reported that the run rows carried no per-item totals. That was wrong — a shallow probe printed only the top-level run keys (`date`/`mode`/`roots`) and missed `items` nested under `roots`. `SKILL.md` Step 6's description is accurate. The finding stands, but its substance is total-comparability, not a missing field.
3. `references/scorecard-format.md:17` — the scorecard table declares a numeric `S3` column. AC8 mandates the string `"unmeasured"`, which no documented output surface accepts.
4. `.gitignore` — AC13 requires a gitignored artifact root, but no such rule exists. As written AC13 is unimplementable.

### Warning

5. Mixed-status aggregation across the 6 paired ablation trials is undefined. AC6 fixes per-run status; AC10/AC11 never say what a partial `ERROR` / `SKIPPED_UNAVAILABLE` set aggregates to.
6. Concurrency is unspecified — two simultaneous runs sharing the artifact root or temp-dir naming.
7. No Non-Functional Requirements section. Cost and wall-clock bounds are applicable (6 trials x 2 arms x N cases) and are left only as Open Question 4.
8. `scripts/validate.sh:610-621` enforces the existence of `score.py` / `test_score.py`; Phase 5 says the runner equivalent is "결정" but commits to nothing, so a deleted runner would pass CI.

### Suggestion

9. AC9 requires a runner start-up warning (Phase 2 behaviour) while the band table lives in Phase 3 — assign the warning to Phase 2 explicitly.
10. `references/scorecard-format.md:68` already documents that `history.mechanical.json` exists so "the judgment tier's natural variance never trips the gate". AC7 re-derives this rule without citing it; cite instead.

### Open questions surfaced to the user (NEEDS_CONTEXT)

1. Should a runner-sourced S3 be recorded in `evals/history.json` at all, or does history stay mechanical-only?
2. What renders in the scorecard `S3` column for an unmeasured item — `·`, `unmeasured`, or blank?
3. Where does the artifact root live, and under which `.gitignore` rule?

**Completion Status: NEEDS_CONTEXT**

## Iteration 2 — 2026-07-22

- **Input**: user resolved the three open questions (D1 totals-honesty, D2 `?` vs `·`, D3 mirror Codex artifact layout); `ywc-plan --update-spec` appended `## Iteration 1 Amendments` with AC16–AC20, NFR1–3, revised Test Strategy, and a revised Confidence Gate. Operative Sections pointer and a `⚠️ SUPERSEDED` marker on the original Confidence Gate were added.
- **Command**: `ywc-spec-validate --spec docs/ywc-plans/claude-skill-eval-runner.md --advisor-budget 2`
- **Findings**: Critical 2, Warning 1, Suggestion 0 (Critical 4 → 2, decreasing — no stall guard fires)
- **Phase 2 advisor calls used**: 0 of 2 (none) — both Criticals are objective factual errors
- **Confidence gate**: 74/100; required dimension `Root cause identified` = 58 (unchanged — isolation still unverified)
- **spec-validate Completion Status**: `NEEDS_CONTEXT`
- **Route**: Step 3 hard stop — `stop-context`. No re-plan (NEEDS_CONTEXT never triggers one).

### Critical

1. **`scripts/validate.sh` has no claude-evaluator check at all — AC20 and an Existing Constraints row rest on a false premise.** The block at `:598` opens with `local skill_dir=".codex/skills/ywc-codex-toolkit-eval"`, and its `score.py` / `inventory_gate.py` / `test_score.py` existence checks belong to the **Codex** evaluator (the claude evaluator has no `inventory_gate.py`). `grep -n "\.claude/skills/ywc-toolkit-eval" scripts/validate.sh` returns nothing. Consequences: (a) the spec's Existing Constraints row citing `scripts/validate.sh:610-621` as guarding "evaluator 의 score.py/test_score.py" is wrong for this side; (b) AC20's "확장" is impossible — there is nothing to extend, it must be **신설**; (c) Iteration 1's Warning 8 understated the gap — today even deleting the claude `score.py` passes `bash scripts/validate.sh`.
2. **`SKILL.md` Output Format section is a second scorecard rendering surface that AC17 does not name.** It carries its own `| Item | S1 | S2 | S3 | S4 | S5 | S6 | Total | Weakest |` example table. AC17 names only `references/scorecard-format.md`, so the `?` / `—` notation from D2 would be documented in one place and contradicted in the other.

### Warning

3. AC16 (replace the `SKILL.md:115` Behavioral judge bullet) has no row in the revised Test Strategy, while AC17–AC20 each gained one. Pass A gap introduced by the amendment itself.

### Verified during this iteration (no finding)

- `.gitignore` rule `docs/skill-agent-eval/*/runs/` behaves as D3 requires — empirically confirmed in a throwaway repo: `runs/` artefacts are ignored while a sibling `<date>-<name>.md` report stays tracked.
- `evals/history.json` shape, `evals/evals.json:15` (`·` = judgment-deferred), `references/scorecard-format.md:68`, and `SKILL.md:115` all match the amendment's claims.

### Post-loop fixes applied (outside the loop, user-directed)

`NEEDS_CONTEXT` never triggers a re-plan, so these were applied as a direct edit rather than by `ywc-plan --update-spec`:

- `## Iteration 2 Amendments` added, carrying §AC17′ (notation legend must land in **both** `references/scorecard-format.md` and `SKILL.md` `## Output Format`), §AC20′ (**신설** a claude-side existence check, not extend), three new Test Strategy rows (AC16 / §AC17′ / §AC20′), and a revised Confidence Gate (75/100, `Root cause identified` unchanged at 58).
- The false Existing Constraints row was corrected in place — `scripts/validate.sh:598` is `local skill_dir=".codex/skills/ywc-codex-toolkit-eval"`, and `grep "\.claude/skills/ywc-toolkit-eval" scripts/validate.sh` returns 0 hits (re-verified after the edit).
- Operative Sections pointer now encodes precedence: Iteration 2 > Iteration 1 > original.
- Iteration 1's own Pass B record carried the claim that `validate.sh:610-621` "was accurate". A correction marker was appended rather than rewriting the record: that pass confirmed the line range existed but never confirmed the block's owner.

### Phase 0 spike executed (2026-07-22) — the blocker moved

`docs/skill-agent-eval/claude/spike-2026-07-22.md`, spend **$0.5409**. Four of six unknowns closed, one new constraint found:

- `CLAUDE_CONFIG_DIR` **exists and relocates the config root** (proved via `claude doctor` diff, zero API calls).
- Project-local `.claude/skills/` loads; `claude -p "/<skill>"` fires (sentinel returned exactly `SENTINEL_OK_7Q4X`).
- `--disable-slash-commands` disables project-local skills too and **short-circuits at $0** — valid ablation without-arm.
- `--output-format json` carries **no activation field** → `activation_observability: unavailable` is the real path.
- Auth is config-dir-scoped: a virgin dir yields `Not logged in`.
- **New constraint** — `--bare` is the closest thing to an isolation mode but *"OAuth and keychain are never read"*, so **isolation and the Claude subscription are in tension**. The account is `subscriptionType: "max"`, and Test A's $0.54 was already billed to that subscription.

Recorded as `## Iteration 3 Amendments`: §AC1′ (Phase 0 now terminates on a **route choice**, not a yes/no), §AC2′ (attribution limited to with/without deltas under route N1), §NFR1′ (measured $0.54/dispatch → ~$6.5/case), §Phase 2 확정 사항. Two original premises corrected: contamination is **243** installed skills, not "40여 개", and isolation is a **cost** lever as well as a correctness one.

`Root cause identified` moved **58 → 72**, clearing the required-dimension threshold. Gate is 79/100, still REVIEW. What remains is no longer an unknown but a **user decision**: route N2 (`claude setup-token`, keeps the subscription) versus N1 (non-isolated + ablation attribution, already proven). N4 (copying credentials into `/tmp`) is prohibited.

### Why this loop cannot reach DONE by amendment

`Root cause identified` is pinned at 58 because the isolation mechanism is an **empirical unknown**, and no amount of spec editing changes an empirical unknown. Only the Phase 0 spike moves it. The loop returning `NEEDS_CONTEXT` twice is the gate working as designed, not a convergence failure.

**Completion Status: NEEDS_CONTEXT**
