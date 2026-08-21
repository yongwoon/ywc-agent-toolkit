# ywc-agent-toolkit

> Este documento está en proceso de traducción. Para el contenido completo, consulte [English](README.md).
>
> Si desea contribuir con la traducción, cree un [Translation Issue](../../issues/new?template=translation.md).

---

Colección de skills para **Claude Code** y **Codex** que automatiza el flujo de desarrollo completo — desde la planificación y la redacción de especificaciones hasta la generación de código, la revisión y la publicación.

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

> 📖 **[Documentación y guía](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/)** — este README es el recorrido breve. Los prerrequisitos, la instalación, la referencia completa de skills y las guías paso a paso están en la guía.

| Lo que busca | Página de la guía |
| ------------ | ----------------- |
| Entregar su primera función en 5 minutos | [03. Inicio rápido](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/03-quickstart/) |
| Qué skill ejecutar y en qué orden | [17. Referencia completa de skills](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/14-skill-reference/) |
| Prerrequisitos, rutas de instalación, variables de entorno | [18. Prerrequisitos e instalación](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/15-prerequisites-installation/) |
| Cambio pequeño / multitarea / bucle autónomo | [04](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/04-general-cycle-small/) · [05](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/05-general-cycle-medium-large/) · [06](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/06-agentic-autonomous-loop/) |

## Herramientas compatibles

| Herramienta | Skills | Custom Agents | Ruta de instalación                      |
| ----------- | ------ | ------------- | ---------------------------------------- |
| Claude Code | 42     | 12            | `~/.claude/skills/`, `~/.claude/agents/` |
| Codex       | 52     | 8             | `~/.codex/skills/`, `~/.codex/agents/`   |

---

## Inicio rápido

### Claude Code

Instale desde el marketplace de plugins — sin clonar y sin prerrequisitos:

```bash
/plugin marketplace add yongwoon/ywc-agent-toolkit    # 1. registrar la fuente
/plugin install ywc-agent-toolkit@ywc-agent-toolkit   # 2. instalar el plugin
```

`marketplace add` solo registra la fuente: a continuación debe ejecutar `/plugin install` o instalarlo desde la pestaña **Marketplaces** de la interfaz de plugins. Reinicie Claude Code después para que aparezcan las skills.

### Codex

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit   # 1. registrar la fuente
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit      # 2. instalar el plugin
```

Si ya había añadido el marketplace, actualice antes su instantánea de Git con `codex plugin marketplace upgrade ywc-agent-toolkit`. También puede ejecutar `codex`, abrir `/plugins` e instalarlo desde la pestaña **YWC Agent Toolkit**.

Si utiliza la **Codex App**, abra **Plugins** en la barra lateral, elija la fuente **YWC Agent Toolkit**, confirme que es `yongwoon/ywc-agent-toolkit` e instálelo desde la vista de detalles del plugin.

### Después, ejecute una skill

Ambas herramientas exponen los mismos comandos:

```bash
/ywc-onboard-repo           # comprender un código desconocido en minutos
/ywc-plan                   # convertir una idea vaga en un plan o una especificación
/ywc-debug-rootcause        # rastrear un error hasta su causa raíz
/ywc-impl-review            # revisar el código por especificación / seguridad / calidad
/ywc-agentic                # ejecutar el pipeline completo de forma autónoma desde un objetivo
```

→ Los prerrequisitos, el fallback por script bash, las rutas de instalación y las variables `CLAUDE_SKILLS_DIR` / `CLAUDE_AGENTS_DIR` / `CODEX_HOME` están documentados en [Prerrequisitos e instalación](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/15-prerequisites-installation/).

### Opciones de instalación no cubiertas en la guía

```bash
# Solo skills concretas
bash scripts/install.sh --cc ywc-plan ywc-commit ywc-create-pr
bash scripts/install.sh --codex ywc-plan ywc-commit ywc-ui-ux-review

# Solo agentes seleccionados, o skills sin agentes
bash scripts/install.sh --cc-agents ywc-backend-coder ywc-qa-engineer
bash scripts/install.sh --cc --skip-agents
```

### Idioma de salida por defecto en Codex

El comando `ywc-setup`, exclusivo de Codex, configura el idioma por defecto de los artefactos de las skills `ywc-*` de Codex:

```bash
ywc-setup --scope project --lang ko
ywc-setup --scope user --lang ja
```

El orden de resolución es: `--lang` explícito > `.codex/ywc.json` del proyecto > guía del proyecto (`AGENTS.md` / `CODEX.md` / `CLAUDE.md`) > `~/.codex/ywc.json` del usuario > preguntar al usuario. No se admiten valores por defecto de sesión.

---

## Skills

La mayoría de las skills `ywc-*` están disponibles tanto para Claude Code como para Codex. El catálogo completo, agrupado por lo que desea hacer, está en la [Referencia completa de skills](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/14-skill-reference/). Empiece por aquí:

| Objetivo | Skills |
| -------- | ------ |
| Convertir una idea en un plan o especificación | [`ywc-plan`](claude-code/skills/ywc-plan/README.md) → [`ywc-spec-writer`](claude-code/skills/ywc-spec-writer/README.md) |
| Comprender un código desconocido | [`ywc-onboard-repo`](claude-code/skills/ywc-onboard-repo/README.md) |
| Dividir el trabajo en tareas sin conflictos de dependencia | [`ywc-task-generator`](claude-code/skills/ywc-task-generator/README.md) |
| Implementar tareas de extremo a extremo | [`ywc-sequential-executor`](claude-code/skills/ywc-sequential-executor/README.md) / [`ywc-parallel-executor`](claude-code/skills/ywc-parallel-executor/README.md) |
| Ejecutar el pipeline completo desde un objetivo | [`ywc-agentic`](claude-code/skills/ywc-agentic/README.md) |
| Encontrar la causa raíz de un error | [`ywc-debug-rootcause`](claude-code/skills/ywc-debug-rootcause/README.md) |
| Revisar calidad y seguridad del código | [`ywc-impl-review`](claude-code/skills/ywc-impl-review/README.md), [`ywc-security-audit`](claude-code/skills/ywc-security-audit/README.md) |
| Abrir un PR y atender comentarios de revisión | [`ywc-create-pr`](claude-code/skills/ywc-create-pr/README.md) → [`ywc-handle-pr-reviews`](claude-code/skills/ywc-handle-pr-reviews/README.md) |
| Generar una hoja de pruebas de QA | [`ywc-gen-testcase`](claude-code/skills/ywc-gen-testcase/README.md) |
| Redactar notas de versión | [`ywc-release-pr-list`](claude-code/skills/ywc-release-pr-list/README.md) + [`ywc-changelog-release-notes`](claude-code/skills/ywc-changelog-release-notes/README.md) |
| Crear una nueva skill `ywc-*` | [`ywc-skill-author`](claude-code/skills/ywc-skill-author/README.md) |

Puede explorar todos los directorios de skills en [`claude-code/skills/`](claude-code/skills) y [`codex/skills/`](codex/skills); cada uno tiene su propio README.

**Cómo encajan:** `ywc-plan` → (Medium/Large) `ywc-spec-writer` → `ywc-spec-ready` → `ywc-task-generator` → `ywc-sequential-executor` / `ywc-parallel-executor`, que entrega cada tarea de extremo a extremo. Los cambios puntuales omiten el executor: `ywc-create-pr` y después `ywc-handle-pr-reviews`. Las [guías del pipeline principal](https://yongwoon.github.io/ywc-agent-toolkit-lp/es/guidebook/02-core-concepts/) recorren cada camino con sus comandos y flags.

### Modo de salida HTML

Nueve skills de revisión e informe aceptan `--format html` y producen un informe HTML autocontenido, listo para el navegador, en lugar de Markdown: color, codificación por severidad, pestañas y controles interactivos, para que la persona que lo recibe realmente lo lea y actúe.

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # hoja de pruebas interactiva con firma en localStorage
```

> **⚠️ Coste en tokens** — la salida HTML consume entre 2 y 4 veces más tokens de salida que Markdown. El valor por defecto es `markdown`; actívelo solo para informes que una persona vaya a leer en el navegador.

Skills compatibles y detalles: [`references/html-output.md`](claude-code/skills/references/html-output.md).

---

## Agentes personalizados

Claude Code incluye 12 agentes personalizados para despacho de tipo worker, reviewer y specialist, instalados en `~/.claude/agents/` y documentados en [`claude-code/agents/README.md`](claude-code/agents/README.md).

Codex incorpora siete agentes especialistas de solo lectura equivalentes, instalados en `~/.codex/agents/` (configurable con `CODEX_HOME`) como un archivo TOML por agente:

| Agente | Propósito |
| ------ | --------- |
| [`ywc-architect`](claude-code/agents/ywc-architect.md) | Asesor de decisiones arquitectónicas y compromisos de diseño |
| [`ywc-security-engineer`](claude-code/agents/ywc-security-engineer.md) | Revisión estática de seguridad y triaje de modelos de amenazas |
| [`ywc-root-cause-analyst`](claude-code/agents/ywc-root-cause-analyst.md) | Análisis de causa raíz y de incidentes |
| [`ywc-performance-engineer`](claude-code/agents/ywc-performance-engineer.md) | Revisión de rendimiento y recomendaciones de perfilado |
| [`ywc-typescript-reviewer`](claude-code/agents/ywc-typescript-reviewer.md) | Revisión específica de TypeScript / JavaScript |
| [`ywc-python-reviewer`](claude-code/agents/ywc-python-reviewer.md) | Revisión específica de Python |
| [`ywc-go-reviewer`](claude-code/agents/ywc-go-reviewer.md) | Revisión específica de Go |

Todos los agentes de Codex son de solo lectura y nunca editan archivos. Devuelven un `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` estandarizado, un conjunto compacto de hallazgos y un `Next action:` cuando quien lo invoca debe aplicar o inspeccionar algo. El TOML fuente está en [`codex/agents/`](codex/agents/).

---

## Hooks de Claude Code

Hooks de automatización que se ejecutan antes y después de las llamadas a herramientas de Claude Code. Se instalan en `~/.claude/hooks/` (global) o `./.claude/hooks/` (local al proyecto) y se registran automáticamente en `settings.json`. Requieren `jq` y `uv`.

```bash
bash scripts/install.sh --hooks                    # todos los hooks, globalmente
bash scripts/install.sh --hooks --local            # en el proyecto actual
bash scripts/install.sh --hooks cost-tracker       # solo hooks concretos
bash scripts/install.sh --list --hooks             # listar los disponibles
```

| Hook                        | Evento                 | Descripción                                                             |
| --------------------------- | ---------------------- | ----------------------------------------------------------------------- |
| `block-dangerous-commands`  | `PreToolUse`           | Bloquea comandos de shell peligrosos (niveles critical/high/strict)      |
| `check-claude-md-freshness` | `PreToolUse`           | Verifica que CLAUDE.md esté actualizado antes de `git push`             |
| `cost-tracker`              | `PostToolUse` + `Stop` | Registra estadísticas de llamadas y muestra un resumen al salir          |
| `notify-permission`         | `Notification`         | Envía un aviso a Slack cuando Claude espera permiso (`CCH_SLA_WEBHOOK`)  |
| `permission-request`        | `PermissionRequest`    | Aprueba automáticamente herramientas seguras (Read, Write, Edit)         |
| `protect-secrets`           | `PreToolUse`           | Bloquea el acceso a `.env`, claves SSH y otros archivos secretos         |
| `session-start`             | `SessionStart`         | Inyecta git status, `CONTEXT.md`, TODOs e issues de GitHub al iniciar    |

Detalles de uso por hook: [`claude-code/hooks/README.md`](claude-code/hooks/README.md).

---

## Contribuir

¡Las contribuciones son bienvenidas! Lea [CONTRIBUTING.md](CONTRIBUTING.md) antes de enviar un PR.

- **Informes de errores y mejoras de skills**: abra un issue o un PR
- **Nuevas skills**: siga las pautas de [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md)
- **Traducciones**: consulte la [guía de traducción](CONTRIBUTING.md#translations)
- **Sincronización del paquete de Codex**: consulte [Maintainer workflow for Codex skills](CONTRIBUTING.md#maintainer-workflow-for-codex-skills)

## License

MIT
