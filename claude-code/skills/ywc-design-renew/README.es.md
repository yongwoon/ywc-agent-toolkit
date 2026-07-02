<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-design-renew

Una Skill de Claude Code que renueva superficies frontend genéricas o de aspecto
"AI-made" (AI-slop) convirtiéndolas en diseños distintivos, y audita una UI en
busca de señales de diseño AI-slop. Delega en la skill `impeccable` como su motor
de diseño cuando está instalada, y recurre a un conjunto de reglas autónomo en
caso contrario — de modo que funciona en cualquier proyecto o runtime.

## Descripción General

Las UI generadas por LLM convergen en clichés visuales predecibles — paletas
cyan-on-dark, texto con gradiente, franjas de acento border-left, Inter, cuadrículas
de card uniformes — porque todos los model fueron entrenados con las mismas
plantillas. Esta skill detecta (check) y elimina (renew) esas señales de AI-slop.

- **renew mode (predeterminado)**: toma una superficie existente, la mejora hacia
  una dirección estética audaz y deja evidencia before/after.
- **check mode**: audita en busca de AI-slop sin editar, aplicando un gate pass/fail.

El criterio de anclaje es el **AI Slop Test** — "Si mostraras esto y dijeras
'AI made this', ¿te creerían de inmediato?"

## Requisitos Previos

- (Opcional) skill `impeccable` — se le delega como motor de diseño más potente
  cuando está presente; en caso contrario, se recurre al conjunto de reglas
  autónomo. **Instalar (cualquiera de las dos)**: en Claude Code ejecutar
  `/plugin marketplace add pbakaus/impeccable`, o `npx impeccable skills install`.
  Tras instalar, ejecutar `/impeccable init` una vez para establecer el Design
  Context del proyecto — escribe los archivos `PRODUCT.md` / `DESIGN.md` a
  continuación para que se omitan las preguntas de context.
- (Opcional) Una URL en vivo (dev server local) — utilizada por Chrome DevTools
  MCP para capturas de pantalla before/after.
- (Opcional) `.impeccable.md` / `PRODUCT.md` / `DESIGN.md` — omite las preguntas
  de recopilación de context cuando el Design Context ya existe.

## Casos de Uso

- "This dashboard looks too generic, like an AI made it. Renew it."
- "Before release, check this screen for AI-slop design tells."
- "Redesign the hero section to feel distinctive."

## Uso

```bash
/ywc-design-renew --target src/components/hero --url http://localhost:3000
/ywc-design-renew --mode check --target src/app/dashboard --fail-on critical
```

O invocar en lenguaje natural:

> "This screen looks AI-generated. Please renew the design."

## Entrada

- **Obligatorio**: `--target` (component / page / route) más el Design Context
  (audience / use-cases / brand tone)
- **Opcional**: `--url` (capturas en vivo), `--mode check`, `--fail-on`,
  `--format html`

## Salida

- **renew**: código renovado más un informe de renovación (dirección elegida,
  findings de slop resueltos before→after, archivos modificados, resultado de la
  reauditoría, capturas de pantalla before/after)
- **check**: un informe de auditoría de slop priorizado (Critical / High / Medium / Low)
  con el veredicto del gate `--fail-on`

## Skills Relacionadas

- `impeccable` — motor de diseño delegado cuando está instalado (craft / polish / audit)
- `ywc-ui-ux-review` — verifica el eje usability / IA / WCAG tras la renovación
  (esta skill posee únicamente el eje aesthetic / slop)
- `ywc-review-learnings` — acumula las preferencias de diseño confirmadas por proyecto
