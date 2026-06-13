# Schema Guide — TypeORM (TS)

TypeORM decorator syntax for the eight invariants (Postgres driver). Read [core.md](core.md) first for the principles; this file shows only **how each rule looks on a TypeORM `@Entity`** plus TypeORM-specific traps.

TypeORM's defining risk: `synchronize: true` and `migration:generate` will happily emit destructive DDL from a model diff. Always run with `synchronize: false` outside local dev, and **read every generated migration** before applying it.

## B1. Bilateral relations

Declare the owning side (`@ManyToOne` with `@JoinColumn`) and the inverse side (`@OneToMany`). TypeORM uses the inverse-side function to connect bidirectional navigation metadata:

```ts
@Entity()
export class LpFormSubmission {
  @ManyToOne(() => LandingPage, (lp) => lp.submissions, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'landing_page_id' })
  landingPage: LandingPage;
}

@Entity()
export class LandingPage {
  @OneToMany(() => LpFormSubmission, (s) => s.landingPage)
  submissions: LpFormSubmission[];   // ← inverse side
}
```

The `@JoinColumn` belongs on the `@ManyToOne` (owning) side only. Putting it on both is wrong. Omitting the inverse function does not necessarily corrupt the underlying database relation, but it can prevent TypeORM from populating or navigating the inverse collection such as `LandingPage.submissions`.

## B2. Cascade rules ↔ API status codes

Two different "cascade" concepts exist — do not confuse them:

- **`onDelete: 'CASCADE'`** (in `@ManyToOne` options) → **database** `ON DELETE` rule. This is the one core B2 is about.
- **`cascade: true`** (TypeORM option) → **application-level** persistence cascade only; emits no DB rule.

```ts
@ManyToOne(() => Tenant, { onDelete: 'RESTRICT' })   // DB rule → 409 on parent delete
```

`'RESTRICT'`/`'NO ACTION'` → endpoint must return `409`; `'SET NULL'` → column nullable + null-tolerant readers.

## B3. NOT NULL adds require backfill

`migration:generate` emits `ADD ... NOT NULL` from a non-nullable property. On a populated table that fails — split across three migrations (expand→migrate→contract per core A3) and write the backfill into the migration's `up()` by hand:

```ts
// step 1 (expand): @Column({ type: 'text', nullable: true }) status: string | null;
// step 2 (migrate): await queryRunner.query(`UPDATE lp_form_submission SET status = 'new' WHERE status IS NULL`);
// step 3 (contract): @Column({ type: 'text' }) status: string;
```

## B4. FK columns require indexes

TypeORM does **not** index `@JoinColumn` FKs automatically. Add `@Index` per FK:

```ts
@Entity()
@Index('idx_lfs_form_config_status', ['formConfigId', 'status'])  // composite
export class LpFormSubmission {
  @Index('idx_lfs_form_config_id')
  @Column({ name: 'form_config_id' }) formConfigId: string;

  @Index('idx_lfs_tenant_id')
  @Column({ name: 'tenant_id' }) tenantId: string;
}
```

## B5. Composite uniqueness

```ts
@Entity()
@Unique('landing_page_tenant_id_slug_key', ['tenantId', 'slug'])
export class LandingPage { /* ... */ }
```

Map the unique violation to `409` with a discriminating error code at the write endpoint.

## B6. Multi-tenant scope

`tenant_id` column + `@ManyToOne(() => Tenant)` + `@Index` (B4) + inverse side on `Tenant`. TypeORM has no RLS abstraction — the policy goes in a raw-SQL migration (`queryRunner.query`), and must be declared in the spec:

```ts
// in the migration up():
await queryRunner.query(`ALTER TABLE lp_form_submission ENABLE ROW LEVEL SECURITY`);
await queryRunner.query(`CREATE POLICY tenant_isolation ON lp_form_submission
  USING (tenant_id = current_setting('app.tenant_id')::uuid)`);
```

## B7. Enum domain

```ts
@Column({ type: 'enum', enum: ['new', 'spam', 'processed'], default: 'new' })
status: 'new' | 'spam' | 'processed';
```

`type: 'enum'` creates a native Postgres enum. For a flexible domain, use `type: 'text'` plus a `CHECK` added in the migration. List the values in the Data Model regardless.

## B8. Timestamps

```ts
@CreateDateColumn({ type: 'timestamptz', name: 'created_at' }) createdAt: Date;
@UpdateDateColumn({ type: 'timestamptz', name: 'updated_at' }) updatedAt: Date;
```

`type: 'timestamptz'` is required — the default for `@CreateDateColumn` can resolve to bare `timestamp` depending on driver config. `@UpdateDateColumn` is bumped by the TypeORM entity manager only; `QueryBuilder` bulk `.update()` and raw queries bypass it, so use a DB trigger if bulk/raw writers exist.

## Self-check

Run the [core.md Part C checklist](core.md#part-c--review-checklist-schema-diff--pr-review). TypeORM-specific gotchas: `synchronize: false` in all non-local envs; every generated migration read before apply; `onDelete` (DB rule) not confused with `cascade` (app-level); `@JoinColumn` on the owning side only; `@Index` on every FK; `type: 'timestamptz'` explicit on date columns; RLS via raw `queryRunner.query`.
