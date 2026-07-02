<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-design-renew

Un Skill de Codex que renueva superficies Frontend genéricas o con aspecto “hecho por AI” hacia diseños más distintivos, y audita una UI para detectar señales de AI-slop. Delega en `impeccable` como design engine cuando está instalado; si no, usa un conjunto de reglas autónomo, por lo que funciona en cualquier proyecto o runtime.

## Resumen

Las UI generadas por LLM tienden a converger en clichés visuales predecibles: paletas cyan sobre fondo oscuro, gradient text, franjas de accent border a la izquierda, Inter y grids uniformes de cards. Este Skill detecta y elimina esas señales.

- **renew mode (por defecto)**: toma una superficie existente, la mejora hacia una dirección estética marcada y deja evidencia before/after.
- **check mode**: audita AI-slop sin editar, aplicando un pass/fail gate.

El criterio central es el **AI Slop Test**: “Si mostraras esto y dijeras que lo hizo AI, ¿te creerían inmediatamente?”

## Prerrequisitos

- (Opcional) Skill `impeccable`: se usa como design engine más fuerte cuando está disponible. Si el proyecto lo permite, `npx impeccable skills install` puede instalarlo. Después de instalarlo, ejecuta `impeccable init` una vez para definir el Design Context del proyecto; esto escribe `PRODUCT.md` / `DESIGN.md` y evita repetir las preguntas de contexto.
- (Opcional) Una live URL (local dev server), usada por Chrome DevTools MCP para screenshots before/after.
- (Opcional) `.impeccable.md` / `PRODUCT.md` / `DESIGN.md`, para saltar la recopilación de contexto cuando el Design Context ya existe.

## Casos de uso

- “Este dashboard se ve demasiado genérico, como hecho por AI. Renuévalo.”
- “Antes del release, revisa esta pantalla para detectar señales de AI-slop.”
- “Rediseña la hero section para que se sienta distintiva.”

## Uso

```text
Use $ywc-design-renew to renew src/components/hero with --url http://localhost:3000.
Use $ywc-design-renew --mode check --target src/app/dashboard --fail-on critical.
```

O en lenguaje natural:

> “This screen looks AI-generated. Please renew the design.”

## Entrada

- **Requerido**: `--target` (component / page / route) más Design Context (audience / use-cases / brand tone)
- **Opcional**: `--url` (live screenshots), `--mode check`, `--fail-on`, `--format html`

## Salida

- **renew**: código renovado y un renewal report (dirección elegida, findings de slop resueltos before→after, changed files, resultado de re-audit y screenshots before/after)
- **check**: slop audit report priorizado (Critical / High / Medium / Low) con el veredicto del `--fail-on` gate

## Skills relacionados

- `impeccable` — design engine delegado cuando está instalado (craft / polish / audit)
- `ywc-ui-ux-review` — verifica el eje de usability / IA / WCAG después de la renovación; este Skill solo cubre el eje aesthetic / slop
- `ywc-review-learnings` — acumula design preferences confirmadas por proyecto
