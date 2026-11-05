# Safe session handoff — scenarios

## AC-4 — seven-section handoff and redaction
1. Create a handoff containing Goal, State, Decisions, Dead ends, Next step, References, and Suggested skills, including a justified N/A section.
2. Include secrets, tokens, private material, and references to existing artifacts.

Expected: all seven sections appear, sensitive values are redacted, artifact references use paths, and the handoff does not copy full source/artifact contents unnecessarily.

## AC-4 — safe path and creation behavior
1. Create under the canonical temporary directory with a valid slug at 48 characters, an empty slug, and a too-long slug.
2. Pre-create a destination; then test symlink destination, path escape/external path, collision retry, unverifiable canonical path, and permission failure.

Expected: empty slug resolves to the session default; overlong/escaping/external/unverifiable paths are refused; existing files and symlinks are never overwritten/followed; exclusive creation uses owner-only permissions; collisions retry only within the bounded policy. Read-only agents return inline evidence while the aggregator owns artifact writes. Test every refusal/failure without creating a durable or external artifact; actual handoff generation is UNVERIFIED absent live execution.
