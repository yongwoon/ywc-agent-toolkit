# Manual Test Plan — yw-000019-020-domain-mine-review-history-skill

## Scenario 1: Bounded scope is required

### Steps
1. Invoke the skill without `--limit` or `--since`.
2. Invoke it with `--since 2026-09-01`.

### Expected Result
The first invocation asks for a scope. The second uses the default limit of 200 and reports the inclusive UTC date boundary.

## Scenario 2: Confirmation precedes every write

### Steps
1. Run a bounded mining request that produces project-local candidates and a threshold-reaching catalog candidate.
2. Inspect the complete proposed changeset before responding.
3. Decline confirmation.

### Expected Result
The report includes cluster, classification, recurrence, PR provenance, target, and text. No project learning or shared catalog file is modified.

## Scenario 3: Conservative evidence handling

### Steps
1. Supply comments with resolved threads and later matching patch hunks.
2. Supply comments with null/outdated anchors, renamed paths, unrelated hunks, unavailable pagination, and ambiguous replies.

### Expected Result
Only comments with both required evidence paths become `DO`; explicit human dismissals become `FALSE-POSITIVE`; unavailable or ambiguous evidence is dropped and accounted for.
