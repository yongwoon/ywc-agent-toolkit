# ywc-team-assemble

Skill de Codex para cuando el usuario pide explícitamente un specialist team, subagent delegation o parallel agent work.

## Cuándo usarlo

- El usuario pide explícitamente formar un team, delegar a agents o ejecutar en parallel.
- El trabajo tiene al menos dos workstreams independientes.
- Los write scopes pueden separarse y el parent agent puede revisar y sintetizar los resultados.

No lo use para preguntas simples, ediciones de un solo archivo o trabajo estrictamente secuencial.

## Archivos incluidos

- `SKILL.md` — team assembly workflow
- `agents/openai.yaml` — Codex metadata
- `references/prompt-templates.md` — templates para explorer, worker y reviewer
