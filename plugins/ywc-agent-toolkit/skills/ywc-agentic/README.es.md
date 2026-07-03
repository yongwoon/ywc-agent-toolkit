# ywc-agentic

Orquesta de forma autónoma el pipeline `ywc-*` desde un objetivo de alto nivel hasta una implementación verificada.

Usa este skill cuando quieras que Codex planifique, ejecute, evalúe y repita el ciclo sin controlar manualmente cada fase.

`--pr-lang en|ja|ko|zh|es` se reenvia sin cambios al executor. `--lang en|ja|ko|zh|es` se pasa a `ywc-task-generator` solo si el usuario lo pide o la shared YWC language policy lo resuelve; si no, downstream pregunta cuando sea necesario.
