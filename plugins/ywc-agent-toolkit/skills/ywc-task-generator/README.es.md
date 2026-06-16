<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Habilidad Generadora de Tareas

Esta Habilidad de Codex convierte una especificación en tareas de implementación seguras en cuanto a dependencias y revisables.

Está diseñada no solo para la descomposición ordinaria de tareas, sino también para conjuntos de tareas que posteriormente pueden ejecutarse en paralelo mediante `git worktree` y sesiones separadas de Codex o Codex.

## Uso

### Uso Básico

Proporciona una especificación y solicita a la Habilidad que genere tareas:

```text
/task-generator [Specification content]
```

También puede solicitar que refine un conjunto de tareas existente:

```text
/task-generator refine docs/spec.md for parallel worktree execution.
```

### Opciones de Idioma

La Habilidad admite salida en coreano, japonés e inglés.

| Idioma | Ejemplo |
|--------|---------|
| Coreano | `Output in Korean.` |
| Japonés | `日本語でタスクを生成してください。` |
| Inglés | `Generate tasks in English.` |

Si el usuario no especifica un idioma, la Habilidad lo pregunta.

Para salidas en coreano y japonés, los términos técnicos permanecen en inglés.

### Opciones de Modo de Granularidad

La Habilidad admite dos modos de granularidad de tareas y **siempre pregunta qué modo aplicar** — no existe un valor predeterminado silencioso.

| Modo   | Guía de tamaño          | Optimizado para                                                  |
|--------|-------------------------|------------------------------------------------------------------|
| human  | ~10 archivos / ~300 LOC | Revisión humana por PR                                           |
| llm    | ~25 archivos / ~800 LOC | Sesión de agente LLM único en un worktree aislado                |

Las Invariantes de Seguridad (separación de migración de BD, separación de introducción de librería, puerta de fase, compilabilidad post-tarea) aplican de forma idéntica en ambos modos. Consulte [references/granularity-modes.md](./references/granularity-modes.md) para la especificación completa.

## Estructura de Salida

### Directorio de Tareas

```text
tasks/
├── 000001-010-db-create-user-table/
│   ├── README.md
│   ├── task.md
│   └── test.md
├── 000001-020-api-user-registration/
│   ├── README.md
│   └── task.md
└── dependency-graph.md
```

### Nomenclatura de Tareas

```text
[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]
```

- `PHASE`: 6 dígitos, etapa de dependencia (reserva margen para el crecimiento de proyectos plurianuales)
- `SEQUENCE`: 3 dígitos, se incrementa de 10 en 10
- `CATEGORY`: `lib` | `db` | `api` | `domain` | `worker` | `ui` | `test` | `refactor` | `infra`

### Finalización de Tareas

Tras la finalización y el merge:

```text
mv tasks/000001-010-db-create-user-table tasks/completed/000001-010-db-create-user-table
```

## Principios Fundamentales

| Principio | Descripción |
|-----------|-------------|
| Revisabilidad | Cada tarea debe ser revisable en aproximadamente 1 hora |
| Seguridad de Dependencias | Sin dependencia hacia adelante; cada tarea es implementable en su posición |
| Separación de Migración de BD | La migración de base de datos debe ser su propia tarea |
| Separación de Introducción de Librerías | Las nuevas librerías y frameworks deben estar aislados |
| Preocupación Única | Una tarea debe representar una preocupación primaria |
| Seguridad Paralela | Las tareas deben incluir suficientes metadatos para ejecución en worktree aislado |

## Operación en Worktree Paralelo

Cuando las tareas puedan ejecutarse en paralelo, el conjunto de tareas generado debe incluir metadatos operacionales.

### Metadatos Requeridos por Tarea

Cada `README.md` debe incluir:

- `Spec Reference` — Fuentes Primarias (enlaces a PRD / diseño técnico), Resumen (orientación en 2–5 oraciones) y guardia de Fuera del Alcance (de la especificación). Las tareas de mantenimiento sin especificación deben registrar explícitamente `N/A — no external spec` en lugar de omitir la sección.
- `Ownership`
- `Shared Surfaces`
- `Conflicts With`
- `Parallelizable After`
- `Task Verify`

> Las URLs externas en `Primary Sources` (Notion, Confluence, Figma, etc.) requieren una política a nivel de proyecto. El valor predeterminado son solo rutas relativas al proyecto; `sequential-executor` almacena la política elegida en `Codex approval settings or the project-local policy file` bajo `taskExecutor.externalSpecUrls`.

### Ownership vs Key Files

- `Key Files` es una previsión de archivos que se tocarán
- `Ownership` es el límite operativo real
- Si difieren, tratar `Ownership` como autoritativo

### Programación del Gráfico de Dependencias

`tasks/dependency-graph.md` permanece como la fuente de verdad para el orden de ejecución.
Cuando se espera trabajo paralelo, incluir `Parallel Execution Notes` describiendo:

- el conjunto inicial listo para ejecutar
- las tareas que se pueden ejecutar después de cada límite de merge
- las tareas bloqueadas por conflictos en lugar de por orden de dependencia

### Adiciones de Prompt Recomendadas

Para salida compatible con ejecución paralela, solicitar explícitamente:

```text
- Parallel Execution Metadata for every task
- Ownership as an operating boundary
- Conflicts With for shared contracts, schema, or config
- Parallel Execution Notes in dependency-graph.md
```

## Ejemplo de Prompt

```text
/task-generator break down this specification into implementation tasks.

Requirements:
- Output in Korean.
- Assume tasks may be executed in parallel via git worktrees and separate Codex sessions.
- For every task README, include Ownership, Shared Surfaces, Conflicts With, Parallelizable After, and Task Verify.
- Ownership must be an operating boundary, not just a summary of expected files.
- In dependency-graph.md, include Parallel Execution Notes.

Specification:
[PASTE SPEC HERE]
```

## Palabras Clave de Activación

Esta Habilidad se ajusta a solicitudes como:

- `task generation`
- `task breakdown`
- `spec to tasks`
- `refine existing tasks`
- `parallel worktree tasks`
