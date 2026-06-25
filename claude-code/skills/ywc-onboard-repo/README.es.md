# ywc-onboard-repo

Un skill de 4 fases (Reconnaissance → Architecture → Conventions → Generate) para entrar en un repositorio existente o desconocido. Emite una Onboarding Guide a la conversación y escribe un Starter CLAUDE.md en la raíz del repo, mejorando in situ cualquier CLAUDE.md existente. **No** es un scaffolder — `ywc-project-scaffold` es la dirección inversa. La Reconnaissance usa solo Glob + Grep para mantener acotado el coste de tokens.

## Versiones localizadas

- [한국어 (entry)](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)
- [中文](./README.zh.md)

## Cuándo usarlo

- El usuario dice "onboard me", "guíame por este repo", "ayúdame a entender este codebase"
- Configurar Claude Code en un proyecto por primera vez (genera el Starter CLAUDE.md)
- Un runner de subagents necesita un CLAUDE.md antes de delegar la implementación

## Cómo invocarlo

```bash
/ywc-onboard-repo --scope apps/web/
```

O en lenguaje natural:

> "onboard me to this repo"
> "genera un CLAUDE.md a partir de las convenciones existentes"

## La Ley de Hierro

1. **La Reconnaissance usa solo Glob + Grep** — Read se reserva para señales ambiguas que surjan en fases posteriores
2. **Las convenciones verificadas desde el código fuente prevalecen sobre las inferidas desde config**
3. **Un CLAUDE.md existente se mejora in situ** — nunca se sobrescribe

## Entradas

- (opcional) `--scope <dir>` — limita la reconnaissance a un workspace (útil en monorepos)
- (opcional) `--guide-only` — emite la Onboarding Guide, omite CLAUDE.md
- (opcional) `--claude-md-only` — escribe el CLAUDE.md, omite la Guide
- (opcional) `--enhance` — fuerza la ruta de mejora incluso cuando aún no existe ningún CLAUDE.md

## Salidas

- **Output A**: Onboarding Guide (Markdown impreso) — Tech Stack, Architecture, Key Entry Points, Directory Map, Request Lifecycle, Conventions, Common Tasks, Where to Look, Detection Confidence
- **Output B**: Starter CLAUDE.md (escrito en la raíz del repo) — si existe un CLAUDE.md, solo se añade la sección `## Detected Conventions (<YYYY-MM-DD>)`. Si hay un `AGENTS.md` (el estándar vendor-neutral) / `.cursorrules` existente, se Read y reconcilia para que el CLAUDE.md generado no lo contradiga (emitir AGENTS.md es tarea del Codex variant — divergencia intencional)

## Skills relacionados

- `ywc-project-scaffold` — dirección inversa (crea un repo nuevo); nunca invoques ambos en una sesión
- `ywc-refactor-clean` — downstream cuando la reconnaissance revela acumulación significativa de dead-code
- `ywc-impl-review` — la Onboarding Guide generada ancla a un reviewer en frío
- `ywc-plan` — el Request Lifecycle de la Fase 2 es el ancla arquitectónica que consume plan Step 2
- `ywc-verify-done` — reglas de vocabulario para la afirmación final "Wrote CLAUDE.md"
