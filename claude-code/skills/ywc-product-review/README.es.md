<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Skill de Revisión de Producto

## Descripción General

**ywc-product-review** es una Skill de Claude Code que analiza un proyecto desde 5 perspectivas de negocio y servicio para entregar un informe de retroalimentación de mejoras priorizado.

Analiza tanto el código como la documentación (README, especificaciones, docs de producto) para identificar oportunidades de mejora desde una perspectiva de **valor para el usuario, crecimiento, riesgo y mercado** — no desde una perspectiva de calidad técnica del código.

**Características Principales:**

- Análisis desde 5 perspectivas de negocio
- Análisis integrado de código + documentación
- Genera automáticamente un informe con prioridades 🔴 Alta / 🟡 Media / 🟢 Baja
- Incluye sugerencias de mejora accionables para cada hallazgo
- El Resumen Ejecutivo destila los insights más importantes

**Usuarios Objetivo:**

- Product Managers y desarrolladores que buscan dirección para mejorar el servicio
- Equipos que desean revisar un proyecto desde una perspectiva de negocio
- Cualquiera que se pregunte "¿qué deberíamos construir a continuación?"

---

## Cómo Usar

### Invocar la Skill

En Claude Code:

```
# Análisis completo (las 5 perspectivas)
/ywc-product-review

# Solo perspectivas específicas
/ywc-product-review user-value growth

# Con referencias de documentos explícitas
/ywc-product-review @README.md @docs/spec.md
```

O en lenguaje natural:

```
Usuario: Revisa este proyecto desde una perspectiva de negocio
Usuario: Encuentra oportunidades de mejora del servicio
Usuario: ¿Qué deberíamos mejorar para crecer?
Usuario: Analiza las brechas en el valor para el usuario
```

### Requisitos Previos

- El código del proyecto objetivo está disponible en el directorio actual, o
- Se puede hacer referencia a documentación como README o especificaciones de producto

---

## Perspectivas de Análisis

### 5 Perspectivas Principales

| Etiqueta | Contenido del Análisis | Archivo de Referencia |
|---|---|---|
| `[User Value]` | Job-to-be-Done, Propuesta de Valor, necesidades del usuario no satisfechas | `references/user-value.md` |
| `[UX Flow]` | Onboarding, puntos de abandono, recorrido principal del usuario | `references/ux-flow.md` |
| `[Growth]` | Retención, bucles virales, activación, engagement | `references/growth.md` |
| `[Risk]` | Puntos de dolor del usuario, causas de churn, problemas no resueltos | `references/risk.md` |
| `[Market]` | Priorización de funciones, tendencias del mercado, brechas competitivas | `references/market-timing.md` |

### Flujo de Análisis

```
Recopilar contexto (README + código)
    ↓
Phase 1: 5 subagentes de perspectiva en paralelo (cada uno Sonnet)
├── User Value  ├── UX Flow  ├── Growth  ├── Risk  └── Market
    ↓
Phase 2: Opus Advisor (conflictos entre perspectivas, máx. 2 llamadas)
    ↓
Clasificar por prioridad (Alta / Media / Baja)
    ↓
Generar informe + Resumen Ejecutivo
```

---

## Formato del Informe de Salida

Tras el análisis, los resultados se presentan en este formato:

```markdown
## Informe de Revisión de Producto: [Nombre del Proyecto]

**Fecha de Análisis**: [Fecha]
**Perspectivas Revisadas**: User Value · UX Flow · Growth · Risk · Market Timing

---

### 🔴 Alta Prioridad — Acción Inmediata Recomendada

| # | Perspectiva   | Problema         | Evidencia          | Sugerencia      |
|---|---------------|------------------|--------------------|-----------------|
| 1 | [User Value]  | [Desc. problema] | [Ref. código/doc]  | [Mejora]        |

---

### 🟡 Prioridad Media — Revisar para el Roadmap a Corto Plazo

...

---

### 🟢 Baja Prioridad — Consideración a Largo Plazo

...

---

### Resumen Ejecutivo

- **Mayor oportunidad**: [Mejora de mayor impacto]
- **Problema más urgente**: [Problema más crítico a resolver]
- **Dirección a largo plazo**: [Dirección estratégica para la próxima fase]
```

---

## Estructura de Archivos

```
ywc-product-review/
├── SKILL.md                        # Definición de la Skill y flujo de trabajo
├── README.md                       # Guía en coreano
├── README.en.md                    # Este archivo (guía en inglés)
├── README.ja.md                    # Guía en japonés
├── README.ko.md                    # Guía en coreano (igual que README.md)
└── references/
    ├── user-value.md               # Checklist de valor para el usuario
    ├── ux-flow.md                  # Checklist de flujo UX
    ├── growth.md                   # Checklist de mecánicas de crecimiento
    ├── risk.md                     # Checklist de riesgos y puntos de dolor
    ├── market-timing.md            # Checklist de timing de mercado
    └── report-template.md          # Plantilla de salida del informe
```

---

## Ejemplos de Uso

### Ejemplo 1: Análisis Completo

```
Usuario: Revisa este proyecto desde una perspectiva de negocio

Claude: Leyendo la estructura del proyecto y el README...

[Análisis del código y la documentación]

Phase 1: Ejecutando 5 subagentes en paralelo...
[User Value Subagent] Revisando claridad del Job-to-be-Done
[UX Flow Subagent] Analizando onboarding y flujos principales
[Growth Subagent] Revisando mecanismos de retención y virales
[Risk Subagent] Identificando puntos de dolor no resueltos
[Market Subagent] Analizando brechas competitivas y timing
Phase 2: Opus Advisor revisando conflictos entre perspectivas...

## Informe de Revisión de Producto: Mi Proyecto

### 🔴 Alta Prioridad

| # | Perspectiva | Problema | Evidencia | Sugerencia |
|---|---|---|---|---|
| 1 | [UX Flow] | El onboarding requiere 5+ pasos | El Quick Start del README es complejo | Simplificar para alcanzar el valor principal en 2 pasos |
| 2 | [Growth] | Sin mecanismo de retención | No se encontraron funciones de re-engagement | Añadir resumen semanal o dashboard de progreso |

...

### Resumen Ejecutivo
- **Mayor oportunidad**: Simplificar el onboarding para mejorar la tasa de activación
- **Problema más urgente**: No hay mecanismo para que los usuarios vuelvan
- **Dirección a largo plazo**: Introducir funciones de colaboración con efectos de red
```

### Ejemplo 2: Análisis de Una Sola Perspectiva

```
Usuario: Analiza solo desde la perspectiva de Crecimiento

Claude: Centrándose en la perspectiva de Mecánicas de Crecimiento.

[Cargar y aplicar references/growth.md]

## Informe de Revisión de Producto: Mi Proyecto
**Perspectivas Revisadas**: Growth

### 🔴 Alta Prioridad
...
```

---

## Mejores Prácticas

### 1. Proporcionar Tanto Docs como Código

Proporcionar README, especificaciones o notas de entrevistas de usuario junto al código permite un análisis más profundo:

```
Usuario: Revisa esto con @README.md @docs/product-spec.md
```

### 2. Usar Repetidamente para Rastrear la Evolución

Volver a ejecutar después de agregar funciones o mejoras para comparar antes/después:

```
# Antes de la mejora
/ywc-product-review

# Re-analizar después del trabajo en funciones (3 meses después)
/ywc-product-review
```

### 3. Usar el Resumen Ejecutivo como Entrada para el Roadmap

Incorporar los elementos de Alta Prioridad directamente en la planificación de Sprint o en las definiciones de Hito.

---

## Documentos Relacionados

### Referencias Internas

- [Skill de Revisión UI/UX](../ywc-ui-ux-review/README.en.md) — Revisión detallada de UI/UX (diseño visual, arquitectura de información)

### Referencias Externas

- [Teoría Jobs-to-be-Done](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done) — Clayton Christensen
- [Hooked: How to Build Habit-Forming Products](https://www.nirandfar.com/hooked/) — Nir Eyal

---

## Versión

- **Última Actualización**: 2026-04-25
- **Versión de la Skill**: 1.0
- **Compatible Con**: Claude Code

---

## Licencia

Esta Skill es parte del proyecto `develop-with-llm`, proporcionada con fines de aprendizaje y referencia.
