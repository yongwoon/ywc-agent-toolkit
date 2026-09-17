# ywc-verify-done

Actúa como gate antes de afirmar que el trabajo está completo, que los tests pasan o que un bug está resuelto.

La afirmación final debe incluir evidencia fresca de comandos ejecutados en la sesión actual.

## Opcional: Gate Ledger

Úsalo solo como escalación adicional cuando varios comandos o artefactos de subagentes aceptados formen una misma afirmación. El checker instalado no inicia subprocess ni cambia bytes con `--status`; el modo bare reanuda únicamente gates sin un `PASS` cached exacto y `--reverify` ejecuta fresh todos los gates ejecutables. Los gates `MANUAL` se omiten. `CHECK` es shell arbitrario: revísalo antes de ejecutarlo y usa un positive control para demostrar una ausencia. Las afirmaciones PR-ready aún requieren polling independiente de review durante 600 segundos, evidencia `--verify` head-SHA, CI y PR-health. Consulta la gramática en [gate-ledger.md](./references/gate-ledger.md).
