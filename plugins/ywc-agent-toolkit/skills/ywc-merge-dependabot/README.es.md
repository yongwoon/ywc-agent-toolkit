<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Skill de Merge Dependabot

Un Skill de Codex para fusionar de forma segura en lotes los Pull Requests creados por Dependabot.

## Descripción general

Este Skill detecta los PRs de Dependabot, aplica verificaciones de seguridad previas al merge y los procesa en orden ascendente de número de PR.

### Características principales

- Detecta y fusiona PRs de Dependabot en lote
- Admite un modo de merge solo para seguridad
- Verifica cambios en la imagen base de Dockerfile, actualizaciones de versión mayor y estado de CI antes del merge
- Resuelve conflictos solo mediante `@dependabot rebase` (nunca a mano), espera el CI del head rebasado y hace merge fijado al head verificado (`--match-head-commit`)
- Genera un informe de resumen al final

## Uso

```text
/merge-dependabot
/merge-dependabot security
```

Los disparadores en lenguaje natural están definidos en [SKILL.md](./SKILL.md).

## Requisitos previos

- La CLI `gh` está instalada y autenticada
- El usuario tiene permisos de merge en el repositorio
- Los PRs de Dependabot ya existen en el repositorio

## Versiones localizadas

- [Coreano (Principal)](./README.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)

## Seguridad operativa

Detecta FROM modificados solo en hunks de Dockerfile; los errores de consulta o análisis quedan sin resolver. El polling de rebase/CI conserva todo el estado y un único deadline run-wide de 1800 segundos entre bloques; un timeout es un fallo. La preferencia de invocación explícita en metadata no garantiza su imposición en runtime.
