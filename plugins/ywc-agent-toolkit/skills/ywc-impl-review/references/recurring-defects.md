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

## Applying this catalog to large diffs

When a diff touches **3 or more** schema / component / model files of the
same structural shape (e.g. several ORM/DDL model definitions in one
migration, several sibling UI components implementing the same pattern), do
not "consider the catalog generally" against the diff as a whole — that
produces a single aggregate judgment that silently skips some of the changed
files. Instead, **enumerate every changed file of that shape and record a
per-file pass/fail against the applicable catalog item(s)**, the same way the
Step 2 trigger #4 complement-grep works in `ywc-plan`: list the full candidate
set, then classify each one, rather than confirming the pattern once and
generalizing.

**Output contract:** record the enumeration as one row per file —
`파일 | 적용 항목 | pass/fail 또는 skip | 근거` — inline in the aspect
agent's findings output, directly above the aggregate verdict for that
catalog item. An aggregate-only result (no per-file rows) does not satisfy
this procedure, even when the aggregate verdict happens to be correct.

This is not a hypothetical failure mode: a checklist item from this catalog
(most often an ownership/access-boundary item from §1) gets correctly applied
to one changed file in a large diff and silently skipped on a structurally
identical sibling file in the very same diff — same reviewer, same PR, same
catalog item, applied to one file and not the other. Per-file enumeration is
what catches it; a single pass over the diff as a whole does not.

## Table of contents

1. [Data-layer access-boundary & integrity](#1-data-layer-access-boundary--integrity) — Architecture + Security
2. [Error handling & external-call resilience](#2-error-handling--external-call-resilience) — Devex
3. [Contract, status & validation](#3-contract-status--validation) — Design
4. [Security specifics](#4-security-specifics) — Security
5. [Test fidelity](#5-test-fidelity) — QA
6. [Frontend reactive-effect & stale-response hygiene](#6-frontend-reactive-effect--stale-response-hygiene) — Architecture + Devex

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
- **Concurrent write / race condition safety for duplicate-sensitive flows.**
  Stock, balance, credits, quota, seats, counters, and similar shared mutable
  values must not be updated with application-level `read-modify-write` logic.
  Prefer an atomic conditional update with an affected-row check for simple
  counters, a row lock inside a transaction for complex decision logic, or an
  optimistic version check when conflicts are expected to be rare. If the system
  spans multiple stores or services, also check whether the architecture needs a
  durable idempotency guard or distributed coordination rather than relying on a
  single row lock.
- **Transaction boundary / partial write prevention.** Multi-step logical writes
  such as stock decrement + order creation, balance debit + ledger entry, or
  provisioning + entitlement write must be all-or-nothing. Flag code that writes
  one step before another without a transaction boundary, rollback-capable unit
  of work, or equivalent consistency mechanism.
- **Durable idempotency for retryable side effects.** Payment, order, and
  provisioning APIs must tolerate duplicate requests, client retries, and
  double-clicks with a durable idempotency key, unique constraint, or persisted
  request/result record. In-memory `Set` values, process-local booleans, and
  best-effort flags are insufficient for production retry paths.

Severity guide: cross-boundary reference or cascade reaching another owner →
Critical. Missing ownership predicate on a read path → High. `NULL`→`0` collapse
→ High when it feeds billing/diagnostics, Medium otherwise. Oversell,
double-charge, cross-ledger inconsistency, or duplicate provisioning → Critical.
Missing transaction on a money/order/provisioning path → High or Critical by
blast radius. In-memory idempotency on a duplicate-sensitive production retry
path → High. Missing concurrency / idempotency coverage for affected code → QA
High unless another integration test proves the same behavior.

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

## 6. Frontend reactive-effect & stale-response hygiene

Any UI layer with a reactive-effect or watcher mechanism (React's `useEffect`,
Vue's `watch`, Svelte's reactive statement, or a manually re-triggered fetch on
route/param change) can key an async fetch off an id read from
props/route/context — a stand-in for whatever identifying value the system
under review uses (an entity id, a resource slug, a selected-record key). If
the id changes again before the in-flight request resolves — a fast user
switching between entities, a rapid navigation — the resolved response is
applied to state (component state, a store, a ref) without first checking that
the response still corresponds to the *current* id. The UI then renders, or
acts on, the previous id's data as if it were the current id's data. The class
recurs because the happy-path test always waits for one fetch to settle before
switching ids, so the missing "is this still current?" guard is never
exercised. Apply the *why* — any reactive effect whose identity depends on a
value that can change before its async work resolves needs to re-validate that
identity before committing the result — not just the specific
framework/hook shown here; skip this item entirely for stacks with no
reactive-effect/watcher layer (note the skip).

**Scan cue:** grep for the stack's reactive-effect/watcher construct (whatever
it is — `useEffect`, `watch`, an RxJS subscription, a manually re-triggered
fetch) whose trigger includes an id-like value, and confirm the stale result is
blocked from reaching state by *either* comparing the resolved response
against the *current* id (read fresh at resolution time, not the id captured
in the closure at fetch-start) *or* an equivalent cancellation/generation guard
— an effect cleanup flag, `AbortController` cancellation, a request-generation
token, or subscription teardown — that prevents a superseded result from being
applied at all. A trigger keyed on an id with none of these protections at the
point the async result is applied is a finding.

**Severity guide:** the stale response drives a user-facing data-corruption or
wrong-target action (e.g. provisioning, deploying, or submitting against the
wrong entity) → High; display-only stale render with no side effect → Medium.

## Appended defect entries

### A-005: CI checkout persists the job token into a workspace that untrusted code or an artifact can read (Security / Supply chain)

`actions/checkout` writes the job's `GITHUB_TOKEN` into `.git/config` by default (`persist-credentials: true`). Any later step that runs PR-author-controllable code (install scripts, tests, E2E, build tools), can then read that token; an artifact upload can publish it only if the uploaded contents actually include the credential. The class recurs because the default is invisible in the YAML: the dangerous line is the one that is *not* written. Apply the *why* — a credential should be present only in the steps that need it — not just this one action.

**Scan cue:** for every changed workflow, enumerate each `actions/checkout` step and confirm `with: persist-credentials: false` when the job runs PR-controlled code, runs E2E, or uploads a workspace-derived artifact. A job that must `git push` afterwards needs an explicit, scoped auth step instead of the persisted default — flag the missing design, do not just flip the flag. Trace uploaded paths, hidden-file inclusion, and token permissions. If `.git/config` is absent from the artifact, that artifact exposure path is not established. Independently check whether later PR-controlled code can read the persisted token; artifact exclusion does not eliminate that code-execution path. Deterministic check: zizmor `artipacked` (its confidence is Low because real exposure depends on later steps — verify actual credential access before surfacing).

**Severity guide:** verified token exposure through later PR-controlled code or credential-bearing artifact contents → High, with the token permissions and resulting impact recorded; trusted-only/no actual exposure → Low/Medium. Workspace artifact upload alone is insufficient for High; do not confirm token disclosure when the artifact excludes the credential.

> Provenance — source: `mining`; date: `2026-10-20`; origin: `bulk mining (3 PRs, 2018-08..2026-10)` (fix diff confirmed in all 3 PRs; review-history linter report, PR #339).

### A-006: Promise not awaited, or a Promise used as a boolean condition (Devex / Security)

An async call whose result is neither awaited, returned, nor given a rejection handler loses both its failure and its ordering: the next step runs before the write finishes, and a rejection disappears. The sharper variant is a Promise in a condition — `if (!isEnabled(id)) throw …` where `isEnabled` is async. A Promise object is always truthy, so the guard never fires and an authorization or feature gate silently passes. The class recurs because the code type-checks and the happy-path test usually resolves fast enough to hide the ordering gap. Apply the *why* — any async result that a later step or a decision depends on must be awaited — not only in TypeScript.

**Scan cue:** in changed code, find calls to async functions used as statements (no `await` / `return` / `.catch`), as `void p` (which does not handle rejection), or inside `if` / `!` / `&&` / `?:` / `.filter()` predicates, and async functions passed where a sync callback is expected. A `.catch()` already present is not this finding — check instead whether ordering still matters. Deterministic check: typescript-eslint `no-floating-promises` (with `ignoreVoid: false`) and `no-misused-promises`, which need a type-aware config.

**Severity guide:** Promise used as an auth/permission/feature-gate condition → Critical; unawaited write that a later step depends on → High; fire-and-forget with a rejection handler and no ordering dependency → not a finding.

> Provenance — source: `mining`; date: `2026-10-20`; origin: `bulk mining (3 PRs, 2018-08..2026-10)` (recurrence confirmed in 3 PRs, fix confirmed in some; review-history linter report, PR #339).

### A-007: Error return value discarded instead of handled (Devex)

The return-value counterpart of §2's swallowing catch. In Go, where an error is an ordinary return value, assigning it to `_`, calling a function as a bare statement, or an unchecked type assertion (`v := x.(T)`) erases the failure with no visible `catch` to review. The class recurs because the discarded value is one character (`_`) and the code still compiles. A known misconfiguration form: the linter is enabled by name but a project-wide exclusion (e.g. golangci-lint `text: "Error return value"`) disables it entirely.

**Scan cue:** in changed Go code, grep `_ =`, `, _ :=`, `, _ =` where the dropped value is an `error`, bare call statements of error-returning functions, and single-value type assertions. In changed lint config, check for an exclusion that disables errcheck wholesale. Deliberate best-effort discards (rollback, `Close` in a cleanup `defer`) are acceptable only with a comment naming why. Deterministic check: golangci-lint `errcheck` (`check-blank`, `check-type-assertions`).

**Severity guide:** discarded error on a write / money / auth path → High; on a read path whose result is used anyway → Medium; commented best-effort cleanup → not a finding.

> Provenance — source: `mining`; date: `2026-10-20`; origin: `bulk mining (3 PRs, 2018-08..2026-10)` (omission flagged in 3 PRs, fix confirmed in some; review-history linter report, PR #339).

**Frozen port source:** `yongwoon/develop-with-llm` PR #340, merge
`2b7c54058da6f15f6c16b9aee5de021fac35f42f`,
`tools/claude-code/skills/ywc-impl-review/references/recurring-defects.md`.
The mining provenance above is upstream-reported history, not a new mining or
live-review result in this repository. Preserve the existing catalog sections.
