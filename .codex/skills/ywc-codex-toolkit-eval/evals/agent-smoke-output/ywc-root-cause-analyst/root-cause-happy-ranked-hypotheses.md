Fixture ID: root-cause-happy-ranked-hypotheses
Agent: ywc-root-cause-analyst
Capture date: 2026-06-23
Source commit: 8adbd54

Status: DONE

Primary cause: stale fixture output made the smoke runner treat a missing-write case as success. This is a `test isolation leak`.

Next action: none

Top hypotheses:
1. Pre-existing `happy.md` satisfied the success check.
Evidence for: fixture says `output_path` is `evals/agent-smoke-output/ywc-reviewer/happy.md`, and that file already existed from a previous case; log shows normal pass accounting (`PASS ...`, `Summary: 1/1 passed`) despite the test expecting failure on missing output.
Evidence against: none in the packet indicates the runner validates freshness or content origin.

2. The smoke harness checks only file existence, not whether the current agent invocation created output.
Evidence for: a reused path plus exit code 0 strongly implies existence-based success criteria.
Evidence against: if the harness also checked timestamps/content markers, stale output would likely not pass.

3. Exit-code handling is coupled to pass/fail summary rather than the missing-output condition.
Evidence for: observed non-zero expectation failed because suite reported `1/1 passed`, suggesting the summary path dominated exit status.
Evidence against: this still depends on the stale file allowing the case to be counted as passed.

Contributing factors: reused temporary repo state, shared output path across cases, and likely missing cleanup or per-case namespacing.
