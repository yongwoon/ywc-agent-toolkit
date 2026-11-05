## Spec Review Result: 20261105-claude-upstream-issue-69-port.md (iteration 3)

### Summary
- Critical: 3, Warning: 13, Suggestion: 6
- Gate: PROCEED (90)
- Phase 2 advisor calls used: 0 of 2 (none)

### Critical Issues
1. [spec:64,111,121] completeness:dangling-legibility-audit — snapshot ywc-retro/SKILL.md:104 and 3 lens refs reference `ywc-agent-legibility-audit`, absent locally; FR3/B5/AC14c cover only architecture-invariants and wayfinder. — Generalize: every `ywc-*` name in ported files must exist locally.
2. [spec:51] completeness:completion-report-site-undefined — A8 "completion-report DONE 정의" targets snapshot `references/completion-report.md` (Out of Scope, absent locally); no local site/AC. Other executor sub-items (advisor-escalation Step 번호, worktree-run) lack file targets. — Drop or name local file:line.
3. [spec:45,99] completeness:ac7b-not-from-snapshot — snapshot "~50 lines" exists only in ywc-tdd-ritual/SKILL.md:40 (local already same); local cookbook:77 "50+ lines", checklist:18 "~10 lines"; AC7b grep `50 lines` not derived. — State target lines + replacement, fix AC.

### Warning Issues
1. [spec:64] completeness:handoff-untrusted-output — State status tags `[unverified]`, gh/git output as data only, not in B5/AC14b.
2. [spec:55] completeness:blocked-sentence-no-ac — create-pr "exit 0/1 이외 = BLOCKED" sentence has no AC.
3. [spec:63] completeness:b4-readme-omitted — B4 behavior change lacks README ×4.
4. [spec:62] completeness:ac13-no-test-score-ac — test_score.py case unchecked (and not CI-gated).
5. [spec:51] completeness:weak-verifiability — refactor-clean/security-audit/code-gen 0→7.5/executor sub-items lack AC or explicit review-only marking.
6. [spec:5] consistency:header-scope-stale — B4 (validate.sh) and C1 (trigger-cases) outside "A8·B3·B5".
7. [spec:60,133] consistency:fr5-claudemd-row — B2 re-check and C3 pair row not in row; B1 table includes C3-only pair.
8. [spec:62,115] consistency:ac17-baseline-once — history.mechanical.json rewritten on every PASS; later tasks change it.
9. [spec:62; score.py:817-848] compat:baseline-regen-impossible-on-drop — `--ci` never writes on drop; exemption must keep S2=5; commit rewritten JSON.
10. [spec:55; snapshot test-scan-secrets.sh:58-106] compat:scan-secrets-test-scope — snapshot test asserts Phase 2b etc. beyond local script; verbatim copy fails; installed bundle ahead of #69 scope → T0 needs hunk filter.
11. [spec:63] feasibility:b4-py310-requirement — poll-merge-queue.py needs Python ≥3.10.
12. [spec:63] feasibility:b4-validate-sh-site — test registration site unnamed (check_cc_support_dirs :701-731); new .sh must be shellcheck-clean (verified clean).
13. [spec:62,68; test_fixture_schema.py:159-165] compat:trigger-cases-schema-gate — CI validates trigger-cases schema; edits must stay valid; C1 rewrite is local-eval only (non-blocking).

### Suggestions
1. [snapshot lens refs] compat:tools-prefix — `tools/claude-code/skills/` → `claude-code/skills/` normalization rule.
2. [spec:55] compat:anchor-drift — validate.sh :701-731.
3. [spec:39] consistency:replan-step6-wording — Scope A1(b) wording.
4. [spec:18] consistency:337-row-misleading.
5. [spec:21] consistency:341-docker-gate-unmapped — map to B4 Dockerfile FROM.
6. [spec:237] consistency:gate-stale — Scope control rationale.

### Completion Status
DONE_WITH_CONCERNS
