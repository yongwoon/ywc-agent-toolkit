<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-impl-review

Un Skill que realiza una verificación integral de conformidad de implementación antes de crear un PR una vez que la implementación está completa. Ejecuta 5 workers de Phase 1 (Architecture / Design / Devex / Security / QA — 4 en Sonnet, 1 en Haiku) en paralelo, y escala los findings ambiguos a un Advisor de Phase 2 en Opus.

## Uso

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
```

`--working-tree` revisa los cambios de source staged, unstaged y untracked sin crear un commit. No lo combine con `--code` ni con `--git-range`.

## Agentes de ejecución

| Agente | Ámbito de verificación |
| --------------------- | ----------------------------------------------------------------------- |
| Architecture (sonnet) | Límites de Module, Layering, dirección de Dependency, conformidad estructural con la especificación |
| Design (sonnet) | Diseño de API/Interface, Naming, Signature, Error Model, conformidad de Contract con la especificación |
| Devex (sonnet) | Legibilidad, Error Message, Logging, Documentation, Debuggability |
| Security (sonnet) | Análisis OWASP Top 10 |
| QA (haiku) | Brechas de Test Coverage, Test Case faltantes |

Phase 2 (opus) — escala únicamente los findings ambiguos de los cinco workers anteriores (Budget: 5 llamadas por defecto, ajustable con `--advisor-budget`, compartido).

## Formato de salida

Informe integrado — El Agregador combina los findings de Phase 1 con los veredictos del Advisor de Phase 2, clasificados por severidad con recomendaciones de corrección priorizadas. Cada finding lleva un marcador `[P1]`/`[P2]` que indica su procedencia de Phase 1/Phase 2.

## Activación

Las condiciones de activación para este Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones localizadas

- [Inglés](./README.en.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
- [Chino](./README.zh.md)
- [Español](./README.es.md)
