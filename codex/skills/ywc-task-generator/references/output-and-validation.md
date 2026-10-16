# Requirement coverage and output validation

At preview generation and approved-preview consumption, enumerate every AC, FR, and present Failure Modes row
from the current spec. Emit one table row per requirement: ID, source, task(s),
verification file/scenario, and `COVERED`, `DEFERRED_WITH_REASON`, or `UNCOVERED`.
`DEFERRED_WITH_REASON` needs a reason and an explicit in-scope/out-of-scope distinction;
never silently reclassify an in-scope gap. Absence of legacy Failure Modes is valid.

Any uncovered or deferred-in-scope requirement prevents clean `DONE`. Return
`DONE_WITH_CONCERNS` with each unresolved ID. Add tasks within approved scope to
repair coverage if permitted; never execute tasks or mark them completed as a repair.
Preserve separate library-introduction and DB-migration tasks; absorb incidental
setup/config/docs into their owning deliverable.

Beside the existing terminal `Status`, emit bounded report evidence:
- current spec identity/revision and exact preview path/revision/digest;
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
