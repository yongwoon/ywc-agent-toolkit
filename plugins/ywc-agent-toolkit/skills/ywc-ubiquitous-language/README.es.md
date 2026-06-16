<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-ubiquitous-language

Un skill para crear y mantener el documento de Lenguaje Ubicuo de un proyecto — el vocabulario de dominio compartido que alinea a desarrolladores, expertos del dominio y LLMs en el uso canónico de términos. Produce y gestiona `docs/ubiquitous-language.md`.

Soporta tres modos: **new** (creación desde cero mediante entrevista), **extract** (descubrimiento de términos de una base de código existente), y **update** (revisión incremental de un documento existente).

## Casos de uso

- Crear un glosario de dominio compartido al inicio de un nuevo proyecto
- Analizar una base de código existente para aflorar términos de dominio implícitos en un documento formal
- Actualizar el glosario después de añadir nuevas funcionalidades
- Dar a los LLMs acceso automático al vocabulario del proyecto via `@docs/ubiquitous-language.md` en CLAUDE.md

## Cómo usar

```bash
/ywc-ubiquitous-language
```

O mediante lenguaje natural:

> "Create a ubiquitous language document"
> "Extract domain terms from the codebase"
> "Update our ubiquitous language"
> "Create a domain glossary"

### Autodetección de modo

| Condición | Modo seleccionado automáticamente |
|-----------|------------------|
| `docs/ubiquitous-language.md` existe | `update` |
| Archivo ausente + archivos fuente encontrados (`src/`, `app/`, etc.) | `extract` |
| Archivo ausente + sin archivos fuente | `new` |

Sobrescribir con `--mode new|extract|update`.

## Entradas

- (Opcional) Descripción del dominio — "This is a B2B e-commerce platform"
- (Opcional) `--mode new|extract|update` — forzar un modo específico
- (Opcional) `--context <name>` — limitar a un único Bounded Context
- (Opcional) `--ddd` — añadir columna de Tipo DDD (Entity / Value Object / Aggregate / Domain Event / Policy)
- (Opcional) `--output <path>` — ruta del archivo de salida (por defecto: `docs/ubiquitous-language.md`)

## Salida

- `docs/ubiquitous-language.md` — tablas de términos organizadas por Bounded Context
- Al finalizar: imprime un prompt para añadir `@docs/ubiquitous-language.md` a CLAUDE.md

## Ejemplo de salida

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

## Skills relacionados

- `ywc-plan` — Usar juntos cuando se establece vocabulario antes de escribir especificaciones
- `ywc-project-docs` — Gestiona la estructura general del directorio docs/ (upstream)
- `ywc-spec-validate` — Verifica que los términos de la especificación coincidan con el lenguaje ubicuo
- `ywc-task-generator` — Downstream: descomponer trabajo después de establecer el vocabulario
- `ywc-code-gen` — Aplica la nomenclatura canónica del glosario durante la generación de código
