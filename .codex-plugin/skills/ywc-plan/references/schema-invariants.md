# Schema Invariants Checklist

This reference complements `ywc-plan` Step 4b (Data Model section) and Step 4b.5 (Self-Consistency Pass). Use it when the spec adds, modifies, or removes DB tables, columns, indexes, or relations.

These rules exist because they are **mechanical** — they produce deterministic failures (`prisma generate` error, FK violation, migration rollback) that no human review will forgive, and they are easy to omit when drafting a Data Model section model-by-model rather than schema-wide.

## 1. Bilateral Relations (Prisma)

Every `@relation` declared on one model **must** have its reverse-relation field declared on the other model in the spec — even if that other model already exists in `schema.prisma` today.

```prisma
// Adding LpFormSubmission with a relation to LandingPage:
model LpFormSubmission {
  id            String      @id @default(uuid())
  landingPageId String
  landingPage   LandingPage @relation(fields: [landingPageId], references: [id], onDelete: Cascade)
}

// Spec MUST also declare the addition to LandingPage:
model LandingPage {
  // ...existing fields...
  lpFormSubmissions LpFormSubmission[]   // ← REQUIRED in the spec
}
```

**Why it matters:** Prisma rejects one-sided relations at `prisma generate` time. The migration file may write, but the client will not build. Spec reviewers (and `ywc-spec-validate` Code Compatibility) cannot infer the reverse side; the spec must declare it.

## 2. Cascade Rules ↔ API Status Codes

Every `onDelete` rule on a relation has a direct consequence in the API Contract. The API behavior must be specified alongside the schema.

| Schema rule | Expected API behavior on parent delete | Required in API Contract |
|---|---|---|
| `onDelete: Cascade` | Parent delete also deletes children, no FK error | Document the cascading side effect in the endpoint description; consider whether the operator UX needs a confirmation step |
| `onDelete: Restrict` | Parent delete fails with FK violation when children exist | **`409 Conflict`** must appear in the endpoint's response table, with the trigger condition stated |
| `onDelete: SetNull` | Children survive parent delete with FK nulled | Children must be tolerant of null FK in subsequent reads; document in Edge Cases |
| `onDelete: NoAction` / default | Behaves like Restrict at runtime, but Prisma will not auto-error at generate time | Same as Restrict: document `409`, and consider switching to explicit `Restrict` |

**Why it matters:** A spec that defines `Restrict` without a corresponding `409` is incomplete — the implementer either writes an unhandled exception path (`500` leak) or silently changes the cascade rule.

## 3. NOT NULL Adds Require Backfill

Adding a `NOT NULL` column to an existing table — even with a `DEFAULT` — requires a backfill plan in the spec for any non-empty production table.

| Scenario | Required in spec |
|---|---|
| New `NOT NULL` column on existing table, no default | Spec must specify: (1) intermediate nullable add, (2) backfill query, (3) `NOT NULL` constraint add, (4) deploy ordering |
| New `NOT NULL` column with computable default | Spec must specify the backfill expression (e.g., `UPDATE table SET col = expr WHERE col IS NULL`) and confirm the migration tool runs it before applying the constraint |
| New `NOT NULL` column on empty table or seed-only data | Spec can declare "no backfill required — table is empty in prod / dev seed handles it" — but the declaration must be explicit |

**Why it matters:** Postgres adds the constraint check transactionally; a `NOT NULL` add on a populated table fails the migration on the first row encountered. The spec is the document the on-call engineer reads at 2 AM when the rollout fails.

## 4. FK Columns Require Indexes

Every FK column should have an index unless the relation is `1:1` and the FK is itself the PK. Otherwise the join performance and the FK constraint check both degrade as the child table grows.

```prisma
model LpFormSubmission {
  id            String @id @default(uuid())
  formConfigId  String
  tenantId      String

  formConfig    LpFormConfig @relation(fields: [formConfigId], references: [id])
  tenant        Tenant       @relation(fields: [tenantId], references: [id])

  @@index([formConfigId])         // required
  @@index([tenantId])             // required
  @@index([formConfigId, status]) // composite for the operator console query
}
```

The spec's Data Model section should declare every FK index it expects. If the implementer reads the spec and the index is missing, they will not add it on their own.

## 5. Composite Uniqueness Must Be Declared

If business rules require uniqueness across more than one column (e.g., `(tenantId, slug)`), the spec must declare it — not as prose, but as a `@@unique([…])` line in the Data Model.

The Acceptance Criteria for the corresponding write endpoint must specify the conflict-resolution status code (typically `409 Conflict` with a discriminating error code).

## 6. Multi-Tenant Tables Inherit Tenant Scope

In multi-tenant projects (RLS, `tenantGuardedPrisma`, or row-level `tenantId` checks in the service layer), every new table that holds tenant-owned data must include:

- A `tenantId String` FK column (and matching index per §4)
- The relation to `Tenant`, with its reverse-relation field on `Tenant` (per §1)
- An RLS policy declaration in the spec (if the project uses RLS) — even if the policy is "inherit default tenant policy", the spec must say so

A new table introduced without `tenantId` is a cross-tenant data leak waiting to happen. `ywc-spec-validate` flags this as Critical because no review pass below this skill catches it.

## 7. Enum Columns: Declare the Domain

When a column is conceptually an enum (`status ∈ {new, spam, processed}`), declare it as a Prisma enum or as a `text` column with an explicit `CHECK` constraint in the migration. The Data Model section must list the allowed values; the API Contract must reject unknown values at the boundary; the Edge Cases section must specify the behavior when an unknown value appears in stored data (after a future enum extension).

## 8. Timestamps: `createdAt`, `updatedAt`, and Time Zone

Every new business-data table needs `createdAt timestamptz` (audit) and usually `updatedAt timestamptz` (concurrency / sort). Both default to `now()`. Both should be `timestamptz` (with time zone), never `timestamp` — the bare type silently loses the offset and produces off-by-hours bugs near DST and across regions.

## Self-Check (run as part of Step 4b.5)

For each new or modified model in the spec:

- [ ] Every `@relation` has its reverse-relation field on the other model declared in the spec
- [ ] Every `onDelete` rule has its API status consequence specified in the API Contract
- [ ] Every new `NOT NULL` column on an existing table has a backfill plan
- [ ] Every FK column has an index (or an explicit "1:1 PK reused" exception)
- [ ] Every multi-column business uniqueness rule is declared as `@@unique([...])`
- [ ] Every multi-tenant table has `tenantId` FK + index + RLS policy declaration
- [ ] Every enum-like column has its allowed values listed
- [ ] Every business timestamp is `timestamptz`

If any answer is no, edit the Data Model before Step 5 handoff. Each omission becomes a Critical finding at `ywc-spec-validate` Code Compatibility, plus a migration that fails on first deploy attempt.
