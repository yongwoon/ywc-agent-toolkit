<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-finish-branch

Un Skill de Codex que entrega una Rama de Feature a su Rama Base en una sola llamada. Cubre Mark-PR-ready, CI Wait + Bot Review Polling, Merge (PR o Local), Post-Merge Verification, Mark Task Complete y Local Branch Cleanup.

## Descripción general

Una extracción de responsabilidad única de la lógica de entrega que `ywc-sequential-executor` y `ywc-parallel-executor` anteriormente incluían por separado. Dado una Rama de Feature para una Tarea con verificación exitosa, este Skill la lleva hasta el estado "completado".

### Características principales

- **Despacho de modo en un lugar**: `normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **Puerta dura post-merge**: confirma que el merge realmente se ejecutó vía `git log -1 --format="%s"`
- **Definición de Hecho aplicada**: mueve el directorio de tarea a `<tasks-dir>/completed/` con una puerta de verificación
- **Compatible con polling de revisión de bot**: `--bot-action sequential|parallel` coincide con la estrategia CI del llamador
- **Agnóstico de worktree**: deja el ciclo de vida del worktree al ejecutor paralelo para un límite limpio de responsabilidades

## Uso

### Por defecto (basado en PR)

```
/ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop
```

### Merge Local

```
/ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### Modo Range con push diferido

```
/ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### Disparadores en lenguaje natural

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## Comparación de modos

| Modo | PR | Espera CI | Merge | Marcar Completo | Limpieza |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | sí (delega a `ywc-create-pr`) | sí | `gh pr merge --delete-branch` | sí | `git branch -d` |
| `local-merge` | no | no | `git merge --no-ff` + push | sí | sí |
| `draft` | sí | no | no | no | no |
| `skip-ci-wait` | sí (marcar como listo) | no | no | no | no |
| `per-task-pr` | sí | no | no | no | no |

## Requisitos previos

- CLI `gh` instalada y autenticada (modos basados en PR)
- Árbol de trabajo limpio
- El llamador ya pasó su puerta de verificación (lint / typecheck / test)
- Pre-autorización configurada en `Codex approval settings or the project-local policy file` (ver `references/local-merge-permissions.md`)

## Herramientas utilizadas

`Bash`, `Read`, `Grep`, Task (delega a `ywc-create-pr` / `ywc-handle-pr-reviews`)

## Integración

- **Upstream**: `ywc-sequential-executor` (reemplaza sus Pasos 5–8), `ywc-parallel-executor` (reemplaza la porción de merge + mark-complete de los Pasos 4e–4f)
- **Delegación interna**: `ywc-create-pr` (Paso 2), `ywc-handle-pr-reviews` (bucle de polling del Paso 4)
