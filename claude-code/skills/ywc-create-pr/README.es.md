<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Crear PR

Un Skill de Claude Code que hace commit de los cambios y crea un PR borrador basado en la plantilla de PR del repositorio.

## Descripción general

Una vez completado el trabajo en una rama de feature, este Skill automatiza el flujo desde la creación del commit hasta la creación del PR borrador.

### Características principales

- Detecta automáticamente la rama base en el orden `develop` → `main` → `master`
- Ejecuta una verificación de seguridad para archivos sensibles como `.env`, `*.key` y `*.pem`
- Admite verificaciones de CI previas al push como lint, format, typecheck y test
- Ejecuta una auto-revisión obligatoria del diff completo antes de presentar el PR (detecta scope creep, restos de debug y secrets)
- Aplica `.github/pull_request_template.md` cuando está disponible
- Crea cada PR como borrador

## Uso

```text
/create-pr
/create-pr main
/create-pr --skip-ci-check
/create-pr main --skip-ci-check
```

Los disparadores en lenguaje natural están definidos en [SKILL.md](./SKILL.md).

## Requisitos previos

- La CLI `gh` está instalada y autenticada
- El trabajo se realiza en una rama de feature dentro de un repositorio Git

## Versiones localizadas

- [Coreano (Principal)](./README.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
