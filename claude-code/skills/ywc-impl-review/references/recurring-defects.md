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
7. [Appendix — mined entries](#appendix--mined-entries) — Devex + Security

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

### Write consistency under concurrency

Integrity is not only about *who* may touch a row (ownership) but *whether
concurrent writers corrupt it*. Shared mutable values and multi-step writes are
the recurring gap here.

- **Concurrent write safety.** Shared mutable values (stock / balance / credits
  / quota / seats / counter) must not be updated with an application-level
  `read → modify → write` — two concurrent requests both read the old value and
  the second overwrites the first's change (lost update / oversell). Depending on
  logic complexity, use one of: an atomic conditional update (`UPDATE ... SET
  stock = stock - 1 WHERE id = ? AND stock >= 1`, then check the affected-row
  count), a row lock (`SELECT ... FOR UPDATE`), or an optimistic version check
  (`WHERE version = ?` + version bump).
- **Transaction boundary.** Multi-step logical writes (stock decrement + order
  create, balance decrement + ledger record) must be all-or-nothing — wrap them
  in one transaction so a mid-flow failure rolls back every step, never leaving a
  decremented balance with no ledger row.
- **Durable idempotency (cross-reference).** For retryable side effects, see §4
  [Idempotency must be durable](#4-security-specifics).
- **Scan cue:** Local/sequential green tests are not evidence of concurrency
  safety — surface a finding when shared mutable-value writes lack an atomicity
  mechanism.

Severity guide: oversell / double-charge / cross-ledger corruption → Critical;
money / order / provisioning transaction-boundary gap → High or Critical by blast
radius; duplicate-sensitive idempotency kept only in in-memory state → High;
absence of a concurrency test for code with these hazards → QA axis, High (unless
another integration test already proves the safe behavior).

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

## Appendix — mined entries

A-001–A-004: exist only upstream, not ported.

These entries come from bulk mining of review history for Issue #69 and keep their upstream IDs for cross-reference.

Entry IDs use an `A-` prefix with a zero-padded counter (`A-001`, `A-002`, …) so appended entries never collide with the §1–§6 numbering and the append-only nature is visible at a glance.

### A-005: CI checkout persists the job token into a workspace that untrusted code or an artifact can read (Security / Supply chain)

`actions/checkout` writes the job's `GITHUB_TOKEN` into `.git/config` by default (`persist-credentials: true`). Any later step that runs PR-author-controllable code (install scripts, tests, E2E, build tools), or any step that uploads the checked-out directory as an artifact, can then read or publish that token. The class recurs because the default is invisible in the YAML: the dangerous line is the one that is *not* written. Apply the *why* — a credential should be present only in the steps that need it — not just this one action.

**Scan cue:** for every changed workflow, enumerate each `actions/checkout` step and confirm `with: persist-credentials: false` when the job runs PR-controlled code, runs E2E, or uploads a workspace-derived artifact. A job that must `git push` afterwards needs an explicit, scoped auth step instead of the persisted default — flag the missing design, do not just flip the flag. Deterministic check: zizmor `artipacked` (its confidence is Low because real exposure depends on later steps — confirm the later step exists before surfacing).

**Severity guide:** PR-triggered job that runs PR-controlled code or uploads the workspace → High; trusted-branch-only job with no artifact upload → Low/Medium.

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

### A-008: Behavior changed, but a surface that describes it still states the old contract (Design / Contract)

A change to a flag, default, output format, path convention, or status set lands in the implementation, while the README (and its translations), the arguments table, the usage/help text, the integration notes for callers, or the validation checklist still describe the previous behavior. Real cases: a script that now writes a heading *and* a `Completed:` line while the docs say only the heading remains; a CLI mode added to the script but missing from the README and the tool inventory; a default that applies only on a fresh run but is documented as also applying on resume; a docs sentence that says fixtures "verify behavior" when the validator only checks a static contract. The class recurs because the diff author edits the file that runs and forgets the files that *describe* it — those are not executed, so no test fails. Downstream readers (users, calling code, other agents) then follow a wrong contract. Apply the *why* — every description of a behavior is part of its contract — not only for Markdown docs.

**Scan cue:** for each changed flag, option, default, output shape, file path, or enum value, grep the repository for its old and new spelling and list every surface that mentions it (README and locale variants, `--help`/usage strings, argument tables, caller docs, checklists, changelog/upgrade notes); each surface still stating the old behavior is a finding. A surface that never described the changed detail is not a finding, and a wording preference with no factual mismatch is not a finding. No general-purpose linter detects prose drift; a project-specific test that diffs `--help` output against the docs is the only deterministic check.

**Severity guide:** a caller-facing contract (path, flag, status, output field) described wrongly so a consumer will break or mis-route → High; user-facing docs that mislead about options or defaults → Medium; descriptive wording that overstates scope without changing what a reader does → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 18 PRs; yongwoon/develop-with-llm).

### A-009: Normative rule restated in several places instead of defined once and referenced (Architecture / Design)

A rule that other parts of the system must obey — a routing threshold, a gate condition, a payload schema, a severity rubric, a status contract — is defined in one canonical place and then paraphrased, partially copied, or re-derived at each consumer. The copies drift: one consumer dispatches at `< 70` while the canonical gate says `≤ 50`; an output placeholder omits a route the routing table defines; a prompt re-implements a subset of a catalog and silently applies different detection criteria; a newly added dispatch site never applies the rule at all. The class recurs because copying a few lines feels cheaper than linking, and each copy looks correct at the moment it is written. Apply the *why* — a rule should have exactly one authority, and every other site should point at it or quote it verbatim — whether the "rule" lives in docs, config, constants, or code.

**Scan cue:** when a diff adds or edits a threshold, enum, schema, or decision rule, search for other sites that state the same rule (same numbers, same status names, same field list) and compare them literally. A paraphrase that differs in a boundary (`<` vs `≤`), omits a case, or lacks a link back to the canonical source is a finding; so is a new consumer site that should apply the rule and does not. A consumer that links to the canonical source and adds only invocation-specific context is not a finding. In code, the deterministic fix is a shared constant/schema imported by every consumer; no linter detects duplicated prose rules.

**Severity guide:** a divergent copy that changes routing, gating, or a security/severity decision → High; a partial copy that omits a case but does not yet contradict → Medium; duplicated but currently identical text with no link → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 13 PRs; yongwoon/develop-with-llm).

### A-010: Path or link resolves only from the author's working directory (Devex)

A script invocation, an import of a sibling helper, or a relative Markdown link is written against the location the author happened to run it from — usually the repository root — rather than the location where the file is actually used. It breaks once the code is installed elsewhere (a user's home config directory, a published package, a container image), invoked from a different working directory, or the link is rendered from the document's own directory. Real cases: a shell wrapper calling `python3 tools/.../parser.py` that fails whenever the caller's cwd is not the repo root, although a sibling script already computes `SCRIPT_DIR`; a parent-relative (`../`) reference link that resolves one directory too high; an inventory table that claims "paths are repo-root relative" but lists a path that does not exist from the root. The class recurs because the author's own environment always matches the assumption. Apply the *why* — resolve paths relative to the file's own location or an explicitly documented root — not only for shell scripts.

**Scan cue:** for each new relative path in a script, resolve it from the script's own directory (`"$(dirname "$0")"`, `Path(__file__).parent`, `import.meta.url`) and check that the code does so instead of relying on cwd; for each new relative Markdown link, resolve it from the linking document's directory and confirm the target exists; for docs that declare a path base, check every listed path against that base. An absolute path that is intentionally environment-specific and documented is not this finding. Deterministic checks: a link checker such as `lychee` or `markdown-link-check` for Markdown links; for scripts, running the entry point from a different cwd in CI.

**Severity guide:** an installed or shipped entry point that fails outside the repo root → High; a broken link to a normative/canonical document → Medium; a broken link in illustrative prose → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 11 PRs; yongwoon/develop-with-llm).

### A-011: Variable or untrusted value interpolated into a command string, or a file list split on whitespace (Security)

A value from user input, an issue/comment body, a branch name, or a file list is pasted into a shell command, a JSON literal, or an `eval`'d string instead of being passed as a separate argument. Quotes and metacharacters in the value then change the command boundary (command substitution, an injected option, a broken JSON payload). The quieter sibling is whitespace splitting: `git diff --name-only | xargs grep` or `for f in $files` splits `new file.tf` into two paths, so a gate silently skips the file, and a path starting with `-` is read as an option. A test variant: storing argument cases in a string (`args="--branch 'bad..branch'"`) and expanding `$args` passes literal quote characters, so the test never exercises the intended value. The class recurs because the happy-path value has no spaces or quotes. Apply the *why* — data must never be parsed as code or split by the shell — in every language that builds commands.

**Scan cue:** in changed scripts and command examples, find `eval`, unquoted `$var` / `$(...)`, a placeholder like `<branch>` or `'<body>'` substituted into a command line, JSON assembled by string concatenation, `subprocess` / `exec` with `shell=True` and an interpolated value, and newline/whitespace-delimited file lists piped to `xargs` or a `for` loop. The fix shape is argv arrays, `"$var"` quoting plus `--` option terminators, `jq --arg` / `--input -` for JSON, and NUL-delimited lists (`git ... -z | xargs -0`, kept in a file rather than a shell variable, which drops NULs). A value already validated against a strict allowlist (e.g. a numeric ID) is lower risk but still should be quoted. Deterministic checks: ShellCheck (SC2086, SC2046 and related quoting warnings); Bandit B602/B604 for `shell=True` in Python.

**Severity guide:** attacker-controllable text (issue/PR/comment content, external input) reaching a shell or `eval` → Critical; internal values that can contain spaces or quotes causing a gate to skip files → High; quoting gaps in a test harness that make a case vacuous → Medium.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 8 PRs; yongwoon/develop-with-llm).

### A-012: Path trusted without canonicalization, symlink rejection, or a private temp location (Security)

Code that reads or writes inside a boundary (the repository, a project directory, an allowed input root) checks the path lexically and then follows it. A symlink inside the boundary pointing outside it passes the check, so a scanner, validator, or inventory reads external files into its evidence, or a writer overwrites an external target. Related defects in the same fixes: `is_file()` / `-x` / `is_dir()` follow symlinks, so a symlinked or non-regular candidate (an executable *directory* passes `-x`) is accepted and a valid fallback is skipped; a test writes to a fixed name in a shared temp directory, so parallel runs collide and a pre-planted symlink redirects the write. The class recurs because test fixtures contain only regular files. Apply the *why* — decide containment on the resolved path and refuse anything that is not a regular file you created or expect — in any language.

**Scan cue:** for each new path read/write at a trust boundary, check that the code (a) resolves the final path (`realpath`, `Path.resolve()`, `os.path.realpath`) and verifies it is under the resolved root, (b) rejects symlinks where they are not expected (`lstat`/`is_symlink()`, `test -L`) and non-regular files (`-f`, `S_ISREG`), and (c) creates temp files with an unpredictable name (`mktemp`, `tempfile.mkstemp` / `TemporaryDirectory`) rather than a fixed name under `/tmp`. A path that is a hard-coded constant inside a directory the process created itself is not a finding. Deterministic check: Bandit B108 flags hard-coded temp paths in Python; no common linter catches missing symlink containment.

**Severity guide:** a write that can follow a symlink outside the boundary, or a read whose content is published/posted → High; a read that only pollutes local evidence or a report → Medium; fixed temp names in tests only → Low/Medium.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 7 PRs; yongwoon/develop-with-llm).

### A-013: Hard-coded count, version, or aggregate not recomputed after the list changed (Design / Contract)

A literal that summarizes a list — "55 skills", "4 Tier-1 workers", a fixture count, a `below_70: 1` aggregate, a "current version" line, a score band label — is left as is when an item is added, removed, archived, or corrected. Real cases: a catalog table gains a row while the header count stays; an archived component disappears from the roster but two sentences still count it; a `VERSION` file is bumped while the README's version line is not; a recorded aggregate disagrees with the corrected per-item scores in the same change; a numeric claim cites evidence that yields a different number. The class recurs because the number lives far from the list it summarizes, and nothing executes it. Apply the *why* — derive summaries from the source, or update every literal copy in the same change — for docs, fixtures, and stored metrics alike.

**Scan cue:** when a diff adds or removes an entry from a list, table, roster, fixture set, or version file, grep for numeric literals and version strings that describe that collection and recount them against the actual list after the change; also check that a stored aggregate equals the recomputation from its own per-item records and that a cited number matches its cited evidence. A count that is computed at build/render time is not a finding. Deterministic fix: generate the number (a script or a CI check that compares the literal with the counted list); no generic linter exists.

**Severity guide:** a wrong aggregate that drives a gate, baseline, or release decision → High; a stale version string shown to users → Medium; a stale descriptive count in docs → Low/Medium.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 7 PRs; yongwoon/develop-with-llm).

### A-014: Configurable location resolved once, then a hard-coded default used on some paths (Architecture / Devex)

A command accepts an override for where it works — a `--tasks-dir`, an output directory, a worktree path, a namespace prefix — and resolves it at the top, but some later read, write, move, or report step still uses the literal default (`tasks/completed/<id>/`) or the main checkout path. With the default, everything works; with an override, reads and writes split across two locations: a script updates the graph in the main checkout while `git add` stages the untouched copy in the worktree, or a ledger is read from one place and written to another. The class recurs because tests and examples almost always run with the default. Apply the *why* — once a location is configurable, every path derived from it must go through the resolved value — in code, scripts, and step-by-step procedures.

**Scan cue:** for each configurable location in the change, grep for its default literal (and for paths built from the cwd) across every step that reads, writes, moves, deletes, stages, or reports, and confirm each uses the resolved variable. Pay special attention to "secondary" steps such as `mkdir`, `mv`, cleanup, and the paths printed in the final report. A default used only to *compute* the resolved value is not a finding. No deterministic linter; a test that runs the flow with a non-default location is the reliable check.

**Severity guide:** writes or deletes landing in the wrong checkout/directory, or a commit staging a stale copy → High; reads that miss artifacts so a step reports "not found" → Medium; a report that prints the default path while the work used the override → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 6 PRs; yongwoon/develop-with-llm).

### A-015: Scan or gate sees only tracked/staged changes and misses new untracked files (QA / Devex)

A pre-commit gate, completeness/stub scan, secret check, or "what changed" detector enumerates files with `git diff --name-only HEAD`, `git diff --cached`, or `git ls-files`. None of those list untracked new files, so the very files a feature adds — the most likely to contain a `TODO`, a stub, or a hard-coded secret — are skipped and the gate reports clean. Edge variants in the same fixes: a root commit has no `HEAD^`, so the diff fails and `|| true` hides it; an empty commit range (`HEAD..HEAD`) returns "clean" before the working tree is checked. The class recurs because the author's test edits an existing tracked file. Apply the *why* — a gate must enumerate the full set it claims to protect, including new and uncommitted files — for any VCS-driven check.

**Scan cue:** for each new gate or scan driven by git, check how the file list is built: it should union tracked changes with `git ls-files --others --exclude-standard` (and, where the gate's contract says so, ignored generated files), handle a repository with no parent commit, and not short-circuit on an empty range before checking the working tree. A gate explicitly documented as "committed changes only" that runs after commit is not a finding. Deterministic check: a fixture test that creates an untracked file with a known pattern and asserts the gate flags it.

**Severity guide:** a secret or security gate that skips untracked files → High; a completeness/stub gate that can pass with stubs in new files → Medium/High by what it blocks; an informational notice that misses root-commit changes → Low/Medium.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 6 PRs; yongwoon/develop-with-llm).

### A-016: Markdown/structured-text parser matches markers inside fenced code blocks (Devex / QA)

A hand-written parser applies a heading regex, a section-end check, a tag matcher, or a fence counter to every line, so an example `## Heading` or `</details>` inside a fenced code block is treated as real structure. Real cases: a validator rejects a correct README because a heading inside a code sample mismatches; a section body ends early at an example heading; an "already has a `## Scope Paths` section" check finds one inside a code sample and skips adding the real section; a renderer closes a disclosure at a `</details>` string inside code; a "exactly one fenced block" check recognizes only column-0 triple backticks, so an indented or longer fence slips past. The class recurs because test inputs rarely contain code samples that look like structure. Apply the *why* — track lexical context before matching structural markers — for any line-based parser of nested formats.

**Scan cue:** for each new line-based Markdown (or similar) parser, check that it tracks fence state — opening char (backtick or tilde), fence length, and up to three spaces of indentation per CommonMark — and skips lines inside a fence before matching headings, tags, or closers; check that fence counters accept the same fence forms. A parser that uses a real Markdown library (e.g. markdown-it, mistune, commonmark) and walks its AST is not this finding. Deterministic check: a fixture with a fenced block containing a heading and a closing tag, asserted to be ignored.

**Severity guide:** a CI validator or gate that rejects valid input or accepts invalid input → High; a generator that silently omits or duplicates a section → Medium; cosmetic rendering corruption → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 5 PRs; yongwoon/develop-with-llm).

### A-017: Automated commit or rollback touches files the current step does not own (Devex)

An automated step that checkpoints, commits a TDD phase, or rolls back a failed change operates on whole files or the whole tree: `git add <path>` stages the user's pre-existing uncommitted hunks in that file; `git add -A` sweeps unrelated work into the commit; `git checkout -- <files>` on rollback discards the user's uncommitted edits along with the step's own change. The mirror defect: a phase commit runs with nothing staged because the step never staged its own files, so the commit fails and the flow stops. The class recurs because the author tests in a clean working tree. Apply the *why* — an automated step may only stage, commit, or revert the changes it made itself — for any tool that drives version control.

**Scan cue:** for each automated `git add` / `commit` / `checkout --` / `restore` / `reset` in the change, check that (a) the tool records which paths were already dirty before it started, (b) it stages only the step's own files (and stops with a "needs context" result, or stages only its hunks, when a path overlaps pre-existing changes), (c) rollback reverts only the step's own patch (saved diff applied in reverse) rather than the whole file, and (d) the overlap check runs *before* the commit, not after. A step running in a fresh, tool-created worktree or branch with no prior changes is not a finding. No deterministic linter; a test that pre-dirties a target file and asserts it survives is the check.

**Severity guide:** rollback that can discard user work → Critical/High; a commit that includes unrelated user changes → High; a phase commit that fails because nothing was staged → Medium.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 5 PRs; yongwoon/develop-with-llm).

### A-018: List API read as a single page, or a cap reached without a defined outcome (Devex / Contract)

A list endpoint or CLI returns a default page size or limit (often 30), and the code processes that first page as if it were the whole set. Real cases: a label lookup misses labels after the 30th and falls into a wrong fallback; an "is my marker comment already posted" check reads one page and posts a duplicate; a "latest event" query paginates but applies its filter per page, so it picks a per-page maximum instead of the global one; a search lists only issues and not PRs and has no explicit limit. Paired with this: when an explicit cap *is* set, nothing says whether hitting it means "stop fetching but process what was returned" or "stop and report incomplete". The class recurs because development repos have fewer items than one page. Apply the *why* — either read every page or make truncation explicit — for any paginated source.

**Scan cue:** for each new list call (REST/GraphQL, `gh ... list`, SDK `list*`), check for full pagination (`--paginate`, cursor/next-link loop, explicit `per_page`/`--limit`) and, when results are aggregated (max, latest, dedupe), that aggregation runs over all pages combined (e.g. `gh api --paginate --slurp ... | jq`, not a per-page `--jq`). Where a cap is intentional, check that hitting it is detected (`returned == limit`) and that the documented outcome is applied. A call against an endpoint that is guaranteed to return a single bounded object is not a finding. No deterministic linter; a test with more items than one page is the check.

**Severity guide:** truncation that causes a duplicate write, a missed security item, or a wrong mutation → High; truncation that yields an incomplete report with no notice → Medium; an undocumented cap whose outcome is still safe → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 4 PRs; yongwoon/develop-with-llm).

### A-019: Redaction applied to one output but not to every persisted or posted artifact (Security)

A secret/PII redaction rule covers the obvious output — the final summary — but not the other artifacts the same flow writes or publishes: generated script source committed to the repository, a handoff or retrospective file, a briefing comment re-posting a reporter's text to a public tracker, screenshots and URLs (with tokens in query strings), logs, filenames. A second form: the redaction pattern list is narrow (a few token formats and PEM headers) while the rule claims "every credential" and "every piece of personal data", so cookies, connection strings, other cloud keys, and emails pass through. The class recurs because redaction is written once at the sink the author was thinking about. Apply the *why* — redaction belongs on every boundary where data leaves the process or is persisted — not only in summaries.

**Scan cue:** for each new write to disk, VCS, an issue/PR comment, a chat/notification, or an uploaded artifact, check that the redaction step runs on *that* payload (including embedded code blocks, URLs, and filenames), and that the pattern set matches the rule's stated scope; where detection is uncertain, check for a fail-safe (omit the value) rather than emitting it. Do not flag redaction that removes required non-secret content — narrowing it to the secret values is the fix, not deleting the action text. Deterministic checks: a secret scanner such as gitleaks or trufflehog over generated artifacts; no common tool covers PII comprehensively.

**Severity guide:** secrets or PII reaching a public tracker, the repository history, or a shared artifact → High (Critical for live credentials); reaching a local-only file → Medium; a narrow pattern list with no current leak path → Medium.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 4 PRs; yongwoon/develop-with-llm).

### A-020: Resume state not bound to the run identity, or not saved before the step that can fail (Devex / Design)

A resumable flow persists progress (a step number, a checkpoint, remaining items) so a later run can continue. Recurring gaps: the state file is shared across procedures and stores only a counter, so one procedure accepts another's `last_step` and silently skips steps; a stored value is not range-checked (`last_step=999` → "All steps complete"); state is written non-atomically, so an interrupted write leaves an empty file; the resume path restores fewer values than the fresh path computed (three of four documented fields, losing prior `merged`/`closed` results); fresh-run selection rules are re-applied on resume, overriding the stored owner or mode; state is recorded only after a step that can fail, so a failure leaves nothing to resume. The class recurs because the happy path is a single uninterrupted run. Apply the *why* — resume must reconstruct exactly the state the fresh path had, for the same run — for any checkpointed job.

**Scan cue:** for each new or changed checkpoint, check that (a) the state carries a run/procedure identity and mismatches are rejected, (b) loaded values are validated against their valid range, (c) writes are atomic (temp file in the same directory + rename), (d) the set of fields written equals the set restored, (e) resume takes precedence over fresh-run defaults and selection logic, and (f) state is persisted before the first operation that can fail. A flow documented as non-resumable is not this finding. No deterministic linter; a test that kills the run mid-step and resumes is the check.

**Severity guide:** resume that skips required (manual, security, or delivery) steps or loses completed results → High; resume that fails loudly and needs manual cleanup → Medium; resume that re-runs an idempotent step → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 4 PRs; yongwoon/develop-with-llm).

### A-021: Status, identifier, or allowlist compared by prefix or substring instead of exact match (Security / Design)

A check meant to accept one exact value accepts look-alikes because it uses `startswith`, `contains`, an unanchored regex, or `\b` word boundaries. Real cases: a title containing `done` anywhere (`— Done criteria`) is treated as the completed marker `— done`; an unanchored bot-login regex admits `not-coderabbitai`; an evidence cache treats any line starting with `PASS` as satisfied, so stale or hand-written evidence skips re-execution; a status validator using `\bDONE\b` accepts `DONE-INVALID` because `-` is a word boundary. The class recurs because the valid values are all the test feeds. Apply the *why* — when the set of valid values is closed, compare the whole value against it — for status fields, identities, cache keys, and suffixes in any language.

**Scan cue:** for each new comparison against a status, role, login, ID, file suffix, or allowlist, check for `startswith` / `endswith` used for identity, `in` / `includes` / `contains` on strings, `grep` without `-x`/`-F`, and regexes without `^...$` anchors or relying on `\b`. The fix is exact equality or set membership on the fully parsed token; for a cache, compare a fingerprint of the inputs (hash of command + expectation), not just a "PASS" prefix. Intentional prefix matching on a documented hierarchical namespace (e.g. a path prefix after canonicalization) is not this finding. No general linter; a negative test with a look-alike value is the check.

**Severity guide:** an allowlist, authorization, or gate-skip decision that admits a look-alike → High; a status or classification mismatch that corrupts data or counts → Medium; cosmetic matching in reports → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 4 PRs; yongwoon/develop-with-llm).

### A-022: Code or entry point deleted while a live or external reference may remain (Architecture / Contract)

A cleanup or migration rule authorizes deleting a function, module, endpoint, or legacy entry point once the in-repository callers are migrated or the item is classified "safe". Two recurring gaps: a live functional reference outside the deletion set still exists, but the procedure allows deletion after a downgrade to a "caution" tier instead of stopping; and "all callers in this repository are migrated" is treated as "no callers exist", which is false for a public API, a published package export, a webhook/CLI contract, or a database schema with a compatibility window. The class recurs because repository-wide search is the only evidence the tool has, and it cannot see external consumers. Apply the *why* — deletion requires proving absence of *every* consumer, and external surfaces need a deprecation path instead — for any refactor or dead-code removal.

**Scan cue:** for each deleted symbol, route, export, or schema element, grep for remaining references (including dynamic lookups, string-based dispatch, config, and docs that are executed), and check whether the item is part of a public surface (exported from a package entry point, documented API, versioned endpoint, DB column read by other services). A remaining functional reference is a finding regardless of tier; a public surface removed without a deprecation/compatibility step is a finding. A private, unexported symbol with zero references is not. Deterministic checks: dead-code tools such as knip, ts-prune, vulture, or `staticcheck` U1000 identify candidates, but none proves absence of external consumers.

**Severity guide:** removal of a public API or schema element still consumed externally → Critical/High; deletion that leaves a dangling internal call → High; deletion of documented-only references → Low.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 3 PRs; yongwoon/develop-with-llm).

### A-023: Publishing, paid, credentialed, or destructive side effect runs without its own explicit confirmation (Security / Devex)

An automated flow performs an action that is hard to undo or costs money — pushing an unpublished base branch, applying infrastructure changes, invoking a paid or credentialed external service, deleting remote branches or data — on the strength of an earlier, broader approval (approving a plan or map) or on an input that was never checked against the precondition it is supposed to prove. Real cases: a recovery rule that pushes local base-branch commits without confirming the target branch and the outgoing commit set; an approval gate defined for the init route but not for an audit route that re-drives the same paid helpers; a scope flag accepted on path existence alone, bypassing the guard it was meant to satisfy. The class recurs because each route is written separately and the confirmation lives in only one of them. Apply the *why* — every route that reaches an irreversible or costly side effect needs a confirmation that names that specific effect — in CLIs, agents, and CI jobs alike.

**Scan cue:** enumerate every code path that reaches a push, publish, deploy/apply, delete, payment/paid-API call, or credentialed external call, and check that each passes through a confirmation (interactive prompt, explicit `--yes`, or an approval step) that shows the concrete target (branch, commit set, resource, cost) immediately before the action; check that inputs used to skip a guard are verified, not just present. A dry-run/plan-only path and a non-interactive mode that requires an explicit opt-in flag are not findings. No deterministic linter.

**Severity guide:** an unconfirmed push to a shared base branch, infra apply, or destructive delete → High (Critical if production); an unconfirmed paid or credentialed call → High; a confirmation that exists but does not show the concrete target → Medium.

> Provenance — source: `mining`; date: `2026-11-08`; origin: `bulk mining (200 PRs, 2026-07..2026-11)` (fix confirmed in 3 PRs; yongwoon/develop-with-llm).
