<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-docker-isolate

## Resumen

`ywc-docker-isolate` evita colisiones de host port de Docker compose durante el desarrollo paralelo con Git worktrees. Cada worktree deriva un bloque determinista de host ports y `COMPOSE_PROJECT_NAME` desde el task name, y solo escribe un bloque gestionado en el `.env` local del worktree y el archivo persistente `.ywc-docker-ports`.

## Cuándo usarlo

| Situación | Uso |
|---|---|
| Varios Git worktrees ejecutan sus propios Docker compose stacks | Sí |
| `ywc-parallel-executor` crea y limpia task worktrees | Sí |
| `ywc-sequential-executor` ejecuta un task a la vez sin worktrees | No |
| Puertos de procesos locales no Docker o aislamiento de devcontainer | No |

## Modes

| Mode | Action | Key args | Exit |
|---|---|---|---|
| `setup` | Deriva el bloque de ports y escribe env-file/persist data | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | Ejecuta `down --volumes` para el stack acotado del worktree | `--task-name` o `--project-name`, `--worktree-path` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | Reporta residual stacks | `--expect t1,t2` `[--prune]` | Siempre 0; stdout no vacío indica residuals |

## Integration

Este Skill se usa como hooks de nivel puntero desde `ywc-parallel-executor`.

- Después de planning: `audit --expect <selected tasks>`
- Después de Step 4a verification: `setup --task-name <task> --worktree-path <worktree>`
- Antes de Step 4g cleanup: `teardown --task-name <task> --worktree-path <worktree>`

## Verification

```bash
bash -n codex/skills/ywc-docker-isolate/scripts/*.sh
bash scripts/validate.sh
find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort
```

Consulta [references/port-allocation.md](references/port-allocation.md) para el algoritmo y [references/preconditions.md](references/preconditions.md) para las reglas de detección.
