<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-parallel-executor

Este documento presenta el workflow Codex `ywc-parallel-executor`. Las condiciones de activacion autoritativas, anti-triggers, pasos de ejecucion y formato de salida estan definidos en [SKILL.md](./SKILL.md).

## Versiones localizadas

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.md)
- [한국어 full](./README.ko.md)
- [中文](./README.zh.md)

## Cuando usarlo

- El usuario usa una frase trigger del skill o una solicitud equivalente en lenguaje natural.
- Codex necesita el workflow y los criterios de validacion especificos del skill antes de actuar.
- Otro skill `ywc-*` referencia este skill como paso upstream o downstream.

## Uso

```bash
$ywc-parallel-executor
```

Sigue las secciones Arguments o Workflow de [SKILL.md](./SKILL.md) para las opciones y modos compatibles.

## Aislamiento Docker

Para worktrees de tareas que usan Docker Compose, el executor delega el aislamiento de puertos en `ywc-docker-isolate`: audita los stacks de las tareas seleccionadas antes de crear worktrees, configura puertos deterministas por tarea despues de verificar cada worktree y desmonta los stacks de tareas exitosas antes de podar worktrees. Los worktrees `BLOCKED` o preservados conservan su estado Docker para recuperacion.

## Contract Gates

La planificacion de waves trata los contratos publicos compartidos como Shared Surfaces, no solo como rutas de archivo. Los payloads de workers requieren Changed Public Contracts, Critical Internals, Cross-Module Impact y evidencia de tests; las tareas que cambian comportamiento sin tests authored/executed necesitan una TDD exception explicita o quedan blocked/with concerns.

## Modos de entrega

| Mode | Comportamiento |
|---|---|
| `--local-merge` | Hace merge local de cada tarea en la rama base y hace push inmediato. No crea PR. |
| `--draft` | Acumula los cambios de tareas mediante merges locales y crea un PR draft agregado al final. |
| `--per-task-pr` | Para cada tarea, crea un PR, espera CI, gestiona revisiones de bots, refresca contra la base mas reciente, mergea el PR, sincroniza la base y marca la tarea como completa. |

En `--per-task-pr`, una tarea anterior de la misma wave puede avanzar la rama base. Antes de mergear, el executor comprueba si la rama del PR contiene la base mas reciente; si no, mergea la base en la rama del worktree, hace push y vuelve a verificar CI. Un conflicto al refrescar base se reporta como `BLOCKED`, y el PR no se mergea usando resultados de CI de un head SHA antiguo.

## Salida

Este skill sigue el formato de reportes, artefactos y estados definido en [SKILL.md](./SKILL.md). Si el skill emite Completion Status, conserva los significados de `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED` y `NEEDS_CONTEXT`.
