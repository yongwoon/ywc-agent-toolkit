<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Setup Language Skill (ywc-setup-language)

Un Claude Code Skill que persiste un **output language** a nivel de project o user, de modo
que cada `ywc-*` skill language-aware produzca document, PR text y commit message en ese
idioma sin un `--lang` flag ni un prompt en cada llamada.

## Descripción general

Este Skill escribe una sección canónica `## Language Policy` en el `CLAUDE.md` apropiado:

- Establece el output language para los ywc-generated document (plan / spec / task), el PR
  title & body y las commit message description.
- Idempotent — al reejecutar, reemplaza la sección en su lugar en vez de añadir un duplicado.
- El mode `--show` de solo lectura informa el idioma resuelto actualmente y su origen.
- Additive y non-blocking — un project sin policy se comporta exactamente igual que antes.

Solo **escribe** la policy. Cómo los consuming skill la resuelven (precedence chain, code
list, section format) vive en la shared reference `references/language-resolution.md`.

## Uso

```text
/ywc-setup-language ko
```

```text
/ywc-setup-language ja --user
```

```text
/ywc-setup-language --show
```

También se aceptan los nombres completos de idioma y se normalizan: `korean` → `ko`,
`japanese` → `ja`, `english` → `en`, `spanish` → `es`, `chinese` → `zh`.

## Arguments

| Argument | Description |
| --- | --- |
| `<language>` | Output language code (`ko\|ja\|en\|es\|zh`) o nombre completo. Requerido salvo con `--show`. |
| `--user` | Escribe en el `~/.claude/CLAUDE.md` user-global en lugar del `CLAUDE.md` del project. |
| `--show` | Informa el idioma resuelto y su source rung (project / user / none). No escribe. |

## Qué escribe

```markdown
## Language Policy

- **Output language**: ko
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
```

## Precedencia

La policy configurada es un rung de la resolution chain que leen los consuming skill:
`--lang` flag → project `## Language Policy` → user `## Language Policy` → el fallback
existente de cada skill. Una project policy gana a una user policy. Consulta
`references/language-resolution.md` para las reglas completas.

## Consuming skills

`ywc-task-generator`, `ywc-spec-writer`, `ywc-plan`, `ywc-create-pr`, `ywc-commit`.
