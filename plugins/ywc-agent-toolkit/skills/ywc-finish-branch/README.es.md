<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-finish-branch

Una Habilidad de Codex que entrega una Rama de Características a su Rama Base en una única llamada. Cubre Mark-PR-ready, CI Wait + Bot Review Polling, Merge (PR u Local), Post-Merge Verification, Mark Task Complete, y Local Branch Cleanup.

## Descripción General

Una extracción de responsabilidad única de la lógica de entrega que `ywc-sequential-executor` y `ywc-parallel-executor` previamente incluían por separado. Dada una Rama de Características para una Tarea con verificación aprobada, esta Habilidad la lleva el resto del camino hasta "done".

### Características principales

- **Distribución de modo en un lugar**: `normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **Puerta de seguridad post-merge fuerte**: confirma que la fusión se ejecutó realmente vía `git log -1 --format="%s"`
- **Definición de Done aplicada**: mueve el directorio de la tarea a `<tasks-dir>/completed/` con una puerta de verificación
- **Sondeo de revisión de bot compatible**: `--bot-action sequential|parallel` coincide con la estrategia CI del llamador
- **Modo ruta-de-worktree**: `--worktree-path <path>` alcanza comandos de entrega con `git -C <path>` para worktrees a nivel de ejecución secuencial, mientras que la creación/eliminación permanece con el llamador
- **Paso de lenguaje de PR**: `--pr-lang en|ja|ko|zh|es` construye títulos `[<TASK_NUMBER>] <translated-slug>` y pasa el mismo valor a `ywc-create-pr` como `--lang <pr-lang>`, manteniendo identificadores de máquina sin cambios

## Uso

### Predeterminado (basado en PR)

```
$ywc-finish-branch --mode normal-pr --branch feature/yk-000001-010-db-create-users \
  --task-name yk-000001-010-db-create-users --base-branch develop
```

Los nombres de tarea sin prefijo existentes (`000001-010-...`) y heredados numéricos (`001010-...`) permanecen válidos y se mueven usando sus nombres completos originales.

### Fusión Local

```
$ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### Modo de rango con push diferido

```
$ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### Lenguaje de PR

```
$ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop --pr-lang zh
```

Valores soportados: `en`, `ja`, `ko`, `zh`, `es`.

### Modo ruta-de-worktree

```
$ywc-finish-branch --mode local-merge --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --worktree-path ../worktree-run
```

### Activadores de lenguaje natural

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## Comparación de modos

| Modo | PR | CI wait | Fusión | Marcar Completo | Limpieza |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | sí (delega a `ywc-create-pr`) | sí | `gh pr merge --delete-branch` | sí | `git branch -d` |
| `local-merge` | no | no | `git merge --no-ff` + push | sí | sí |
| `draft` | sí | no | no | no | no |
| `skip-ci-wait` | sí (marcar listo) | no | no | no | no |
| `per-task-pr` | sí | no | no | no | no |

## Requisitos previos

- CLI `gh` instalado y autenticado (modos basados en PR)
- Árbol de trabajo limpio
- El llamador ya ha pasado su puerta de verificación (lint / typecheck / test)
- Pre-autorización configurada en `Codex approval settings` o en el archivo de política local del proyecto (ver `references/local-merge-permissions.md`)

## Herramientas utilizadas

`Bash`, `Read`, `Grep`, Task (delega a `ywc-create-pr` / `ywc-handle-pr-reviews`)

## Integración

- **Upstream**: `ywc-sequential-executor` (reemplaza sus Pasos 5–8), `ywc-parallel-executor` (reemplaza la porción fusión + marcar-completo de los Pasos 4e–4f)
- **Delegación interna**: `ywc-create-pr` (Paso 2), `ywc-handle-pr-reviews` (Paso 4 bucle de sondeo de bot)

## Seguridad operacional

Las pasadas separadas de eliminación remota pasan estas puertas en orden: una lista permitida de rama más `git check-ref-format "refs/heads/$branch"`, una única URL de push `origin` fijada, un repositorio calificado por host vinculado a través de `env -u GH_HOST gh` (y su padre para un fork), la punta remota exacta, un check de fusión de PR incondicional en la rama base prevista y la punta actual, un conteo de PR abiertos de cero como la última verificación, y un delete de concesión de punta exacta. Permanece una pequeña ventana de carrera entre la verificación de PR abierto y el delete.
