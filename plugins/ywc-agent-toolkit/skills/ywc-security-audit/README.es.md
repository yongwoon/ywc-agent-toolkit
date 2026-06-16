<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Spanish -->

# ywc-security-audit

Una Skill de Agente de Seguridad para realizar auditorías de seguridad cuando hay cambios en código relacionado con autenticación, pagos o datos personales, o para revisiones de seguridad periódicas.

## Uso

```text
/ywc-security-audit --code api/src/middleware/
```

## Checklist de Auditoría (OWASP Top 10)

1. Inyección (SQL, Command, LDAP)
2. Autenticación Rota (Token, Sesión)
3. Exposición de Datos Sensibles
4. XSS (Reflejado, Almacenado, DOM)
5. Control de Acceso Roto
6. Configuración Incorrecta de Seguridad
7. SSRF
8. Validación de Entrada
9. Limitación de Tasa
10. Ataques de Temporización

## Agente de Ejecución

- **Security Agent** (claude-opus-4-20250514)

## Escenarios Recomendados

- Al modificar middleware/ (lógica de autenticación/autorización)
- Al agregar o modificar endpoints de API que aceptan entrada externa
- Revisiones de seguridad periódicas (por ejemplo, mensualmente)

## Formato de Salida

Clasificado por severidad: Critical / High / Medium / Low. Cada hallazgo incluye archivo:línea, descripción del riesgo y corrección recomendada.

## Activación

Las condiciones de activación de esta Skill están definidas en el campo `description` de [SKILL.md](./SKILL.md).

## Versiones Localizadas

- [Inglés](./README.en.md)
- [Japonés](./README.ja.md)
- [Coreano](./README.ko.md)
