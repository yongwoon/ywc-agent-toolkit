<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-worktrees

Skill de gestión del ciclo de vida de Git worktree. Fuente única de verdad para la resolución de prioridad de worktree (`.worktrees/` > CLAUDE.md `worktree_root` > `--root` fallback), invocada por `ywc-parallel-executor` y `ywc-finish-branch`.

## Modos

- `--mode resolve` — imprime la ruta donde aterrizaría un worktree (sin efectos secundarios)
- `--mode create` — ejecuta `git worktree add` y verifica el registro
- `--mode audit` — detecta worktrees obsoletos / filtrados / faltantes (Pre-flight o wave-end)
- `--mode prune` — limpieza post-merge (`git worktree remove` + eliminación de la branch local + `git worktree prune` + verificación). Pasa `--keep-branch` para eliminar solo el worktree y preservar la branch local (por ejemplo, mantener una integration branch para un PR de trunk posterior).

Para la tabla completa de argumentos y la cadena de resolución de prioridad, consulta [SKILL.md](./SKILL.md).

## Scripts Incluidos

| Script | Purpose |
|---|---|
| `scripts/audit-worktrees.sh` | Lógica central de auditoría para `--mode audit` |
| `scripts/cleanup-worktree.sh` | Lógica central de limpieza y eliminación de branch para `--mode prune` |

Ambos scripts se movieron desde `ywc-parallel-executor/scripts/` mediante `git mv` para preservar su historial de commits.

## Origen del Diseño

Adaptado de la Skill [superpowers / using-git-worktrees](https://github.com/anthropic-experimental/superpowers) — la cadena de resolución de prioridad y la interfaz de cuatro modos siguen ese patrón. La política de runtime autocontenido de este proyecto significa que la skill de superpowers se referencia solo por su intención de diseño; **no** se despacha en runtime.

## Integración

- **upstream**: [`ywc-parallel-executor`](../ywc-parallel-executor/) (Pre-flight audit, Step 4 create por task, Step 4g prune), [`ywc-finish-branch`](../ywc-finish-branch/) (limpieza en Step 5 / 8)
- **downstream**: ninguna (leaf-operation skill)

## Sincronización de 3-Root

Esta Skill entrega contenido idéntico a los tres skill roots (claude-code, codex-skill, pi-skills) porque la gestión de worktree es una característica universal. **No** está en `is_diverged()`.
