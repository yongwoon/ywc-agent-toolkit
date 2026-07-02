<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-confidence-gate

Una skill de disciplina previa a la implementación que fuerza una puntuación de confianza explícita de 5 dimensiones y presenta una decisión PROCEED / REVIEW / STOP antes de invocar cualquier herramienta de implementación.

## Qué hace

Aplica la Iron Law:

> **SIN IMPLEMENTACIÓN SIN UNA PUNTUACIÓN DE CONFIANZA EXPLÍCITA Y UNA DECISIÓN DE BAND**

Puntúa 5 dimensiones (cada una de 0 a 100), toma la suma ponderada y la mapea a un band.

| Dimension | Weight | One-sentence test |
|---|---|---|
| Scope clarity | 25% | ¿Puedes enunciar lo in-scope y lo out-of-scope, cada uno en una frase y sin términos vagos? |
| Architecture compliance | 25% | ¿El cambio planeado sigue la estructura / el naming / las abstractions existentes? |
| Evidence quality | 20% | ¿Las afirmaciones se respaldan con fuentes primarias (code, official docs, test output)? |
| Reuse verified | 15% | ¿Has buscado utilities existentes y descartado cada una con una razón? |
| Root cause identified | 15% | Bug: ¿nombras la causa, no el síntoma? Greenfield: ¿la necesidad subyacente, no la solicitud superficial? |

| Band | Aggregate | Action |
|---|---|---|
| **PROCEED** | ≥ 90 | Iniciar la implementación; llevar la puntuación al executor report |
| **REVIEW** | 70–89 | Presentar 1–3 alternativas o preguntas abiertas; plantear primero la dimensión más débil |
| **STOP** | < 70 | No iniciar; exponer las dimensiones débiles y enrutar de vuelta a la skill anterior |

**Anulación por dimensión única `< 50`**: la suma ponderada fija un band tentativo, y luego cualquier dimensión que puntúe por debajo de 50 lo baja un nivel (PROCEED → REVIEW, REVIEW → STOP) — siempre un nivel, nunca un salto directo a STOP, y una dimensión exactamente en 50 no lo dispara. Evita que una dimensión fuerte enmascare una debilidad fatal.

## Cuándo se activa

- El usuario dice "ready to implement", "should I proceed", "confidence check", "確信度チェック", "구현 시작해도 돼".
- Entrada de frontera de `ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-agentic`.
- Tras la evaluación de Scale de `ywc-plan`, justo antes del traspaso posterior.
- Antes de cualquier commit con impacto architectural material.

## Cuándo NO usarla

- Verificación posterior a la implementación → `ywc-verify-done` (el gate simétrico que usa el mismo rubric)
- Revisión de la calidad del spec → `ywc-spec-validate`
- Puntuación de revisión de implementación → `ywc-impl-review` (también usa este rubric — puntuaciones comparables)
- Aclaración de intención → `ywc-brainstorm`

## Referencias

El flujo de trabajo completo y los anti-patterns están en [SKILL.md](./SKILL.md). La definición canónica del rubric es la referencia compartida [../references/confidence-gate.md](../references/confidence-gate.md). La skill se inspira en el patrón de confidence-check de ECC y en el rubric del PM Agent de SuperClaude.

## Versiones localizadas

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
