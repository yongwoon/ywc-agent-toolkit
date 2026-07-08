# Reliability Lens — Availability And Resilience Checklist

> Shared infra reliability lens for Terraform review, design follow-through,
> and optimization planning.

## Reliability Taxonomy

| # | Risk | Signal in Terraform | Fix |
|---|---|---|---|
| 1 | Single point of failure | One instance, one AZ, or one node | Add redundancy across failure domains |
| 2 | Single-zone data tier | Non-regional DB or storage | Use multi-AZ or regional primitives |
| 3 | No backups or PITR | Zero retention or missing backup config | Enable backups and point-in-time recovery |
| 4 | Missing health checks | No readiness, liveness, or target checks | Add health probes |
| 5 | No autoscaling | Fixed desired count under variable load | Add scaling primitives with safe minimums |
| 6 | No graceful degradation | Hard dependency without timeout or fallback | Add retries, timeouts, and fallback paths |
| 7 | Stateful destroy risk | Plan destroys DB, volume, or bucket | Snapshot first and protect critical resources |
| 8 | Single-region posture | No DR path outside one region | Add replica or backup aligned to RTO/RPO |

## RTO And RPO Anchoring

- RTO drives redundancy topology and recovery speed expectations.
- RPO drives backup frequency and replication depth.
- Review should confirm the Terraform realization matches the intended target.

## Review Procedure

1. Ask what fails if one node, one AZ, or one region goes away.
2. Flag destroys against stateful resources immediately.
3. Report each risk with the affected resource and the concrete remediation.

## Boundary

- In scope: availability, redundancy, backup, recovery, health, and scaling.
- Out of scope: security-only and cost-only findings.
- Provider-specific examples live under `../providers/`.
