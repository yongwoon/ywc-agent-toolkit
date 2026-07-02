<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-verify-done

Una Skill de disciplina de proceso que exige evidencia de verificación fresca antes de cualquier afirmación de finalización.

## Qué Hace

Invoca esta Skill inmediatamente antes de exponer cualquier afirmación de finalización — "work done", "tests pass", "build succeeds", "bug fixed", "requirements met". Impone una Gate Function de 5 pasos:

1. **IDENTIFY** — Nombra el comando shell exacto que prueba la afirmación.
2. **RUN** — Ejecuta el comando de nuevo **en el mensaje actual**.
3. **READ** — Lee la salida completa y el exit code.
4. **VERIFY** — Confirma que la salida respalda la redacción exacta de la afirmación.
5. **CLAIM** — Solo después de los pasos 1–4, expón la afirmación **junto con el bloque de verificación**.

El vocabulario de aserción no verificada ("should", "probably", "seems") queda bloqueado.

## Cuándo Se Activa

- El usuario señala la finalización ("완료", "done", "完了").
- Justo antes de un commit, la creación de un PR o un merge.
- Justo antes de que un executor pase a la siguiente task.
- Inmediatamente después de recibir el payload de retorno de un subagent.

## Cuándo NO Usar

- Durante el borrador de implementación activa → `ywc-code-gen`
- Investigación de root-cause de un bug → `ywc-debug-rootcause`
- Verificación de confianza previa a la implementación → `ywc-confidence-gate` (planificada)
- Exploración del codebase antes de planificar → `ywc-plan`

## Referencias

Para el conjunto completo de reglas, el output format y la Rationalization Defense, consulta [SKILL.md](./SKILL.md). La disciplina subyacente está adaptada de `superpowers:verification-before-completion`.

## Versiones Localizadas

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
