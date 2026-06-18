<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-code-gen

Una Skill para generar código en múltiples capas simultáneamente. Ejecuta los Agentes de Backend, Frontend y QA en paralelo.

## Uso

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
```

## Agentes de ejecución

| Agente                   | Salida                                     |
| ----------------------- | ------------------------------------------ |
| Agente Backend (sonnet)  | Ruta de API, Servicio, Migración de BD           |
| Agente Frontend (sonnet) | Componente UI, Query Hook, Gestión de Estado |
| Agente QA (sonnet)       | Test Unitario, Test de Integración, Escenario E2E  |

## Contrato y baseline TDD

Antes de ejecutar los workers, la Skill prepara un Contract Snapshot compartido para que Backend, Frontend y QA usen los mismos public contracts. La generación que cambia comportamiento es test-first por defecto; `--tdd` habilita checkpoint commits RED/GREEN/REFACTOR más estrictos.

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
