# Dispatch artifact: ywc-refactor-clean (deleted body, run 1)

**Key**: claude-code/skills/ywc-refactor-clean/SKILL.md:45-45
**Scenario**: I need help with the following: removing dead code (unused functions / exports / files / dependencies / imports), consolidating near-duplicate utilities, or running a scheduled hygiene pass on a codebase.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a full refusal — proceeding with the skill's workflow, but per the procedure I would ask a clarifying question up front (desired --scope, --tier since duplicate consolidation requires --tier all, and dry-run vs live) and would decline to run the cleanup on the current active feature branch, requiring a dedicated cleanup branch first before any deletion occurs.

## Actions
- Read the procedure file docs/ywc-plans/pilot-artifacts/variant-ywc-refactor-clean-45-45.md (only tool used)
- Narrated: announce ywc-refactor-clean skill usage
- Narrated: git status / git branch --show-current to check for active feature-branch conflict
- Narrated: git checkout main && git pull && git checkout -b chore/dead-code-cleanup-2026-07-13 to isolate cleanup
- Narrated: ask clarifying question on --scope, --tier (safe vs all for duplicate consolidation), and dry-run vs live
- Narrated: Read references/detection-tools.md for the grep-based fallback since repo isn't JS/TS/Python/Go/Rust at root
- Narrated: Step 1 Detect via git grep passes over scripts/*.sh and skill markdown/reference files
- Narrated: Read references/safety-tiers.md and classify findings into SAFE/CAUTION/DANGER
- Narrated: Step 3 SAFE loop - bash scripts/validate.sh baseline, git grep verify, Edit tool delete, re-run validate.sh, commit chore(cleanup): remove unused <symbol> (grep) per item, or git revert + reclassify on red
- Narrated: Step 4 CAUTION triple-check (dynamic-reference grep, string-reference grep, public-surface check) before any CAUTION deletion
- Narrated: Step 5 DANGER items reported only, never deleted
- Narrated: Step 6 duplicate consolidation only under --tier all, with behavior-change items routed to ywc-tdd-ritual + ywc-code-gen instead
- Narrated: Step 7 handoff to ywc-verify-done with Dead Code Cleanup Report in canonical PASS/FAIL format, then ywc-create-pr for a standalone cleanup PR

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-refactor-clean-45-45.md (read only)

## Gates enforced
- Iron Law: detection tool + grep + tests-pass-after-each-batch before any deletion
- SAFE tier: one deletion per commit, no batching, revert (not forward-fix) on red tests
- CAUTION tier: mandatory 3-check verification (dynamic import grep, string-reference grep, public-API check) before deletion
- DANGER tier: report only, never delete
- Cleanup must run on its own branch, never mixed with active feature-branch diff
- Duplicate consolidation gated behind explicit --tier all; behavior-changing consolidations routed out of scope to ywc-tdd-ritual + ywc-code-gen
- Final ywc-verify-done handoff mandatory unless --skip-verify-done passed by an upstream caller, using PASS/FAIL wording only

## Full narrative

See detailed step-by-step narrative above (opening announcement, branch isolation, clarifying question on scope/tier, Step 1 Detect via grep fallback, Step 2 Classify using safety-tiers.md, Step 3 SAFE per-item delete loop with test-before/after and single-item commits, Step 4 CAUTION triple verification, Step 5 DANGER report-only, Step 6 opt-in duplicate consolidation with behavior-change carve-out, Step 7 ywc-verify-done handoff and ywc-create-pr).
