# Security Lens — IaC Misconfiguration Taxonomy

> Shared infra security lens for Terraform review. This covers infrastructure
> misconfiguration, not application-code vulnerabilities.

## High-Frequency Checks

| # | Misconfiguration | Signal in Terraform | Fix |
|---|---|---|---|
| 1 | Public object storage | Bucket without public-access guardrails | Block public access by default |
| 2 | Open ingress | `0.0.0.0/0` on admin or data ports | Scope CIDR or use private access paths |
| 3 | IAM or RBAC over-privilege | Wildcards or owner-level grants | Reduce to least privilege |
| 4 | Secrets in code or state | Hardcoded credentials or unprotected backend | Externalize secrets and protect state |
| 5 | Missing encryption | No encryption at rest or in transit | Enable provider-native encryption and TLS |
| 6 | Broad network exposure | Public DB or no private boundary | Use private subnets or endpoints |
| 7 | Missing audit logging | No account, project, or flow logs | Enable provider audit logging |

## Review Procedure

1. Scan for public exposure, IAM wildcards, RBAC drift, and secrets-in-state.
2. Assign severity based on exposure and blast radius.
3. Report each finding with the affected resource and a narrow remediation.

## Boundary

- In scope: IaC misconfiguration.
- Out of scope: application-code security review.
- Provider-specific examples live under `../providers/`.
