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
- Intenta resolver conflictos cuando es posible
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
