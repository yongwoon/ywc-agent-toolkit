# Loop Log Schema

`ywc-spec-ready` writes an append-only loop log (default
`<spec-dir>/<slug>.spec-ready-log.md`, override with `--log`). One entry per
iteration, never rewrite prior entries. The log is the audit trail for cost
(advisor calls), convergence (Critical trend, signatures), and the final action.

## Entry fields

| Field | Required | Notes |
|---|---|---|
| `timestamp` | yes | ISO-8601 UTC of the iteration end |
| `spec_path` | yes | The `--spec` path |
| `iteration` | yes | 1-based; paired with `max` (`--max-iterations`) |
| `status` | yes | `ywc-spec-validate` Completion Status: `DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT` / `SOCRATIC` / `UNPARSEABLE` |
| `critical_count` / `warning_count` / `suggestion_count` | yes | From the report Summary |
| `advisor_calls_used` / `advisor_remaining` | yes | Parsed from `Phase 2 advisor calls used: X of N`; on parse failure assume the per-iteration cap consumed |
| `finding_signatures` | yes | Normalized signatures for this iteration (recurrence detection; see convergence.md) |
| `action` | yes | One of the 9 values below |

## `action` enum (9 values)

| action | Meaning |
|---|---|
| `replan` | DONE_WITH_CONCERNS, guards passed → re-plan and continue |
| `handoff` | DONE → handoff printed, loop ended |
| `stop-cap` | Iteration cap reached without DONE |
| `stop-non-converging` | A stall guard fired (non-decreasing / repeated signature / identical scope) |
| `stop-advisor-exhausted` | Advisor budget exhausted and a mandatory ambiguous Critical remains |
| `stop-blocked` | spec-validate returned BLOCKED or report unparseable |
| `stop-context` | spec-validate returned NEEDS_CONTEXT |
| `stop-replan-failed` | `ywc-plan --update-spec` call itself failed (file vanished / error) |
| `stop-misuse` | spec-validate returned SOCRATIC, or other misuse |

## Markdown entry shape

```markdown
## Iteration <N>/<max> — <ISO-8601 UTC>
- spec: <spec_path>
- status: <status>
- findings: Critical <c> / Warning <w> / Suggestion <s>
- advisor: used <X> / remaining <R>
- action: <action>
- signatures:
  - <severity> <pointer> — <first-sentence>
```

`--dry-run` writes no log entry. A hard stop (Step 3) still writes its iteration
entry with the terminal `action` before the Completion Report.
