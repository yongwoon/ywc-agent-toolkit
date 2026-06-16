# Convergence Rules

`ywc-spec-ready` stops or continues based on validation status plus convergence evidence. These rules prevent unbounded spec churn while allowing useful amendment loops.

## Critical Trend

Track the Critical finding count for every validation iteration.

| Trend | Action |
|---|---|
| Critical count decreases | Continue when under `--max-iterations`. |
| Critical count stays flat for two consecutive iterations with similar signatures | Stop with `DONE_WITH_CONCERNS`. |
| Critical count increases | Stop with `DONE_WITH_CONCERNS`; report non-convergence. |
| Critical count reaches 0 and status is `DONE` | Print `ywc-task-generator <spec-path>`. |

Warnings do not drive non-convergence unless the validation report explicitly states that the Warning blocks `DONE` or the Warning is coupled to a Critical finding.

## Finding Signature

Create a signature for each Critical finding:

```text
<dimension>|<section-or-file-line>|<normalized-critical-summary>
```

Normalize by lowercasing, collapsing whitespace, and removing iteration-specific numbering. The signature is for convergence detection only; reports should keep the original finding text.

## Repeated Signature Guard

Stop when the same Critical signature appears in two consecutive validation reports after a re-plan. This means the amendment did not address the actual issue.

## Identical Amendment Scope Guard

Stop when two consecutive `ywc-plan --update-spec` calls would target the same spec section with materially the same failure context. Repeating the same amendment request usually produces churn rather than convergence.

## Advisor Budget Handling

`remaining_total_advisor_budget` is owned by `ywc-spec-ready`.

For every validation iteration:

```text
per_iteration_advisor_budget = min(remaining_total_advisor_budget, 2)
```

Pass that value to `ywc-spec-validate --advisor-budget <n>`.

After validation, subtract parsed advisor calls used. If parsing fails, assume the full per-iteration budget was consumed.

## Advisor Status Routing

Consume `advisor_budget_status` values verbatim from the `ywc-spec-validate` Programmatic Consumer Policy machine-readable example. This reference does not define, paraphrase, or mirror the allowed values.

Routing rules:

- Continue normal Completion Status routing when the upstream status means budget remains usable, budget is disabled, or budget was exhausted after a deterministic report.
- Stop with final action `stop-advisor-required` only when the upstream status means advisor escalation is required and the validation Completion Status is `BLOCKED` or `NEEDS_CONTEXT`.
- If the upstream status is absent or unparsable, assume the full per-iteration budget was consumed and continue only if the validation Completion Status is parseable.
