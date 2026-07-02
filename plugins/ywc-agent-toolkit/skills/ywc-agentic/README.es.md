# ywc-agentic

Orquesta de forma autónoma el pipeline `ywc-*` desde un objetivo de alto nivel hasta una implementación verificada.

Usa este skill cuando quieras que Codex planifique, ejecute, evalúe y repita el ciclo sin controlar manualmente cada fase.

`--pr-lang en|ja|ko|zh|es` se reenvia sin cambios al executor para el idioma del titulo/cuerpo del PR. Solo se pasa `--lang en|ja|ko|zh|es` a `ywc-task-generator` cuando el usuario o project guidance pide explicitamente un idioma de task/spec; en caso contrario se conserva el comportamiento existente sin `--lang`.
