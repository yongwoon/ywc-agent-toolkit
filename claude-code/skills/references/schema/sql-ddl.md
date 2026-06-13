# Schema Guide — Raw SQL DDL (Postgres)

Hand-written SQL DDL for the eight invariants — for ORM-less projects, or for the raw-SQL migrations that even ORM projects fall back to (RLS policies, `CHECK` constraints, concurrent indexes). Read [core.md](core.md) first for the principles; this file shows only **the Postgres DDL** plus Postgres-specific migration traps.

## B1. Relations (FK + reverse path)

Raw SQL has no "reverse relation field", but the obligation in core B1 still holds: declare the FK constraint, and the reverse access path is "an index on the child FK so the parent→children query is cheap" (see B4).

```sql
ALTER TABLE lp_form_submission
  ADD CONSTRAINT lp_form_submission_landing_page_id_fkey
  FOREIGN KEY (landing_page_id) REFERENCES landing_page (id) ON DELETE CASCADE;
```

## B2. Cascade rules ↔ API status codes

The `ON DELETE` clause carries the same API consequence as core B2.

| Clause | Behavior | API Contract |
|---|---|---|
| `ON DELETE CASCADE` | children deleted with parent | document the cascade |
| `ON DELETE RESTRICT` | parent delete raises `foreign_key_violation` (SQLSTATE 23503) | **`409`** + trigger condition |
| `ON DELETE SET NULL` | child FK nulled (column must be nullable) | child reads tolerate null |
| `NO ACTION` (default) | Restrict-like, checked at statement end | same as `RESTRICT` |

## B3. NOT NULL adds require backfill

Never `ADD COLUMN ... NOT NULL` on a populated table in one step — it rewrites the table and fails on existing rows. Use the expand→migrate→contract sequence (core A3), and validate the constraint without a long lock:

```sql
-- step 1 (expand): nullable add, instant in PG 11+
ALTER TABLE lp_form_submission ADD COLUMN status text;
-- step 2 (migrate): backfill in batches to avoid a long-held lock on big tables
UPDATE lp_form_submission SET status = 'new' WHERE status IS NULL;
-- step 3 (contract): add a NOT VALID check, then VALIDATE separately (no full-table AccessExclusive lock)
ALTER TABLE lp_form_submission ADD CONSTRAINT lp_form_submission_status_not_null
  CHECK (status IS NOT NULL) NOT VALID;
ALTER TABLE lp_form_submission VALIDATE CONSTRAINT lp_form_submission_status_not_null;
```

## B4. FK columns require indexes

Postgres auto-indexes PKs and `UNIQUE` constraints, but **not** FK columns. Create the index concurrently to avoid blocking writes on a live table:

```sql
CREATE INDEX CONCURRENTLY idx_lp_form_submission_form_config_id
  ON lp_form_submission (form_config_id);
CREATE INDEX CONCURRENTLY idx_lp_form_submission_tenant_id
  ON lp_form_submission (tenant_id);
CREATE INDEX CONCURRENTLY idx_lp_form_submission_form_config_status
  ON lp_form_submission (form_config_id, status);   -- composite, prefix-anchored
```

`CONCURRENTLY` cannot run inside a transaction block — keep it in its own migration step, and note that a failed concurrent build leaves an `INVALID` index to drop.

## B5. Composite uniqueness

```sql
ALTER TABLE landing_page ADD CONSTRAINT landing_page_tenant_id_slug_key
  UNIQUE (tenant_id, slug);
```

The write endpoint maps the resulting `23505 unique_violation` to `409` with a discriminating error code.

## B6. Multi-tenant scope

Tenant-owned tables get `tenant_id` + FK + index, and — in raw SQL projects this is where RLS actually lives — an explicit policy:

```sql
ALTER TABLE lp_form_submission ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON lp_form_submission
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

Declare the policy in the spec even when it "inherits the default" — RLS that is silently absent is a cross-tenant leak.

## B7. Enum domain

Two valid forms — a native enum, or a `text` + `CHECK`:

```sql
-- native enum (rigid, ALTER TYPE ... ADD VALUE to extend, cannot remove)
CREATE TYPE submission_status AS ENUM ('new', 'spam', 'processed');
-- or text + CHECK (flexible, easy to alter the constraint)
ALTER TABLE lp_form_submission
  ADD CONSTRAINT lp_form_submission_status_chk
  CHECK (status IN ('new', 'spam', 'processed'));
```

`ALTER TYPE ... ADD VALUE` is forward-compatible; you cannot drop an enum value without a type swap. List allowed values in the Data Model regardless.

## B8. Timestamps

```sql
created_at timestamptz NOT NULL DEFAULT now(),
updated_at timestamptz NOT NULL DEFAULT now()
```

Always `timestamptz`, never `timestamp` — the bare type stores no offset. `updated_at` is not auto-bumped in raw SQL; either set it in every `UPDATE` or attach a `BEFORE UPDATE` trigger.

## Self-check

Run the [core.md Part C checklist](core.md#part-c--review-checklist-schema-diff--pr-review). Postgres-specific gotchas: index builds on live tables use `CONCURRENTLY` (own migration, not in a txn); `NOT NULL`/FK validation uses `NOT VALID` + `VALIDATE` to avoid long `AccessExclusive` locks; RLS `ENABLE` + `POLICY` both present on tenant tables; `updated_at` has a trigger or is set on every write.
