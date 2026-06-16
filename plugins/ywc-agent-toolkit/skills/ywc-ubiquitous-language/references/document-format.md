# Ubiquitous Language Document Format

This file specifies the exact format that `ywc-ubiquitous-language` produces and maintains in `docs/ubiquitous-language.md`.

## Design Principles

| Principle | Rationale |
|-----------|-----------|
| Single file | LLMs can inject the full vocabulary via `@docs/ubiquitous-language.md` in CLAUDE.md |
| Table-first | Tables are token-efficient for LLM context; humans can scan them quickly |
| Bounded Context sections | Prevents homonym collisions across domain boundaries |
| Synonyms to Avoid column | The highest-value field — tells the LLM what NOT to generate |
| `<!-- updated -->` comment | Machine-readable freshness signal without polluting rendered output |

---

## Full Format Specification

```markdown
# Ubiquitous Language — [Project Name]

<!-- updated: YYYY-MM-DD -->

## Overview

[2–3 sentences describing the domain. Who are the users? What core problem does the system solve?
This paragraph is injected as LLM context preamble — write it from the domain's perspective, not the technical implementation's.]

## Bounded Contexts

| Context | Responsibility |
|---------|---------------|
| [ContextA] | [What domain concerns this context owns] |
| [ContextB] | [What domain concerns this context owns] |

---

## [ContextA]

| Term | Korean | Definition | Synonyms to Avoid |
|------|--------|-----------|------------------|
| [Term] | [한국어] | [1–2 sentence definition from domain perspective] | [Comma-separated list, or — if none] |

### Deprecated Terms

| Term | Korean | Replaced By | Reason |
|------|--------|------------|--------|
| ~~[OldTerm]~~ | ~~[한국어]~~ | [NewTerm] | [Why it was renamed or removed] |

---

## [ContextB]

...

---

## Change Log

| Date | Mode | Summary |
|------|------|---------|
| YYYY-MM-DD | new | Initial creation — N terms across M contexts |
| YYYY-MM-DD | update | Added [X]; deprecated [Y] |
```

---

## With `--ddd` Flag

When `--ddd` is set, insert a `Type` column between `Korean` and `Definition`:

```markdown
| Term | Korean | Type | Definition | Synonyms to Avoid |
|------|--------|------|-----------|------------------|
| Order | 주문 | Aggregate | The root of the order lifecycle, from placement through fulfillment. | Cart, Purchase, Transaction |
| OrderItem | 주문 항목 | Value Object | A single product-quantity pair within an Order. Immutable after placement. | LineItem, CartEntry, ProductLine |
| OrderPlaced | 주문 완료 | Domain Event | Emitted when a customer successfully submits an Order. | OrderCreated, PurchaseCompleted |
```

### DDD Type Reference

| Type | When to Use |
|------|-------------|
| Entity | Has identity (ID), lifecycle, mutable state |
| Value Object | Defined by value alone, immutable, no identity |
| Aggregate | Entity that is the root of a consistency boundary |
| Domain Event | Something that happened in the domain, past tense, immutable |
| Policy | Business rule or decision logic that reacts to events |
| Service | Stateless operation that doesn't fit Entity or Value Object |

---

## Minimal Single-Context Example

For projects without explicit Bounded Context boundaries, use `## Core Domain` as the single section:

```markdown
# Ubiquitous Language — ShopBot

<!-- updated: 2026-05-02 -->

## Overview

ShopBot is a B2C e-commerce platform where Customers browse a Catalog,
add Products to a Cart, and place Orders for fulfillment by the Warehouse team.

## Bounded Contexts

| Context | Responsibility |
|---------|---------------|
| Core Domain | All domain concepts (single-context project) |

---

## Core Domain

| Term | Korean | Definition | Synonyms to Avoid |
|------|--------|-----------|------------------|
| Customer | 고객 | A registered user who has completed email verification and can place Orders. | User, Member, Buyer |
| Order | 주문 | A confirmed request by a Customer to purchase one or more Products. Created when Cart checkout succeeds. | Cart, Purchase, Invoice |
| OrderItem | 주문 항목 | A single Product with quantity and locked price within an Order. Immutable after Order creation. | LineItem, CartItem |
| Cart | 장바구니 | A temporary collection of Products a Customer intends to purchase. Destroyed upon Order creation. | Basket, Bag |
| Product | 상품 | A sellable item in the Catalog with SKU, price, and inventory count. | Item, Good, Merchandise |
| Catalog | 카탈로그 | The browsable collection of active Products available for purchase. | Shop, Store, Inventory |

---

## Change Log

| Date | Mode | Summary |
|------|------|---------|
| 2026-05-02 | new | Initial creation — 6 terms, Core Domain |
```

---

## LLM Injection Pattern

To give every Claude session automatic access to this vocabulary, add to `CLAUDE.md`:

```markdown
@docs/ubiquitous-language.md
```

This injects the full file into every session's context. Keep the file under 200 lines to avoid context pressure. If the file grows beyond 200 lines, split into per-context files and reference them individually.
