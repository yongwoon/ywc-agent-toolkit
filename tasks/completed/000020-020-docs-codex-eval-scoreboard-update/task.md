# Task: Codex Eval Scoreboard Update

## Summary

Update `docs/skill-agent-eval/codex/scoreboard.md` from the 2026-06-18 report while preserving historical trend semantics.

## Implementation Steps

- [ ] Read the 2026-06-18 report and identify supported score/trend changes.
  - Related AC/FR: AC2, FR-2
  - Contract / Behavior Change: Scoreboard changes must be derived from report evidence, not from mechanical PASS alone.
  - Verification Command / Evidence: Use `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md` as the source for each changed row.
- [ ] Update scoreboard rows and summary notes.
  - Related AC/FR: AC2, FR-2
  - Contract / Behavior Change: Preserve `Current`, `Previous`, `Trend`, and `Last evaluated`; use `up` only for confirmed score movement and `same` for clean-but-unchanged items.
  - Verification Command / Evidence: `rg -n "2026-06-18|ywc-code-gen|ywc-task-generator|ywc-skill-author|same|up" docs/skill-agent-eval/codex/scoreboard.md`
- [ ] Cross-check the scoreboard against the report.
  - Related AC/FR: AC2, FR-2
  - Contract / Behavior Change: No scoreboard entry claims a score movement absent from the report.
  - Verification Command / Evidence: Manual line-by-line comparison of changed scoreboard rows against the report's evidence notes.

## Task Verify

```bash
test -f docs/skill-agent-eval/codex/2026-06-18-full-sweep.md
rg -n "2026-06-18|Current|Previous|Trend|Last evaluated" docs/skill-agent-eval/codex/scoreboard.md
rg -n "ywc-code-gen|ywc-task-generator|ywc-skill-author|same|up" docs/skill-agent-eval/codex/scoreboard.md
git diff -- docs/skill-agent-eval/codex/scoreboard.md docs/skill-agent-eval/codex/2026-06-18-full-sweep.md
```

Expected Passing Signal:

- Scoreboard contains 2026-06-18 evaluation references.
- Changed trend values are justified by the report.
- Diff is limited to scoreboard content, with the report used as read-only evidence unless correcting a typo.

Pre-change Failing Evidence / Exception:

- Before this task, the scoreboard does not reflect the 2026-06-18 cycle.

Contract/Test Evidence:

- Every `up` trend in the changed section corresponds to report evidence for an actual score change.

## Out of Scope

- New evaluator commands unless needed to resolve an inconsistency.
- Skill or agent source edits.
