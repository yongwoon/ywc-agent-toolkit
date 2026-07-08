# Security Lens — IaC Misconfiguration Taxonomy

> Shared reference for the infra skill suite. One of the three review lenses
> (security / cost / reliability, design §2.3). This is the **infrastructure**
> security lens — IaC misconfiguration, not application-code vulnerabilities
> (those route to `ywc-security-engineer`). `ywc-infra-review` fans this lens
> out; `ywc-infra-design` and `ywc-iac-author` pre-check against it.

## The high-frequency misconfiguration taxonomy

| # | Misconfiguration | Signal in Terraform | Fix |
|---|---|---|---|
| 1 | **Public object storage** | S3 bucket without `public_access_block`; GCS without `uniform_bucket_level_access`; Storage Account `allow_nested_items_to_be_public = true` | Block public access; private by default |
| 2 | **Open security group / firewall** | ingress `cidr_blocks = ["0.0.0.0/0"]` to 22/3389/db ports | Scope CIDR to known ranges; use a bastion / SSM / IAP |
| 3 | **IAM wildcard** | policy `Action = "*"` or `Resource = "*"`; GCP `roles/owner`/`editor`; Azure `Owner` at subscription | Least privilege: enumerate actions, scope resources |
| 4 | **Secrets in state / code** | hardcoded password/key in `.tf`; unencrypted remote backend | Externalize to secret manager; encrypt state; `sensitive = true` |
| 5 | **No encryption at rest** | DB/bucket/volume without KMS/CMEK | Enable encryption; use customer-managed keys where required |
| 6 | **No encryption in transit** | LB/DB allowing plaintext; TLS min version unset | Enforce TLS; set min protocol version |
| 7 | **Over-broad network exposure** | DB with public IP; no private subnet / endpoint | Private subnets, private endpoints, no public IP on data tier |
| 8 | **Missing audit / logging** | no CloudTrail / audit logs / flow logs | Enable provider audit logging on the account/project |

## Review procedure

1. Scan the diff for each taxonomy row above (grep for `0.0.0.0/0`, `"*"`,
   `public`, hardcoded secrets).
2. For each finding, assign a severity (CRITICAL = public data / open admin
   port / wildcard admin; HIGH = missing encryption / broad exposure; MEDIUM =
   missing logging).
3. Report finding + resource + concrete fix — never just "looks insecure".

## Boundary

- **In scope**: IaC misconfiguration (the table above).
- **Out of scope**: application-code security (injection, auth bypass, XSS) →
  route to `ywc-security-engineer`. Cost and reliability have their own lenses:
  [`cost.md`](cost.md), [`reliability.md`](reliability.md).

Provider-specific instances of these rows live in
[`../providers/aws.md`](../providers/aws.md),
[`gcp.md`](../providers/gcp.md), [`azure.md`](../providers/azure.md),
[`k8s.md`](../providers/k8s.md).
