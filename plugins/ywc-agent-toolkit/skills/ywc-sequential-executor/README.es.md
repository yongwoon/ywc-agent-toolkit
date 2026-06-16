<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Skill Sequential Executor (ywc-sequential-executor)

Esta Skill de Codex ejecuta tareas generadas por la Skill ywc-task-generator. Automatiza el ciclo de vida completo de desarrollo, desde la creación de ramas hasta la implementación, commit, creación de PR, verificación de CI, merge y sincronización local.

Soporta tanto la ejecución de una sola tarea como la ejecución secuencial de rangos.

## Uso

### Uso Básico

Ejecutar una sola tarea:

```text
/ywc-sequential-executor 000001-010-db-create-users-table
```

También se puede especificar por prefijo de fase+secuencia:

```text
/ywc-sequential-executor 000001-010
```

### Ejecución por Rango

Ejecutar tareas consecutivas secuencialmente en un bucle:

```text
/ywc-sequential-executor 000001-010..000002-030
```

### Detección Automática de la Siguiente Tarea

Cuando no se especifica ninguna tarea, la Skill analiza el grafo de dependencias y selecciona la siguiente tarea ejecutable:

```text
/ywc-sequential-executor
```

### Opciones

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--pr-lang <lang>` | Idioma del título/descripción del PR | `--pr-lang ja` |
| `--tasks-dir <path>` | Ruta del directorio de tareas (predeterminado: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--skip-ci-wait` | Omitir espera de CI y auto-merge (solo creación de PR) | |
| `--draft` | Crear PR borrador, omitir merge | |
| `--local-merge` | Omitir PR completamente — mergear la rama de función en la rama base localmente y hacer push (la verificación del Paso 4 sigue ejecutándose) | |
| `--base-branch <branch>` | Sobrescribir la rama base (predeterminado: auto-detección) | `--base-branch develop` |
| `--dry-run` | Mostrar el plan de ejecución (orden de tareas, dependencias, modo) sin ejecutar | |

> `--local-merge`, `--draft` y `--skip-ci-wait` son mutuamente excluyentes. La Skill se detiene y pregunta qué modo se pretendía si se pasa más de uno.
> `--local-merge` **no ejecuta CI remoto**, por lo que la única red de seguridad para el merge es la verificación local del Paso 4 (lint/typecheck/test). Evítalo para cambios sensibles.

## Ciclo de Ejecución

Para cada tarea, los siguientes pasos se ejecutan en orden. **En modo de rango, el ciclo completo (Paso 1 → Paso 8) se repite para cada tarea. Cada tarea obtiene su propia rama de función independiente.**

### Ciclo de Vida de Rama Por Tarea en Modo de Rango

**Modo normal (flujo de PR):**
```text
Por tarea: checkout base → pull → crear rama de función → implementar → PR → CI → merge → repetir
```

**Modo `--local-merge`:**
```text
Por tarea: checkout base → pull → crear rama de función → implementar → merge local → push → repetir
```

**Modo `--draft` / `--skip-ci-wait`:**
```text
Por tarea: crear rama desde la rama de función anterior (ramificación en cadena) → implementar → PR borrador → repetir
```

### Detalles de los Pasos

```text
Paso 1: Validación de Dependencias y Carga de Especificaciones
  └─ Verificar que todas las tareas de Depends On existen en tasks/completed/
  └─ Cargar la Referencia de Especificaciones de README.md (Fuentes Primarias / Resumen / Fuera de Alcance)
  └─ Las URLs externas siguen la política taskExecutor.externalSpecUrls en Codex approval settings or the project-local policy file

Paso 2: Creación de Rama (se ejecuta para cada tarea — nunca se omite en modo de rango)
  └─ (normal/local-merge) git checkout <base> && git pull && git checkout -b feature/<task-name>
  └─ (rango+draft/skip-ci-wait) Crear rama desde la rama de función anterior (ramificación en cadena)

Paso 3: Implementación
  └─ Implementar siguiendo los Pasos de Implementación de task.md, hacer commit en límites lógicos

Paso 4: Verificación de Tarea
  └─ Ejecutar comandos de Verificación de Tarea y lint/typecheck/test

Paso 5: Creación de PR
  └─ Invocar Skill create-pr (incluye verificación de seguridad, validación pre-push de CI)
  └─ (--local-merge) omitir — no se crea PR

Paso 6: Verificación de CI y Merge
  └─ gh pr checks --watch → gh pr merge --delete-branch
  └─ (--local-merge) git checkout base → git merge --no-ff feature/<task> → git push → git branch -d

Paso 7: Sincronización Local
  └─ git checkout <base-branch> && git pull origin <base-branch>

Paso 8: Marcar como Completado
  └─ mv tasks/<task-name> tasks/completed/<task-name> → commit
  └─ Rango --local-merge: push inmediatamente después de cada tarea
  └─ Rango normal de PR: push se ejecuta una vez después de que la tarea final se completa

Paso 9: Siguiente Tarea (Modo de rango)
  └─ Volver al Paso 1 y repetir el ciclo completo (incluyendo el Paso 2) si quedan tareas
```

## Idioma del PR

Cuando `--pr-lang` no se especifica, el idioma se detecta con esta prioridad:

1. **CLAUDE.md** — Verificar directivas de idioma (por ejemplo, `Git commits: Japanese`)
2. **AGENTS.md** — Verificar preferencias de idioma
3. **Historial reciente de PRs** — Detectar el idioma dominante
4. **Fallback** — Inglés

## Manejo de Errores

| Situación | Comportamiento |
|-----------|----------------|
| Fallo de CI | Hasta 2 intentos de corrección, luego notificar al usuario |
| Conflicto de merge | Detenerse y pedir al usuario que lo resuelva manualmente |
| Timeout de CI (>30 min) | Reportar el estado y preguntar al usuario si continuar |
| Dependencia no cumplida | Listar dependencias incompletas y detenerse |
| Tarea no encontrada | Mostrar tareas disponibles |

## Integración

Esta Skill funciona con:

- **ywc-task-generator** — Generación de tareas (upstream)
- **create-pr** — Creación de PR (invocado en el Paso 5)

## Ejemplo de Prompt

### Ejecución de tarea única (PR en japonés)

```text
/ywc-sequential-executor 000001-010-db-create-users-table --pr-lang ja
```

### Ejecución de rango completo

```text
/ywc-sequential-executor 000001-010..000003-020 --pr-lang ja
```

### Solo PR borrador (sin merge)

```text
/ywc-sequential-executor 000001-010..000002-030 --draft --pr-lang ko
```

### Comportamiento con conflicto de flags

Si se pasan `--local-merge`, `--draft` y `--skip-ci-wait` juntos, la Skill se detiene y pregunta qué modo se desea realmente. Estos flags producen estados finales incompatibles (el primero significa "sin PR, mergeado"; los otros significan "el PR existe, no mergeado"), por lo que la Skill se niega a adivinar.

```text
/ywc-sequential-executor 000001-010 --local-merge --draft
# → Se detiene. "--local-merge and --draft are mutually exclusive. Which mode did you want?"
```

### Merge local sin PR

Usar cuando el flujo de trabajo con PR es innecesario — por ejemplo, proyectos personales o hotfixes:

```text
/ywc-sequential-executor 000001-010-db-create-users-table --local-merge
```

El lint/typecheck/test del Paso 4 sigue ejecutándose. En caso de éxito, la rama de función se mergea en la rama base con `git merge --no-ff` y se hace push.

## Activación

Las condiciones de activación de esta Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).
