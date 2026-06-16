# Loop Log Schema

`ywc-spec-ready` writes an append-only markdown log so each validation/re-plan loop is auditable. Dry-run mode prints planned entries and does not write the log.

## Location

Default path:

```text
docs/ywc-plans/<slug>.spec-ready-log.md
```

The `--log <path>` flag overrides this path.

The path must be canonicalized against the repository root. Reject absolute paths, `..` traversal, paths outside the repository, and paths outside `docs/ywc-plans/` unless project guidance explicitly documents another spec/log directory.

## Entry Format

Append one section per iteration:

```markdown
## Iteration <n> — <ISO-8601 UTC timestamp>

- spec_path: `<path>`
- action: `<action>`
- validation_status: `<DONE|DONE_WITH_CONCERNS|BLOCKED|NEEDS_CONTEXT|SOCRATIC|UNPARSEABLE>`
- critical_count: `<number|unknown>`
- advisor_budget_limit: `<number>`
- advisor_calls_used: `<number|unknown>`
- advisor_budget_status: `<value parsed verbatim from the upstream ywc-spec-validate Programmatic Consumer Policy example>`
- raw_validation_report_path: `<path|N/A>`
- failure_context_summary: `<one-line summary|N/A>`
```

## Action Enum

| Action | Meaning |
|---|---|
| `initial-plan` | Goal mode generated the first spec with `ywc-plan --non-interactive`. |
| `validate` | Ran `ywc-spec-validate`. |
| `replan` | Ran `ywc-plan --update-spec` after `DONE_WITH_CONCERNS`. |
| `handoff` | Validation returned `DONE`; printed `ywc-task-generator <spec-path>`. |
| `stop-cap` | Stopped because `--max-iterations` was reached. |
| `stop-non-convergent` | Stopped because Critical trend or signatures did not improve. |
| `stop-advisor-required` | Stopped because validation required advisor escalation but budget/status prevented a deterministic result. |
| `stop-blocked` | Validation returned `BLOCKED`. |
| `stop-needs-context` | Validation returned `NEEDS_CONTEXT`. |
| `stop-unparseable` | Validation status or required headers could not be parsed. |

## Append-Only Rule

Never rewrite previous entries. If a loop is resumed manually, append a new entry that states the resumed command and current spec path.

## Parser Contract

`advisor_budget_status` must be derived verbatim from the upstream `ywc-spec-validate` Programmatic Consumer Policy machine-readable example. This file intentionally does not define a local enum.
