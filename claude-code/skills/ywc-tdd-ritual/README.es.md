<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-tdd-ritual

Una Skill de disciplina TDD que impone RED → GREEN → REFACTOR con un paso obligatorio de watch-it-fail antes de escribir cualquier production code.

## What It Does

Impone la Iron Law:

> **NO HAY PRODUCTION CODE SIN UN TEST QUE FALLE PRIMERO**

Un ciclo de 7 pasos controla cada commit de production-code.

1. **RED** —— Escribe un test mínimo que falle para un behavior (aún sin production code).
2. **Verify RED** —— Observa que el test falle por la razón **esperada**. Este paso es obligatorio.
3. **GREEN** —— Escribe el production code más simple que haga pasar el test.
4. **Verify GREEN** —— El nuevo test y el suite más amplio pasan ambos.
5. **REFACTOR** —— Mejora los nombres / elimina duplicación mientras el suite se mantiene en verde.
6. **Verify after REFACTOR** —— Todos los tests siguen pasando.
7. Repite el loop con el siguiente behavior, o traspasa a `ywc-verify-done`.

El patrón "code first, tests later" está bloqueado porque los tests escritos después del code pasan en la primera ejecución —— nunca los ves capturar un defecto, así que no puedes confiar en que capturen uno en el futuro.

## When It Triggers

- El usuario dice "TDD", "test first", "테스트 먼저", "RED-GREEN".
- Al implementar cualquier nuevo feature, bug fix o cambio de behavior.
- `ywc-code-gen --tdd` delega aquí.
- `ywc-debug-rootcause` Phase 4 §1 necesita un regression test.

## When NOT to Use

- El usuario ha optado explícitamente por no usarlo en un prototype desechable en este turno.
- Investigar un test failure existente → `ywc-debug-rootcause`.
- Code generado / archivos de config.
- Verificación de completion-claim → `ywc-verify-done` (TDD es la disciplina de escritura; verify-done es la disciplina de declaración).

## References

Las reglas completas del ciclo, la Rationalization Defense y el output format están en [SKILL.md](./SKILL.md). La disciplina subyacente está adaptada de `superpowers:test-driven-development`, ajustada para traspasar las declaraciones a `ywc-verify-done` y enrutar la investigación a `ywc-debug-rootcause`.

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
