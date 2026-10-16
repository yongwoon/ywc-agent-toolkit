# Convergence Rules

`ywc-spec-ready` stops or continues based on validation status plus convergence evidence. These rules prevent unbounded spec churn while allowing useful amendment loops.

## Blocking Trend

`ywc-spec-ready` treats Critical and Warning findings as blocking (see `SKILL.md`), so track the blocking count (Critical + Warning) for every validation iteration. Suggestions are never part of this count.

| Trend | Action |
|---|---|
| Blocking count decreases | Continue when under `--max-iterations`. |
| Blocking count stays flat for two consecutive iterations with similar signatures | Stop with `DONE_WITH_CONCERNS`. |
| Blocking count increases | Stop with `DONE_WITH_CONCERNS`; report non-convergence. |
| Blocking count reaches 0 and status is `DONE` | Print `ywc-task-generator <spec-path>`. |

## Finding Signature

Create a signature for each Critical or Warning finding:

```text
<severity>|<dimension>|<section-or-file-line>|<normalized-summary>
```

Normalize by lowercasing, collapsing whitespace, and removing iteration-specific numbering. The signature is for convergence detection only; reports should keep the original finding text.

## Repeated Signature Guard

Stop when the same Critical or Warning signature appears in two consecutive validation reports after a re-plan. This means the amendment did not address the actual issue.

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

## Single Suggestion allowance

The owner is Step 7 of `ywc-spec-ready/SKILL.md`. Explicit user instructions and
apply/defer override the default; with no blocking findings and Suggestions present,
at most one amendment/revalidation is attempted in either mode. No Suggestions
means no pass; explicit defer means no amendment. Residual advisory Suggestions
never restart this allowance or create another prompt/missing-policy status.
New Critical/Warning findings return to the existing bounded blocking convergence
with no ready handoff; limits and malformed-evidence failures remain effective.
