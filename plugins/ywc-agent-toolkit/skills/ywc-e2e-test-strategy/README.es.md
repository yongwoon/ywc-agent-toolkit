<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-e2e-test-strategy

Un skill para diseñar e implementar una estrategia de pruebas E2E automatizadas usando Playwright. Gestiona la configuración inicial de Playwright en nuevos proyectos, análisis de brechas de cobertura en proyectos existentes, generación de pruebas para flujos de usuario individuales e integración de CI en GitHub Actions.

## Escenarios de uso

- **Nuevo proyecto**: "Configurar Playwright", "Añadir pruebas E2E por primera vez"
- **Auditoría de proyecto existente**: "Encontrar cobertura faltante en rutas críticas", "Verificar brechas E2E"
- **Flujo único**: "Escribir una prueba Playwright para el flujo de login", "Generar una prueba E2E de checkout"
- **Integración CI**: "Conectar Playwright con GitHub Actions"

## Uso

```bash
/ywc-e2e-test-strategy --init           # Configurar Playwright desde cero
/ywc-e2e-test-strategy --audit          # Auditar cobertura E2E existente
/ywc-e2e-test-strategy --flow login     # Generar prueba para un flujo específico
/ywc-e2e-test-strategy --init --ci      # Init + flujo de trabajo de GitHub Actions
```

O invocar con lenguaje natural:

> "Diseñar una estrategia de pruebas E2E con Playwright"
> "Automatizar las rutas de usuario críticas"
> "Auditar mi cobertura E2E"

## Modos

| Modo | Flag | Cuándo usar |
|------|------|-------------|
| Init | `--init` | No se encuentra `playwright.config.*` |
| Audit | `--audit` | Pruebas E2E existentes presentes |
| Flow | `--flow <name>` | Añadir una sola prueba de flujo de usuario |

Sin un flag, el skill detecta automáticamente el modo desde el sistema de archivos.

## Salida

- `playwright.config.ts` — configuración de baseURL basada en variables de entorno
- `e2e/*.spec.ts` — archivos de prueba por ruta crítica
- `.github/workflows/e2e.yml` — flujo de trabajo de CI (`--ci` o `--init`)
- Reporte de auditoría — análisis de brechas de cobertura y riesgo de pruebas inestables

## Skills relacionados

- `ywc-gen-testcase` — hojas de prueba de verificación manual (verificadas por humanos, no automatizadas)
- `ywc-impl-review` — revisión de implementación a nivel de código
- `ywc-security-audit` — auditoría de seguridad para flujos de autenticación y manejo de entrada
