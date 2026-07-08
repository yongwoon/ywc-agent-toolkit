# Cost Lens — FinOps Review Checklist

> Shared infra cost lens for Terraform review and optimization planning.

## Cost Taxonomy

| # | Cost driver | Signal | Optimization |
|---|---|---|---|
| 1 | Over-provisioned compute | Large fixed instances or node pools | Right-size and autoscale |
| 2 | On-demand steady load | 24/7 baseline on on-demand pricing | Reserved or committed pricing |
| 3 | Full-price interruptible load | Batch or stateless work on on-demand | Spot or preemptible capacity |
| 4 | Idle resources | Unattached disks, IPs, NAT, or stopped-but-billed resources | Delete and alert on orphaning |
| 5 | Hot storage for cold data | Premium storage for archival data | Add lifecycle tiering |
| 6 | Transfer cost | Cross-region or internet-heavy traffic | Co-locate or use private paths |
| 7 | Over-requested clusters | Requests far above usage | Right-size requests and autoscale |
| 8 | Redundant non-prod | Prod-sized environments running continuously | Schedule off-hours shutdown or scale to zero |

## Review Procedure

1. Check whether each changed resource is sized to demand.
2. Separate immediate savings from commitment-based savings.
3. Surface the trade-off when cost reduction can weaken reliability.

## Boundary

- In scope: cost, right-sizing, waste, and pricing-shape review.
- Out of scope: security misconfiguration and reliability architecture.
- Provider-specific examples live under `../providers/`.
