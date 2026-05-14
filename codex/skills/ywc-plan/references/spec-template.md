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

## Acceptance Criteria

<Observable, testable conditions that prove the feature is complete.>

- [ ] <Criterion 1>
- [ ] <Criterion 2>

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
