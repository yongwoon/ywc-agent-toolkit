<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-agentic (Agentic Orchestrator)

Una Skill que toma un único objetivo en lenguaje natural y orquesta de forma autónoma las skills `ywc-*` existentes hasta la implementación del código. Mediante un bucle **Plan → Execute → Evaluate → Repeat**, replanifica hasta que la evaluación de `ywc-impl-review` pasa o se alcanza un límite máximo de iteraciones definido por el usuario.

Úsalo solo cuando el user solicite explícitamente autonomous end-to-end lifecycle delivery. Routea generic planning a `ywc-plan` y ordinary direct change al implementation workflow.

```text
User → Goal → Agent [Plan → Execute → Evaluate → Repeat] → Result
```

## Uso

```text
/ywc-agentic "Implement user authentication API"          # Objetivo en lenguaje natural
/ywc-agentic --goal "Add search feature" --max-iterations 5  # Establecer límite de iteraciones
/ywc-agentic "Implement payment module" --executor parallel  # Forzar un executor
/ywc-agentic "Refactoring work" --resume                  # Reanudar desde tasks/ existente
/ywc-agentic "Goal" --dry-run                             # Solo imprimir el plan de fases
```

## Opciones

| Opción                 | Descripción                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------- |
| `<goal>`               | Descripción en lenguaje natural del objetivo a lograr (posicional, obligatorio)        |
| `--goal <text>`        | Alternativa al `<goal>` posicional (el posicional gana si se proporcionan ambos)        |
| `--max-iterations <n>` | Máximo de iteraciones del bucle (predeterminado: 3, una válvula de seguridad que nunca se eleva de forma autónoma) |
| `--executor <mode>`    | Forzar un executor: sequential / parallel / auto (predeterminado: auto)                |
| `--tasks-dir <path>`   | Directorio para los directorios de task y agentic-log.md (predeterminado: tasks/)       |
| `--resume`             | Omitir la Plan Phase y reanudar desde tasks/ existente                                 |
| `--dry-run`            | Solo imprimir el plan de fases; no invocar ninguna skill                               |
| `--terse`              | Salida mínima (solo encabezados de fase y el informe final)                            |
| `--pr-lang <lang>`     | Idioma del título/descripción del PR (predeterminado: auto, inferido de CLAUDE.md)      |

## Flujo de Ejecución

1. Recibir y validar el objetivo
2. Detectar el context del proyecto → decidir Resume / Full Mode
3. Plan Phase — invocar `ywc-plan` (`--update-spec` en Re-plan)
4. Task Phase — invocar `ywc-task-generator` (solo Medium/Large)
5. Execute Phase — ejecutar el executor con `--local-merge` (Small Path usa `ywc-code-gen`)
6. Evaluate Phase — `ywc-impl-review --git-range` contra el spec original
7. Loop Control — Pass sale / Fail replanifica / informe de finalización parcial al alcanzar el límite
8. Iteration Log — añadir a `tasks/agentic-log.md`
9. Completion Report

## Small Path vs. Medium/Large Path

| Path              | Condición                                  | Ejecución                                             |
| ----------------- | ------------------------------------------ | ----------------------------------------------------- |
| Small Path        | `ywc-plan` devuelve un veredicto Small     | `ywc-code-gen` directamente (sin Task Phase ni executor) |
| Medium/Large Path | `ywc-plan` devuelve un veredicto Medium/Large | `ywc-spec-validate` → `ywc-task-generator` → executor |

## Skills Orquestadas

`ywc-plan` · `ywc-spec-validate` · `ywc-task-generator` · `ywc-sequential-executor` / `ywc-parallel-executor` · `ywc-impl-review` · `ywc-code-gen`

## Activación

Las condiciones de activación de esta Skill se definen en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones Localizadas

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
