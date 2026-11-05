## Spec Review Result: 20261105-claude-upstream-issue-69-port.md (iteration 2)

### Summary
- Critical: 3, Warning: 13, Suggestion: 8
- Gate: PROCEED (90) — Criticals are omissions with concrete, repo/snapshot-evidenced fixes
- Phase 2 advisor calls used: 0 of 2 (none)

### Critical Issues
1. [spec:63,108; ~/.claude/skills/ywc-merge-dependabot/scripts/] completeness:b4-scripts-omitted — B4 behavior lives in snapshot scripts `poll-merge-queue.py` (only place `chunk_deadline` appears), `wait-dependabot-rebase.sh`, `detect-dockerfile-from.sh`, plus `detect-major-bump.py` (listed in `claude-code/skills/CLAUDE.md:361` but absent locally) and `test_merge_dependabot_scripts.py`; local dir has only `group-by-ecosystem.py`. AC13b (`chunk_deadline` in SKILL.md) fails on a faithful port. — Add scripts + test to B4, Bundled Execution Scripts rows, CI registration decision, point AC13b at the script.
2. [spec:64; ~/.claude/skills/ywc-retro/references/*.md] completeness:retro-references-omitted — ywc-retro ships 4 references (judgment/tooling/divergent-lens, synthesizer) linked from SKILL.md:56-58,74, a batch-dispatch callout enforced by `tests/named_agent_release_test.py` (run at `scripts/validate.sh:832`), and shared reference links. — List them in B5; add AC.
3. [spec:77,120; ywc-retro/SKILL.md:104 + lens refs; ywc-handoff/SKILL.md:61, README.md:32] completeness:dangling-skill-refs — New skills reference `ywc-architecture-invariants` / `ywc-wayfinder`, both absent locally and Out of Scope; FR3 has no mapping. — Add drop rule to FR3/B5 + grep AC (0 hits).

### Warning Issues
1. [spec:122-132] consistency:fr5-table-incomplete — Missing shared files: verify-done SKILL.md/gate-ledger.md (A8,B2), aggregate-pr.md (A8,B2), both checkpoint-resume.md (A8,B2), trigger-cases.json (B3,C1), cross-skill-graph.md (B3,B5,C3), root CLAUDE.md (B3,B5).
2. [spec:130] consistency:fr5-claudemd-row — `claude-code/skills/CLAUDE.md` row wrong: A8 edits it (scripts table), B2 does not → "A8 → B1 → B3".
3. [spec:60] consistency:b1e-before-b2 — B1(e) greps "after B2" but B1 runs before B2.
4. [spec:5] consistency:header-scope-stale — Header scope omits scripts/validate.sh, .github/workflows, .claude/skills/ywc-toolkit-eval, root CLAUDE.md/README.
5. [spec:55,100; validate.yml:41-54] compat:shellcheck-list-misread — `:41-54` is `ignore_paths`; new test is linted automatically by scandir and must be shellcheck-clean; only real registration is `validate.sh` `check_cc_support_dirs` (~:722, `-f` + `bash`). AC8 grep on validate.yml is wrong.
6. [spec:62,68; trigger-cases.json] compat:trigger-cases-incomplete — 18 merge-dependabot/setup-language lines (421…4214) and ~30 reviewer case ids beyond 1170-1373; cite by `"expected"` grep/ids; local-eval only, not CI.
7. [spec:140; score.py:373,386-390] compat:nfr1-wrong-gate — Gate is score.py body lines (frontmatter excluded): sequential 498, parallel 496; headroom 2/4; new refs must be ≥30 lines (S4) and named in body (A14).
8. [spec:62; score.py:376-378; validate-skill.sh:67-69] compat:validator-line-drift — A2–A4 at 376-378; validate-skill.sh has A2 (:67) and A3 (:68-69), no A4; validate-skill.sh is not run by CI; add a `test_score.py` exemption case.
9. [spec:64,121] completeness:readme-locales-not-in-snapshot — Snapshot handoff/retro have only README.md; .en/.ja/.ko must be authored.
10. [spec:60,183; ywc-onboard-repo/SKILL.md:68] completeness:onboard-repo-path-form — Third `${CLAUDE_SKILLS_DIR:-…}` site not classified in B1(d).
11. [spec:63,108] completeness:b4-no-behavior-ac — B4 behaviors (required-check gate, baseRefName, failed/pending split, rebase once, major skip) have no AC.
12. [spec:66; cross-skill-graph.md:42-52] completeness:graph-omits-new-skills — Standalone-skills list lacks ywc-handoff/ywc-retro.
13. [spec AC4; snapshot ywc-finish-branch/SKILL.md:369] feasibility:ac4-ordering-ambiguous — Guard text itself contains `gh pr merge --delete-branch`; snapshot guard sits after deletion step and also requires baseRefName/headRefOid for "merged" — AC4 ordering check and "no --base" note are inaccurate.

### Suggestions
1. [spec:228] consistency:confidence-gate-oq-count — 6 Open Questions now.
2. [spec:173] feasibility:step6-description — Step 4c step 6 re-runs 4b.5 before handoff; handoff text is in Step 5.
3. [spec Scope A8] feasibility:a8-oversized-task — Split scan-secrets into its own task.
4. [spec AC9] feasibility:ac9-learnings-gap — No AC for `.ywc-learnings.jsonl` prose.
5. [spec:62] compat:validate-skill-not-in-ci — State validate-skill.sh edit is consistency, not CI.
6. [spec:80-130] [unverifiable-ac] AC8, AC10, AC14, AC14b, AC17 are not single-grep checks.
7. [spec:55] compat:scan-secrets-ignored — scan-secrets.sh is in ignore_paths; edits stay unlinted.
8. [spec:68] compat:c1-cases-scattered — cite ids.

### Completion Status
DONE_WITH_CONCERNS
