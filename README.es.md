# ywc-agent-toolkit

> Este documento está siendo traducido. Consulte la documentación completa en [English](README.md).
>
> Si desea contribuir con la traducción, cree un [Translation Issue](../../issues/new?template=translation.md).

---

Colección de skills para **Claude Code** y **Codex** que automatiza el flujo de trabajo de desarrollo completo — desde la planificación y escritura de especificaciones hasta la generación de código, revisión y lanzamiento.

Actualmente incluye 36 skills para Claude Code, 37 skills para Codex, 12 agentes de Claude Code y 7 custom agents de Codex.

## Instalación

### Marketplace de plugins de Claude Code (recomendado)

```bash
# Añadir como fuente de marketplace (una sola vez)
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

Después de ejecutar el comando, abra la pestaña **Marketplaces** en el Plugin UI e instale **ywc-agent-toolkit** desde allí.
Las skills se instalan automáticamente en `~/.claude/skills/` sin necesidad de clonar ni ejecutar bash.

### Script bash

```bash
git clone https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit

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

Ocho skills de revisión y reporte soportan un flag opt-in `--format html` que genera un informe HTML autocontenido y listo para el navegador, en lugar de Markdown.

**Skills compatibles:** `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`

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
