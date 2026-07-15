# ywc-wayfinder

Esta es una discovery Skill para cambios grandes o inciertos que necesitan un mapa local y reanudable a través de varias sesiones. Mantiene exactamente un active ticket y decide el siguiente routing en lugar de implementar código.

## Casos de uso

- Hay demasiadas decisiones sin resolver para pasar directo al planning normal
- La discovery debe continuar en varias sesiones
- Se necesita un handoff local y revisable dentro del repo, sin tracker write externo

## Contrato principal

- canonical map path: `docs/ywc-plans/<slug>-wayfinder.md`
- Solo se permite un active ticket
- El estado terminal resolved devuelve `DONE` sin escritura final
- El estado terminal deferred / blocked devuelve `NEEDS_CONTEXT` sin escritura final
