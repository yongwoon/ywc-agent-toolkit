# Task: Eval Fixture Coverage

## Summary

Add objective eval fixtures for selected S5=3 skills or document why a fixture is not suitable in this cycle.

## Implementation Steps

- [ ] Inspect existing eval fixture conventions.
  - Related AC/FR: AC4, FR-4
  - Contract / Behavior Change: New fixtures must match the schema/style already used in `codex/skills/*/evals/evals.json`.
  - Verification Command / Evidence: Compare at least two existing eval files before editing.
- [ ] Select objective fixture candidates.
  - Related AC/FR: AC4, FR-4
  - Contract / Behavior Change: Only add fixtures with verifiable output/behavior that does not require a model judge.
  - Verification Command / Evidence: Record selected candidates or omission reasons in the 2026-06-18 report.
- [ ] Add or update `evals/evals.json` files.
  - Related AC/FR: AC4, FR-4
  - Contract / Behavior Change: Each added fixture checks a meaningful behavior and is not a restatement of the prompt.
  - Verification Command / Evidence: `python3 -m json.tool <evals/evals.json>` for each touched file.
- [ ] Run targeted mechanical scoring for touched skills.
  - Related AC/FR: AC4, FR-4
  - Contract / Behavior Change: S5 evidence improves or omission reason is explicit; no mechanical regression is introduced.
  - Verification Command / Evidence: `score.py --target codex/skills --item <skill-name> --format markdown`.

## Task Verify

```bash
for file in \
  codex/skills/ywc-spec-ready/evals/evals.json \
  codex/skills/ywc-verify-done/evals/evals.json \
  codex/skills/ywc-finish-branch/evals/evals.json \
  codex/skills/ywc-agentic/evals/evals.json \
  codex/skills/ywc-brainstorm/evals/evals.json
do
  if [ -f "$file" ]; then python3 -m json.tool "$file" >/dev/null; fi
done

for item in ywc-spec-ready ywc-verify-done ywc-finish-branch ywc-agentic ywc-brainstorm; do
  python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item "$item" --format markdown
done

rg -n "S5|eval fixture|omission|not suitable|objective" docs/skill-agent-eval/codex/2026-06-18-full-sweep.md
git diff -- codex/skills/ywc-spec-ready/evals/evals.json codex/skills/ywc-verify-done/evals/evals.json codex/skills/ywc-finish-branch/evals/evals.json codex/skills/ywc-agentic/evals/evals.json codex/skills/ywc-brainstorm/evals/evals.json docs/skill-agent-eval/codex/2026-06-18-full-sweep.md
```

Expected Passing Signal:

- Touched eval files are valid JSON.
- Targeted scoring exits 0 for touched skills.
- The report records fixture additions or explicit omission reasons.

Pre-change Failing Evidence / Exception:

- The 2026-06-18 report identifies S5 fixture gaps or confirms that candidates remain evidence-limited.

Contract/Test Evidence:

- Added fixtures are objective and mechanically parseable.

## Out of Scope

- Scorer/rubric changes.
- Agent fixture harness changes.
