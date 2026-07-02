<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-review-learnings

Un Skill que acumula preferencias de code-review por proyecto para que la calidad de review mejore con el tiempo. Implementa el concepto de “learnings” de CodeRabbit en una forma runtime-agnostic (sin bot alojado), almacenada como un archivo Markdown versionable `docs/review-learnings.md` que `ywc-impl-review` carga antes de revisar.

La propiedad clave es que cada learning registra no solo *qué* hacer sino **por qué**. Ese why permite que un learning se generalice a situaciones parecidas pero no idénticas, en lugar de degradarse en un keyword match frágil.

## Modes

- **read** — carga los learnings cuyo scope coincide con los review-target globs y los inyecta en los reviewers
- **update** — captura nuevos learnings desde feedback del usuario, un review completado o comentarios de PR bot
- **list** — muestra los learnings actuales
- **curate** — depreca learnings obsoletos o contradictorios (nunca hard-delete)

## Cuándo usarlo

- Enseñar al reviewer que un false positive es aceptable en tu entorno, para que no lo vuelva a reportar
- Acumular recurring findings (por ejemplo, falta de owner-key predicate en una ownership-scoped query) como durable rules detectadas antes
- Absorber los comentarios de CodeRabbit / Codex PR que aceptaste en tu review interno
- Añadir una instrucción en AGENTS.md o CODEX.md para leer `docs/review-learnings.md`, de modo que cada Codex session comparta las preferencias de review del proyecto

## Uso

```text
Use $ywc-review-learnings to update the project review learnings.
```

O en lenguaje natural:

> “this is a false positive, remember it”
> “load the review learnings that apply to this path”
> “turn PR #128's CodeRabbit comments into review learnings”
> “clean up the review learnings”

## Entrada

- (opcional) `--mode read|update|list|curate` — fuerza un mode (auto-detectado si se omite)
- (opcional) `--target <glob|path...>` — review-target paths
- (opcional) `--source feedback|review|pr` — learning source para update mode (por defecto `feedback`)
- (opcional) `--pr <number>` — PR desde el que se cosechan comentarios de bot con `--source pr`
- (opcional) `--output <path>` — learnings file path (por defecto `docs/review-learnings.md`)
- (opcional) `--dry-run` — muestra el CHANGESET sin escribir

## Salida

- `docs/review-learnings.md` — tabla de `ID / Scope / Category / Polarity / Rule / Why / Provenance`
- en update: bloque de confirmación `Learnings added` que indica exactamente qué cambió
- en la primera creación del archivo: prompt de activación que recomienda una instrucción en AGENTS.md o CODEX.md para que futuras Codex sessions lean `docs/review-learnings.md`

## Skills relacionados

- `ywc-impl-review` — llama a este Skill en read mode antes de revisar y en update mode después
- `ywc-handle-pr-reviews` — un comentario de bot descartado puede alimentar `update --source pr`
- `ywc-ubiquitous-language` — misma arquitectura de knowledge-file por proyecto, distinto dominio de contenido
- `ywc-receive-review` — disciplina para *responder* feedback de review; este Skill *almacena* la lección durable producida
