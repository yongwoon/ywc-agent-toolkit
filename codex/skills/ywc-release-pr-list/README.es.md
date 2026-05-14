<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Release PR List

Una Skill de Codex que extrae los PRs incluidos en un PR de release, los agrupa por autor y actualiza la descripción del PR.

## Descripción General

Al crear un PR de release como `develop` → `main`, esta Skill extrae los números de PR de los encabezados de los commits, busca sus autores y reescribe la sección `## PR LIST`.

### Características Principales

- Extrae números de PR de los patrones `#<número>` en los encabezados de los commits
- Agrupa los PRs por login de autor y los ordena alfabéticamente
- En cada ejecución, pregunta al usuario si desea agregar un resumen de una línea sobre lo que aplicó cada PR; solo cuando se confirma, deriva un resumen conciso del título del PR
- Preserva la descripción existente excepto la sección `## PR LIST`
- Es idempotente cuando se ejecuta múltiples veces

## Uso

```text
/release-pr-list 301
```

Los disparadores en lenguaje natural están definidos en [SKILL.md](./SKILL.md).

## Requisitos Previos

- El CLI `gh` está instalado y autenticado
- El PR de release ya ha sido creado

## Versiones Localizadas

- [Coreano (Principal)](./README.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
