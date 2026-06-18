# Fix Plan — Toolkit-Eval Mechanical-Tier Findings

**Scale:** Small (direct execution plan). Source: `ywc-toolkit-eval --mode full --target all` mechanical tier, 2026-06-18.
**Boundary note:** 7 files exceed the nominal Small ≤3-file line, but no hard-disqualifier applies (no DB migration, no new library, no new API contract, no cross-cutting logic) and every change is an isolated micro-edit or a single file extraction. If you prefer per-fix PR isolation or task tracking, this can be re-routed to the Medium path instead.

## Goal

Resolve the confirmed findings from the mechanical evaluation so all 40 skills pass the deterministic structure checks, and land the three scorer-bug fixes that corrected 6 false-positive structure failures.

## Why

The eval found 3 genuine skill defects + 3 scorer bugs. The scorer bugs were falsely failing 6 healthy skills (suppressing real signal); the 3 skill defects are real activation/economy regressions in the distributed catalog.

## Out of Scope

- **Judgment-tier findings (S1/S3/S6, A1/A2/A6).** The judge pass was blocked by the account session limit (resets 2:20pm Asia/Tokyo) and produced no data. Activation/behavioral/catalog-fit defects may add backlog items. This plan covers only the **confirmed mechanical findings**; re-validate it against the full scorecard once the judgment tier completes.
- Any skill not flagged by the mechanical tier (no "while I'm here" edits).
- README prose rewrites — only the SKILL.md frontmatter `description:` changes for ywc-commit / ywc-spec-validate.

## Done When

- `python3 .../score.py --target all` reports **zero** structure failures across all 40 skills (the 3 mechanical findings cleared).
- `python3 -m unittest test_score` is green (≥20 tests).
- `bash scripts/validate.sh` passes.
- `history.mechanical.json` regenerated to reflect the corrected scorer.

## Existing Constraints Touched

- `.claude/skills/ywc-toolkit-eval/scripts/score.py` — `parse_yaml_lite`, A2/A3/A4 structure checks, `JAPANESE` regex (fixes already applied, uncommitted).
- `score.py` writes `history.mechanical.json` only in `--ci`/`mechanical` modes; the committed baseline currently reflects pre-fix (buggy) scores and must be regenerated.
- `claude-code/skills/ywc-gen-testcase/SKILL.md:244-373` — embedded single-file testsheet template (~130 lines), the Tier-3 extraction target per `ywc-skill-author` A14.
- Skill descriptions are SKILL.md frontmatter only; the en/ja/ko README locale set is unaffected by description edits (S5 checks locale-set existence, not description-to-README sync).

## Files to Touch

1. `.claude/skills/ywc-toolkit-eval/scripts/score.py` — DONE (3 fixes, uncommitted)
2. `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` — DONE (+5 regression tests, uncommitted)
3. `claude-code/skills/ywc-commit/SKILL.md` — add Japanese triggers (A4)
4. `claude-code/skills/ywc-spec-validate/SKILL.md` — "Use after" -> "(ywc) Use when" (A2)
5. `claude-code/skills/ywc-gen-testcase/SKILL.md` — extract template, add pointer (A8)
6. `claude-code/skills/ywc-gen-testcase/references/testsheet-template.md` — NEW (extracted content)
7. `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — regenerate baseline

## Implementation Steps

- [ ] **Fix 1 — ywc-commit A4 (missing Japanese triggers).** In `claude-code/skills/ywc-commit/SKILL.md` `description:`, add Japanese trigger phrases (e.g. `"コミット"`, `"コミットして"`, `"プッシュ"`) alongside the existing Korean/English ones, matching the already-correct globally-installed copy. Keep the `(ywc) Use when` opening and the "Do not use for…" clause intact.
- [ ] **Fix 2 — ywc-spec-validate A2 ("Use after").** In `claude-code/skills/ywc-spec-validate/SKILL.md` `description:`, reword the opening from `(ywc) Use after writing a specification and before task decomposition, when…` to `(ywc) Use when a specification has been written and before task decomposition, and…` so it satisfies the canonical `(ywc) Use when` prefix without changing meaning.
- [ ] **Fix 3a — ywc-gen-testcase A8 (extract template).** Move the embedded testsheet template block (SKILL.md:244-373, "Single-file template" through "Length Management Guidelines") into a new `claude-code/skills/ywc-gen-testcase/references/testsheet-template.md`.
- [ ] **Fix 3b — add the pointer.** Replace the extracted block in SKILL.md with a one-line Tier-3 pointer: `See [references/testsheet-template.md](references/testsheet-template.md) for the full single-file/split testsheet template and length-management rules.` Confirm post-frontmatter body <= 500 lines.
- [ ] **Fix 4 — regenerate the mechanical baseline.** Run the scorer so `history.mechanical.json` reflects the corrected scores via the documented `--ci`/mechanical path. Verify the new baseline shows the previously-false-failing A2/A3/A4 sub-scores corrected.

## Verification

```bash
# 1. Scorer tests green (>=20)
cd .claude/skills/ywc-toolkit-eval/scripts && python3 -m unittest test_score

# 2. Zero structure failures across all skills
python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
    fails=[(i['name'],[k for k,v in i['signals']['structure_checks'].items() if not v]) \
    for i in d['claude-code/skills'] if any(not v for v in i['signals']['structure_checks'].values())]; \
    print('FAILS:', fails); assert not fails, fails"

# 3. CI mirror (frontmatter, locale set, shellcheck, --list dry run)
bash scripts/validate.sh

# 4. gen-testcase body under cap
awk '/^---$/{c++;next} c>=2{n++} END{print n}' claude-code/skills/ywc-gen-testcase/SKILL.md   # expect <= 500
```

## Risks / Rollback

- **Risk:** template extraction breaks an internal SKILL.md cross-reference. **Mitigation:** the extracted block is a leaf template with no inbound anchors; verify with `grep -n "Single-file template\|testsheet-template" SKILL.md` after the edit.
- **Risk:** `history.mechanical.json` regeneration masks a real future regression. **Mitigation:** regenerate only after tests are green and the 3 findings are visibly cleared; commit the baseline in the same change as the score.py fix so the diff is auditable.
- **Rollback:** all edits are isolated; `git checkout -- <file>` per file. The scorer fixes are guarded by the 5 new tests, so a bad revert is caught.

---

✅ Plan ready: `plan.md`
Next: implement directly, or run `/ywc-code-gen`, or `/ywc-sequential-executor` if you prefer Branch + PR isolation.
