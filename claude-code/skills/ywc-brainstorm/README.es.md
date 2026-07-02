<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-brainstorm

Una skill de diálogo socrático que convierte una idea aproximada en un diseño aprobado antes de que comience cualquier trabajo de implementación.

## Qué Hace

Impone el Hard Gate:

> **NINGUNA SKILL DE IMPLEMENTACIÓN, REDACCIÓN DE SPEC O ESCRITURA DE CÓDIGO HASTA QUE SE PRESENTE UN DISEÑO Y EL USUARIO LO HAYA APROBADO.**

Un flujo de trabajo de diálogo de 6 pasos:

1. **Step 1 — Explorar el context del proyecto** — Leer el `CLAUDE.md` del área afectada, `docs/` y los commits recientes para prevenir suposiciones obsoletas.
2. **Step 2 — Detectar "demasiado grande para un solo diseño"** — Si la solicitud abarca múltiples subsistemas independientes, DETENERSE y descomponer primero.
3. **Step 3 — Hacer preguntas aclaratorias una a la vez** — Sacar a la luz los cuatro anclajes (What / Why / Out of Scope / Done When), una pregunta por mensaje.
4. **Step 4 — Proponer 2–3 enfoques con sus compensaciones** — Encabezar con la recomendación; mostrar las alternativas explícitamente.
5. **Step 5 — Presentar el diseño y obtener la aprobación** — Presentar por secciones; confirmar cada una antes del gate de aprobación final.
6. **Step 6 — Traspaso a `ywc-plan`** — Pasar los anclajes y el enfoque elegido como entrada explícita.

La skill nunca se ramifica directamente hacia `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator` ni ningún executor — su estado terminal es siempre invocar `ywc-plan`.

## Cuándo Se Activa

- El usuario dice "idea", "brainstorm", "let's build", "アイディア", "구상" y similares.
- La intención no está clara o la implementación podría tomar varios caminos.
- La solicitud parece abarcar múltiples subsistemas.
- `ywc-plan` Step 1 delega aquí el diálogo de aclaración.

## Cuándo NO Usarla

- La solicitud ya especifica rutas de archivo y criterios de aceptación → usar `ywc-plan` directamente
- Validar un spec existente → `ywc-spec-validate`
- Elegir entre librerías o frameworks → `ywc-tech-research` primero
- Preguntas en tiempo de implementación → `ywc-code-gen`

## Referencias

El flujo de trabajo completo y la Rationalization Defense están en [SKILL.md](./SKILL.md). La disciplina subyacente está adaptada de `superpowers:brainstorming`, ajustada para traspasar a `ywc-plan`.

## Versiones Localizadas

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
