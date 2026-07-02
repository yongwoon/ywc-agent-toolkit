<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-spec-ready (Spec Readiness Loop)

Una Skill que converge automáticamente un spec producido por `ywc-plan` al estado `DONE` de `ywc-spec-validate`. Cada iteración ejecuta `ywc-spec-validate`; en `DONE_WITH_CONCERNS` añade una enmienda mediante `ywc-plan --update-spec` y vuelve a validar. Al alcanzar `DONE` imprime el traspaso a `ywc-task-generator` y **se detiene** (nunca ejecuta task-generator de forma automática).

```text
spec ──> [ywc-spec-validate ──DONE_WITH_CONCERNS──> ywc-plan --update-spec]* ──DONE──> handoff
```

El loop existente `ywc-agentic` gira en torno a `ywc-impl-review` (code evaluation) y ejecuta `ywc-spec-validate` solo **una vez**. Esta Skill cubre el loop interno que falta —— **la convergencia de spec en múltiples iteraciones**.

## Usage

```text
/ywc-spec-ready --spec docs/ywc-plans/feature.md                       # Default (max 5 iterations)
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-iterations 8    # Set iteration ceiling
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-advisor-calls 2 # Advisor cost guard
/ywc-spec-ready --spec docs/ywc-plans/feature.md --dry-run             # Print command sequence only
```

## Options

| Option                   | Description                                                       |
| ------------------------ | ---------------------------------------------------------------- |
| `--spec <path>`          | Archivo de spec a converger (requerido, un output de `ywc-plan`). Ausente → `NEEDS_CONTEXT` |
| `--max-iterations <n>`   | Límite del validation loop (por defecto: 5, nunca elevado de forma autónoma)  |
| `--max-advisor-calls <n>`| Presupuesto total de Opus advisor en todas las iteraciones (por defecto: 4, cost guard) |
| `--log <path>`           | Loop log append-only (por defecto: `<spec-dir>/<slug>.spec-ready-log.md`) |
| `--dry-run`              | Imprime solo la secuencia de comandos planeada; no invoca ninguna sibling skill |
| `--lang <lang>`          | Idioma del report/handoff (por defecto: auto, inferido de CLAUDE.md) |
| `--focus <area>`         | Reenviado a `ywc-spec-validate`                                  |
| `--format <fmt>`         | Reenviado a `ywc-spec-validate` (markdown / html)               |
| `--terse`                | Salida mínima (solo phase headers y el report final)         |

## Execution Flow

1. Pre-flight —— verifica que `--spec` exista, deriva `<slug>`, gestiona `--dry-run`
2. Iteration Loop —— `ywc-spec-validate` → Status Routing → (en DONE_WITH_CONCERNS) guard check → `ywc-plan --update-spec` → log → repetir
3. Hard Stop —— se detiene de inmediato en `BLOCKED` / `NEEDS_CONTEXT` / `SOCRATIC` / no parseable
4. Handoff —— en `DONE`, imprime la guía de `ywc-task-generator` y se detiene
5. Completion Report —— un único report (la última línea es el Completion Status)

## Loop-prevention Guards

| Guard | Stop condition |
| --- | --- |
| Iteration cap | `iteration >= --max-iterations` y status ≠ DONE |
| Non-decreasing Criticals | El Critical count aumenta o se mantiene igual durante 2 iteraciones consecutivas (signature overlap) |
| Repeated signature | La misma Critical signature reaparece en iteraciones consecutivas tras un re-plan |
| Identical amendment scope | El nuevo amendment scope es igual al anterior (recursion guard) |

Consulta [references/convergence.md](references/convergence.md) para las reglas completas y [references/loop-log.md](references/loop-log.md) para el schema del log.

## Triggering

Las condiciones de trigger de esta Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
