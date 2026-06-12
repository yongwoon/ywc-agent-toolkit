<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-changelog-release-notes

Una skill para generar entradas de CHANGELOG.md y notas de versión orientadas al usuario
a partir del historial de git, PRs fusionados o la salida de ywc-release-pr-list.
Produce tanto un CHANGELOG técnico (formato Keep a Changelog) como un
resumen de versión en lenguaje simple orientado al usuario, como documentos separados.

## Concepto central: dos salidas distintas

Esta skill produce **dos documentos con propósitos diferentes**.

| | CHANGELOG.md | Notas de versión |
|---|---|---|
| Audiencia | Desarrolladores, mantenedores | Usuarios finales, clientes |
| Incluye | Todos los cambios, CVEs, números de PR | Solo cambios visibles para el usuario |
| Tono | Técnico, conciso | Lenguaje simple, orientado a beneficios |
| refactor/chore | Incluido | Omitido |

## Escenarios de uso

### Caso 1: Antes de etiquetar una nueva versión (el más común)

```
/ywc-changelog-release-notes --both --version 1.2.0
```

Genera tanto una entrada de CHANGELOG.md orientada al desarrollador como un documento de Notas de versión orientado al usuario en un solo paso.
Úsalo cuando necesitas contenido para la página de GitHub Release.

### Caso 2: Actualizar solo CHANGELOG.md

```
/ywc-changelog-release-notes --changelog
```

Usa esto para proyectos internos sin usuarios externos, donde solo se necesita un historial de cambios orientado al desarrollador.
Ejecútalo antes de crear un `git tag`.

### Caso 3: Escribir un anuncio para clientes o una publicación en Slack

```
/ywc-changelog-release-notes --release
```

Úsalo cuando escribes anuncios orientados al usuario como "v1.3.0 ya está disponible."
Los detalles técnicos se filtran automáticamente y se reformulan desde la perspectiva del usuario.

### Caso 4: Vista previa antes de modificar archivos

```
/ywc-changelog-release-notes --dry-run
```

Úsalo para ver qué se escribiría en `CHANGELOG.md` antes de modificar el archivo realmente.
Revisa la salida y vuelve a ejecutar sin `--dry-run` si parece correcto.

### Caso 5: Combinación con `ywc-release-pr-list`

Cuando ya se ha preparado una lista de PRs, proporciónala como entrada a esta skill.

```
/ywc-release-pr-list > pr-list.md
/ywc-changelog-release-notes --both --pr-list pr-list.md --version 1.2.0
```

`ywc-release-pr-list` lista los PRs en una tabla; esta skill los **formatea** como entradas de CHANGELOG legibles y categorizadas.

## Todas las banderas

```
/ywc-changelog-release-notes --changelog              # Solo entrada de CHANGELOG.md
/ywc-changelog-release-notes --release                # Solo notas de versión orientadas al usuario
/ywc-changelog-release-notes --both --version 1.2.0  # Generar ambos documentos
/ywc-changelog-release-notes --from v1.1.0 --to HEAD # Rango específico
/ywc-changelog-release-notes --dry-run               # Imprimir en stdout, sin cambios en archivos
```

## Flujo típico de versión

```
1. ywc-release-pr-list          → Compilar la lista de PRs para esta versión
2. ywc-changelog-release-notes  → Generar CHANGELOG + Notas de versión
3. ywc-commit                   → Confirmar el CHANGELOG.md actualizado
4. ywc-create-pr                → Crear el PR de versión
5. git tag -a v1.2.0 -m "..."   → Etiquetar la versión (la skill sugiere el comando)
```

## Skills relacionadas

- `ywc-release-pr-list` — Generar la lista de PRs para alimentar `--pr-list`
- `ywc-commit` — Confirmar el CHANGELOG.md actualizado
- `ywc-create-pr` — Crear el PR de versión
- `ywc-incident-postmortem` — Análisis post-incidente que motivó una versión de parche
