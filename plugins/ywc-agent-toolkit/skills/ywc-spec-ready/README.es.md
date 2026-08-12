<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-spec-ready

Este documento introduce el workflow Codex `ywc-spec-ready`. Las condiciones de activación, anti-triggers, pasos de ejecución y formato de salida autoritativos están definidos en [SKILL.md](./SKILL.md).

## Versiones localizadas

- [한국어](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어 full](./README.ko.md)
- [Chinese (Simplified)](./README.zh.md)

## Cuándo usarlo

- Un natural-language goal debe convertirse en una spec validada antes de task generation.
- Una spec existente debe alcanzar `DONE` desde `ywc-spec-validate` antes de `ywc-task-generator`.
- `DONE_WITH_CONCERNS` debe pasar por loops repetidos de `ywc-plan --update-spec` dentro de límites estrictos.

## Uso

```bash
$ywc-spec-ready "Design payment failure recovery UX"
$ywc-spec-ready --spec docs/ywc-plans/example.md --max-iterations 4
$ywc-spec-ready --spec docs/ywc-plans/example.md --dry-run
```

Cuando tiene éxito, este Skill imprime `ywc-task-generator <spec-path>` y se detiene. No genera tasks ni implementa code directamente.

## Salida

Este Skill sigue el report, loop log y status format definidos en [SKILL.md](./SKILL.md).

## Agentic artifact profile

Con `--artifact-profile agentic`, el éxito devuelve un único bloque Result con solo `Status: DONE` y `Artifact: <path>`. Artifact debe ser un Markdown relativo al repositorio, existente y regular, dentro de la raíz candidata validada; se rechazan `Scale` y los fallbacks de prose/basename/raw-response.
