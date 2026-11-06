# ywc-confidence-gate

Evalúa si una implementación no trivial está lista para empezar antes de delegar a code generation o executors.

Produce una decisión PROCEED / REVIEW / STOP basada en claridad de alcance, arquitectura, evidencia, reutilización y root cause.

## Analyst contract

`Caller: ywc-confidence-gate` · `analysis_mode=confidence_root_cause`

Indica Caller y analysis_mode explícitamente. La ausencia, un valor desconocido o una pareja incorrecta devuelve `NEEDS_CONTEXT` sin inferencias. Valida Status → Summary → Finding counts → Analysis mode y conserva el gate original del caller.

Devuelve exactamente una causa candidata con evidencia a favor y en contra; sin alternativas ordenadas ni 5 Whys. Un rechazo consume el único dispatch permitido; el caller conserva la puntuación y la decisión de band.

Live runtime: `UNVERIFIED — instruction contract only`.
