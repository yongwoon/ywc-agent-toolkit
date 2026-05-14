<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-spec-writer

Redactor de especificaciones de proyecto. Crea y mantiene el directorio `docs/specification/` con documentación Markdown legible por humanos. Escrito tanto para desarrolladores como para no desarrolladores — sin código de programa, solo objetivos, funcionalidades, datos, flujos de usuario y requisitos no funcionales.

## Casos de Uso

- **Nuevo proyecto**: Escribir la especificación completa inicial cuando no existe ninguna
- **Actualización basada en tarea**: Reflejar un documento de tarea de `ywc-task-generator` en la especificación
- **Sincronización post-commit**: Sincronizar la especificación después de cambios en el código
- **Actualización completa**: Regenerar toda la especificación desde el codebase actual

## Uso

```bash
/ywc-spec-writer                          # Modo automático (actualización basada en commit)
/ywc-spec-writer --full                   # Generación completa de especificación (requiere confirmación)
/ywc-spec-writer --update                 # Regenerar todas las secciones
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --setup-hook             # Instalar git hook
/ywc-spec-writer --lang ja                # Escribir en japonés
```

## Entradas

- (opcional) `--full` / `--update` — generación completa o actualización
- (opcional) `--from-task <path>` — ruta del directorio de tarea
- (opcional) `--from-commit <ref>` — referencia de commit (por defecto: `HEAD`)
- (opcional) `--lang ko|ja|en` — idioma de salida (por defecto: `ko`)
- (opcional) `--setup-hook` — instalar git pre-commit hook

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
