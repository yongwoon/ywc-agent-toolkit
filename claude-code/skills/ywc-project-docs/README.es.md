<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# project-docs

Una Skill de Claude Code para generar documentación en coreano o japonés que sigue
la estructura de directorios y las convenciones del directorio `docs/` del proyecto.

El idioma objetivo nunca se detecta automáticamente. Si se proporciona `--lang kr|ja` se
usa directamente; de lo contrario, la Skill pregunta qué idioma (coreano / japonés) antes
de escribir nada.

## Uso

### Activación automática

La Skill se activa con frases en lenguaje natural como:

```
"문서 작성해줘"       (Coreano: escribe un documento)
"문서 만들어줘"       (Coreano: crea un documento)
"document this"
"write a doc"
"add to docs/"
"ドキュメント作成して" (Japonés: crea un documento)
"ドキュメントを書いて" (Japonés: escribe un documento)
```

### Invocación manual

```
/ywc-project-docs              # muestra el prompt de selección de idioma
/ywc-project-docs --lang kr    # escribe en coreano directamente
/ywc-project-docs --lang ja    # escribe en japonés directamente
```

## Qué Hace Esta Skill

1. **Selección de idioma** — usa `--lang` si está presente, de lo contrario pregunta coreano / japonés (nunca auto-detecta)
2. **Enrutamiento de directorios** — coloca los documentos en el subdirectorio correcto de `docs/` según la intención
3. **Convenciones de nomenclatura** — aplica kebab-case en minúsculas con sufijos mínimos
4. **Estructura del documento** — genera bloques de documentos relacionados, tabla de contenidos y secciones numeradas
5. **Referencias cruzadas** — agrega enlaces bidireccionales entre documentos relacionados
6. **Política de idioma** — el cuerpo del texto en el idioma seleccionado; los términos técnicos se mantienen en inglés (sin transliteración)
7. **Orden de lectura** — preserva `product → architecture → specification → plans` para el consumo de LLM
8. **Antipatrones** — previene la mezcla de límites de carpetas, el almacenamiento duplicado y la confusión entre borradores y documentos oficiales

## Mapeo de Directorios

### Eje principal (documentos principales)

| Tipo de Solicitud | Directorio Objetivo |
|---|---|
| Objetivos del producto, alcance, PRD | `docs/product/` |
| Diseño del sistema, decisiones técnicas | `docs/architecture/` |
| Reglas de funciones, criterios de implementación | `docs/specification/` |
| Orden de implementación, hitos | `docs/plans/` |

### Eje secundario (operaciones, recursos, borradores)

| Tipo de Solicitud | Directorio Objetivo |
|---|---|
| Procedimientos operativos, guías de configuración | `docs/manuals/` |
| Gestión de incidentes, problemas conocidos | `docs/troubleshooting/` |
| Maquetas de UI, recursos de diseño | `docs/design/` |
| Imágenes de soporte | `docs/imgs/` |
| Ideas no confirmadas, notas temporales | `docs/todo/` |

## Ejemplos

```
"제품 개요 문서 작성해줘"
→ docs/product/product-overview.md (Coreano)

"인증 시스템 아키텍처 문서 작성해줘"
→ docs/architecture/authentication.md (Coreano)

"認証システムのアーキテクチャドキュメントを書いて"
→ docs/architecture/authentication.md (Japonés)
```

## Versiones Localizadas

- [Coreano (Principal)](./README.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
