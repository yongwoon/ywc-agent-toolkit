<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-debug-rootcause

Una skill de disciplina de proceso que fuerza la **identificación del root cause antes de cualquier fix** para bugs, fallos de test, fallos de build y comportamiento inesperado.

## Qué hace

Aplica la Iron Law:

> **NINGÚN FIX SIN UNA INVESTIGACIÓN DE ROOT CAUSE PRIMERO**

No se puede proponer ningún fix antes de que la Phase 1 (Investigation) esté completa. El proceso de 4 fases:

1. **Phase 1 — Investigación del root cause** — Leer los errores por completo, reproducir de forma fiable, revisar los cambios recientes, instrumentar las fronteras entre múltiples componentes, rastrear el flujo de datos aguas arriba hasta el origen.
2. **Phase 2 — Análisis de patrones** — Localizar un hermano que funcione en la misma codebase, leerlo de principio a fin, listar cada diferencia entre lo roto y lo que funciona (incluidas las que "no pueden importar").
3. **Phase 3 — Hipótesis y prueba** — Formar una única hipótesis con la forma "X es el root cause; el cambio mínimo Z lo arregla"; probar cambiando una variable a la vez.
4. **Phase 4 — Implementación** — Escribir un regression test, aplicar un único fix, verificar red-green-red, controlar la afirmación de finalización mediante `ywc-verify-done`, y luego emitir la prevención sistémica (§6): una clase recurrente se ofrece a `ywc-review-learnings --source debug`, una causa puntual se declara explícitamente.

**Si 3 o más fixes fallan en la misma superficie**, la situación es "architecture is wrong", no "fix harder". Detente y expón la preocupación de diseño al usuario — no intentes un 4.º fix.

## Cuándo se activa

- El usuario menciona "bug", "debug", "왜 안돼", "落ちる", "通らない" o similares.
- Un test, build o type-check falla.
- Ya han fallado dos o más intentos de fix en la misma superficie.
- La tabla de failure-routing de `ywc-verify-done` envía la investigación aquí.

## Cuándo NO usarla

- Redacción activa de la implementación → `ywc-code-gen`
- Retrospectiva posterior a un incidente → `ywc-incident-postmortem`
- Triaje de vulnerabilidades de seguridad → `ywc-security-audit`
- Comprobación de confianza previa a la implementación → `ywc-confidence-gate` (planned)

## Referencias

Las listas de comprobación por fase, la Rationalization Defense y las señales de architectural-stop están en [SKILL.md](./SKILL.md). La disciplina subyacente se adapta de `superpowers:systematic-debugging`.

## Versiones localizadas

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
