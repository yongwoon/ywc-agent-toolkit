# Handoff

Verify created-handle identity, regular type, expected owner and mode `0600` before any content write. Failure permits no content write or chown; empty or incomplete cleanup requires both creation-identity proof and a verified expected-owner match. Preserve post-write/close verification.

The expected owner is the effective UID/user of the authorized aggregator process that exclusively creates the file. Compare ownership against that identity; if it cannot be determined or does not match, return `NEEDS_CONTEXT` without chown or touching a file of uncertain ownership.

Save a concise temporary Markdown handoff from the current conversation and explicitly pasted or attached artifacts. Do not search session logs, open mentioned paths/URLs, or copy existing artifacts; reference artifacts by path only and redact credentials, tokens, personal data and unrelated private material.

Include Goal, State, Decisions, Dead ends, Next step, References and Suggested skills in order. Empty sections use `N/A — <reason>`; do not invent state or decisions. Read-only agents return inline evidence; only the authorized aggregator writes. Owner/input/output/status mismatch returns `NEEDS_CONTEXT`.

Use the canonical `${TMPDIR:-/tmp}` root and a verified stable directory handle. The basename uses `ywc-handoff-`, a timestamp, normalized `[a-z0-9-]` slug and unique suffix. Trim end hyphens; empty becomes `session`; reject normalized slugs longer than 48 characters. Refuse external/escaping/unverifiable paths. Create exclusively with no-follow semantics and mode `0600`; never overwrite existing files or symlinks. Retry only name collisions, five attempts total. Permission or write failures stop without a success claim; clean up only a file proven to be newly created by this operation.

Report `DONE` and the path only after identity, owner, permissions and complete redacted content are verified. Temporary files are not automatically deleted. Moving to durable storage requires an explicitly approved destination.

Use: `Use $ywc-handoff to save a concise handoff for this session.`

`allow_implicit_invocation: false` prefers explicit invocation; it does not guarantee runtime enforcement. Evals and source fixtures verify instructions only; live model/tool/filesystem behavior remains `UNVERIFIED` without safe isolated execution.
