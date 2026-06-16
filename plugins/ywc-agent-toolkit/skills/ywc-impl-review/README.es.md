<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-impl-review

Un Skill que realiza una verificación integral de conformidad de implementación antes de crear un PR una vez que la implementación está completa. Ejecuta 3 Agentes (Reviewer + Security + QA) en paralelo.

## Uso

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
```

## Agentes de ejecución

| Agente | Ámbito de verificación |
| --------------------- | ----------------------------------------------------------------------- |
| Reviewer Agent (opus) | Brechas de implementación vs especificación, calidad del código, consistencia de patrones |
| Security Agent (opus) | OWASP Top 10, autenticación/autorización faltante, validación de entrada |
| QA Agent (sonnet) | Análisis de cobertura de pruebas, sugerencias de casos de prueba faltantes |

## Formato de salida

Informe integrado — El Agregador combina los resultados de 3 Agentes, clasificados por severidad con recomendaciones de corrección priorizadas.

## Activación

Las condiciones de activación para este Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones localizadas

- [Inglés](./README.en.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
