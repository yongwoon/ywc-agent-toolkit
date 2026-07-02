<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-project-mission

Una skill que persiste la Mission / North-Star duradera de un proyecto, los Success Criteria medibles y los no-objetivos Out-of-Scope en `docs/project-mission.md`, un archivo Markdown confirmado e independiente del runtime. Sigue la misma arquitectura stateful-file que `ywc-review-learnings`: `ywc-plan` carga este archivo antes de aclarar cualquier solicitud nueva, de modo que cada planning session queda enmarcada por la misma north-star en lugar de rederivarse desde cero.

La idea clave: a diferencia de un plan puntual que se descarta una vez que se entrega una funcionalidad, la Mission registra la intención *duradera* que sobrevive a cualquier funcionalidad individual. Cada entrada lleva su procedencia y fecha, de modo que un lector puede distinguir un compromiso actual de una dirección abandonada.

## Modos compatibles

- **read** — carga la Mission para enmarcar la planificación (normalmente llamado por `ywc-plan`)
- **update** — captura o revisa Mission / Success Criteria / no-objetivos desde una fuente confirmada
- **list** — muestra la Mission actual
- **curate** — deja obsoletas las entradas antiguas o superadas (nunca las borra por completo)

## Cuándo usarla

- Cuando quieras persistir la Mission (What+Why) y los Success Criteria (Done When) producidos por un brainstorm a nivel de proyecto
- Cuando quieras que `ywc-plan` enmarque sus preguntas y Acceptance Criteria a partir de la misma Mission en lugar de rederivar la north-star cada session
- Cuando quieras registrar explícitamente no-objetivos duraderos ("este proyecto nunca hará X")
- Cuando quieras que los LLM entiendan automáticamente la Mission del proyecto añadiendo `@docs/project-mission.md` a CLAUDE.md

## Cómo usarla

```bash
/ywc-project-mission
```

O actívala mediante lenguaje natural:

> "Remember this project's mission"
> "Capture the success criteria"
> "What is the current project mission?"

## Entrada

- (opcional) `--mode read|update|list|curate` — fuerza un modo (autodetectado si se omite)
- (opcional) `--source brainstorm|plan` — procedencia de una Mission/criterio en modo update (por defecto `brainstorm`)
- (opcional) `--output <path>` — ruta del archivo de mission (por defecto `docs/project-mission.md`)
- (opcional) `--dry-run` — muestra el CHANGESET sin escribir

## Salida

- `docs/project-mission.md` — Mission / North-Star, tabla de Success Criteria (`ID | Criterion | Source | Added | Status`), Out of Scope, un Change Log mantenido automáticamente
- En update: presenta un CHANGESET ADD / MODIFY / DEPRECATE, escribe solo las entradas confirmadas, imprime un bloque de confirmación `Mission updated`
- En la primera creación del archivo: imprime el prompt de activación `@docs/project-mission.md` de CLAUDE.md exactamente una vez
- Reejecución idempotente: un CHANGESET vacío → sin escritura de archivo, sin actualización de fecha

## Skills relacionadas

- `ywc-brainstorm` — el Step 6 Handoff ofrece persistir la Mission (What+Why) y los Success Criteria (Done When) mediante `update --source brainstorm` (opt-in)
- `ywc-plan` — el Step 1 carga la Mission en modo read para enmarcar preguntas y sembrar Acceptance Criteria
- `ywc-review-learnings` — la misma arquitectura stateful-file por proyecto (read/update/list/curate, escrituras confirmadas por el usuario), dominio distinto (intención duradera vs preferencias de review)
- `ywc-ubiquitous-language` — gestiona el *vocabulario* del dominio; esta skill almacena la *intención* del dominio (no confundir ambas)
