<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-docker-isolate

Elimina la colisión de puertos de host de Docker Container ("port is already
allocated") que surge durante el desarrollo paralelo con Git worktree. Cada
worktree deriva un bloque único de puertos de host de forma **determinista** a
partir de su nombre de task, de modo que múltiples worktrees pueden ejecutar
stacks de Docker independientes simultáneamente.

## Comportamiento Principal

- **per-worktree namespacing**: `COMPOSE_PROJECT_NAME = ywc-<sanitized-task>` más
  `port = 20000 + (hash(task) % 100) * 100 + var_index`.
- **original inmutable (NFR-1)**: escribe únicamente un bloque gestionado en el
  env-file local del worktree y el archivo de persistencia `.ywc-docker-ports`;
  nunca modifica el compose / env-file confirmado.
- **determinista (AC2)**: las reejecuciones vuelven a leer `.ywc-docker-ports`
  para obtener puertos idénticos y ejecutan una comprobación en vivo
  multiplataforma que falla ruidosamente ante un ocupante.

## Modes

| Mode | Acción | Argumentos clave | Exit |
|---|---|---|---|
| `setup` | derivar bloque de puertos + escribir env-file/persistencia | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | `down --volumes` solo para el stack de este worktree | `--task-name`\|`--project-name` `--worktree-path` `[--keep-volumes]` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | reportar stacks residuales (stdout no vacío) | `--expect t1,t2` `[--prune]` | always 0 |

## Puntos de Integración con ywc-parallel-executor

- **Pre-flight**: `audit --expect <wave tasks>` — abortar la ejecución si hay residuales.
- **Step 4a** (por task): `setup` — exit 1 → task BLOCKED, worktree preservado.
- **Step 4g** (antes de `cleanup-worktree.sh`): `teardown` — los worktrees preservados lo omiten.

## Ejemplo

```bash
# Aplicar aislamiento de puertos a un worktree de task
bash scripts/setup-docker-ports.sh --task-name feat-a --worktree-path /path/wt-a

# Desmontar el stack del worktree (incluyendo volumes)
bash scripts/teardown-docker.sh --task-name feat-a --worktree-path /path/wt-a

# Auditar stacks residuales
bash scripts/audit-docker-stacks.sh --expect feat-a,feat-b
```

## Referencias

- [references/port-allocation.md](references/port-allocation.md) — fórmula de hash, regla de ordenación, salt chain, garantía de determinismo
- [references/preconditions.md](references/preconditions.md) — detección de compose, límites de env-var, herramientas de plataforma, precedencia
