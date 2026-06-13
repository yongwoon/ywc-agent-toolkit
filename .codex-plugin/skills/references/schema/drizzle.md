# Schema Guide — Drizzle (TS)

Drizzle ORM syntax for the eight invariants (Postgres dialect, `drizzle-orm` + `drizzle-kit`). Read [core.md](core.md) first for the principles; this file shows only **how each rule looks in a Drizzle schema** plus Drizzle-specific traps.

Drizzle's defining trait: the table definition emits the DDL, but `relations()` is a **query-layer convenience only** — it generates no SQL. The real FK lives in the `references()` call. This split is the source of most Drizzle schema mistakes.

## B1. Relations (FK in the column, both sides in `relations()`)

The FK constraint comes from `.references()` on the column. The `relations()` helper declares both directions for the query builder — and core B1's "both sides" obligation maps directly onto declaring `one`/`many` on each side:

```ts
export const lpFormSubmission = pgTable('lp_form_submission', {
  id: uuid('id').primaryKey().defaultRandom(),
  landingPageId: uuid('landing_page_id').notNull()
    .references(() => landingPage.id, { onDelete: 'cascade' }),  // ← real FK + cascade
});

export const lpFormSubmissionRelations = relations(lpFormSubmission, ({ one }) => ({
  landingPage: one(landingPage, {
    fields: [lpFormSubmission.landingPageId], references: [landingPage.id],
  }),
}));
export const landingPageRelations = relations(landingPage, ({ many }) => ({
  lpFormSubmissions: many(lpFormSubmission),   // ← reverse side
}));
```

A `relations()` block without a matching `.references()` produces **no FK constraint** — the join works in TS but the database enforces nothing. Always put `onDelete` on `.references()`, not on `relations()`.

## B2. Cascade rules ↔ API status codes

`onDelete` is an option on `.references()`. Its API consequence is identical to [core B2](core.md#part-b--mechanical-invariants-deterministic-failure-checklist): `'cascade'` documents the side effect, `'restrict'` / `'no action'` requires a `409`, `'set null'` requires a nullable column and null-tolerant readers.

```ts
tenantId: uuid('tenant_id').notNull().references(() => tenant.id, { onDelete: 'restrict' }),
```

## B3. NOT NULL adds require backfill

`drizzle-kit generate` will emit `ADD COLUMN ... NOT NULL` directly from a `.notNull()` column. On a populated table that fails — so split it across three generated migrations (expand→migrate→contract per core A3), and hand-edit the backfill `UPDATE` into the migration SQL, because `drizzle-kit` does not generate data backfills:

```ts
// step 1 (expand): nullable
status: text('status'),
// step 2 (migrate): add  UPDATE lp_form_submission SET status = 'new' WHERE status IS NULL;
//                  by hand into the generated .sql file
// step 3 (contract): add .notNull()
status: text('status').notNull(),
```

## B4. FK columns require indexes

Drizzle does not create FK indexes implicitly. Declare them in the table's second callback argument:

```ts
export const lpFormSubmission = pgTable('lp_form_submission', {
  formConfigId: uuid('form_config_id').notNull().references(() => lpFormConfig.id),
  tenantId: uuid('tenant_id').notNull().references(() => tenant.id),
  status: text('status'),
}, (t) => ({
  formConfigIdx: index('idx_lfs_form_config_id').on(t.formConfigId),
  tenantIdx: index('idx_lfs_tenant_id').on(t.tenantId),
  consoleIdx: index('idx_lfs_form_config_status').on(t.formConfigId, t.status),  // composite
}));
```

## B5. Composite uniqueness

```ts
}, (t) => ({
  tenantSlugUnique: unique('landing_page_tenant_id_slug_key').on(t.tenantId, t.slug),
}));
```

Map the resulting unique violation to `409` at the write endpoint.

## B6. Multi-tenant scope

`tenant_id` column + `.references(() => tenant.id)` + index (B4) + reverse `relations()`. Drizzle has first-class RLS helpers (`pgPolicy`, `pgTable(..., extraConfig)`, and `.withRLS()` for policy-free RLS); declare the policy explicitly:

```ts
export const lpFormSubmission = pgTable('lp_form_submission', {
  tenantId: uuid('tenant_id').notNull().references(() => tenant.id),
}, (t) => ({
  tenantIdx: index('idx_lfs_tenant_id').on(t.tenantId),
  isolation: pgPolicy('tenant_isolation', {
    using: sql`tenant_id = current_setting('app.tenant_id')::uuid`,
  }),
}));
```

## B7. Enum domain

```ts
export const submissionStatus = pgEnum('submission_status', ['new', 'spam', 'processed']);
export const lpFormSubmission = pgTable('lp_form_submission', {
  status: submissionStatus('status').notNull().default('new'),
});
```

Prefer `pgEnum` over a bare `text`; if `text` is required, add a `CHECK` via `sql` in the table callback and list the values in the Data Model.

## B8. Timestamps

```ts
createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow()
  .$onUpdate(() => new Date()),
```

`{ withTimezone: true }` is required — the default maps to bare `timestamp` and loses the offset. `.$onUpdate()` runs in the Drizzle client only; raw SQL writes bypass it, so use a DB trigger if non-Drizzle writers exist.

## Self-check

Run the [core.md Part C checklist](core.md#part-c--review-checklist-schema-diff--pr-review). Drizzle-specific gotchas: every relation has a real `.references()` (not just a `relations()` entry); `onDelete` is on `.references()`; `{ withTimezone: true }` on every timestamp; FK `index()` declared in the table callback; `.enableRLS()` + `pgPolicy` on tenant tables; the generated migration SQL was reviewed (drizzle-kit can silently emit a destructive `ALTER` when it misreads a rename as drop+add).
