<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-brainstorm

Una habilidad de diálogo socrático que convierte una idea áspera en un diseño aprobado antes de que comience cualquier trabajo de implementación.

## Qué hace

Hace cumplir la Puerta Dura:

> **SIN HABILIDAD DE IMPLEMENTACIÓN, REDACCIÓN DE ESPECIFICACIONES O ESCRITURA DE CÓDIGO HASTA QUE SE PRESENTE UN DISEÑO Y EL USUARIO LO HAYA APROBADO.**

Un flujo de diálogo de 6 pasos:

1. **Paso 1 — Explorar el contexto del proyecto** — Leer `CLAUDE.md` del área afectada, `docs/`, y commits recientes para evitar suposiciones obsoletas.
2. **Paso 2 — Detectar "demasiado grande para un diseño"** — Si la solicitud abarca múltiples subsistemas independientes, DETENER y descomponer primero.
3. **Paso 3 — Hacer preguntas de aclaración una a la vez** — Exponer los cuatro anclajes (Qué / Por Qué / Fuera de Alcance / Hecho Cuando), una pregunta por mensaje.
4. **Paso 4 — Proponer 2–3 enfoques con compensaciones** — Comenzar con la recomendación; mostrar las alternativas explícitamente, y exponer suposiciones que vale la pena validar antes de recomendar.
5. **Paso 5 — Presentar el diseño y obtener aprobación** — Presentar en secciones; cuando el diseño se basa en hechos del repositorio, mostrar una tabla de Premisas cargadas con evidencia citada `file:line` y no pedir handoff mientras alguna fila sea `UNVERIFIED`.
6. **Paso 6 — Handoff a `ywc-plan`** — Pasar los anclajes y el enfoque elegido como entrada explícita.

La habilidad nunca se ramifica directamente hacia `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator`, o cualquier ejecutor — su estado terminal es siempre invocar `ywc-plan`.

## Cuándo se activa

- El usuario dice "idea", "brainstorm", "let's build", "アイディア", "구상", y similares.
- La intención es poco clara o la implementación podría ir de varias formas.
- La solicitud parece abarcar múltiples subsistemas.
- El Paso 1 de `ywc-plan` delega el diálogo de aclaración aquí.

## Cuándo NO usar

- La solicitud ya especifica rutas de archivo y criterios de aceptación → usar `ywc-plan` directamente
- Validar una especificación existente → `ywc-spec-validate`
- Elegir entre bibliotecas o marcos → `ywc-tech-research` primero
- Preguntas en tiempo de implementación → `ywc-code-gen`

## Referencias

El flujo de trabajo completo y la Defensa de Racionalización están en [SKILL.md](./SKILL.md). La disciplina subyacente está adaptada de `superpowers:brainstorming`, restringida para transferencia a `ywc-plan`. La exposición de puntos ciegos utiliza [../references/unknown-matrix.md](../references/unknown-matrix.md) internamente.

## Versiones localizadas

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
