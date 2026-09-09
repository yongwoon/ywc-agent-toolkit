<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-impl-review

Un Skill que realiza una verificación integral de conformidad de implementación antes de crear un PR una vez que la implementación está completa. Ejecuta 5 workers de Phase 1 (Architecture / Design / Devex / Security / QA) en paralelo, y escala los findings ambiguos a un Advisor de Phase 2.

Antes de distribuir el trabajo, se rechaza un objetivo vacío o con más de 200 archivos. Los objetivos con diff (`--base`, `--git-range` y `--working-tree`) también se rechazan por encima de 5.000 líneas añadidas más eliminadas; `--code` solo usa el límite de archivos porque es un objetivo por ruta. Al rechazar, se informan los conteos exactos y los archivos más grandes.

Después de Phase 1, cada finding Critical o High elegible recibe una verificación independiente blind usando solo `file:line` y la severidad declarada. El informe distingue `reproduced`, `verification-failed`, `verification-error` y `cap-unverified`. Estas llamadas no consumen el budget del Advisor de Phase 2, y la procedencia `[P1]`/`[P2]` permanece separada del estado de verificación.

## Uso

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --base main
```

`--working-tree` revisa cambios source staged, unstaged y untracked sin crear un commit. `--base <ref>` revisa desde `git merge-base <ref> HEAD` hasta `HEAD` e informa el ref suministrado y el merge-base resuelto. `--git-range A..B` sigue siendo la comparación explícita de dos extremos. Se requiere exactamente uno de los cuatro modos de destino; son mutuamente excluyentes.

## Agentes de ejecución

| Agente | Ámbito de verificación |
| --------------------- | ----------------------------------------------------------------------- |
| Architecture | Límites de Module, Layering, dirección de Dependency, conformidad estructural con la especificación |
| Design | Diseño de API/Interface, Naming, Signature, Error Model, conformidad de Contract con la especificación |
| Devex | Legibilidad, Error Message, Logging, Documentation, Debuggability |
| Security | Análisis OWASP Top 10 |
| QA | Brechas de Test Coverage, Test Case faltantes |

Advisor de Phase 2 — escala únicamente los findings ambiguos de los cinco workers anteriores (Budget: 5 llamadas por defecto, ajustable con `--advisor-budget`, compartido). Las llamadas de verificación independiente quedan fuera de este budget.

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
