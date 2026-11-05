# ywc-worktrees

Gestiona creación, auditoría, resolución de ubicación y limpieza de git worktrees para espacios de trabajo aislados.

Se usa de forma independiente o como helper delegado por executors y finish-branch.

## Ramas existentes y worktrees de PR

`create` acepta exactamente uno entre `--base-branch` y `--existing-branch <H>`. Usa refs local/origin exactas y distingue ausencia, fallo de transporte, checkout existente, estado dirty y bloqueo.
