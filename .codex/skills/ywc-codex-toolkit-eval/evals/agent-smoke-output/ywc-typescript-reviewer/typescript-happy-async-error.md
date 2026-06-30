Fixture ID: typescript-happy-async-error
Agent: ywc-typescript-reviewer
Capture date: 2026-06-23
Source commit: 8adbd54

Status: DONE_WITH_CONCERNS

Summary: 1 finding. Critical: 1, High: 0, Medium: 0, Low: 0, Info: 0.

Critical - `src/jobs/sync.ts:31` - Async
`void pushToRemote(payload).catch(() => undefined)` creates a swallowed rejection on a user-facing sync path. The TS contract says `pushToRemote` returns `Promise<SyncResult>`, and rejection means remote persistence failed, but this call erases that failure and leaves callers with no warning, no status transition, and no way to distinguish "synced" from "local only." That is an observable correctness bug, not just missing logging.

Narrow TS-idiomatic remediation: propagate the promise result into the sync flow and model failure explicitly. For example, `await pushToRemote(payload)` in the enclosing async path and return or surface a discriminated status such as `{ ok: false, reason: "remote_sync_failed" } satisfies SyncResultLike`. If fire-and-forget is truly required, the catch must at minimum record the operation and entity identifier and update user-visible sync state to failed/pending-retry rather than resolving to `undefined`.
