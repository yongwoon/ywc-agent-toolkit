<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-finish-branch

Una Habilidad de Codex que entrega una rama de características a su rama base en una sola llamada. Cubre Mark-PR-ready, CI Wait + Bot Review Polling, Merge (PR o Local), Post-Merge Verification, Mark Task Complete y Local Branch Cleanup.

## Descripción general

Una extracción de responsabilidad única de la lógica de entrega que `ywc-sequential-executor` y `ywc-parallel-executor` previamente alineaban por separado. Dada una rama de características para una tarea con verificación aprobada, esta Habilidad la lleva el resto del camino a "done".

### Características clave

- **Envío de modo en un solo lugar**: `normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **Puerta difícil posterior a la fusión**: confirma que la fusión realmente se ejecutó a través de `git log -1 --format="%s"`
- **Definición de Done aplicada**: mueve el directorio de tareas a `<tasks-dir>/completed/` con una puerta de verificación
- **Compatible con sondeo de revisión de bot**: `--bot-action sequential|parallel` coincide con la estrategia de CI de la persona que llama
- **Modo worktree-path**: `--worktree-path <path>` define el alcance de los comandos de entrega con `git -C <path>` para worktrees de nivel de ejecución secuencial, mientras que la creación/eliminación permanece con la persona que llama
- **Paso de idioma de PR**: `--pr-lang en|ja|ko|zh|es` construye títulos `[<TASK_NUMBER>] <translated-slug>` y pasa el mismo valor a `ywc-create-pr` como `--lang <pr-lang>`, manteniendo identificadores de máquina sin cambios

## Uso

### Predeterminado (basado en PR)

```
$ywc-finish-branch --mode normal-pr --branch feature/yk-000001-010-db-create-users \
  --task-name yk-000001-010-db-create-users --base-branch develop
```

Los nombres de tarea sin prefijo existentes (`000001-010-...`) y numéricos heredados (`001010-...`) permanecen válidos y se mueven utilizando sus nombres completos originales.

### Fusión local

```
$ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### Modo de rango con empuje diferido

```
$ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### Idioma de PR

```
$ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop --pr-lang zh
```

Valores admitidos: `en`, `ja`, `ko`, `zh`, `es`.

### Modo worktree-path

```
$ywc-finish-branch --mode local-merge --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --worktree-path ../worktree-run
```

### Activadores de lenguaje natural

```
"terminar rama"
"entregar esta rama"
"branch 마무리"
"ブランチ完了"
```

## Comparación de modos

| Modo | PR | Espera de CI | Fusión | Marcar completado | Limpieza |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | sí (delega a `ywc-create-pr`) | sí | `gh pr merge --delete-branch` | sí | `git branch -d` |
| `local-merge` | no | no | `git merge --no-ff` + push | sí | sí |
| `draft` | sí | no | no | no | no |
| `skip-ci-wait` | sí (marcar como listo) | no | no | no | no |
| `per-task-pr` | sí | no | no | no | no |

## Requisitos previos

- `gh` CLI instalado y autenticado (modos basados en PR)
- Árbol de trabajo limpio
- La persona que llama ya ha pasado su puerta de verificación (lint / typecheck / test)
- Preautorización configurada en `Codex approval settings o el archivo de política local del proyecto` (ver `references/local-merge-permissions.md`)

## Herramientas utilizadas

`Bash`, `Read`, `Grep`, Task (delega a `ywc-create-pr` / `ywc-handle-pr-reviews`)

## Integración

- **Upstream**: `ywc-sequential-executor` (reemplaza sus pasos 5–8), `ywc-parallel-executor` (reemplaza la parte de fusión + marcar completado del paso 4e–4f)
- **Delegación interna**: `ywc-create-pr` (Paso 2), `ywc-handle-pr-reviews` (Paso 4, bucle de sondeo de bot)

## Seguridad operativa

La eliminación remota separada pasa estas protecciones en orden: una lista permitida de ramas más `git check-ref-format "refs/heads/$branch"`, una URL de inserción `origin` única anclada, un repositorio calificado por host vinculado a través de `env -u GH_HOST gh` (y su elemento padre para una bifurcación), la punta remota exacta, una verificación de PR fusionado incondicional en la base prevista y la punta actual, un recuento de PR abierto de cero como la última verificación y una eliminación de concesión de punta exacta. Permanece una pequeña ventana de carrera entre la verificación de PR abierto y la eliminación.
