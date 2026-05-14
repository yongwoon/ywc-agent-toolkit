<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-parallel-executor (Ejecutor Paralelo)

Un Skill que ejecuta Tareas generadas por task-generator en paralelo usando Agentes. Analiza dependency-graph.md para realizar ejecución paralela basada en Waves con aislamiento de Git Worktree.

## Uso

```text
/ywc-parallel-executor 000001-010-db-create-events           # Tarea única
/ywc-parallel-executor 000001-010..000002-040                # Rango (paralelo)
/ywc-parallel-executor --all                                 # Ejecutar todo
/ywc-parallel-executor 000001-010..000002-040 --review       # Paralelo + Revisión automática
/ywc-parallel-executor 000001-010..000002-040 --local-merge  # Merge local sin PR
/ywc-parallel-executor 000001-010..000002-040 --draft        # Crear PR Borrador
```

## Opciones

| Opción | Descripción |
|--------|-------------|
| `--tasks-dir <path>` | Ruta del directorio de tareas (por defecto: tasks/) |
| `--review` | Ejecutar /ywc-impl-review automáticamente después de cada Tarea (combinable) |
| `--local-merge` | Sin PR, solo push a la rama base (comportamiento por defecto) |
| `--draft` | Crear PR Borrador después de que todas las Tareas estén completas |
| `--per-task-pr` | Crear PR individual por Tarea |

## Flujo de ejecución

1. Parsear dependency-graph.md
2. Planificar Waves (Ordenamiento Topológico)
3. Ejecutar por Wave: Crear Worktree → Ejecución de Agente Paralelo → Merge → Eliminar Worktree

## Mapeo automático Tarea → Agente

| Categoría | Agente |
|----------|-------|
| db, api, domain, lib, worker | Backend Agent (sonnet) |
| ui | Frontend Agent (sonnet) |
| test | QA Agent (sonnet) |
| infra | DevOps Agent (sonnet) |
| refactor | Reviewer Agent (opus) |

Sobrescribir con Agent Hint:
```markdown
## Parallel Execution Metadata
- Agent Hint: frontend
```

## Comparación con sequential-executor

| Escenario | Herramienta recomendada |
|----------|-----------------|
| Alcance pequeño (1-3 Tareas) | sequential-executor |
| Dependencias secuenciales fuertes | sequential-executor |
| Alcance grande (4+ Tareas) | /ywc-parallel-executor |
| Muchas Tareas paralelizables | /ywc-parallel-executor |

## Activación

Las condiciones de activación para este Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones localizadas

- [Inglés](./README.en.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
