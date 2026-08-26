# Task: Codex Eval Judgment Report

## Summary

Create the 2026-06-18 full sweep report for Codex skills and agents. The report must preserve the distinction between mechanical evidence and judgment scoring.

## Implementation Steps

- [ ] Gather fresh evaluator evidence.
  - Related AC/FR: AC1, FR-1
  - Contract / Behavior Change: Report evidence comes from current local evaluator commands, not stale copied values.
  - Verification Command / Evidence: Capture outputs from `inventory_gate.py --json`, `score.py --target all --mode mechanical --format markdown`, and `score.py --target all --ci`.
- [ ] Compare against prior report and scoreboard.
  - Related AC/FR: AC1, FR-1
  - Contract / Behavior Change: The new report explains what is new on 2026-06-18 and what is carried forward from 2026-06-16.
  - Verification Command / Evidence: Reference `docs/skill-agent-eval/codex/2026-06-16-full-sweep.md` and `docs/skill-agent-eval/codex/scoreboard.md` in the report.
- [ ] Write `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`.
  - Related AC/FR: AC1, FR-1
  - Contract / Behavior Change: Include Gate Summary, Mechanical Scorecard, CI baseline, judgment scoring notes for S1/S4/S8 and A1/A3/A8, and Priority Backlog ranked by release impact.
  - Verification Command / Evidence: `test -f docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`
- [ ] Mark uncertainty honestly.
  - Related AC/FR: AC1, FR-1
  - Contract / Behavior Change: If judgment scoring is not fully rerun, status is `PASS_WITH_ACTIONS` and carry-forward rationale is explicit.
  - Verification Command / Evidence: `rg -n "PASS_WITH_ACTIONS|mechanical|judgment|S1|S4|S8|A1|A3|A8" docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`

## Task Verify

```bash
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --mode mechanical --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci
test -f docs/skill-agent-eval/codex/2026-06-18-full-sweep.md
rg -n "PASS_WITH_ACTIONS|mechanical|judgment|S1|S4|S8|A1|A3|A8|Priority Backlog" docs/skill-agent-eval/codex/2026-06-18-full-sweep.md
git diff --name-only
```

Expected Passing Signal:

- Evaluator commands exit 0.
- The new report exists and contains mechanical, judgment, and backlog sections.
- `git diff --name-only` shows this task's report file only.

Pre-change Failing Evidence / Exception:

- Before this task, `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md` does not exist.

Contract/Test Evidence:

- The report directly cites command outputs or records carry-forward decisions for each judgment-sensitive axis.

## Out of Scope

- Scoreboard edits.
- Codex source edits.
- Generated plugin sync.
