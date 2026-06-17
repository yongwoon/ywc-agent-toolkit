# ywc-agent-toolkit

> Este documento está siendo traducido. Consulte la documentación completa en [English](README.md).
>
> Si desea contribuir con la traducción, cree un [Translation Issue](../../issues/new?template=translation.md).

---

Colección de skills para **Claude Code** y **Codex** que automatiza el flujo de trabajo de desarrollo completo — desde la planificación y escritura de especificaciones hasta la generación de código, revisión y lanzamiento.

Actualmente incluye 38 skills para Claude Code, 37 skills para Codex, 12 agentes de Claude Code y 7 custom agents de Codex.

## Prerrequisitos

La instalación mediante marketplace de plugins y plugins de Codex **no tiene prerrequisitos** — la herramienta lo gestiona todo automáticamente.

Para el **script bash fallback**, lo siguiente debe estar instalado antes de ejecutar `install.sh`:

| Herramienta | Necesario para | Instalación |
| ----------- | -------------- | ----------- |
| `git` | Clonar el repositorio | Preinstalado en la mayoría de sistemas |
| `bash ≥ 3.2` | Ejecutar `install.sh` | Preinstalado en macOS / Linux |
| `jq` | Registro de hooks | `brew install jq` / `apt-get install jq` |

En **tiempo de ejecución de skills** (no requerido para la instalación):

| Herramienta | Utilizado por | Instalación |
| ----------- | ------------- | ----------- |
| `python3 ≥ 3.9` | Helpers de runtime de skills: `ywc-parallel-executor`, `ywc-finish-branch`, `ywc-merge-dependabot`; los hooks de Claude Code requieren Python ≥ 3.11 | Preinstalado en macOS 12.3+; `brew install python3` |
| `gh` CLI | Skills/modos basados en PR y releases de GitHub: `ywc-handle-pr-reviews`, `ywc-spec-writer --from-pr/--from-prs`, `ywc-release-pr-list`, `ywc-create-pr`, modo PR de `ywc-finish-branch`, `ywc-merge-dependabot`, `ywc-sequential-executor`/`ywc-parallel-executor`, `ywc-gen-testcase` | `brew install gh` / [cli.github.com](https://cli.github.com) |

---

## Instalación

### Marketplace de plugins de Claude Code (recomendado)

```bash
# Añadir como fuente de marketplace (una sola vez)
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

Después de ejecutar el comando, abra la pestaña **Marketplaces** en el Plugin UI e instale **ywc-agent-toolkit** desde allí.
Las skills se instalan automáticamente en `~/.claude/skills/` sin necesidad de clonar ni ejecutar bash.

### Directorio de plugins de Codex CLI

Este repositorio sigue el mismo patrón de empaquetado multi-harness que proyectos como Superpowers: los metadatos de Claude Code viven en [`.claude-plugin/`](.claude-plugin/), mientras que los metadatos de Codex viven en [`.codex-plugin/`](.codex-plugin/). La fuente de verdad de Codex es [codex/skills](codex/skills). El catálogo de marketplace de Codex con alcance de repositorio en [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) expone el paquete generado `plugins/ywc-agent-toolkit`; su directorio `skills/` se produce desde `codex/skills` con `bash scripts/sync-codex-plugin.sh` y se verifica con `bash scripts/validate.sh`.

Esto permite instalar `ywc-agent-toolkit` desde Codex después de añadir este repositorio como fuente de marketplace de plugins, pero no implica que esté listado en el marketplace oficial curado por OpenAI.

Añada este repositorio como fuente de marketplace de plugins de Codex:

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit
```

Si el marketplace ya estaba añadido, actualice primero su snapshot de Git:

```bash
codex plugin marketplace upgrade ywc-agent-toolkit
```

Luego instale directamente desde el marketplace configurado:

```bash
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit
```

O abra el directorio de plugins:

```text
codex
/plugins
```

Dentro de la sesión interactiva de Codex, elija la pestaña de marketplace **YWC Agent Toolkit**, busque **ywc-agent-toolkit** y seleccione **Install plugin**.

### Barra lateral Plugins de Codex App

En Codex App, abra **Plugins** desde la barra lateral, elija la fuente **YWC Agent Toolkit**, busque o explore **ywc-agent-toolkit**, confirme que la fuente del plugin sea `yongwoon/ywc-agent-toolkit` e instálelo desde la vista de detalles del plugin.

Si la instalación de fuentes de marketplace no está disponible en su entorno, use el fallback bash de abajo.

### Flujo de mantenimiento para skills de Codex

Edite las skills de Codex en [codex/skills](codex/skills). No edite `plugins/ywc-agent-toolkit/skills` como fuente primaria; es el generated marketplace package usado por `codex plugin add`.

Instale una vez los Git hooks del repositorio para mantener sincronizado automáticamente el Codex marketplace package:

```bash
bash scripts/install-git-hooks.sh
```

Con los hooks instalados, los commits que tengan cambios staged en `codex/skills` ejecutan `bash scripts/sync-codex-plugin.sh`, stagean automáticamente el generated package `plugins/ywc-agent-toolkit` y luego ejecutan `bash scripts/validate.sh`. Los pushes que incluyan cambios de Codex skill/package también ejecutan el stale-package check y la validación.

Si los hooks no están instalados, ejecute manualmente los mismos comandos antes del commit:

```bash
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
```

El bash fallback (`bash scripts/install.sh --codex`) instala directamente desde `codex/skills`. El marketplace flow (`codex plugin add ywc-agent-toolkit@ywc-agent-toolkit`) instala desde el generated package `plugins/ywc-agent-toolkit`.

### Script bash fallback

```bash
YWC_REF=<release-tag-or-reviewed-commit>
git clone --branch "$YWC_REF" --depth 1 https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit
git remote get-url origin
git rev-parse --verify HEAD

# Claude Code
bash scripts/install.sh --cc

# Codex
bash scripts/install.sh --codex

# Ambos
bash scripts/install.sh --all
```

Consulte [README.md](README.md) para más detalles.

---

## Modo de salida HTML para Review Skills

Nueve skills de revisión y reporte soportan un flag opt-in `--format html` que genera un informe HTML autocontenido y listo para el navegador, en lugar de Markdown.

**Skills compatibles:** `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`, `ywc-design-renew`

**Motivación:** Los documentos Markdown de más de ~100 líneas generados por IA raramente se leen de principio a fin — un informe que nadie lee no puede impulsar una decisión. HTML añade color, codificación de severidad, pestañas y controles interactivos (casillas, `Copy as Markdown`), para que quien lo recibe realmente lo lea y actúe en consecuencia.

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # hoja de pruebas interactiva con sign-off en localStorage
```

> **⚠️ Coste en tokens** — La salida HTML consume 2-4× más tokens de salida que Markdown y tarda más en generarse. El valor predeterminado es `markdown`; active HTML solo para informes que un humano leerá en un navegador.

---

## Agentes personalizados

Claude Code incluye **12 agentes** personalizados para worker, reviewer y specialist dispatch. Se instalan en `~/.claude/agents/` y están documentados en [`claude-code/agents/README.md`](claude-code/agents/README.md).

Codex incluye **7 agentes** especialistas de solo lectura que complementan los skills `ywc-*`. Se instalan en `~/.codex/agents/`.

| Agente | Propósito | Sandbox |
|--------|-----------|---------|
| `ywc-architect` | Asesor de decisiones arquitectónicas y trade-offs | `read-only` |
| `ywc-security-engineer` | Revisión estática de seguridad y clasificación de threat model | `read-only` |
| `ywc-root-cause-analyst` | Análisis de causa raíz e incidentes | `read-only` |
| `ywc-performance-engineer` | Revisión de rendimiento y recomendaciones de profiling | `read-only` |
| `ywc-typescript-reviewer` | Revisión específica de TypeScript / JavaScript | `read-only` |
| `ywc-python-reviewer` | Revisión específica de Python | `read-only` |
| `ywc-go-reviewer` | Revisión específica de Go | `read-only` |

Consulte [README.md](README.md) para más detalles.
