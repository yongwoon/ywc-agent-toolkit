# Feature oriented PR body — scenarios

## AC-10 — Changes and API table decision
1. Build a feature-only diff with supported what/location/intent; omit unsupported claims.
2. Test endpoint addition, deletion, method/path change, request/response/auth/status change, auth/schema-only change bound to a route, and internal implementation-only refactor.

Expected: Changes summarize supported feature intent/location. Method+Path rows appear only for endpoint or route-bound contract changes; internal refactor produces no API table. Rows sort deleted, changed, new; host/token/query values never appear.

## AC-10 — placement and compatibility
1. Render with the template containing Impact and with fallback templates containing neither Impact nor Design Background.
2. Update an existing PR and verify Step 7 remains skipped; test each supported output language.

Expected: API table follows Impact, otherwise body/Design Background fallback; required template sections and language remain intact; update flow preserves the Step 7 skip. Auth/schema-only route changes are included; non-route internal changes are excluded.
