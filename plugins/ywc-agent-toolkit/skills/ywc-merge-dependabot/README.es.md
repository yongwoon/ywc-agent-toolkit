<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# Habilidad de Fusión de Dependabot (Codex)

## Descripción general

Esta habilidad fusiona de forma segura lotes de solicitudes de extracción creadas por Dependabot.
Se puede utilizar tanto desde Claude Code como desde la CLI de Codex.

## Características

- Fusionar todas las solicitudes de extracción de Dependabot o solo las relacionadas con seguridad
- Ejecutar comprobaciones de seguridad previas a la fusión para cambios de `FROM` en Dockerfile, actualizaciones de versión principal y estado de CI
- Resolver conflictos de fusión solo a través de `@dependabot rebase` (nunca manualmente), esperar a que se ejecute el CI de la cabeza rebasada e fusionar fijando a la cabeza verificada (`--match-head-commit`)
- Procesar solicitudes de extracción secuencialmente por número de solicitud ascendente de forma predeterminada
- **Modo de auto-fusión paralelo**: agrupar solicitudes de extracción en carriles de ecosistema de archivos de bloqueo y mantener una solicitud de extracción de auto-fusión activa por carril para reducir el tiempo total para lotes grandes; cada inicio de auto-fusión primero confirma que la rama base de la solicitud de extracción tiene una comprobación de estado requerida, y las solicitudes de extracción no confirmadas van a la pasada secuencial final
- Emitir un informe de resumen final

## Uso

### Claude Code

```text
/ywc-merge-dependabot                          # todas las solicitudes de extracción, secuencial
/ywc-merge-dependabot security                 # solo solicitudes de extracción de seguridad, secuencial
/ywc-merge-dependabot parallel-auto            # todas las solicitudes de extracción, auto-fusión de carril de ecosistema
/ywc-merge-dependabot security parallel-auto   # solo solicitudes de extracción de seguridad, auto-fusión de carril de ecosistema
```

### CLI de Codex

```text
Usar $ywc-merge-dependabot para fusionar todas las solicitudes de extracción abiertas de Dependabot.
Usar $ywc-merge-dependabot security para fusionar solo las solicitudes de extracción de Dependabot relacionadas con seguridad.
Usar $ywc-merge-dependabot parallel-auto para fusionar un lote grande mediante programación de auto-fusión de carril de ecosistema.
Usar $ywc-merge-dependabot security parallel-auto para combinar el alcance de seguridad con el indicador de ejecución paralelo-automático.
```

## Requisitos previos

- GitHub CLI (`gh`) instalada y autenticada
- Permiso de fusión para el repositorio de destino
- Para `parallel-auto`: "Permitir auto-fusión" habilitada en el repositorio. Si está deshabilitada, la habilidad vuelve al modo secuencial.

## Modos

Esta habilidad admite dos indicadores ortogonales.

**Indicador de alcance** — solicitudes de extracción de destino:

| Token | Alcance |
| --- | --- |
| `security` | Solo solicitudes de extracción de Dependabot relacionadas con seguridad |
| _(ninguno)_ | Todas las solicitudes de extracción de Dependabot |

**Indicador de ejecución** — estrategia de procesamiento:

| Token | Ejecución | Cuándo usar |
| --- | --- | --- |
| `parallel-auto` | Carriles de ecosistema + una solicitud de extracción de auto-fusión activa por carril | Cinco o más solicitudes de extracción distribuidas entre múltiples ecosistemas |
| _(ninguno)_ | Secuencial por número de solicitud ascendente | Lotes pequeños o entornos de protección de rama estricta |

## Condiciones de omisión

| Condición | Razón |
| --- | --- |
| Cambio de `FROM` en Dockerfile | Los cambios de imagen base de contenedor necesitan revisión manual |
| Actualización de versión principal | Riesgo de cambio importante |
| CI no pasando | Previene fusionar compilaciones/pruebas fallidas |

## Formato de resultado

```text
Mode: parallel-auto (security)
Ecosystem groups processed: npm (3), github-actions (2), python (2)

- Merged    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- Skipped   (Major version upgrade) : #130 Bump webpack from 4.x to 5.x
- Failed    (lane stalled)   : #132 Bump express from 4.18.0 to 4.19.2 - CONFLICTING after 30 min
```

El modo secuencial aún imprime la línea `Mode`, pero omite el encabezado `Ecosystem groups` y las anotaciones de ecosistema por solicitud de extracción.

## Estructura de archivos

```text
ywc-merge-dependabot/
├── README.md
├── README.en.md / README.ja.md / README.ko.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    ├── group-by-ecosystem.py
    ├── check-base-required-checks.sh
    └── test_merge_dependabot_scripts.py
```

## Habilidades relacionadas

- [ywc-create-pr](../ywc-create-pr/SKILL.md) — crear solicitudes de extracción
- [ywc-handle-pr-reviews](../ywc-handle-pr-reviews/SKILL.md) — manejar comentarios de revisión de solicitudes de extracción
- [ywc-release-pr-list](../ywc-release-pr-list/SKILL.md) — generar listas de solicitudes de extracción de lanzamiento

## Seguridad operativa

Detectar instrucciones `FROM` cambiadas solo en hunks de diferencia de Dockerfile; los fallos de consulta/analizador permanecen sin resolver. La rebase/sondeo de CI preserva un plazo de 1800 segundos único en toda la ejecución y estado completo entre fragmentos; el agotamiento del tiempo es un error. La invocación explícita es metadatos preferidos, no cumplimiento en tiempo de ejecución.
