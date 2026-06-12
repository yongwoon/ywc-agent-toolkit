<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-skill-author

Una **meta-habilidad** para crear nuevas habilidades ywc-* y reestructurar las existentes. Codifica las reglas canónicas derivadas del análisis de las 18 habilidades ywc-* en producción (formato de Frontmatter, Defensa de Racionalización, disparadores multilingües, divulgación progresiva, etc.) para que los LLMs sigan automáticamente el estándar.

## Casos de Uso

- Crear una nueva habilidad ywc-* desde cero.
- Reestructurar el frontmatter, las secciones del cuerpo o las referencias de una habilidad ywc-* existente.
- Auditar las 18 habilidades ywc-* contra el conjunto de reglas canónicas.

## Invocación

```bash
/ywc-skill-author
```

O mediante lenguaje natural:

> "Create a new ywc skill"
> "Audit my ywc skill against the rules"
> "Upgrade ywc skill structure"

## Entrada

- Nueva habilidad: propósito de la habilidad y escenarios de disparo primarios.
- Auditoría: ruta al directorio de la habilidad objetivo.

## Salida

- Un archivo SKILL.md que sigue la estructura estándar (Frontmatter + Defensa de Racionalización + Flujo de Trabajo + Lista de Verificación de Validación).
- Archivos `references/` complementarios donde corresponda.
- El conjunto completo de archivos README por idioma (`README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`).

## Reglas Principales

El estándar aplicado por esta habilidad consiste en:

- **Reglas Obligatorias**: Frontmatter / Cuerpo / Sistema de Archivos (A1–A13).
- **Reglas Recomendadas**: Directrices situacionales (B1–B7).
- **Convenciones de Formato**: Prosa en coreano con términos técnicos en inglés, disparadores multilingües, etc.
- **Anti-patrones**: Descripciones tipo resumen de flujo de trabajo, código de esbozo, referencias cruzadas con `@`, y trampas similares.

Consulte `SKILL.md` y los cuatro documentos de referencia en `references/` para la especificación completa.

## Habilidades Relacionadas

- `ywc-task-generator` — aplica la misma política multilingüe y el patrón de extracción de referencias.
- Todas las habilidades ywc-* — deben cumplir con las reglas definidas aquí.

## Documentos de Referencia

- `references/skill-template.md` — plantilla inicial para nuevas habilidades.
- `references/rationalization-defense-cookbook.md` — guía para escribir la tabla de Defensa de Racionalización.
- `references/description-anti-patterns.md` — anti-patrones a evitar en el campo de descripción.
- `references/cross-skill-graph.md` — gráfico de dependencias y referencias cruzadas para las 18 habilidades ywc-*.
