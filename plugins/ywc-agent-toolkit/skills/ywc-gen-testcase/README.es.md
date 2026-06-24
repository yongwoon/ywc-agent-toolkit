<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Skill Gen Testcase (ywc-gen-testcase)

Esta Skill de Codex toma un PR de GitHub, un directorio de tarea completada, un rango de directorios de tarea, un rango de Git o el diff de git actual y produce una **hoja de pruebas con checkboxes para dos audiencias**: la Sección A para desarrolladores (puerta previa al merge) y la Sección B para QA/Navegador (puerta previa al release). Markdown es el formato de salida predeterminado, y `--format html` produce una hoja de pruebas HTML interactiva para la aprobación en navegador. La ruta de salida predeterminada es el directorio `docs/test-case/` del proyecto.

Los ingenieros de backend y los responsables de QA/PM/Product Owner pueden firmar cada uno su propia sección de forma independiente y en paralelo, de modo que la decisión de merge y la decisión de release queden claramente separadas.

## Uso

### Uso básico

Generar una hoja de pruebas a partir de una URL de PR:

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

Dentro del mismo repositorio, basta con el número de PR:

```text
/ywc-gen-testcase 250
```

### Generación basada en tarea

```text
/ywc-gen-testcase 000001-010-db-create-users-table
```

### Generación por rango de tareas

Cuando ambos extremos parecen prefijos de tarea (por ejemplo, `000012-010..000019-010`), la Skill resuelve la entrada como un rango de tareas inclusivo antes de intentar interpretarla como rango de Git. Ordena lexicográficamente los basenames de los directorios de tarea en `<tasks-dir>` (los prefijos numerados están pensados para ordenarse por ejecución) y lee `task.md` / `README.md` de cada tarea desde el inicio hasta el final como fuentes de escenarios.

```text
/ywc-gen-testcase 000012-010..000019-010 --lang ja
```

> Si falta algún extremo o es ambiguo, la Skill se detiene y pregunta. No hace fallback a `git rev-parse` para extremos con aspecto de tarea.
> Si la tarea inicial aparece después de la tarea final en la lista ordenada, la Skill se detiene y pregunta si se pretendía un rango inverso.
> Cuando una rama / tag / SHA parezca accidentalmente un prefijo de tarea, fuerza el rango de Git con `--range A..B`.

### Generación por rango de Git

Generar a partir de un rango de commits arbitrario. SHA, tag, nombre de rama y `HEAD~N` funcionan todos.

```text
/ywc-gen-testcase v1.2..v1.3
/ywc-gen-testcase HEAD~5..HEAD
/ywc-gen-testcase main..feature-x
/ywc-gen-testcase --range abc1234..def5678
```

> El rango solo admite la forma **de dos puntos `A..B`**. La forma de tres puntos `A...B` se rechaza porque su semántica de merge-base cambia el alcance silenciosamente.
> Si el HEAD del rango forma parte de un PR abierto/mergeado (≥80% de solapamiento de commits), la Skill sugiere automáticamente cambiar al modo PR — el cuerpo del PR / etiquetas / Criterios de Aceptación producen escenarios materialmente mejores.
> Si la calidad de los mensajes de commit es baja (≥70% de encabezados ≤10 caracteres), la Skill advierte antes de continuar.

### Generación basada en diff

```text
/ywc-gen-testcase --from-diff
```

### Opciones

| Opción | Descripción | Ejemplo |
| --- | --- | --- |
| `--output-dir <path>` | Sobreescribir directorio de salida (predeterminado: `docs/test-case/`) | `--output-dir ./qa/manual-tests` |
| `--lang <code>` | Idioma de la hoja de pruebas (`ja`, `ko`, `en`). Predeterminado: detección automática | `--lang ja` |
| `--filename <name>` | Sobreescribir nombre de archivo (sin `.md`) | `--filename release-v2-smoke` |
| `--tasks-dir <path>` | Directorio de tareas usado por entradas de Tarea y Rango de tareas (predeterminado: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--format <fmt>` | Formato de salida (`markdown` \| `html`). Predeterminado: `markdown` | `--format html` |
| `--include-regression` | Añadir una sección de Regresión (B.3) | |
| `--audience <who>` | `dev` \| `qa` \| `both`. Predeterminado: `both` (archivo único, A+B) | `--audience qa` |
| `--split` | Dividir físicamente en `<slug>-dev.md` + `<slug>-qa.md` | |
| `--force-single` | Omitir la sugerencia de división para nivel L; siempre archivo único | |
| `--no-toc` | Suprimir TOC automático para nivel M/L | |
| `--from-diff` | Generar desde `git diff HEAD` | |
| `--range <spec>` | Rango de git explícito (`A..B`). Equivalente al posicional | `--range v1.2..v1.3` |
| `--dry-run` | Mostrar solo el plan de generación (no se escribe ningún archivo) | |

> El identificador de PR, el especificador de tarea, el Rango de tareas (posicional `<task>..<task>`), el Rango de Git (posicional `A..B` o `--range`) y `--from-diff` son mutuamente excluyentes. `--split` y `--force-single` son mutuamente excluyentes. Si se pasan flags incompatibles, la Skill se detiene y pregunta qué modo se pretendía.

## Dos audiencias, dos puertas

El principio de diseño central de la hoja de pruebas es dividir por **"quién lo ejecuta, cuándo, con qué herramientas"**.

| Sección | Audiencia | Herramientas | Puerta |
| --- | --- | --- | --- |
| **A. Verificación del Desarrollador** | Ingeniero de Backend / DB / DevOps | psql, gh CLI, curl, docker | **Pre-merge** — contratos, migraciones, workers, contenedores |
| **B. Verificación QA / Navegador** | QA, PM, Product Owner, diseñador | Chrome + DevTools, UI de administración, origin de prueba | **Pre-release** — experiencia del usuario final y cualquier efecto observable en el navegador |

Dev y QA pueden trabajar en paralelo; cada uno lee solo su propia sección.

## Decisión automática de Nivel

El diseño se elige automáticamente según el número de escenarios, protegiendo a los lectores de paredes de 1000 líneas sin leer.

| Nivel | Escenarios | Diseño |
| --- | --- | --- |
| **S** | ≤ 20 | Archivo único, secciones A+B, sin TOC, sin colapsable |
| **M** | 21–40 | Archivo único, secciones A+B, TOC automático al principio, `<details>` colapsable para Prerrequisitos + Casos extremos |
| **L** | > 40 | Pregunta al usuario: archivo único con TOC / `--split` / división por fase, luego continúa |

La mayoría de los PRs caen naturalmente en el nivel S o M; el prompt del nivel L es una red de seguridad para releases masivos.

## Ciclo de Ejecución

```text
Paso 1: Resolución de entrada
  └─ PR: obtener metadatos y diff vía gh pr view / gh pr diff
  └─ Tarea: cargar task.md / README.md desde <tasks-dir>/<name>/ (preferir completed/)
  └─ Rango de tareas: cargar task.md / README.md de cada tarea incluida
  └─ Diff: capturar git diff HEAD + log de commits recientes

Paso 2: Clasificación de audiencia y superficie
  └─ Etiqueta de audiencia: A (Desarrollador) o B (QA / Navegador)
  └─ Superficie: UI / Base de datos / API / Trabajo en segundo plano / Configuración / Docs
  └─ Efectos observables en el navegador: añadir sección B incluso para PRs solo de backend cuando corresponda

Paso 3: Generación de escenarios
  └─ 2–5 escenarios por par (audiencia, superficie)
  └─ Cada escenario: Objetivo / Precondiciones / Pasos / Esperado / Checkbox
  └─ Prioridad de fuente: cuerpo del PR o Criterios de Aceptación de la Tarea > commits > superficie > casos extremos del diff

Paso 4: Decisión de Nivel
  └─ Contar escenarios y decidir S / M / L
  └─ El nivel L pregunta al usuario cómo proceder antes de escribir

Paso 5: Escribir la hoja de pruebas
  └─ Archivo único (predeterminado) o dividido (--split / --audience)
  └─ El nivel M/L inserta TOC y envuelve Prerrequisitos/Casos extremos en <details>
  └─ Si el destino ya existe, añadir -v<N> (nunca sobreescribir)

Paso 6: Validar e informar
  └─ El archivo existe, conteo de checkboxes, Esperado concreto, anclas de TOC
  └─ Informar resumen de nivel / audiencia / superficie
```

## Regla de nombre de archivo predeterminado

| Entrada | Archivo único (predeterminado) | `--split` |
| --- | --- | --- |
| PR | `pr-<number>-<slug>.md` | `pr-<number>-<slug>-dev.md` + `...-qa.md` |
| Tarea | `task-<phase>-<sequence>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| Rango de tareas | `tasks-<start-prefix>-<end-prefix>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| Rango | `range-<short-start>-<short-end>-<slug>.md` (se usan nombres de tag cuando ambos extremos son tags, p. ej. `range-v1.2-v1.3-<slug>.md`) | `...-dev.md` + `...-qa.md` |
| Diff | `<yyyymmdd-HHMM>-<branch-slug>.md` | `...-dev.md` + `...-qa.md` |

## Estructura de la hoja de pruebas (archivo único predeterminado)

```text
1. Resumen
2. Prerrequisitos
   2.0 Comunes
   2.A Solo para Dev
   2.B Solo para QA
A. Verificación del Desarrollador  [puerta pre-merge]
   A.1 Base de datos / Tabla
   A.2 API
   A.3 Trabajos en segundo plano / Workers
   A.4 Configuración
   A.5 Casos extremos de Dev
   A.6 Firma del Dev
B. Verificación QA / Navegador  [puerta pre-release]
   B.1 Escenarios de UI / Navegador
   B.2 Casos extremos visibles para el usuario
   B.3 Regresión (con --include-regression)
   B.4 Firma del QA
Apéndice (opcional)
```

El front matter YAML contiene `dev_tester` / `dev_status` / `qa_tester` / `qa_status` como puertas independientes.

Cada escenario debe incluir un **resultado Esperado concreto**. Las formulaciones vagas como "verificar que funciona" están prohibidas.

## Pautas de gestión de longitud

Principios integrados para prevenir el exceso:

1. **Prerrequisitos: prefijo común + sufijo de audiencia** — sin duplicación
2. **Extraer material de verificación de más de 20 líneas** a `scripts/qa/*.sql` (o similar); referenciar solo la ruta
3. **Regresión por referencia** — enlazar a hojas de pruebas anteriores en lugar de duplicar
4. **Solución de problemas larga / ejemplos de payload → `## Apéndice`**, enlazado desde el escenario relevante

Aplicado de forma consistente, la mayoría de las hojas de pruebas de nivel M se mantienen por debajo de ~800 líneas.

## Detección de idioma

Prioridad cuando no se especifica `--lang`:

1. **CLAUDE.md / AGENTS.md** — directivas como `PR言語: 日本語`, `Documentation: Korean`
2. **Hojas de pruebas recientes** en `docs/test-case/`
3. Idioma del **`README.md` del proyecto**
4. **Fallback** — inglés

Las claves del front matter YAML, los números de sección y el andamiaje de la plantilla permanecen en inglés independientemente de `--lang`.

## Manejo de errores

| Situación | Comportamiento |
| --- | --- |
| No se proporciona entrada | Detenerse; solicitar PR / tarea / `--from-diff` |
| Se proporcionan múltiples entradas | Detenerse; preguntar qué modo |
| `--split` + `--force-single` ambos activos | Detenerse; preguntar cuál se pretende |
| `gh` no autenticado (entrada de PR) | Pedir al usuario que ejecute `gh auth login`; detenerse |
| PR no encontrado | Informar el número de PR; detenerse |
| Tarea no encontrada | Listar tareas similares (coincidencia difusa); detenerse |
| Diff vacío (entrada de diff) | Informar "nada que probar"; detenerse |
| Directorio de salida no escribible | Informar la ruta fallida; detenerse (sin fallback silencioso) |
| El archivo destino ya existe | Añadir sufijo `-v<N>` |
| Nivel L detectado sin `--split`/`--force-single` | Detenerse y preguntar al usuario cómo proceder |

## Integración

Descendiente de las Skills `ywc` orientadas a la implementación:

- **ywc-sequential-executor** — genera el PR/Tarea a probar (upstream)
- **ywc-parallel-executor** — igual, para ejecución en paralelo (upstream)
- **ywc-merge-dependabot** — bumps de dependencias mergeados que necesitan una hoja de pruebas de smoke (upstream)

## Ejemplos de prompts

### Generar desde una URL de PR (predeterminado: archivo único A+B)

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

### División física en dos archivos

```text
/ywc-gen-testcase 250 --split --lang ja
```

### Hoja de pruebas solo para QA (para entregar al equipo de QA)

```text
/ywc-gen-testcase 250 --audience qa --lang ja
```

### Forzar archivo único incluso para un PR grande

```text
/ywc-gen-testcase 250 --force-single
```

### Basado en tarea con sección de regresión

```text
/ywc-gen-testcase 000001-010-db-create-users-table --include-regression
```

### Rango de tareas (inclusivo, desde la tarea inicial hasta la final)

```text
/ywc-gen-testcase 000012-010..000019-010 --lang ja
```

### Rango de Git (entre dos tags)

```text
/ywc-gen-testcase v1.2..v1.3 --lang ja
```

### Rango local pre-PR

```text
/ywc-gen-testcase HEAD~5..HEAD
```

### Dry-run

```text
/ywc-gen-testcase 250 --dry-run
```

## Activación

Las condiciones de activación para esta Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).
