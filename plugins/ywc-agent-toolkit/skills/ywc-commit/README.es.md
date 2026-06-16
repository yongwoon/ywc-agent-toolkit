<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Skill de Commit (ywc-commit)

Un Skill de Codex que realiza staging, commits y, opcionalmente, push de los cambios de la sesión actual de forma segura.

## Descripción general

Este Skill gestiona automáticamente lo siguiente:

- Selecciona solo los archivos relevantes de la sesión para el staging
- Divide los cambios lógicamente distintos en commits separados
- Aprende el estilo de commits del proyecto (`type/scope/message`) desde `git log` y lo aplica de forma consistente
- Genera un resumen conciso de todos los commits creados

## Uso

Solicitar en lenguaje natural o con un slash command:

```text
/ywc-commit
```

```text
commit and push
```

```text
commit only the authentication-related files
```

Las frases en coreano también son reconocidas: `커밋 해줘`, `커밋푸쉬 ㄱㄱ`, `지금까지 한 작업 커밋`.

## Reglas principales

| Regla | Detalle |
| --- | --- |
| Solo hacer staging de archivos relevantes a la sesión | Solo archivos creados, modificados o discutidos en esta conversación |
| Dividir commits por unidad lógica | Un commit = un propósito |
| Push solo cuando se solicita explícitamente | Activado por "push", "푸쉬", "올려줘" o equivalente |
| `--no-verify` está prohibido | Corregir fallos del hook o reportarlos — nunca omitirlos |
| `git add .` está prohibido | Siempre hacer staging de archivos por ruta explícita |
| Confirmar antes de hacer commit en main/master | Casi siempre es un error — preguntar primero |
| Excluir secretos y artefactos de build | Omitir `.env*`, `dist/`, `build/` a menos que se hayan añadido intencionalmente |
| Sin trailer de co-autor específico de herramienta por defecto | Incluirlo solo cuando la convención del repositorio o el usuario lo solicite explícitamente |

## Flujo de trabajo

```text
Paso 1: Evaluar el estado actual
  └─ git status, git diff, git log (aprender estilo), verificar rama

Paso 2: Clasificar archivos modificados
  └─ IN (relevante a la sesión) / UNKNOWN (origen poco claro) / OUT (no relacionado)
  └─ Mostrar tabla de clasificación al usuario y obtener aprobación si se encuentran archivos UNKNOWN/OUT

Paso 3: Dividir en commits lógicos
  └─ Planificar commits separados para cambios lógicamente distintos
  └─ Usar git add -p para staging a nivel de hunk cuando sea necesario
  └─ Mostrar commits planificados (archivos + mensajes borrador) al usuario para aprobación

Paso 4: Escribir mensajes de commit
  └─ Aprender el estilo del proyecto desde git log y aplicarlo exactamente
  └─ Incluir un trailer de co-autor solo cuando la convención del repositorio o el usuario lo solicite

Paso 5: Staging y Commit
  └─ Hacer staging por ruta explícita → verificar diff → commit con heredoc

Paso 6: Verificar resultado
  └─ Verificar git log y git status para commits faltantes o cambios inesperados

Paso 7: Push (solo cuando se solicita)
  └─ Push por defecto; usar flag -u si no hay upstream configurado
  └─ Force-push solo cuando se solicita explícitamente
```

## Formato del mensaje de commit

Coincide con el estilo existente de `git log` del proyecto. Formato general:

```text
<type>(<scope>): <summary>

<body — solo cuando sea necesario>
```

**Tipos comunes** (usar solo los que ya usa este repositorio):
`feat`, `fix`, `refactor`, `perf`, `chore`, `docs`, `test`

**Scope**: derivado de los patrones de `git log` (nombre del paquete, nombre del módulo, etc.). Omitir cuando el cambio abarca múltiples áreas.

No añadir un trailer `Co-Authored-By` por defecto. Añadirlo solo cuando el historial de commits reciente usa consistentemente un trailer de co-autor de IA o el usuario lo solicita explícitamente. Si no hay convención en el repositorio y el usuario pide uno, usar `Co-Authored-By: Claude <noreply@anthropic.com>`.

## Formato del reporte

Después de que todos los commits estén completados:

```text
✅ N commit(s) creado(s) [+ pushed]
  1. <hash> <type>(<scope>): <summary>
  2. <hash> <type>(<scope>): <summary>
Archivos excluidos: <lista si hay alguno, omitir si no>
```

## Manejo de errores

| Situación | Comportamiento |
| --- | --- |
| Archivo UNKNOWN encontrado | Mostrar tabla de clasificación al usuario y esperar aprobación |
| Fallo del hook | Nunca usar `--no-verify`; reportar causa raíz y detener |
| Commit directo a main/master | Pedir confirmación al usuario primero |
| Push rechazado por non-fast-forward | Explicar la situación y presentar opciones; force-push solo con solicitud explícita |
| Archivo secreto o artefacto encontrado | Informar al usuario y excluir del commit |

## Integración

Este Skill se usa junto con:

- **ywc-create-pr** — invocado internamente en el Paso 3 cuando los cambios sin commit deben ser confirmados antes de crear el PR
- **ywc-sequential-executor** — puede ser referenciado durante el paso de commit de la ejecución de tareas

## Prompts de ejemplo

```text
/ywc-commit
commit and push
commit only the authentication-related files
```
