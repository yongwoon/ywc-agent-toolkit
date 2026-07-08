# IaC Security — Misconfiguration Taxonomy for `ywc-security-engineer`

> Reference for the `ywc-security-engineer` agent when its scope includes
> Infrastructure-as-Code (Terraform `.tf` files, provider config, module
> definitions). This extends the agent's OWASP application-security review with
> an **infrastructure misconfiguration** lens. It is the security-engineer's
> deeper companion to the shared review lens at
> [`lenses/security.md`](lenses/security.md) — same taxonomy, agent-facing
> depth (severity + concrete Terraform remediation).

## Scope boundary

- **In scope for this reference**: IaC misconfiguration in Terraform — public
  exposure, over-broad identity, secrets in state, missing encryption.
- **Still application security** (the agent's primary lens): OWASP Top 10 on
  app code. This reference does not replace that; it adds the infra surface when
  the diff includes `.tf` files.

## The misconfiguration taxonomy (severity-rated)

| Class | Terraform signal | Severity | Remediation |
|---|---|---|---|
| **Public object storage** | `aws_s3_bucket` without `aws_s3_bucket_public_access_block`; GCS without `uniform_bucket_level_access`; `azurerm_storage_account` with public blobs allowed | **Critical** if data is sensitive | Add the public-access-block resource (all four AWS flags `true`); enable uniform bucket-level access |
| **Open ingress to admin/data ports** | SG / firewall ingress `0.0.0.0/0` to 22 / 3389 / 5432 / 3306 / 6379 | **Critical** | Scope `cidr_blocks` to known ranges; front with a bastion / SSM Session Manager / IAP |
| **IAM wildcard / over-privilege** | policy `Action = "*"` or `Resource = "*"`; GCP `roles/owner` / `roles/editor`; Azure `Owner`/`Contributor` at subscription scope | **High** | Enumerate the exact actions; scope resources by ARN / self-link / resource-id |
| **Secrets in state or code** | hardcoded password / access key / token in `.tf`; remote backend without encryption | **Critical** | Externalize to a secret manager data source; encrypt the backend; mark variables `sensitive = true` |
| **No encryption at rest** | DB / bucket / volume without KMS / CMEK | **High** | Enable provider encryption; use customer-managed keys where compliance requires |
| **Public data-tier** | RDS / Cloud SQL / managed DB with a public IP or no private subnet | **High** | Place in a private subnet; use private endpoints; disable public accessibility |
| **Overly-broad network egress** | unrestricted egress from a sensitive workload | **Medium** | Scope egress to required destinations where the threat model warrants it |
| **Missing audit logging** | no CloudTrail / audit logs / VPC flow logs at the account/project | **Medium** | Enable provider-level audit logging as an account baseline |

## Review procedure (when `.tf` is in scope)

1. Grep the diff for the high-signal strings: `0.0.0.0/0`, `"*"`, `public`,
   `password =`, `secret =`, access-key patterns.
2. For each hit, map to a taxonomy class above and assign severity by data
   sensitivity and exploitability (public sensitive data / open admin port /
   wildcard admin → Critical).
3. Cite `file:line`, name the concrete misconfiguration (not the class title),
   and give the specific Terraform remediation.
4. Treat an **access-boundary** infra issue (an IAM policy or SG that lets one
   tenant/account reach another's resources) as Broken Access Control (A01),
   the same severity discipline as the app-code IDOR check.

## Handoff

- The **reliability** dimension of an infra change (SPOF, backup, HA) is the
  `ywc-cloud-engineer` / infra-review reliability lens, not this reference.
- The **cost** dimension is [`finops.md`](finops.md) /
  [`lenses/cost.md`](lenses/cost.md).
- Provider-specific instances live in
  [`providers/aws.md`](providers/aws.md),
  [`providers/gcp.md`](providers/gcp.md),
  [`providers/azure.md`](providers/azure.md),
  [`providers/k8s.md`](providers/k8s.md).
