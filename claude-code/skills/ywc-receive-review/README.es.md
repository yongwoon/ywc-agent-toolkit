<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-receive-review

Una skill de disciplina en la capa de actitud que **bloquea el acuerdo performativo y fuerza la verificación técnica** al recibir feedback de code-review.

## Qué hace

Impone la Iron Law:

> **VERIFY BEFORE IMPLEMENTING. NO PERFORMATIVE AGREEMENT, EVER.**

Un Response Pattern de 6 pasos se aplica a cada comentario del reviewer:

1. **READ** — Lee el feedback completo sin reaccionar (sin acuerdo, sin desacuerdo, todavía sin llamadas a herramientas).
2. **UNDERSTAND** — Reformula el requisito técnico con tus propias palabras; pregunta si algún ítem no está claro antes de avanzar.
3. **VERIFY** — Abre el archivo, ejecuta el test, haz grep del símbolo: contrasta la afirmación del reviewer con el codebase actual.
4. **EVALUATE** — Decide si la sugerencia se sostiene para este codebase en su estado actual (compatibilidad, decisiones previas, YAGNI, restricciones de la plataforma).
5. **RESPOND** — Reconoce con una frase de arreglo, o rebate con razonamiento técnico. **Prohibido**: "You're absolutely right!", "Great point!", "Thanks!"
6. **IMPLEMENT** — Un ítem a la vez, testea cada uno, presenta un bloque de verificación según `ywc-verify-done`.

**Vocabulario prohibido** (lista completa en references/forbidden-acknowledgments.md):

| Forbidden | Replace with |
|---|---|
| "You're absolutely right!" | Enuncia el arreglo: "Fixed — `<file:line>` now <behavior>" |
| "Great point!" / "Excellent feedback!" | Enuncia la acción o plantea la pregunta |
| "Thanks for catching that!" / "Thanks for the review!" | Elimínalo por completo; el arreglo es el agradecimiento |
| "Let me implement that right now" (antes del Step 3) | "Verifying before implementing: <check>" |

## Cuándo se activa

- El usuario dice "리뷰 받았어", "review feedback", "コメント返信".
- `ywc-handle-pr-reviews` delega la capa de actitud durante la iteración de inline-comments.
- `ywc-finish-branch` presenta un bot review post-CI que requiere respuesta.
- Estás a punto de responder a CodeRabbit / Codex Review / Claude Review.

## Cuándo NO usarla

- Realizar una review tú mismo → `ywc-impl-review`
- Crear un PR → `ywc-create-pr`
- Automatización de obtención / threading / respuesta a comentarios de PR → `ywc-handle-pr-reviews` (esta skill es su capa de actitud)
- Verificación de reclamo de finalización → `ywc-verify-done`

## References

El Response Pattern completo, la lista de acknowledgments prohibidos, las condiciones de pushback y el manejo específico por fuente (human partner / external reviewer / bot) están en [SKILL.md](./SKILL.md). Adaptado de `superpowers:receiving-code-review`, ajustado para la separación de responsabilidades respecto a `ywc-handle-pr-reviews` (actitud vs. automatización).

## Versiones localizadas

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
