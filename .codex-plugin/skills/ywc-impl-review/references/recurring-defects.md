# Recurring Real-World Defects Catalog

> Shared reference for the five `ywc-impl-review` reviewer agents. Each agent
> reads the section(s) mapped to its aspect and folds the checks into its
> Phase 1 pass. The parallel/sequential executors point `--review` at this file
> too, so the same classes are caught **before** the PR opens.

## Why this catalog exists

The per-aspect agent prompts (architecture / design / devex / security / qa)
describe review dimensions in the abstract. This catalog adds the **concrete,
high-frequency defect classes that automated PR reviewers (CodeRabbit, Codex
Review) flag again and again** in production TypeScript / SQL services. The
point is not to memorize a checklist — it is to know where real bugs cluster so
review depth lands where defects actually occur.

These patterns were distilled from a large sample of bot-review comments on
multi-tenant SaaS codebases. They are framed generally; apply the *why*, not the
literal example. A check that does not apply to the stack under review (no ORM,
single-owner, no external API) is simply skipped — note the skip, do not invent
a finding to satisfy the catalog.

**A finding from this catalog still obeys the aspect's severity rubric and the
Phase 1 / Phase 2 escalation rules.** The catalog tells you *what to look for*;
the agent prompt tells you *how confident you must be before escalating*.

## Table of contents

1. [Data-layer access-boundary & integrity](#1-data-layer-access-boundary--integrity) — Architecture + Security
2. [Error handling & external-call resilience](#2-error-handling--external-call-resilience) — Devex
3. [Contract, status & validation](#3-contract-status--validation) — Design
4. [Security specifics](#4-security-specifics) — Security
5. [Test fidelity](#5-test-fidelity) — QA

---

## 1. Data-layer access-boundary & integrity

The single highest-frequency cluster. Wherever rows are owned or partitioned by
a boundary key — `tenant_id` in a multi-tenant system, but equally `org_id`,
`user_id`, `workspace_id`, `account_id`, or `project_id` in any B2B / multi-user
app — the database is the last line of defense for that boundary, because
application-layer filtering fails open the moment one query forgets its
`WHERE <owner_key> = ?`. Multi-tenant `tenantId` is the most common instance and
appears in the examples below; **read every `tenantId` as a stand-in for whatever
ownership column the system under review actually uses**, and skip this section
entirely for genuinely single-owner or non-relational code (note the skip).

- **Ownership-scoped foreign keys.** When a child row carries its own owner key
  (`tenantId` / `orgId` / `userId`) but references a parent by the parent's `id`
  alone, the database will happily accept a child pointing at *another owner's*
  parent. Prefer a composite `(ownerKey, id)` foreign key so cross-boundary
  references are structurally impossible. This is acutely dangerous when the
  relation has `onDelete: Cascade` — a mislinked row lets one owner's delete
  reach into another's data.
- **Composite index / query lead column.** Indexes and queries on
  ownership-scoped tables should lead with the owner key. A single-column FK or a
  query that filters only by the business key both miss the ownership predicate
  and the supporting index. **Scan cue:** for every `@@index(...)` / `.index(...)`
  / `CREATE INDEX` declared on a table/model that also has an ownership column
  (`tenant_id` / `org_id` / `user_id` / `workspace_id`), confirm the owner key is
  the *leading* column. An index keyed on the business key alone (e.g.
  `@@index([campaignId])` on a table that also has `tenantId`) is a finding — it
  both weakens isolation and fails to support the owner-filtered query.
- **Explicit ownership predicate in every query.** Every read/write against an
  ownership-scoped table must include the owner-key condition explicitly — do not
  rely on an upstream filter or an ORM default scope that a future caller can
  bypass.
- **Ownership-context state reset (client).** When the active owner (tenant, org,
  workspace) changes, reset *all* owner-dependent fields, not just the key
  itself. Swapping the owner id while leaving stale `projectId` / selection state
  in the query strands the previous owner's identifiers and produces wrong or
  cross-boundary results.
- **Migration safety & referential integrity.** Prefer additive migrations with
  backfill over destructive ones. Confirm a new model cannot persist a
  contradictory parent graph (a row whose two FK paths disagree about its
  parent). Re-examine `nullable + default` columns for type-safety: a column the
  type says is non-null but the DB defaults can be subtly wrong at the boundary.
- **`NULL` is not `0`.** Do not collapse a nullable metric/aggregate with `?? 0`
  (or `COALESCE(x, 0)`) when the column is genuinely nullable. "Unobserved"
  silently becomes "measured zero", and any preview / diagnostic / billing logic
  downstream misreads a missing value as a real one. Keep `null` / `undefined`
  and let the consumer decide.

Severity guide: cross-boundary reference or cascade reaching another owner →
Critical. Missing ownership predicate on a read path → High. `NULL`→`0` collapse
→ High when it feeds billing/diagnostics, Medium otherwise.

## 2. Error handling & external-call resilience

- **No swallowing catch.** An empty `catch {}`, `catch(() => undefined)`, or
  `.catch(() => null)` erases the failure and makes the eventual incident
  un-debuggable. At minimum log a `warn` with the operation name and the
  triggering identifier; rethrow or surface unless the swallow is *deliberate
  and commented* with the reason it is safe.
- **External calls need timeout + bounded retry.** Any network call to a
  third-party API (payment, ads, mail, auth provider) without a timeout and a
  bounded retry (exponential backoff for `429` / `5xx` / transient blips) raises
  the failure rate under load and hangs the caller on a stalled socket. Flag
  unguarded `fetch` / SDK calls on a hot or user-facing path.
- **Resource lifecycle.** A client / connection / subscription that is created
  must be closed, disconnected, or unsubscribed on every exit path (including
  error paths). Repeatedly constructing an ORM client (e.g. a fresh Prisma
  instance per call) without disconnecting leaks connections until the pool
  exhausts.

Severity guide: swallowed error on a money/auth/data path → High. Missing
timeout/retry on an external call in the request path → High. Resource leak →
Medium unless it exhausts a pool under normal traffic.

## 3. Contract, status & validation

- **HTTP status semantics.** Return `4xx` for client/input faults, not `500`.
  An invalid account, a malformed payload, or an unsupported configuration is a
  `400` / `409` / `422`, not an internal error — `500` both misleads the caller
  and pollutes error budgets / alerting. Check `401` vs `403` and `200` vs `201`
  too.
- **Validation strictness & fail-fast.** Validation must actually *reject* bad
  input: a date/month regex that accepts impossible values, a parse failure
  treated as a valid result (`parse(x)` returning a default instead of an
  error), or an unsupported setting (wrong currency, wrong region) accepted and
  only failing deep in a side-effecting path. Reject at the boundary, before any
  write or external call, with an actionable message. **Scan cues:** (a) an
  external-identifier normalizer/parser (`normalizeCustomerId`, `parseAccountId`)
  that returns `null`/a default on malformed input instead of throwing — push the
  rejection to the boundary; (b) a `currency` / `region` / `locale` / `plan`
  value read and used without an up-front guard that the value is supported
  (e.g. a non-`JPY` currency must `throw` *before* the account/charge is created,
  not be discovered downstream); (c) a `new RegExp` / inline regex on a
  date/month/quantity field — check it actually excludes impossible values.
- **Non-null contract guarantees.** A field declared non-null (type, schema, or
  doc) must be *guaranteed* non-null at every construction site, not merely
  hoped for. Flag a non-null-typed value that can be reached as `undefined`.
- **URL / format contracts.** Cross-origin calls need absolute URLs; redirect
  and callback URLs must match the format the other side expects (a trailing
  slash or scheme mismatch produces a silent `400` at the boundary).

Severity guide: wrong status that breaks a client contract → High. Permissive
validation that admits invalid data to a write/external call → High. Non-null
contract gap → Medium/High by blast radius.

## 4. Security specifics

Access-boundary isolation (§1) is the dominant security theme — treat a missing
ownership predicate (`tenant_id` / `org_id` / `user_id`, etc.) as A01 Broken
Access Control / IDOR, not just a data bug. Beyond it:

- **Output escaping.** Any user- or system-supplied value rendered into HTML,
  Markdown, or a template must be escaped at the sink (a verification code, a
  name, an error string echoed back). Unescaped interpolation into an
  innerHTML-style or Markdown sink is XSS / formatting corruption.
- **No identity decisions on mutable labels.** Authorization or routing
  decisions keyed on a display name, label, or other user-editable string are
  bypassable. Key them on stable identifiers (account id, role id), not names.
- **Idempotency must be durable.** An in-process `Set` / boolean flag cannot
  prevent duplicate provisioning, double-charge, or replay across instances or
  restarts. Enforce idempotency with a durable guard — a unique constraint, a
  DB lock, or an idempotency key.
- **Supply chain & secrets.** Pin third-party GitHub Actions by commit SHA, not
  a moving tag. New secrets / env vars must be documented in the secret
  inventory and `.env.example`; a manually-managed secret silently missing from
  the deploy config fails at runtime.

## 5. Test fidelity

A passing test that does not actually exercise the code is worse than no test —
it manufactures false confidence. These are the recurring ways tests lie:

- **Mock-implementation drift.** A mock must target the symbol the
  implementation *actually calls*. If the code calls `createSearchCampaign` but
  the test mocks `deploySearchCampaign`, the `toHaveBeenCalled` assertion passes
  while testing nothing. **Scan cue:** for each `jest.fn()` / `vi.fn()` /
  `mockResolvedValue` / `spyOn(x, 'method')` in the test, find the matching call
  site in the implementation under test and confirm the method name and arity
  match. A mocked method name that appears nowhere in the implementation is a
  finding — the test exercises a method that no longer exists.
- **Test isolation.** Prefer `resetAllMocks()` / `mockReset()` over
  `clearAllMocks()` — `clearAllMocks` clears call records but *keeps* the mock
  implementation, so a `mockReturnValue` from one test bleeds into the next.
  Mutated globals (`NODE_ENV`, `process.env.*`, `IS_REACT_ACT_ENVIRONMENT`) must
  be restored to their *original captured* value in `afterEach`, never to a
  hardcoded default that diverges from the real environment.
- **Assertion currency.** When a feature, flag, or column is removed, the
  count/value assertions that referenced it must be updated. A stale assertion
  that still passes hides the regression the change introduced.
- **Strict argument assertions.** For calls that carry security- or
  correctness-critical arguments (`tenantId`, `actor`, request body), assert
  `toHaveBeenCalledWith(...)`, not just `toHaveBeenCalled()` — argument-passing
  bugs (a dropped `tenantId`) are exactly the class a presence-only assertion
  misses.
- **Placement convention.** Put test files where the project's guideline says
  (colocated next to source vs a `__tests__` directory). A misplaced test can be
  silently excluded from the run by the test glob.

Severity guide: mock drift / stale assertion that masks a real regression →
High. Isolation leak that makes the suite order-dependent → High. Placement /
strictness → Medium.
