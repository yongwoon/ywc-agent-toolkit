# Requirement coverage and output validation

For preview generation, direct generation, and approved-preview consumption,
enumerate every AC, FR, and present Failure Modes row from the current spec.
Emit one table row per requirement: ID, source, task(s),
verification file/scenario, and `COVERED`, `DEFERRED_WITH_REASON`, or `UNCOVERED`.
`DEFERRED_WITH_REASON` needs a reason and an explicit in-scope/out-of-scope distinction;
never silently reclassify an in-scope gap. Absence of legacy Failure Modes is valid.

Any uncovered or deferred-in-scope requirement prevents clean `DONE`. Return
`DONE_WITH_CONCERNS` with each unresolved ID. Add tasks within approved scope to
repair coverage if permitted; never execute tasks or mark them completed as a repair.
Preserve separate library-introduction and DB-migration tasks; absorb incidental
setup/config/docs into their owning deliverable.

Beside the existing terminal `Status`, emit bounded report evidence:
- current spec identity/revision;
- exact preview path/revision/digest when a preview flag is used; omit preview identity on the direct-generation path;
- covered, deferred-in-scope, and uncovered integer counts;
- deduplicated unresolved requirement IDs (union of deferred-in-scope and uncovered).
Counts, IDs and coverage rows must agree and account for every enumerated requirement.
Explicit out-of-scope deferrals retain their reason/table row but are not unresolved
in-scope counts. No unresolved IDs with zero unresolved counts, or missing IDs with
positive counts. Bind the summary to this call, not a prior preview.

This is report evidence only: no checkpoint field, handoff schema, or planner/ready
Result extension. Preserve preview approval/path/digest checks and write boundaries;
a clean coverage summary is not approval evidence. Preview-only still writes no tasks.

For an explicitly declared owned public interface, compare consumed names and
signatures against its owner declaration. Report mismatches with both producer and consumer evidence.
Do not invent signatures for prose-only dependencies; record missing contract
evidence when correctness depends on it. Each task maps covered AC IDs to verification
files/scenarios. Existing tests may use a documented mapping instead of inline comments.
Command-bearing AC baselines remain recorded evidence or explicit unmeasured gaps;
validation never executes commands copied from the input spec.

## Model Hint consistency

The preview table and final task list summary must include a `Model Hint` column for every task, organized by phase with Task ID and Title. Direct generation must include the hint in each README and the final summary without requiring a preview table.

Copy the same tier and rationale into the preview, generated README, and final summary; do not infer a different hint during consumption. Direct generation must use one validated value in its README and final summary.
Validate each task against the canonical tiers in
[task-metadata-rules.md](task-metadata-rules.md) before persisting a preview or
writing directly, and again before consuming an approved preview. An unresolved metadata mismatch
must not trigger re-decomposition, silent preview repair, or partial task writes;
preserve the existing preview identity/digest and approval gates.

Missing or duplicate hints, invalid tiers, empty or unsupported rationales, model-ID pins, and preview/README/summary mismatches fail validation and return `NEEDS_CONTEXT` before preview or task-artifact writes.
Do not report clean DONE for a failed hint check. Keep hint validation independent
of the conditional Quality Gate Contract and preserve existing Status semantics.

Unavailable live runtime evidence is `UNVERIFIED — instruction contract only`; source assertions and expected traces are not live model behavior.
