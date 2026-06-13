# Schema Guide — Prisma (TS/Node)

Prisma-specific syntax for the eight invariants. Read [core.md](core.md) first for the principles (Part A) and the rule rationale (Part B); this file shows only **how each rule looks in `schema.prisma`** plus Prisma-specific traps.

## B1. Bilateral relations

Every `@relation` on one model **must** have its reverse-relation field declared on the other model — even if that other model already exists in `schema.prisma` today. Prisma rejects one-sided relations at `prisma generate`: the migration file may write, but the client will not build.

```prisma
model LpFormSubmission {
  id            String      @id @default(uuid())
  landingPageId String
  landingPage   LandingPage @relation(fields: [landingPageId], references: [id], onDelete: Cascade)
}

model LandingPage {
  // ...existing fields...
  lpFormSubmissions LpFormSubmission[]   // ← REQUIRED reverse side
}
```

## B2. Cascade rules ↔ API status codes

| `onDelete` | Runtime behavior | Required in API Contract |
|---|---|---|
| `Cascade` | Parent delete removes children, no FK error | Document the cascade; consider an operator confirmation step |
| `Restrict` | Parent delete fails when children exist | **`409 Conflict`** in the endpoint response table, with trigger condition |
| `SetNull` | Children survive with FK nulled | Child reads must tolerate null FK; note in Edge Cases |
| `NoAction` / default | Restrict-like at runtime, no generate-time error | Same as `Restrict`; prefer switching to explicit `Restrict` |

## B3. NOT NULL adds require backfill

Prisma generates the `ALTER TABLE ... SET NOT NULL` inside one migration. On a populated table, model it as three migrations (expand → migrate → contract per core A3):

```prisma
// step 1 (expand): nullable add
status String?
// step 2 (migrate): backfill via raw SQL in the migration, or a data migration script
//   UPDATE "LpFormSubmission" SET status = 'new' WHERE status IS NULL;
// step 3 (contract): drop the `?`
status String
```

Prisma's `migrate dev` does **not** run data backfills for you — an inline `UPDATE` must be added to the migration SQL by hand, or the `NOT NULL` step fails on the first existing row.

## B4. FK columns require indexes

Prisma does **not** auto-create an index for `@relation` scalar FKs (it indexes `@id` and `@unique` only). Declare every FK index:

```prisma
model LpFormSubmission {
  id            String @id @default(uuid())
  formConfigId  String
  tenantId      String
  status        SubmissionStatus @default(new)

  formConfig    LpFormConfig @relation(fields: [formConfigId], references: [id])
  tenant        Tenant       @relation(fields: [tenantId], references: [id])

  @@index([formConfigId])          // required
  @@index([tenantId])              // required
  @@index([formConfigId, status])  // composite for the operator console query
}
```

## B5. Composite uniqueness

```prisma
model LandingPage {
  tenantId String
  slug     String
  @@unique([tenantId, slug])   // "one slug per tenant"
}
```

The write endpoint's Acceptance Criteria must specify the conflict status (`409` + discriminating error code).

## B6. Multi-tenant scope

A tenant-owned table needs `tenantId` + index + reverse relation on `Tenant`, plus an RLS policy declaration in the spec (Prisma does not manage RLS — the policy lives in a raw-SQL migration). If the project uses a `tenantGuardedPrisma` wrapper, note that the new model is covered by it.

```prisma
model LpFormSubmission {
  tenantId String
  tenant   Tenant @relation(fields: [tenantId], references: [id])
  @@index([tenantId])
}
```

## B7. Enum domain

```prisma
enum SubmissionStatus {
  new
  spam
  processed
}
model LpFormSubmission {
  status SubmissionStatus @default(new)
}
```

Prefer a Prisma `enum` over `String`; if `String` is unavoidable (dynamic domain), add a `CHECK` constraint via raw-SQL migration and list allowed values in the Data Model.

## B8. Timestamps

```prisma
createdAt DateTime @default(now())              @db.Timestamptz(6)
updatedAt DateTime @default(now()) @updatedAt    @db.Timestamptz(6)
```

`@db.Timestamptz(6)` is required — without it Prisma maps `DateTime` to bare `timestamp`, losing the offset. `@updatedAt` is skipped on `updateMany`/bulk raw writes; if bulk updates must bump it, set it explicitly.

## Self-check

Run the [core.md Part C checklist](core.md#part-c--review-checklist-schema-diff--pr-review). Prisma-specific gotchas to add: `@db.Timestamptz` present on every `DateTime`; FK `@@index` present (not auto-added); reverse relation field present on the counterpart model; `@updatedAt` not silently relied upon for bulk writes.
