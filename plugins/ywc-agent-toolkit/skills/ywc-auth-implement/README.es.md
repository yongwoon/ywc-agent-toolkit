# ywc-auth-implement

Una habilidad de orquestación de Codex que convierte una intención de autenticación en una ruta de implementación con política, auditoría de seguridad y puertas E2E. No expone secretos ni recomienda implementar JWT, contraseñas o criptografía de secretos a mano.

## Cuándo usarla

- Para planificar inicio de sesión, OAuth, sesiones o eliminación de cuenta
- Para decidir si la autenticación existente es `new`, `extend` o `migrate`
- Para elegir una biblioteca consolidada o un servicio gestionado según la evidencia del proyecto

## Invocación

```text
$ywc-auth-implement
```

La habilidad realiza una comprobación previa de solo lectura y una entrevista de política de nueve secciones. Después imprime, sin invocar automáticamente, esta ruta:

```text
$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec <path> --feature <auth feature> --tdd --review
```

Los hallazgos Critical/High omiten E2E, la propuesta de PR y la caché. El texto legal siempre lleva `법적 검토 전 임시본`.
