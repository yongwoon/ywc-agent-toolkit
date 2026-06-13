# Schema Guide — Core (stack-agnostic)

The single source of truth for designing, reviewing, and changing database schemas across the `ywc-*` skill family. This `core.md` holds the **principles and invariants that hold regardless of ORM** — the "why". Each stack file holds only the **syntax and stack-specific traps** — the "how":

| Stack | File | Use when |
|---|---|---|
| Prisma (TS/Node) | [prisma.md](prisma.md) | `schema.prisma`, `@relation`, `prisma migrate` |
| Raw SQL DDL (Postgres) | [sql-ddl.md](sql-ddl.md) | hand-written `CREATE TABLE` / `ALTER` migrations, any ORM-less project |
| Drizzle (TS) | [drizzle.md](drizzle.md) | `drizzle-orm` schema files, `drizzle-kit` migrations |
| TypeORM (TS) | [typeorm.md](typeorm.md) | TypeORM `@Entity` classes, `typeorm migration:*` |

> **Extending to a new stack:** add one file next to the others, translate Part B's eight invariants into that stack's syntax, and link it in the table above. Do not duplicate Part A — link back to it. That is the whole maintenance contract.

Read `core.md` first, then open the one stack file that matches the project. When a schema change is in play, the calling skill (`ywc-plan`, `ywc-task-generator`, `ywc-sequential-executor`, `ywc-code-gen`, `ywc-impl-review`) should point you here before the Data Model is drafted, generated, or reviewed.

---

## Part A — Design principles (maintainable, extensible, efficient)

These are judgment calls, not mechanical checks. They shape a schema that survives growth instead of fighting it.

### A1. Naming is a public API

Column and table names outlive the code that reads them — migrations, analytics queries, and downstream consumers all bind to them, and renaming later is a coordinated breaking change. So pick one convention per project and never mix:

- One pluralization rule for tables (`users` xor `user`), one case rule (`snake_case` is safest because it survives case-insensitive SQL identifiers without quoting).
- Foreign keys read as `<entity>_id` (`tenant_id`, `landing_page_id`) so joins are self-documenting.
- Booleans read as a predicate (`is_active`, `has_consent`), timestamps as `*_at` (`created_at`, `deleted_at`).

If the existing schema already has a convention, **inherit it even if you prefer another** — consistency beats personal preference, because a reader scanning the schema should never have to ask "which style is this table?".

### A2. Normalize by default; denormalize as a deliberate, documented exception

Start at 3NF: every fact lives in exactly one place. Duplication is the root of update anomalies — when the same value is stored twice, the two copies drift and no reader knows which is authoritative. Denormalize only when a measured read path demands it, and when you do, **write down (in the spec / migration comment) what keeps the copies consistent** (a trigger, an application invariant, an accepted staleness window). An undocumented denormalized column is a future data-integrity incident.

### A3. Schema evolution is expand → migrate → contract, never edit-in-place

A schema change ships against a running system with old and new code live at once. The only safe shape is three deployable steps, each backward-compatible with the step before it:

1. **Expand** — add the new column/table/index as nullable/optional. Old code ignores it; new code can start writing it.
2. **Migrate** — backfill data and switch reads to the new shape.
3. **Contract** — once nothing reads the old shape, drop it.

Collapsing these into one migration (add `NOT NULL` + backfill + drop-old in a single deploy) is what breaks production at the rollout boundary. Renames are the classic trap: a rename is *add new + backfill + dual-write + drop old*, not an in-place `RENAME`, because the old name is still referenced by code that hasn't deployed yet.

### A4. Every migration must be reversible — or say loudly why it is not

Write the down-path before you ship the up-path. A migration with no thought-out rollback is a one-way door at the worst possible time. Destructive steps (drop column, drop table) are inherently irreversible — those must be the *contract* phase of A3, gated behind "nothing reads this anymore", never bundled with the feature that stops using it.

### A5. Index for the queries you actually run

An index is a write-time cost paid for a read-time gain. Add indexes that serve real query predicates and join columns (see B4); do **not** speculatively index every column. A composite index's column order matters — it serves queries that filter on a left-anchored prefix of its columns, so order them most-selective-and-always-present first.

---

## Part B — Mechanical invariants (deterministic-failure checklist)

Unlike Part A, these are not judgment calls. Each one, if violated, produces a *deterministic* failure — a generate-time error, a failed migration, an FK violation, or a silent data leak — that no human review reliably forgives and that is easy to omit when drafting a Data Model model-by-model rather than schema-wide. The stack files show the exact syntax for each; the rule itself is universal.

**B1. Relations are declared on both sides / both directions.** Where the ORM materializes a relation, the reverse side must be declared too (Prisma rejects one-sided relations at generate time). In raw SQL, declare the FK constraint *and* document the reverse access path. A relation the reviewer cannot see from one model is a relation that will not build or will not be queryable.

**B2. Every `onDelete` rule has an API status consequence.** `Cascade` deletes children silently — document the side effect. `Restrict`/`NoAction` makes the parent delete fail when children exist — the endpoint **must** specify `409 Conflict` with its trigger condition, or the implementer writes an unhandled `500` path. `SetNull` requires every child reader to tolerate a null FK. The schema rule and the API behavior are one decision; specify them together.

**B3. Adding a `NOT NULL` column to a populated table requires a backfill plan.** Postgres validates the constraint row-by-row in the migration transaction; the first existing row fails it. The spec/migration must state: nullable add → backfill expression → constraint add, as separate steps (A3 expand/migrate). "Table is empty in prod" is a valid answer — but it must be stated explicitly, not assumed.

**B4. Every FK column has an index.** Exception: a `1:1` relation where the FK is itself the PK. Otherwise both the join and the FK constraint-check degrade as the child table grows, and Postgres does **not** auto-index FK columns (it auto-indexes PKs and unique constraints only). The Data Model must declare the index — an implementer reading a spec will not add an undeclared one.

**B5. Multi-column business uniqueness is declared as a constraint, not prose.** If the rule is "one `slug` per `tenant`", that is a `UNIQUE (tenant_id, slug)` constraint, and the corresponding write endpoint must specify the conflict status (typically `409` with a discriminating error code). Uniqueness enforced only in application code is a race condition under concurrency.

**B6. Multi-tenant tables carry tenant scope.** In any project with row-level tenant isolation (RLS, a tenant-guarded client, or service-layer `tenant_id` checks), every new table holding tenant-owned data needs: a `tenant_id` FK (+ index per B4), the relation to the tenant table (per B1), and an explicit RLS/policy declaration — *even if* the policy is "inherits the default tenant policy", the spec must say so. A new table without `tenant_id` is a cross-tenant data leak waiting to happen, and no review pass below the schema layer catches it.

**B7. Enum-like columns declare their domain.** A column conceptually constrained to a value set (`status ∈ {new, spam, processed}`) is a native enum or a `text` column with a `CHECK` constraint — never an unconstrained `text`. List the allowed values in the Data Model; reject unknown values at the API boundary; and specify the read behavior when a *future* value appears in old stored data (enum extension is forward-compatible, narrowing is not).

**B8. Business tables carry `created_at`/`updated_at` as `timestamptz`.** Audit and concurrency/sort both need them, both default to `now()`, and both must be `timestamptz` (with time zone) — never bare `timestamp`, which silently discards the offset and produces off-by-hours bugs around DST and across regions.

---

## Part C — Review checklist (schema diff / PR review)

When reviewing a schema-touching change, run Part B as pass/fail, then sanity-check Part A as judgment:

- [ ] **B1** Every relation declared on both sides / FK + reverse path documented
- [ ] **B2** Every `onDelete` rule has its API status consequence specified
- [ ] **B3** Every new `NOT NULL` column on a populated table has a 3-step backfill plan
- [ ] **B4** Every FK column has an index (or the `1:1`-PK exception is explicit)
- [ ] **B5** Every multi-column business uniqueness rule is a DB constraint
- [ ] **B6** Every multi-tenant table has `tenant_id` FK + index + policy declaration
- [ ] **B7** Every enum-like column has a declared, enforced domain
- [ ] **B8** Every business timestamp is `timestamptz` with a default
- [ ] **A1** Naming matches the existing schema convention (no mixed styles)
- [ ] **A3** The change is expand-only (no `NOT NULL`+backfill+drop bundled into one deploy; no in-place rename)
- [ ] **A4** A rollback path exists, or the irreversibility is the deliberate contract phase

Any unchecked B-item is a Critical finding — it will fail at generate time, at the first migration, or at the first concurrent write. An unchecked A-item is a maintainability finding: not a blocker, but called out so the cost is chosen, not stumbled into.
