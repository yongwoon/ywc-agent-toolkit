<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-spec-validate

Una habilidad de Agente Revisor de Especificaciones que valida la calidad de las especificaciones después de escribirlas y antes de ejecutar el generador de tareas.

## Uso

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
/ywc-spec-validate --spec docs/ywc-plans/example.md --advisor-budget 0
```

## Dimensiones de Revisión

| Dimensión               | Qué se revisa                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------- |
| Completitud             | Elementos requeridos faltantes (Manejo de Errores, Casos Límite, Paginación, etc.)     |
| Consistencia            | Inconsistencias de terminología/formato/estructura de datos entre documentos           |
| Factibilidad            | Si puede implementarse con el stack actual                                             |
| Compatibilidad con código | Conflictos con el Esquema de BD existente y los patrones de Rutas API               |

## Agente de Ejecución

- **Agente Revisor de Especificaciones** (claude-opus-4-20250514)

## Formato de Salida

Problemas clasificados por severidad (Crítico / Advertencia / Sugerencia), cada uno con referencias de archivo:línea y sugerencias de mejora.

## Advisor Budget

`--advisor-budget <n>` establece el presupuesto de asesores de Phase 2 para esta invocación. Si se omite, usa el valor predeterminado `2`; `0` desactiva advisor escalation. El encabezado del reporte incluye `Phase 2 advisor calls used: X of N (...)` y `Advisor budget status: available | disabled | exhausted | advisor-required | not-reported`.

## Activación

Las condiciones de activación de esta Habilidad están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones Localizadas

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
