Fixture ID: performance-happy-query-plan
Agent: ywc-performance-engineer
Capture date: 2026-06-23
Source commit: 8adbd54

Status: DONE_WITH_CONCERNS

Summary: 1 High finding, 0 Medium, 0 Low.

1. High - Backend-Query - api/report.ts:88
   observed metric vs target: p95 latency is 2400 ms vs 500 ms target.
   Evidence: the request path loads all report rows, then filters in memory by `workspace_id`. The query plan shows a sequential scan across 2.4M rows with no leading `workspace_id` predicate, so the database does unnecessary I/O and the API also pays application-side filtering cost.
   Remediation: push the `workspace_id` filter into the SQL/ORM query so row elimination happens in the database, and shape the access path around that predicate. The effective fix is:
   - add `WHERE workspace_id = ?` at query time rather than post-fetch filtering
   - ensure an index exists with `workspace_id` as the leading column, extended by common sort/filter columns if this endpoint uses them
   - select only required columns and apply pagination/limit before materialization

Impact: this is the dominant latency risk in the scoped backend path and is consistent with the sequential scan evidence. Until the predicate is pushed down, the endpoint will scale with table size rather than workspace-local cardinality.
