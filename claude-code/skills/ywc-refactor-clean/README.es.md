<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-refactor-clean

Skill de eliminación de código muerto respaldada por herramientas de detección (knip / depcheck / ts-prune / vulture / deadcode / cargo-udeps). Los hallazgos se clasifican en niveles SAFE / CAUTION / DANGER, se eliminan uno por uno con una ejecución de Test acotada antes y después de cada eliminación, y luego se cierran con un Verification Report que sigue el formato de evidence-block de `ywc-verify-done`. Los cambios de comportamiento (por ejemplo, la consolidación de duplicados que necesita reconciliación semántica) quedan explícitamente fuera de alcance y se enrutan a `ywc-tdd-ritual` + `ywc-code-gen`.

## Versiones Localizadas

- [한국어 (entry)](./README.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## Cuándo Usar

- El usuario dice "remove dead code", "run knip", "clean unused imports"
- Después de un sprint, como una pasada de higiene mensual programada en su propia branch
- Cuando `ywc-onboard-repo` detecta que la acumulación de código muerto bloquea la comprensión de la arquitectura en un repo recién explorado

## Cómo Invocar

```bash
/ywc-refactor-clean --scope src/ --tier safe
```

O en lenguaje natural:

> "clean up the dead code"
> "run knip and remove the safe findings"

## La Ley de Hierro

**Nunca eliminar sin tres testigos**: (1) la herramienta de detección lo marca, (2) grep encuentra cero referencias, (3) los Test permanecen en verde después de cada lote.

## Entradas

- (opcional) `--scope <dir>` — restringir la detección + eliminación a una ruta (por defecto: repo root)
- (opcional) `--tier safe | safe+caution | all` — detenerse después del nivel indicado (por defecto: `safe`)
- (opcional) `--dry-run` — emitir un informe sin modificar archivos
- (opcional) `--skip-verify-done` — solo válido cuando el llamador upstream gestiona verify-done por sí mismo

## Salidas

- Una serie de commits por elemento (`chore(cleanup): remove unused <symbol> (knip)`)
- Un Verification Report final (Output Format — incorpora el evidence block de `ywc-verify-done`)
- Una lista de elementos de nivel DANGER no eliminados (recomendados para un PR separado)

## Skills Relacionadas

- `ywc-verify-done` — handoff obligatorio del Step 7; proporciona el formato de evidence-block PASS / FAIL
- `ywc-tdd-ritual` — objetivo de escalada cuando la consolidación requiere reconciliación de comportamiento
- `ywc-code-gen` — la limpieza que cambia el comportamiento pertenece aquí, no a esta Skill
- `ywc-confidence-gate` — clasificación límite CAUTION ↔ DANGER mediante la rúbrica de 5 dimensiones
- `ywc-onboard-repo` — llamador upstream tras entrar en un nuevo repository
