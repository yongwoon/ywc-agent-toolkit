<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-spec-writer

Redactor de especificaciones de proyecto. Crea y mantiene el directorio `docs/specification/` con documentación Markdown legible por humanos. Escrito tanto para desarrolladores como para no desarrolladores — sin código de programa, solo objetivos, funcionalidades, datos, flujos de usuario y requisitos no funcionales.

## Casos de Uso

- **Nuevo proyecto**: Escribir la especificación completa inicial cuando no existe ninguna
- **Actualización basada en tarea**: Reflejar un documento de tarea individual de `ywc-task-generator` en la especificación
- **Actualización de rango / múltiples tareas**: Reflejar varias tareas (rango, glob o multi-id) en un solo paso
- **Actualización basada en PR**: Actualizar la especificación desde uno o más PR diffs junto con el contexto narrativo del PR
- **Sincronización post-commit**: Sincronizar la especificación después de cambios en el código
- **Actualización completa**: Regenerar toda la especificación desde el codebase actual

## Uso

```bash
/ywc-spec-writer                          # Modo automático (actualización basada en commit)
/ywc-spec-writer --full                   # Generación completa de especificación (requiere confirmación)
/ywc-spec-writer --update                 # Regenerar todas las secciones
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-tasks 000002-010..000003-020   # Rango de tareas (puede cruzar fases)
/ywc-spec-writer --from-tasks 000002-* 000003-010      # Glob + ID individual mixto
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --from-pr 42                          # PR individual
/ywc-spec-writer --from-prs 42 43 51                   # Múltiples PRs (union diff)
/ywc-spec-writer --setup-hook             # Instalar git hook
/ywc-spec-writer --lang ja                # Escribir en japonés
```

## Entradas

- (opcional) `--full` / `--update` — generación completa o actualización
- (opcional) `--from-task <path>` — ruta del directorio de tarea individual
- (opcional) `--from-tasks <id-or-pattern> ...` — rango de tareas / glob / multi-ID (busca en active + completed)
- (opcional) `--from-commit <ref>` — referencia de commit (por defecto: `HEAD`)
- (opcional) `--from-pr <num>` — PR individual (requiere gh CLI)
- (opcional) `--from-prs <num> ...` — union diff de múltiples PRs (archivos duplicados auto-deduplicados)
- (opcional) `--lang ko|ja|en` — idioma de salida (por defecto: `ko`)
- (opcional) `--setup-hook` — instalar git pre-commit hook

> `--from-pr` / `--from-prs` requieren que la CLI `gh` esté instalada y autenticada. El título / cuerpo / `headRefOid` del PR se registran como contexto narrativo y audit trail al actualizar la especificación.

## Salida

```
docs/specification/
├── README.md              # Índice + registro de cambios
├── 01-overview.md         # Descripción general del proyecto
├── 02-features.md         # Requisitos de funcionalidades (formato de historia de usuario)
├── 03-data.md             # Modelo de datos
├── 04-interfaces.md       # Interfaces externas
├── 05-user-flows.md       # Flujos de usuario
├── 06-requirements.md     # Requisitos no funcionales
└── 07-glossary.md         # Glosario
```

## Habilidades Relacionadas

- `ywc-plan` — produce especificaciones de funcionalidades que alimentan esta habilidad
- `ywc-spec-validate` — valida la especificación escrita
- `ywc-task-generator` — descompone la especificación revisada en tareas
- `ywc-ubiquitous-language` — alinea el vocabulario de la especificación con los términos del dominio
