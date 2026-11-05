# Model hint metadata — scenarios

## AC-1 — tier metadata and consistency
1. Create one task with a narrow existing-pattern change, one ordinary feature slice, and one architecture-critical surface; inspect the generated README metadata.
2. Generate preview and final summary rows for the same three tasks.
3. Remove a Model Hint, use an invalid tier, mismatch the preview and README tier, or add a specialist model pin in a negative-control fixture.

Expected: each task has exactly one advisory `economy`, `standard`, or `advanced` tier plus a rationale tied to scope/criticality; preview, README, and final summary agree. Runtime model resolution and specialist pins remain outside this metadata contract.

## AC-1 — preserved boundaries
1. Inspect generator and executor routing clauses before and after the metadata change.
2. Review a fixture containing unavailable live runtime evidence.

Expected: no runtime routing redesign is implied; unavailable runtime evidence remains UNVERIFIED. This task covers Failure Mode “upstream path/locale provenance”: source references retain frozen provenance, and no missing locale is silently represented as complete.
