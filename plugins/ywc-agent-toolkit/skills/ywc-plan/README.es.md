<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-plan

Un Skill de planificación previa a la implementación que convierte una idea aproximada en uno de dos artefactos listos para ejecutar: un plan de ejecución directa de ruta Small, o un documento de especificación de ruta Medium/Large. Evalúa automáticamente la escala y enruta al Skill downstream correcto.

## Casos de uso

- Cuando el usuario dice "Haz un plan para esta funcionalidad"
- Cuando no hay Spec o tarea aún y el usuario no sabe por dónde empezar
- Cuando no está claro si el cambio es una edición Small de un solo paso o justifica una Spec completa
- Cuando se prepara la Spec de entrada que consumirá `ywc-task-generator`

## Uso

```bash
/ywc-plan "<solicitud aproximada>"
```

O invocar de forma natural:

> "Quiero añadir preferencias de notificación a la página de perfil — haz un plan."

## Entrada

- Una solicitud de cambio en lenguaje natural (idea aproximada, solicitud de funcionalidad, descripción del cambio)

## Salida

Dependiendo de la escala, uno de:

| Escala | Salida |
|---|---|
| Small | `./plan.md` — un plan de un solo PR directamente ejecutable |
| Medium / Large | `docs/ywc-plans/<slug>.md` — un documento Spec que consumirá `ywc-spec-ready` o el flujo manual `ywc-spec-validate` -> `ywc-task-generator` |

Cada ruta emite un mensaje de traspaso explícito nombrando el siguiente Skill.

## Flujo

1. **Clarificar** — Preguntar al usuario una vez por los cuatro anclajes: Qué / Por qué / Fuera de Alcance / Cuándo está Listo
2. **Investigar** — Leer solo los archivos esenciales: `CLAUDE.md`, `package.json`, `docs/architecture/`, etc.
3. **Evaluar Escala** — Elegir exactamente uno de Small / Medium / Large (por defecto Medium cuando es ambiguo)
4. **Ramificar** — Small escribe `plan.md`; Medium/Large escribe un documento Spec
5. **Traspaso** — Imprimir el atajo de convergencia automática `ywc-spec-ready` o los siguientes Skills manuales (la ejecución es decisión del usuario, no de este Skill)

## Invariantes de seguridad

Cualquiera de los siguientes escala automáticamente a Medium o superior:

- Migración de base de datos / cambio de esquema
- Introducción de nueva biblioteca / framework
- Nuevo contrato de API expuesto a consumidores externos
- Lógica de autenticación / autorización tocada
- Cambio transversal en 2+ módulos

## Skills relacionados

- `ywc-tech-research` — Ejecutar antes de `ywc-plan` cuando la elección de tecnología no está establecida
- `ywc-product-review` — Ejecutar antes de `ywc-plan` cuando el marco de producto/negocio no está claro
- `ywc-spec-ready` — Atajo aprobado por el usuario para converger validate -> DONE en la ruta Medium/Large
- `ywc-spec-validate` — Siguiente paso en la ruta Medium/Large
- `ywc-task-generator` — Descompone la Spec en tareas después de que pase la revisión
- `ywc-code-gen` — Opción de ejecución directa para la ruta Small
- `ywc-sequential-executor` / `ywc-parallel-executor` — Ejecutan las tareas generadas

## Activación

Las condiciones de activación están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones localizadas

- [Coreano (por defecto)](./README.md)
- [Japonés](./README.ja.md)
