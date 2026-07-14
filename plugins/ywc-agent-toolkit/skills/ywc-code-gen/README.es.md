<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-code-gen

Una Skill para generar código en múltiples capas simultáneamente. Ejecuta los Agentes de Backend, Frontend y QA en paralelo.

## Uso

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
```

## Agentes de ejecución

| Agente                   | Salida                                     |
| ----------------------- | ------------------------------------------ |
| Agente Backend (sonnet)  | Ruta de API, Servicio, Migración de BD           |
| Agente Frontend (sonnet) | Componente UI, Query Hook, Gestión de Estado |
| Agente QA (sonnet)       | Test Unitario, Test de Integración, Escenario E2E  |

## Contrato y baseline TDD

Antes de ejecutar los workers, la Skill prepara un Contract Snapshot compartido para que Backend, Frontend y QA usen los mismos public contracts. La generación que cambia comportamiento es test-first por defecto; `--tdd` habilita checkpoint commits RED/GREEN/REFACTOR más estrictos.

## Revisión de implementación opcional

Usa `--review` para ejecutar `ywc-impl-review` después de que la generación supere la verificación y el Confidence Gate. Revisa cambios generados staged, unstaged, untracked y eliminados sin crear un commit exclusivo de revisión (con `--tdd`, que hace commit en cada checkpoint y deja el working tree limpio, el objetivo de revisión pasa a ser `--git-range <pre-generation-sha>..HEAD`). El working tree debe estar limpio al empezar; los hallazgos Critical/High reciben una pasada de corrección y nueva revisión, y las preocupaciones no resueltas quedan en el resultado.

**Incluso sin `--review`**, si los archivos generados caen en un critical path (auth, payment, crypto, PII, external input) se fuerzan tanto `ywc-impl-review` como `ywc-security-audit` (el mismo contrato que aplica `ywc-sequential-executor`). Los hallazgos Critical/High de **ambas** revisiones entran en el único fix cycle acotado, y un `BLOCKED` o `NEEDS_CONTEXT` de cualquiera de las dos se propaga en lugar de reportar éxito. Como este Skill no hace merge, el gate es advisory, no blocking: los hallazgos que sobreviven degradan el estado a `DONE_WITH_CONCERNS`, no descartan el código generado.

## Relación con sequential-executor

- **sequential-executor**: Ejecución secuencial (adecuado para tareas con dependencias)
- **/ywc-code-gen**: Generación paralela de capas independientes (cuando se necesitan SDK/API/Web simultáneamente)
- Se usan de forma complementaria

## Activación

Las condiciones de activación de esta Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones localizadas

- [Inglés](./README.en.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
