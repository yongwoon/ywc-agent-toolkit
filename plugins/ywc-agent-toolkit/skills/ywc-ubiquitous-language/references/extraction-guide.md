# Extraction Guide — Finding Domain Terms in a Codebase

This guide is used by `ywc-ubiquitous-language` in `extract` mode to discover domain term candidates from an existing codebase.

## Extraction Philosophy

Not every class name is a domain term. The goal is to find names that represent **business concepts**, not technical plumbing. A `UserRepository` is a technical artifact; `User` and `Order` are domain concepts.

**Signal: likely domain term** — appears in domain/business layer, has meaningful state, is discussed in requirements
**Noise: likely plumbing** — has suffix Controller, Repository, Handler, Middleware, DAO, DTO, Mapper

---

## Step 1: Locate Domain Layer Files

Scan for directories and files that indicate domain logic:

```bash
# Common domain layer locations
find . -type d \( \
  -name "domain" -o \
  -name "model" -o \
  -name "models" -o \
  -name "entity" -o \
  -name "entities" \
\) | grep -v node_modules | grep -v .git

# Also check for DDD-style structures
find . -type d \( \
  -name "aggregate" -o \
  -name "valueobject" -o \
  -name "vo" \
\) | grep -v node_modules | grep -v .git
```

---

## Step 2: Extract Class / Struct / Type Names

### TypeScript / JavaScript

```bash
grep -rn "^export class\|^class\|^export interface\|^export type\|^export enum" \
  --include="*.ts" --include="*.tsx" \
  src/ app/ lib/ \
  | grep -v "\.spec\.\|\.test\.\|Controller\|Repository\|Service\|Handler\|Middleware\|DTO\|Mapper\|Factory\|Builder"
```

### Python

```bash
grep -rn "^class " \
  --include="*.py" \
  src/ app/ domain/ \
  | grep -v "test_\|Test\|Controller\|Repository\|Service\|Handler\|Middleware"
```

### Go

```bash
grep -rn "^type .* struct\|^type .* interface" \
  --include="*.go" \
  . \
  | grep -v "_test.go\|Repository\|Handler\|Controller\|Middleware\|DAO"
```

### Kotlin / Java

```bash
grep -rn "^data class\|^class\|^interface\|^enum class" \
  --include="*.kt" --include="*.java" \
  src/ \
  | grep -v "Test\|Controller\|Repository\|Service\|Handler\|DTO\|Mapper"
```

### Ruby

```bash
grep -rn "^class " \
  --include="*.rb" \
  app/models/ app/domain/ \
  | grep -v "test\|spec"
```

---

## Step 3: Extract Enum Values (Domain Event / State candidates)

Enum values often surface Domain Events and state transitions:

```bash
# TypeScript enums
grep -rn "= ['\"]" --include="*.ts" src/ | grep -i "status\|state\|type\|event"

# Python Enum
grep -rn "class.*Enum" --include="*.py" src/
```

---

## Step 4: Scan Comments and Docstrings

Domain term candidates often appear in comments near class definitions:

```bash
# Find classes with inline doc comments (TypeScript JSDoc)
grep -rn "^\s*\/\*\*\|^\s*\* " --include="*.ts" src/ | head -50

# Python docstrings
grep -rn '"""' --include="*.py" src/ | head -30
```

---

## Step 5: Check OpenAPI / Schema Definitions

If the project has API schemas, they often reflect the canonical domain model:

```bash
# OpenAPI definitions
find . -name "openapi.yaml" -o -name "openapi.json" -o -name "swagger.yaml" | head -5

# JSON Schema / Prisma / Drizzle / TypeORM models
find . \( -name "schema.prisma" -o -name "*.schema.ts" -o -name "*.entity.ts" \) \
  | grep -v node_modules
```

---

## Step 6: Cluster by Module Path

Once candidates are collected, group them by the top-level module/package they come from. Each group is a Bounded Context candidate.

Example mapping:

| Candidate Terms | Source Path | Context Candidate |
|----------------|-------------|------------------|
| Order, OrderItem, Cart | `src/order/` | Order |
| Payment, Invoice, Refund | `src/payment/` | Payment |
| Product, Category, Catalog | `src/catalog/` | Catalog |
| User, Profile, Address | `src/user/` | Identity |

---

## Noise Filter — Terms to Exclude

| Pattern | Example | Reason |
|---------|---------|--------|
| Infrastructure suffixes | `OrderRepository`, `PaymentGateway` | Technical, not domain |
| Controller/Handler/Middleware | `OrderController` | Presentation layer |
| DTO/Request/Response | `CreateOrderRequest` | Transport layer |
| Test classes | `OrderTest`, `MockPayment` | Test artifacts |
| Generic utilities | `BaseEntity`, `AbstractModel` | Framework boilerplate |
| Pure config | `DatabaseConfig`, `AppSettings` | Not domain concepts |

---

## Output Format for User Confirmation

After extraction, present candidates as a table grouped by context:

```
Found the following domain term candidates:

## Order Context (src/order/)
| Candidate | Source | Keep? |
|-----------|--------|-------|
| Order | order.entity.ts:5 | ✓ |
| OrderItem | order-item.value-object.ts:3 | ✓ |
| OrderStatus | order-status.enum.ts:1 | ? |

## Payment Context (src/payment/)
| Candidate | Source | Keep? |
|-----------|--------|-------|
| Payment | payment.entity.ts:7 | ✓ |
| Invoice | invoice.entity.ts:2 | ? |

Please confirm which terms to include. For each confirmed term,
I'll ask for definition, Korean equivalent, and synonyms to avoid.
```
