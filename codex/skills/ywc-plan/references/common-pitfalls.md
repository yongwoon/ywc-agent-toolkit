# Common Pitfalls Catalog

This reference complements `ywc-plan` Step 2 (Investigate the Codebase). Skim it before writing Data Model, API Contract, or any section that touches DB / middleware / framework primitives.

Each entry is a recurring trap surfaced by `ywc-spec-validate` Critical findings — failure modes that the planner can prevent at spec-writing time if they remember to look. The catalog is intentionally stack-flavoured (NestJS / Prisma / Postgres dominate because that's the stack that produces the most validation findings in this project); add new entries as new traps surface.

## How to use this file

1. Open it at Step 2, alongside the project's instruction files (`AGENTS.md`, `CODEX.md`, `CLAUDE.md`, or equivalent).
2. For each section below that could apply to your request, run the suggested grep / file read.
3. Capture the actual behavior in the spec's **Existing Constraints Touched** section, with `file:line` citations.

Do not skip a section because "this isn't about DB / middleware". The traps are subtle precisely because they live one level below the visible feature — a "small form submission endpoint" trips at least three of these.

---

## NestJS / Express: Global vs Route-Scoped Middleware

**Trap:** `main.ts` configures global middleware (CORS, body parser, throttler, exception filter) that overrides or pre-empts any per-route configuration the spec assumes.

**Past spec-review examples (this codebase):**

- `app.use(json({ limit: '6mb' }))` set globally, but the spec assumes `32kb` on a public endpoint → multi-MB DoS attack surface
- `app.use(urlencoded({ limit: '6mb', extended: true }))` is the silent **sibling** of `json()`. Path-scoping `json()` to 32kb is not enough — `Content-Type: application/x-www-form-urlencoded` requests still flow through the global `urlencoded()` middleware at 6MB. The spec must path-scope **both** parsers (and `raw()` / `text()` if the endpoint reads those)
- `app.enableCors({ origin: FRONTEND_URL })` configured globally, but a path-conditional bypass function (`isBeaconPublicCorsPath`) short-circuits *only specific paths* → new public path is silently blocked
- Global `ThrottlerGuard` with IP-only keying, but the spec assumes composite (IP + formKey) → must subclass the guard, not just `@Throttle()`
- Global `ValidationPipe({ whitelist: true })` strips unknown fields silently, but the spec assumes 400 on unknown fields → contract drift

**Required reads at Step 2:**

```bash
# Find global middleware registration — include all body parser variants (json / urlencoded / raw / text)
grep -nE "app\.(use|enableCors|useGlobalPipes|useGlobalFilters|useGlobalGuards|useGlobalInterceptors)|express\.(json|urlencoded|raw|text)" backend/src/main.ts

# Find path-conditional short-circuits
grep -rn "isPublic\|isAnonymous\|isBypass\|isExcluded" backend/src/
```

**Capture in spec:** Every global middleware your new endpoint inherits, with the override mechanism if the spec deviates.

---

## NestJS: `@HttpCode` vs Documented Status Code

**Trap:** The controller method is decorated with `@HttpCode(202)`, but the spec body talks about returning `200`. The decorator wins at runtime; the spec is wrong.

**Required at Step 4b.5:** Every status code mentioned in the spec must trace to the same number in the API Contract. The Self-Consistency Pass (Step 4b.5) row #2 covers this.

**Capture in spec:** The exact `@HttpCode(N)` value the implementer must use, named once in the API Contract and referenced (not redefined) elsewhere.

---

## Prisma / Postgres schema invariants

The DB-side mechanical rules (bilateral relation, cascade ↔ API status, NOT NULL backfill, FK index, composite uniqueness, multi-tenant `tenantId`, enum domain, `timestamptz`) are not duplicated here. They live in the shared schema guide at [../../references/schema/core.md](../../references/schema/core.md) with stack-specific files for Prisma, SQL DDL, Drizzle, and TypeORM.

Read that file once at Step 2 whenever the spec adds, modifies, or removes DB tables, columns, indexes, or relations. The two highest-frequency Criticals — one-sided `@relation` and `onDelete: Restrict` without `409` — also appear in `SKILL.md` Step 4b.5 Pass C as inline reminders.

---

## CORS: `Allow-Credentials` with Public Endpoints

**Trap:** Spec inherits an existing CORS interceptor that unconditionally sets `Access-Control-Allow-Credentials: true`, but the new endpoint is anonymous and the spec's AC explicitly states "no credentials header". Implementer copies the interceptor verbatim and silently violates the AC.

**Required reads at Step 2:**

```bash
# Read every interceptor / middleware the spec "extends" or "follows"
grep -rn "setHeader.*Allow-Credentials\|credentials:\s*true" backend/src/ frontend/src/
```

**Capture in spec:** "Do not extend `BeaconSiteCorsInterceptor` — copy the structure only, omit `Allow-Credentials`" — with the override mechanism named (subclass, alternate interceptor, configuration flag).

---

## NestJS: Public Endpoint Inheriting Module Auth

**Trap:** A module is wrapped in `@UseGuards(JwtAuthGuard)` at the module level (or in `app.module.ts` via `APP_GUARD` provider). The spec declares a "public endpoint", but the implementer adds the controller to the module without `@Public()` decorator → public endpoint silently requires auth.

**Required reads at Step 2:**

```bash
grep -rn "APP_GUARD\|@UseGuards.*JwtAuthGuard\|@Public()" backend/src/
```

**Capture in spec:** Either route the public endpoint to a separate module without the guard, or list `@Public()` (or equivalent decorator) as a required implementation detail in the spec.

---

## KMS / Encryption: Per-Request Wrap + Unwrap Without Caching

**Trap:** Spec wraps a DEK with a KEK on every write and unwraps it on every read, with no caching layer. Concurrent reads (e.g., operator console pagination) exhaust the per-key QPS quota under modest load.

**Required at Step 2:** Note the KMS provider, key location, and current quota limits. If the spec hot-path includes unwrap, the spec must either declare a cache or accept the quota risk explicitly.

**Capture in spec:** Caching layer (in-memory LRU with TTL, or no cache + acknowledged quota assumption) under NFR or Edge Cases.

---

## Resend / Third-Party HTTP Calls: Sync vs Async + Timeout vs LB Timeout

**Trap:** Spec includes a synchronous outbound HTTP call (Resend, Stripe, etc.) inside the request path. Provider default timeout is 30s but the LB timeout is also 30s — first slow upstream tips the endpoint into LB-side `504` cascades.

**Required in spec:** Explicit timeout on the outbound call that is smaller than the LB timeout by a meaningful margin (e.g., 5s call vs 30s LB), and a fallback behavior (record status, return success without the side effect, retry asynchronously).

---

## Error Handling Discipline: Silent Swallow, Fallback, Retry Exhaustion

This is one of the most prolific Critical-finding categories. The traps below appear together — a spec that misses one usually misses all three.

### Trap A — silent error swallow in compensating cleanup

**Pattern:** Spec contains a `.catch(() => {})` (or `try { ... } catch {}`) around a compensating cleanup operation — typically a storage delete after a DB transaction rollback, an undo of a side effect, or a non-critical notification.

**Why it's a Critical:** The cleanup failure is silently consumed. DB and storage drift accumulates over weeks. Recovery is manual and the on-call engineer has no signal until the drift is noticed downstream.

**Required in spec:** Every error path that catches must specify three things:
- A structured log line (severity, error class, contextual identifiers)
- A counter / metric (e.g., `gcs_compensating_delete_failures_total`)
- An alert threshold (e.g., "> 0 / minute → Slack `#oncall`")

Never `.catch(() => {})` in the spec — even if you trust the operation. The cost of the three lines is trivial; the cost of the silent drift is unbounded.

### Trap B — undefined fallback for external-service failures

**Pattern:** Spec uses an external service (KMS encrypt/decrypt, Throttler storage backend like Redis, third-party HTTP API, OAuth provider) inside the request path but does not specify behavior when that service returns `UNAVAILABLE` / `DEADLINE_EXCEEDED` / 5xx / connection-refused.

**Why it's a Critical:** Implementer guesses. Production behavior is unpredictable and often varies by environment.

**Required in spec:** For every external dependency the request path touches, declare per-environment fallback policy:

| Decision | Required statement |
|---|---|
| Fail-open or fail-closed? | "On KMS UNAVAILABLE in prd: fail-closed, return `503 KMS_UNAVAILABLE`. In dev/stg: same. In local: in-memory sentinel key fallback (already governed by `LP_FORM_ENCRYPTION_MODE=local`)" |
| Observability | The metric / log / alert tying this failure to a counter and threshold |
| Cleanup | If the failure occurs mid-transaction, the rollback or compensating action |

### Trap C — retry without exhaustion code

**Pattern:** Spec says "retry on collision" or "retry on transient error" but does not name `max_retries`, the backoff strategy, or the HTTP code on exhaustion.

**Why it's a Critical:** Implementer defaults to infinite retry (request can hang the LB), or to retry-once-and-return-500 (no discriminating error code for the client).

**Required in spec:** For every retry loop, specify:
- `max_retries` (an integer, not "a few")
- Backoff strategy (constant / linear / exponential with jitter), or "no backoff — pure retry"
- The HTTP code on exhaustion (typically `503` with a discriminating error code, e.g., `SLUG_GENERATION_EXHAUSTED`)
- The action if the underlying constraint failure recurs after retry budget (typically log + alert)

### Trap D — DB-level race / unique violation without API mapping

**Pattern:** Spec declares a `@@unique([...])` or relies on optimistic concurrency, but the API Contract for the write endpoint omits the corresponding `409 Conflict` response.

**Why it's a Critical:** The first concurrent insert raises Prisma `P2002` (or equivalent) which surfaces as an uncaught exception → `500 Internal Server Error`, leaking the constraint name and obscuring the actual cause from the client.

**Required in spec:** API Contract for every write endpoint backed by a unique constraint must list `409 Conflict` with a discriminating error code that names the constraint (e.g., `PUBLISH_CONFLICT` for `@@unique([landingPageId])`).

### Required reads at Step 2

```bash
# Catch existing silent-swallow patterns in this project (sanity check on local convention)
grep -rnE '\.catch\(\(?[^)]*\)? *=> *\{ *\}\)|catch \([^)]*\) *\{\s*\}' backend/src/ | head -20

# Catch existing fallback patterns to mirror
grep -rn 'UNAVAILABLE\|DEADLINE_EXCEEDED\|fail-open\|fail-closed\|P2002' backend/src/ | head -20
```

### Capture in spec

For every external-dependency or retryable operation the new endpoint touches:

- An **Error Codes** subsection in the API Contract enumerating every HTTP code with its discriminating error code string
- An **Edge Cases** row per external dependency with the fallback policy (per environment if it differs)
- An **NFR** row per retry loop with the exhaustion budget and post-exhaustion behavior

The most common shape of this section is a 6-to-8-row table at the end of the API Contract — much shorter than the cost of discovering each undefined error path during implementation review.

## Audit Log: Specified by Behavior Only, Not by Schema

**Trap:** Spec says "delete writes an audit log" but does not specify what columns the audit log row contains. Implementer picks an arbitrary subset; compliance review fails 3 months later.

**Required in spec:** Audit log row shape (minimum: `{ event, entity, entityId, tenantId, actorId, actorType, occurredAt, payload }`), and storage destination (separate table, Cloud Logging, both).

---

## File Naming / Slug Conflicts

**Trap:** Spec is written at `docs/ywc-plans/lp-form-mvp.md` but the project also has `docs/specification/landing-page/lp-form-spec.md` covering overlapping scope. Two specs drift, downstream `ywc-task-generator` ingests the wrong one.

**Required reads at Step 2:**

```bash
# Find adjacent / overlapping specs
find docs/ -name "*<keyword>*" -type f
```

**Capture in spec:** A "Spec Reference" line at the top that names the upstream design doc and any sibling specs to be kept in sync.

---

## Verification Commands: Single-line grep vs Multi-line Calls

**Trap:** A grep-based Acceptance Criterion uses a single-line regex (`landingPage\.update\([^)]*generatedHtml`) to prove a write site is gone. The actual write is a multi-line `.update({ … generatedHtml … })` call, which the single-line regex cannot match. The AC passes while the write still exists — the verification command shares the exact blind spot that produced the finding.

**Past spec-review example (this codebase):** AC1's single-line `update\([^)]*generatedHtml` could not match `markDone`'s multi-line `.update({ … })`; the broad fallback grep (`grep -rn 'generatedHtml' <module>`) is what actually caught it. The single-line regex would have falsely passed.

**Required when writing grep-based ACs:**

```bash
# Prefer a broad identifier grep that is shape-agnostic …
grep -rn "<identifier>" <module>   # catches single- and multi-line call sites

# … or, if a narrow regex is genuinely needed, pair it with the broad grep
# and treat the broad grep as the authoritative zero-match check.
```

**Capture in spec:** When an AC asserts "zero match", make the authoritative check the broad identifier grep. A narrow single-line regex may accompany it as a convenience, never as the sole gate. Note the multi-line `.update({ … })` blind spot inline so the implementer does not trust the narrow regex alone.

---

## Adding to this catalog

When `ywc-spec-validate` surfaces a Critical finding that traces to a generalizable pitfall (not a one-off domain quirk), add a new entry following the template:

```markdown
## <Stack / Layer>: <Trap name>

**Trap:** <What goes wrong>

**Required reads at Step 2:**
\`\`\`bash
<grep / find command>
\`\`\`

**Capture in spec:** <What to write in Existing Constraints Touched or the relevant section>
```

The catalog earns its keep by capturing the "I would have caught this if I'd thought to look" moments. Each new entry is a small premium paid by one session to save the next ten.
