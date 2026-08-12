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
- `evals/evals.json` — evaluaciones del contrato de aislamiento de roles, Claim/Evidence, límite y privacidad

## Context Safety

Los prompts del equipo validan Claims acotados y evidencia citada antes de proyectarlos. El revisor independiente recibe solo el alcance y las rutas de artifacts; el rol dependiente recibe solo Claims y los artifacts citados. Se rechazan conclusiones o recomendaciones de pares, transcript, contenido raw, artifacts no citados y Claims inválidos o fuera del límite.
