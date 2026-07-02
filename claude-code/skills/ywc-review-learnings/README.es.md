<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-review-learnings

Una Skill que acumula preferencias de code-review por proyecto para que la calidad de la review mejore con el tiempo. Implementa el concepto de "learnings" de CodeRabbit en una forma independiente del runtime (sin necesidad de un bot alojado), almacenado como un archivo Markdown commiteable `docs/review-learnings.md` que `ywc-impl-review` carga antes de revisar.

La propiedad clave es que cada learning registra no solo *qué* hacer, sino **por qué**. El porqué es lo que permite que un learning se generalice a situaciones similares-pero-no-idénticas en lugar de degradarse en una coincidencia de keyword frágil.

## Modos

- **read** — carga los learnings cuyo scope coincide con los globs del objetivo de review y los inyecta en los reviewers
- **update** — captura nuevos learnings a partir de la retroalimentación del usuario, una review completada o comentarios recolectados de PR bots
- **list** — muestra los learnings actuales
- **curate** — deprecia learnings obsoletos o contradictorios (nunca los elimina de forma definitiva)

## Cuándo Usar

- Enseñar al reviewer que un false positive es aceptable en tu entorno, para que deje de volver a plantearlo en la siguiente review
- Acumular hallazgos recurrentes (por ejemplo, un predicado owner-key faltante en una consulta con scope de propiedad) como reglas duraderas detectadas antes
- Absorber los comentarios de PR de CodeRabbit / Codex que aceptaste en tu review interna
- Agregar `@docs/review-learnings.md` a CLAUDE.md para que cada session de LLM comparta las preferencias de review del proyecto

## Uso

```bash
/ywc-review-learnings
```

O mediante lenguaje natural:

> "this is a false positive, remember it"
> "load the review learnings that apply to this path"
> "turn PR #128's CodeRabbit comments into review learnings"
> "clean up the review learnings"

## Entrada

- (opcional) `--mode read|update|list|curate` — forzar un modo (auto-detectado si se omite)
- (opcional) `--target <glob|path...>` — rutas del objetivo de review
- (opcional) `--source feedback|review|pr|debug|incident` — fuente del learning para el modo update (por defecto `feedback`; `debug`/`incident` capturan elementos de root-cause / prevención de incidentes)
- (opcional) `--pr <number>` — PR del que recolectar comentarios de bot con `--source pr`
- (opcional) `--output <path>` — ruta del archivo de learnings (por defecto `docs/review-learnings.md`)
- (opcional) `--dry-run` — mostrar el CHANGESET sin escribir

## Salida

- `docs/review-learnings.md` — una tabla de `ID / Scope / Category / Polarity / Rule / Why / Provenance`
- en update: un bloque de confirmación `Learnings added` que indica exactamente qué cambió
- en la primera creación del archivo: un prompt de activación que recomienda agregar `@docs/review-learnings.md` a CLAUDE.md (esta referencia es lo que hace que cada review y session de LLM futuras carguen los learnings automáticamente)

## Ejemplo de Salida

```markdown
# Review Learnings — ShopBot

<!-- updated: 2026-06-13 -->

## Learnings

| ID   | Scope          | Category | Polarity       | Rule | Why | Provenance |
|------|----------------|----------|----------------|------|-----|-----------|
| L001 | `**/*.sql`     | Security | DO             | Every query on an ownership-scoped table includes the owner-key predicate | App-layer filtering fails open the moment one query forgets WHERE owner_id=? | PR#42, 2026-06-13 |
| L002 | `**/*.test.ts` | Test     | FALSE-POSITIVE | Do not flag top-level await in test setup files | The runner supports it; flagging it is noise | dismissed PR#51, 2026-06-13 |
```

## Skills Relacionadas

- `ywc-impl-review` — llama a esta Skill en modo read antes de revisar y en modo update después
- `ywc-handle-pr-reviews` — un comentario de bot descartado puede alimentar `update --source pr`
- `ywc-ubiquitous-language` — misma arquitectura de knowledge-file por proyecto, diferente dominio de contenido
- `ywc-receive-review` — disciplina para *responder* a la retroalimentación de review; esta Skill *almacena* la lección duradera que produjo
