# ywc-ubiquitous-language

A skill for creating and maintaining a project's Ubiquitous Language document — the shared domain vocabulary that aligns developers, domain experts, and LLMs on canonical term usage. Produces and manages `docs/ubiquitous-language.md`.

Supports three modes: **new** (interview-driven creation from scratch), **extract** (term discovery from an existing codebase), and **update** (incremental revision of an existing document).

## Usage Scenarios

- Creating a shared domain glossary at the start of a new project
- Analyzing an existing codebase to surface implicit domain terms into a formal document
- Updating the glossary after new features are added
- Giving LLMs automatic access to project vocabulary via `@docs/ubiquitous-language.md` in CLAUDE.md

## How to Use

```bash
/ywc-ubiquitous-language
```

Or via natural language:

> "Create a ubiquitous language document"
> "Extract domain terms from the codebase"
> "Update our ubiquitous language"
> "Create a domain glossary"

### Mode Auto-Detection

| Condition | Auto-selected Mode |
|-----------|------------------|
| `docs/ubiquitous-language.md` exists | `update` |
| File absent + source files found (`src/`, `app/`, etc.) | `extract` |
| File absent + no source files | `new` |

Override with `--mode new|extract|update`.

## Inputs

- (Optional) Domain description — "This is a B2B e-commerce platform"
- (Optional) `--mode new|extract|update` — force a specific mode
- (Optional) `--context <name>` — scope to a single Bounded Context
- (Optional) `--ddd` — add a DDD Type column (Entity / Value Object / Aggregate / Domain Event / Policy)
- (Optional) `--output <path>` — output file path (default: `docs/ubiquitous-language.md`)

## Output

- `docs/ubiquitous-language.md` — term tables organized by Bounded Context
- After completion: prints a prompt to add `@docs/ubiquitous-language.md` to CLAUDE.md

## Output Example

```markdown
# Ubiquitous Language — ShopBot

<!-- updated: 2026-05-02 -->

## Bounded Contexts

| Context | Responsibility |
|---------|---------------|
| Order   | Order lifecycle from placement through fulfillment |

---

## Order

| Term      | Korean    | Definition                                          | Synonyms to Avoid |
|-----------|-----------|-----------------------------------------------------|------------------|
| Order     | 주문      | A confirmed request by a Customer to purchase items | Cart, Purchase    |
| OrderItem | 주문 항목 | A single product-quantity pair within an Order      | LineItem, CartItem |
```

## Related Skills

- `ywc-plan` — Use together when establishing vocabulary before writing specs
- `ywc-project-docs` — Manages the overall docs/ directory structure (upstream)
- `ywc-spec-validate` — Checks that spec terms match the ubiquitous language
- `ywc-task-generator` — Downstream: decompose work after vocabulary is established
- `ywc-code-gen` — Applies canonical naming from the glossary during code generation
