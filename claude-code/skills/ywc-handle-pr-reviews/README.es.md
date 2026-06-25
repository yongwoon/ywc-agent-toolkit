<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Gestionar Revisiones de PR

Un Skill de Claude Code que verifica los comentarios de revisión de PR, aplica correcciones donde corresponde y responde a cada hilo.

## Descripción general

Este Skill automatiza el trabajo repetitivo después de que llega una revisión de PR. Las solicitudes de cambio claras se corrigen directamente, mientras que los comentarios ambiguos o debatibles se presentan al usuario para su juicio.

"Gestionar" un PR significa dejarlo **mergeable**, no solo responder a los comentarios. El Skill limpia **tres gates independientes** — (1) comentarios de revisión, (2) estado de CI, (3) merge-readiness (conflicto) — en **cada** invocación. CI puede estar en rojo y la base puede haber avanzado a un conflicto incluso sin comentarios, por lo que los gates de CI y conflicto nunca se omiten.

### Características principales

- Clasifica los comentarios en solicitudes de corrección, comentarios debatibles, preguntas y elementos ya gestionados
- Agrupa los comentarios por archivo y gestiona las correcciones relacionadas juntas
- Hace coincidir el idioma de respuesta con el idioma del revisor
- Omite comentarios que ya fueron gestionados o ya respondidos
- Limpia fallos de CI y conflictos con la rama base tras los comentarios, dejando el PR mergeable (ambos gates siempre se ejecutan, incluso con cero comentarios)

## Uso

```text
/handle-pr-reviews
/handle-pr-reviews 123
```

Los disparadores en lenguaje natural están definidos en [SKILL.md](./SKILL.md).

## Requisitos previos

- La CLI `gh` está instalada y autenticada
- El comando se ejecuta en una rama que ya tiene un PR

## Versiones localizadas

- [Coreano (Principal)](./README.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
