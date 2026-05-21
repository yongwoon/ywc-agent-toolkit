# Medium/Large Path — Spec Document Template

Use this template when `ywc-plan` Step 3 selects **Medium** or **Large** scale. The output is a markdown file under `docs/ywc-plans/<feature-slug>.md` (or the project's equivalent path).

The structure is aligned with `ywc-spec-validate`'s evaluation dimensions (Completeness, Consistency, Feasibility, Code Compatibility) so the downstream review pass has all required input.

## Structure

```markdown
# <Feature Name>

> Status: Draft
> Scale: Medium | Large
> Created: YYYY-MM-DD
> Author: <user or agent name>
> Spec Reference: <link to product/architecture doc, or `N/A — standalone feature`>

## Purpose

<2-3 sentences: What problem does this feature solve, and why now?>

## Scope

<Bulleted list of what is included.>

- <In-scope item 1>
- <In-scope item 2>

## Out of Scope

<Bulleted list of what is explicitly excluded.>

- <Excluded item 1, with reason>
- <Excluded item 2, with reason>

## Existing Constraints Touched

<Enumerate every existing piece of infrastructure that the new code will interact with — global middleware, guards, interceptors, body parsers, FK cascade rules, env-gated short-circuits, throttling defaults, exception filters. For each row, include the `file:line` citation and the **exact** behavior the new code must comply with or override.>

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `<path>:<line>` `<symbol>` | `<one-line summary of what the cited code actually does>` | `<comply / override / extend / bypass — with the named override mechanism>` |

This section exists because Code Compatibility is the largest source of `ywc-spec-validate` Critical findings, and the failure mode is always the same: the spec says "follows X" without ever transcribing what X actually does, so the implementer copies X verbatim and silently violates an AC.

Use `N/A — no interaction with existing constrained infrastructure` only after **active consideration** — i.e., you've grepped for global middleware in the new code path and confirmed nothing intercepts it.

## Acceptance Criteria

<Observable, testable conditions that prove the feature is complete. Each AC must be **declarative and verifiable** — written so a tester (human or automated) knows exactly what to send, what to observe, and how to decide pass/fail.>

Preferred form for each AC:

```
[ ] <Name>: When <trigger / input>, system does <behavior>, observable as <concrete check — status code, DB row state, response field, log entry, UI state>.
```

Examples below are written in the preferred form. The first two are generic (any project that has users, items, or scheduled state); the bracketed ones are from a past LP-form session and are included for concreteness — adapt the *shape*, not the LP identifiers.

- [ ] **AC1 — Save notification preference**: When `PATCH /api/v1/users/me/notification-preferences` is called with `{ event_type, channel, enabled }`, system upserts one row in `notification_preferences`, observable as HTTP `200 OK` with the upserted row in the response and the matching row reflecting the new `enabled` value in the DB.
- [ ] **AC2 — Order cancellation requires open status**: When `POST /api/v1/orders/:id/cancel` is called for an order with `status='shipped'`, system rejects the request, observable as HTTP `422 Unprocessable Entity` with body `{ code: 'ORDER_NOT_CANCELLABLE', currentStatus: 'shipped' }` and no change to the order row.
- [ ] *(past LP-form session)* **AC3 — Submit happy path**: When `POST /api/lp-forms/:formKey/submissions` is called with a valid body, system inserts one row in `lp_form_submission`, observable as HTTP `202 Accepted` with body `{ id: <uuid> }` and a row with `status='new'`, `encryptedPayload` non-null.
- [ ] *(past LP-form session)* **AC4 — Honeypot triggered**: When the request includes a non-empty `honeypot` field, system marks the submission `status='spam'` and skips dispatch, observable as HTTP `202` with body `{ id }` (no leak) and a row with `status='spam'`, `notifyStatus='skipped'`.

Boundary-value ACs (time windows, size limits, rate thresholds) must state inclusive/exclusive at every boundary:

- [ ] **AC5 — Trial expiry boundary**: When a user's `trial_ends_at` is read at server time `T`, the trial is considered active for `T < trial_ends_at` (**boundary exclusive — equality counts as expired**), observable as HTTP `403 TRIAL_EXPIRED` for requests issued at or after `trial_ends_at` and `200` for requests strictly before.
- [ ] *(past LP-form session)* **AC6 — Dedupe 60-second window**: When a second identical submission arrives **within ≤ 60,000ms (boundary inclusive)** of the first, system marks the second as duplicate and skips notification, observable as HTTP `202` with body `{ id, deduplicated: true }` and exactly one row with `notifyStatus='sent'` in the DB.

Any AC with a numeric boundary (`60s`, `32kb`, `5 req / minute`, `p95 < 200ms`) must answer two questions in the AC text itself: (1) is the boundary value itself included or excluded? (2) what is the unit of measurement (ms vs s, KiB vs KB, request-arrival vs request-completion)? An AC that says only "within 60s" is ambiguous — the implementer picks `<= 60000` or `< 60000` arbitrarily, the e2e test picks the other, and the dedupe behavior changes between code review and production.

Anti-patterns to avoid:

- `[ ] e2e test for golden path` — section name, not a criterion
- `[ ] form submission works` — no observable
- `[ ] response is appropriate` — no measurable threshold
- `[ ] dedupe within 60s` — boundary inclusive or exclusive? what unit? what does "within" measure from?
- `[ ] body ≤ 32kb returns 413` — `≤ 32kb` would return 200, not 413. Reverse the comparator and name the unit (KiB vs decimal KB)

## Functional Requirements

<Numbered list of behaviors the system must implement. Each requirement should be concrete enough that a task can be derived from it.>

### FR-1: <Requirement Name>

<Description. Include trigger conditions, expected behavior, and any constraints.>

### FR-2: <Requirement Name>

<Description.>

## Non-Functional Requirements

<Performance, security, scalability, accessibility constraints. Use `N/A — no NFR identified` only after active consideration.>

| Category | Requirement |
|---|---|
| Performance | <e.g., "p95 response time < 200ms"> |
| Security | <e.g., "All endpoints require authenticated user"> |
| Scalability | <e.g., "Handle 1000 concurrent users"> |

## Data Model

<New tables, columns, indexes, or schema changes. Use `N/A — no data model change` if applicable.>

**Before drafting this section, scan [schema-invariants.md](schema-invariants.md).** It enumerates the mechanical rules that produce `BLOCKED` migrations or runtime FK errors when omitted (Prisma bilateral `@relation`, FK cascade ↔ API status mapping, NOT NULL backfill, index policy). Most of them are not visible in a single-table view; they only manifest at `prisma generate` or at first delete attempt.

### Table: `<table_name>`

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `id` | uuid | no | `gen_random_uuid()` | Primary key |
| `<col>` | <type> | <yes/no> | <default> | <notes> |

### Migration Notes

<Backfill strategy, downtime expectations, rollback plan.>

## API Contract

<New or modified endpoints. Use `N/A — no API contract change` if applicable.>

### `POST /api/v1/<resource>`

**Request:**

```json
{
  "field1": "string",
  "field2": "number"
}
```

**Response (200):**

```json
{
  "id": "uuid",
  "field1": "string"
}
```

**Errors:**

| Status | Condition | Body |
|---|---|---|
| 400 | <validation failure condition> | `{ "error": "..." }` |
| 401 | Unauthenticated | `{ "error": "Unauthorized" }` |
| 422 | <business-rule violation> | `{ "error": "..." }` |

## Edge Cases

<Boundary conditions, error states, race conditions the implementation must handle.>

- **<Edge case 1>**: <Expected behavior>
- **<Edge case 2>**: <Expected behavior>
- **<Empty / null / unicode / large input>**: <Expected behavior>

## Dependencies

<External services, libraries, or upstream features required.>

- <Dependency 1>
- <Dependency 2>

(Use `N/A — no external dependencies` if applicable.)

## Open Questions

<Items the spec cannot answer yet. Block implementation until resolved.>

- [ ] <Question 1 — who can answer?>
- [ ] <Question 2 — what decision is needed?>

(Use `N/A — none identified` only after active consideration.)

## References

- <Link to product doc, related spec, or external standard>
- (Use `N/A — standalone spec` if applicable.)
```

## Worked Example (Abbreviated)

For a request like *"Add a settings page that lets users configure notification preferences"* (Medium scale):

```markdown
# User Notification Preferences

> Status: Draft
> Scale: Medium
> Created: 2026-05-01

## Purpose

Users currently receive all notifications by default with no opt-out. This causes noise and a measurable churn signal in our retention metrics. Adding per-channel preferences gives users control and reduces unsubscribe-from-all rate.

## Scope

- Settings page UI for notification preferences
- Per-channel toggles: email, push, in-app
- Per-event-type granularity: comments, mentions, follows, system announcements
- Default state for existing users: all channels enabled (preserve current behavior)
- Default state for new users: email + in-app enabled, push prompted on first login

## Out of Scope

- SMS notifications — separate spec, separate vendor decision
- Notification scheduling (quiet hours, timezone) — Phase 2
- Admin override for system announcements — orthogonal feature

## Acceptance Criteria

- [ ] User can toggle notification preferences per channel and event type
- [ ] Preferences persist across sessions
- [ ] Notification dispatcher respects preferences before sending
- [ ] Default state applied correctly for new and existing users
- [ ] Settings page is keyboard-accessible (WCAG AA)

## Functional Requirements

### FR-1: Settings Page UI

A new route `/settings/notifications` displays a table of event types × channels with checkbox toggles. Save button persists changes via `PATCH /api/v1/users/me/notification-preferences`.

### FR-2: Preferences Storage

A new table `notification_preferences` stores `(user_id, event_type, channel, enabled)`. Default state for existing users is backfilled by migration.

### FR-3: Dispatcher Integration

Existing notification dispatcher reads `notification_preferences` before sending. If no preference row exists, fall back to default-by-event-type.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | Preferences lookup must be cached; dispatch latency increase ≤ 5ms |
| Security | Users can only modify their own preferences |
| Migration | Backfill existing users without downtime |

## Data Model

### Table: `notification_preferences`

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `id` | uuid | no | `gen_random_uuid()` | Primary key |
| `user_id` | uuid | no | — | FK to `users.id`, cascade delete |
| `event_type` | text | no | — | Enum: `comment`, `mention`, `follow`, `system` |
| `channel` | text | no | — | Enum: `email`, `push`, `in_app` |
| `enabled` | boolean | no | `true` | — |
| `updated_at` | timestamptz | no | `now()` | — |

Composite unique index on `(user_id, event_type, channel)`.

### Migration Notes

Backfill: insert `(user, event, channel, true)` for every existing user × every event_type × every channel — preserves current "all on" behavior.

## API Contract

### `GET /api/v1/users/me/notification-preferences`

Returns array of preference rows for the authenticated user.

### `PATCH /api/v1/users/me/notification-preferences`

Accepts array of `{event_type, channel, enabled}`. Upserts each row.

## Edge Cases

- **User updates preferences while a notification is mid-dispatch**: dispatcher reads at send-time, not enqueue-time — accept this small race
- **Event type added in the future**: dispatcher falls back to default-by-event-type for missing rows
- **Bulk preference toggle (all off)**: still allow — no special-case UI

## Dependencies

- N/A — uses existing dispatcher and existing UI framework

## Open Questions

- [ ] Should "system announcements" be opt-out-able, or always on for security/compliance reasons? (Decision needed from product)

## References

- `docs/product/retention-metrics-2026-q1.md`
```

## Slug Naming for the Spec File

Derive the slug from the feature name:

- `User Notification Preferences` → `notification-preferences.md`
- `Add SSO with Google` → `sso-google.md`
- `Refactor email-sending utility to use a queue` → `email-queue-refactor.md`

Slug rules: lowercase, hyphens only, ≤40 characters, no `and` (use a unifying noun). Aligns with `ywc-task-generator` task naming conventions.
