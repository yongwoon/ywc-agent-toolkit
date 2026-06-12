<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# UI/UX Review - Auditor Híbrido de Código y UI en Vivo

Un Codex Skill que audita un proyecto desde una perspectiva UI/UX combinando análisis estático de código con exploración de UI en vivo mediante available browser tooling, y produce un informe Markdown priorizado.

## Descripción general

Este Skill responde "¿dónde debemos mejorar primero la UX?" con hallazgos respaldados por evidencia. Cada problema cita una heurística autorizada (Nielsen 10 / WCAG 2.2 AA / Material 3 / Apple HIG / sistema de diseño interno).

### Características principales

- Revisión híbrida: análisis estático de código + exploración de UI en vivo
- Áreas de enfoque: Arquitectura de Información, Diseño Visual
- Salida de severidad en cuatro niveles: Critical / High / Medium / Low
- Cada hallazgo incluye una ubicación y una cita de heurística
- Eficiente en tokens mediante snapshots del árbol de accesibilidad de available browser tooling

## Uso

```text
Review the UI/UX of http://localhost:3000 — focus on the dashboard.
```

```text
Audit usability and Information Architecture of the settings flow.
```

Los disparadores en lenguaje natural están definidos en [SKILL.md](./SKILL.md).

## Referencias

- Las listas de verificación de dominio y las citas de heurísticas se encuentran en [`references/`](./references)
- El andamiaje del informe se encuentra en [`assets/`](./assets)
- El flujo de trabajo y las frases de activación están definidos en [SKILL.md](./SKILL.md)

## Herramientas de UI en vivo

Este Skill prefiere available browser tooling para tareas enfocadas en inspección (snapshot del árbol de accesibilidad, auditoría de Lighthouse, estilo calculado, capturas de pantalla). Playwright MCP se usa solo para automatización de interacciones de múltiples pasos cuando es necesario.

## Versiones localizadas

- [Coreano (Principal)](./README.md)
- [Japonés](./README.ja.md)
- [Coreano (Resumen)](./README.ko.md)
