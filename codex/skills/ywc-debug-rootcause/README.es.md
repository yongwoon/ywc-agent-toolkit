# ywc-debug-rootcause

Guía una investigación disciplinada de bugs, fallos de tests, fallos de build o comportamientos inesperados.

Bloquea los parches sintomáticos hasta identificar root cause y evidencia reproducible.

## Analyst contract

`Caller: ywc-debug-rootcause` · `analysis_mode=debug_hypotheses`

Indica Caller y analysis_mode explícitamente. La ausencia, un valor desconocido o una pareja incorrecta devuelve `NEEDS_CONTEXT` sin inferencias. Valida Status → Summary → Finding counts → Analysis mode y conserva el gate original del caller.

Registra el feedback loop mínimo, el fallo y catches/misses; ordena 3–5 hipótesis falsables y cambia una variable por experimento. Sin reproducción automática, registra pruebas manuales y límites sin inventar RED. Detente tras tres fixes fallidos. Solo ambos campos separados y respaldados por evidencia, `Fix #4 signal: fix harder` y `Next fix worth attempting: <one concrete minimal change>`, en una respuesta debug válida permiten un cuarto intento final. Si falla, detente; no hay quinto intento.

Live runtime: `UNVERIFIED — instruction contract only`.
