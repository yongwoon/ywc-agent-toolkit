<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-incident-postmortem

Un skill para redactar post-mortems de incidentes estructurados tras un incidente en producción.
Cubre reconstrucción de cronología, análisis de causa raíz (5 Porqués), evaluación de impacto,
elementos de acción de prevención y, opcionalmente, un informe sanitizado para clientes.

## Cuándo usar

| Situación | Ejemplos |
|-----------|---------|
| Interrupción del servicio | Fallo de conexión a DB, servidor caído tras despliegue, interrupción de CDN |
| Incidente de seguridad | Exposición de clave API, bypass de autenticación, acceso sospechoso |
| Pérdida o corrupción de datos | Migración fallida, eliminación accidental |
| Errores de pago | Cargo duplicado, bucle de fallo de pago |
| Degradación repentina del rendimiento | Pico de tiempo de respuesta tras despliegue |

## Uso

```
/ywc-incident-postmortem             # Modo borrador interactivo (por defecto)
/ywc-incident-postmortem --template  # Generar una plantilla en blanco para rellenar
/ywc-incident-postmortem --client    # También generar un informe sanitizado para clientes
```

## Salida

- **Post-mortem interno** — Documento técnico completo: cronología, 5 Porqués, elementos de acción
- **Informe para clientes** (con `--client`) — Resumen del impacto en el usuario sin detalles internos

## Skills relacionados

- `ywc-security-audit` — Auditoría de seguridad proactiva *antes* de los incidentes
- `ywc-impl-review` — Revisión general de calidad de código
- `ywc-changelog-release-notes` — Documentar cambios tras un lanzamiento de parche
